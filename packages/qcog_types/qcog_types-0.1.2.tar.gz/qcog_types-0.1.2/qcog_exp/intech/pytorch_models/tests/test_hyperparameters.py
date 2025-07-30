import pytest
import torch  # type: ignore
import logging

from qcog_exp.intech.pytorch_models.hyperparameters import (
    ModelHyperparameters,
    OptimizerConfig,
    LossFunctionConfig,
    SchedulerConfig,
    EarlyStoppingConfig,
    PerGroupOptimizerParams,
    GeneralHSModelHyperparameters,
    PauliHSModelHyperparameters,
    GradientClippingConfig
)

# Mock a loss function for testing Callable type
def mock_loss_fn():
    return torch.nn.MSELoss()

# Define the logger name consistently
HYPERPARAMS_LOGGER_NAME = "qcog_exp.intech.pytorch_models.hyperparameters"

class TestOptimizerConfig:
    def test_optimizer_config_minimal(self):
        config = OptimizerConfig(type="Adam")
        assert config.type == "Adam"
        assert config.default_params == {}
        assert config.group_params is None

    def test_optimizer_config_with_defaults(self):
        config = OptimizerConfig(type="SGD", default_params={"lr": 0.01, "momentum": 0.9})
        assert config.type == "SGD"
        assert config.default_params == {"lr": 0.01, "momentum": 0.9}

    def test_optimizer_config_with_groups(self):
        group_params = [
            PerGroupOptimizerParams(param_name_contains=["bias"], params={"lr": 0.001}),
            PerGroupOptimizerParams(param_name_contains=["weight"], params={"lr": 0.002, "weight_decay": 0.01}),
        ]
        config = OptimizerConfig(
            type="AdamW",
            default_params={"lr": 0.0005},
            group_params=group_params
        )
        assert config.type == "AdamW"
        assert config.default_params == {"lr": 0.0005}
        assert len(config.group_params) == 2
        assert config.group_params[0].param_name_contains == ["bias"]
        assert config.group_params[1].params == {"lr": 0.002, "weight_decay": 0.01}


class TestLossFunctionConfig:
    def test_loss_function_config_string_type(self):
        config = LossFunctionConfig(type="MSELoss", params={"reduction": "sum"})
        assert config.type == "MSELoss"
        assert config.params == {"reduction": "sum"}

    def test_loss_function_config_callable_type(self):
        config = LossFunctionConfig(type=mock_loss_fn)
        assert config.type == mock_loss_fn
        assert config.params == {} # Params should be ignored for callable

    def test_loss_function_config_minimal_string(self):
        config = LossFunctionConfig(type="CrossEntropyLoss")
        assert config.type == "CrossEntropyLoss"
        assert config.params == {}


class TestSchedulerConfig:
    def test_scheduler_config_minimal(self):
        config = SchedulerConfig(type="StepLR", params={"step_size": 30})
        assert config.type == "StepLR"
        assert config.params == {"step_size": 30}
        assert config.interval == "epoch"

    def test_scheduler_config_with_interval(self):
        config = SchedulerConfig(type="CosineAnnealingLR", params={"T_max": 100}, interval="step")
        assert config.type == "CosineAnnealingLR"
        assert config.params == {"T_max": 100}
        assert config.interval == "step"


class TestModelHyperparametersBase:
    @pytest.fixture
    def minimal_optimizer_config(self):
        return OptimizerConfig(type="Adam", default_params={"lr": 0.001})

    @pytest.fixture
    def minimal_loss_config(self):
        return LossFunctionConfig(type="MSELoss")

    def test_model_hyperparameters_minimal(self, minimal_optimizer_config, minimal_loss_config):
        config = ModelHyperparameters(
            hsm_model="general",
            epochs=10,
            batch_size=32,
            optimizer_config=minimal_optimizer_config,
            loss_fn_config=minimal_loss_config,
            target="output_value"
        )
        assert config.hsm_model == "general"
        assert config.epochs == 10
        assert config.batch_size == 32
        assert config.target == "output_value"
        assert config.seed == 42
        assert config.num_workers == 0
        assert config.pin_memory is False
        assert config.device in ["cpu", "cuda", "mps"]

    def test_model_hyperparameters_device_cpu(self, minimal_optimizer_config, minimal_loss_config):
        config = ModelHyperparameters(
            hsm_model="general",
            epochs=10,
            batch_size=32,
            optimizer_config=minimal_optimizer_config,
            loss_fn_config=minimal_loss_config,
            target="output_value",
            device="cpu"
        )
        assert config.device == "cpu"
    
    def test_model_hyperparameters_invalid_device(self, minimal_optimizer_config, minimal_loss_config):
        with pytest.raises(ValueError, match="Unsupported device: my_gpu"):
            ModelHyperparameters(
                hsm_model="general",
                epochs=10,
                batch_size=32,
                optimizer_config=minimal_optimizer_config,
                loss_fn_config=minimal_loss_config,
                target="output_value",
                device="my_gpu"
            )

    def test_model_hyperparameters_full(self, minimal_optimizer_config, minimal_loss_config):
        scheduler_conf = SchedulerConfig(type="StepLR", params={"step_size": 10})
        early_stop_conf = EarlyStoppingConfig(monitor="val_loss", patience=5)
        grad_clip_conf = GradientClippingConfig(max_norm=1.0)

        config = ModelHyperparameters(
            hsm_model="pauli",
            epochs=100,
            batch_size=64,
            seed=123,
            optimizer_config=minimal_optimizer_config,
            loss_fn_config=minimal_loss_config,
            scheduler_config=scheduler_conf,
            early_stopping_config=early_stop_conf,
            gradient_clipping_config=grad_clip_conf,
            num_workers=4,
            pin_memory=True,
            target="target_col",
            device="cuda"
        )
        assert config.hsm_model == "pauli"
        assert config.epochs == 100
        assert config.batch_size == 64
        assert config.seed == 123
        assert config.num_workers == 4
        assert config.pin_memory is True
        assert config.target == "target_col"
        assert config.device == "cuda"
        assert config.scheduler_config.type == "StepLR"
        assert config.early_stopping_config.monitor == "val_loss"
        assert config.gradient_clipping_config.max_norm == 1.0

    def test_scheduler_early_stopping_monitor_mismatch_warning(
        self, minimal_optimizer_config, minimal_loss_config, caplog
    ):
        scheduler_conf = SchedulerConfig(type="ReduceLROnPlateau", params={"monitor": "val_accuracy"})
        early_stop_conf = EarlyStoppingConfig(monitor="val_loss", patience=5)
        
        caplog.clear()
        with caplog.at_level(logging.WARNING):
            ModelHyperparameters(
                hsm_model="general",
                epochs=10,
                batch_size=32,
                optimizer_config=minimal_optimizer_config,
                loss_fn_config=minimal_loss_config,
                scheduler_config=scheduler_conf,
                early_stopping_config=early_stop_conf,
                target="output"
            )
        assert any(
            "Scheduler 'ReduceLROnPlateau' monitors 'val_accuracy' while EarlyStopping monitors 'val_loss'" in record.message
            for record in caplog.records
        )
    
    def test_scheduler_non_standard_monitor_warning(
        self, minimal_optimizer_config, minimal_loss_config, caplog
    ):
        scheduler_conf = SchedulerConfig(type="ReduceLROnPlateau", params={"monitor": "custom_metric"})
        caplog.clear()
        with caplog.at_level(logging.WARNING):
            ModelHyperparameters(
                hsm_model="general",
                epochs=10,
                batch_size=32,
                optimizer_config=minimal_optimizer_config,
                loss_fn_config=minimal_loss_config,
                scheduler_config=scheduler_conf,
                target="output"
            )
        assert any(
            "Scheduler 'ReduceLROnPlateau' monitor 'custom_metric' might not be standard" in record.message
            for record in caplog.records
        )

    def test_early_stopping_non_standard_monitor_warning(
        self, minimal_optimizer_config, minimal_loss_config, caplog
    ):
        early_stop_conf = EarlyStoppingConfig(monitor="my_custom_metric", patience=5)
        caplog.clear()
        with caplog.at_level(logging.WARNING):
            ModelHyperparameters(
                hsm_model="general",
                epochs=10,
                batch_size=32,
                optimizer_config=minimal_optimizer_config,
                loss_fn_config=minimal_loss_config,
                early_stopping_config=early_stop_conf,
                target="output"
            )
        assert any(
            "EarlyStopping monitor 'my_custom_metric' might not be standard" in record.message
            for record in caplog.records
        )

    def test_optimizer_lr_warning(self, minimal_loss_config, caplog):
        opt_conf = OptimizerConfig(type="Adam") # No lr
        caplog.clear()
        with caplog.at_level(logging.WARNING):
            ModelHyperparameters(
                hsm_model="general",
                epochs=10,
                batch_size=32,
                optimizer_config=opt_conf,
                loss_fn_config=minimal_loss_config,
                target="output"
            )
        assert any(
            ("Learning rate ('lr' or 'learning_rate') not found" in record.message and \
            "The optimizer's default LR will be used if available." in record.message)
            for record in caplog.records
        )

    def test_optimizer_lr_in_group_no_warning(self, minimal_loss_config, caplog):
        group_params = [PerGroupOptimizerParams(param_name_contains=["layer1"], params={"lr": 0.01})]
        opt_conf = OptimizerConfig(type="Adam", group_params=group_params)
        caplog.clear()
        with caplog.at_level(logging.WARNING):
            ModelHyperparameters(
                hsm_model="general",
                epochs=10,
                batch_size=32,
                optimizer_config=opt_conf,
                loss_fn_config=minimal_loss_config,
                target="output"
            )
        assert not any(
            "Learning rate ('lr' or 'learning_rate') not found" in record.message
            for record in caplog.records
        )
        
class TestGeneralHSModelHyperparameters:
    @pytest.fixture
    def base_hyperparameters(self):
        return {
            "hsm_model": "general",
            "epochs": 1,
            "batch_size": 1,
            "optimizer_config": OptimizerConfig(type="Adam", default_params={"lr": 0.001}),
            "loss_fn_config": LossFunctionConfig(type="MSELoss"),
            "target": "target",
            "device": "cpu" # Force CPU for tensor comparisons
        }

    def test_general_hsm_minimal(self, base_hyperparameters):
        config = GeneralHSModelHyperparameters(
            **base_hyperparameters,
            input_operator_count=2,
            output_operator_count=1,
            hilbert_space_dims=3
        )
        assert config.input_operator_count == 2
        assert config.output_operator_count == 1
        assert config.hilbert_space_dims == 3
        assert config.complex is True

    def test_general_hsm_with_tensors(self, base_hyperparameters):
        input_ops = torch.randn(2, 3, 3, dtype=torch.complex64)
        output_ops = torch.randn(1, 3, 3, dtype=torch.complex64)
        init_mean = torch.randn(3) # 2 input + 1 output
        init_std = torch.rand(3)

        config = GeneralHSModelHyperparameters(
            **base_hyperparameters,
            input_operator_count=2,
            output_operator_count=1,
            hilbert_space_dims=3,
            input_operators=input_ops,
            output_operators=output_ops,
            initialization_mean_per_operator=init_mean,
            initialization_std_per_operator=init_std,
            beta=0.5,
            complex=True,
            eigh_eps=1e-7
        )
        assert torch.equal(config.input_operators, input_ops)
        assert torch.equal(config.output_operators, output_ops)
        assert torch.equal(config.initialization_mean_per_operator, init_mean)
        assert torch.equal(config.initialization_std_per_operator, init_std)
        assert config.beta == 0.5
        assert config.eigh_eps == 1e-7

    def test_general_hsm_input_op_shape_mismatch(self, base_hyperparameters):
        with pytest.raises(ValueError, match="input_operators shape mismatch"):
            GeneralHSModelHyperparameters(
                **base_hyperparameters,
                input_operator_count=2,
                output_operator_count=1,
                hilbert_space_dims=3,
                input_operators=torch.randn(2, 3, 4, dtype=torch.complex64) # Wrong dim
            )

    def test_general_hsm_output_op_shape_mismatch(self, base_hyperparameters):
        with pytest.raises(ValueError, match="output_operators shape mismatch"):
            GeneralHSModelHyperparameters(
                **base_hyperparameters,
                input_operator_count=2,
                output_operator_count=1,
                hilbert_space_dims=3,
                output_operators=torch.randn(1, 4, 3, dtype=torch.complex64) # Wrong dim
            )
    
    def test_general_hsm_input_op_type_mismatch(self, base_hyperparameters):
        with pytest.raises(ValueError, match="input_operators must be complex"):
            GeneralHSModelHyperparameters(
                **base_hyperparameters,
                input_operator_count=2,
                output_operator_count=1,
                hilbert_space_dims=3,
                complex=True,
                input_operators=torch.randn(2, 3, 3, dtype=torch.float32) # Wrong dtype
            )

    def test_general_hsm_output_op_type_mismatch(self, base_hyperparameters):
        with pytest.raises(ValueError, match="output_operators must be complex"):
            GeneralHSModelHyperparameters(
                **base_hyperparameters,
                input_operator_count=2,
                output_operator_count=1,
                hilbert_space_dims=3,
                complex=True,
                output_operators=torch.randn(1, 3, 3, dtype=torch.float32) # Wrong dtype
            )

    def test_general_hsm_init_mean_len_mismatch(self, base_hyperparameters):
        with pytest.raises(ValueError, match="initialization_mean_per_operator length mismatch"):
            GeneralHSModelHyperparameters(
                **base_hyperparameters,
                input_operator_count=2,
                output_operator_count=1,
                hilbert_space_dims=3,
                initialization_mean_per_operator=torch.randn(4) # Expected 3
            )

    def test_general_hsm_init_std_len_mismatch(self, base_hyperparameters):
        with pytest.raises(ValueError, match="initialization_std_per_operator length mismatch"):
            GeneralHSModelHyperparameters(
                **base_hyperparameters,
                input_operator_count=2,
                output_operator_count=1,
                hilbert_space_dims=3,
                initialization_std_per_operator=torch.randn(2) # Expected 3
            )

    # Note: Device consistency for tensors is harder to test without mocking torch.cuda.is_available
    # or forcing a specific device that might not be available.
    # For now, ensuring the config itself has the right device is covered by ModelHyperparameters tests.
    # The tensor validation checks if str(tensor.device) == self.device.


class TestPauliHSModelHyperparameters:
    @pytest.fixture
    def base_hyperparameters_pauli(self):
        return {
            "hsm_model": "pauli",
            "epochs": 1,
            "batch_size": 1,
            "optimizer_config": OptimizerConfig(type="Adam", default_params={"lr": 0.001}),
            "loss_fn_config": LossFunctionConfig(type="MSELoss"),
            "target": "target",
            "device": "cpu"
        }

    def test_pauli_hsm_minimal(self, base_hyperparameters_pauli):
        config = PauliHSModelHyperparameters(
            **base_hyperparameters_pauli,
            input_operator_count=3,
            output_operator_count=2,
            qubits_count=2,
        )
        assert config.input_operator_count == 3
        assert config.output_operator_count == 2
        assert config.qubits_count == 2
        # No assertion for hilbert_space_dims

    def test_pauli_hsm_full(self, base_hyperparameters_pauli):
        input_coeffs = torch.randn(3, 10)
        output_coeffs = torch.randn(2, 10)

        config = PauliHSModelHyperparameters(
            **base_hyperparameters_pauli,
            input_operator_count=3,
            output_operator_count=2,
            qubits_count=3,
            input_operator_pauli_weight=1,
            output_operator_pauli_weight=2,
            input_pauli_coeffs=input_coeffs,
            output_pauli_coeffs=output_coeffs,
            eigh_eps=1e-9
        )
        assert config.input_operator_pauli_weight == 1
        assert config.output_operator_pauli_weight == 2
        assert torch.equal(config.input_pauli_coeffs, input_coeffs)
        assert torch.equal(config.output_pauli_coeffs, output_coeffs)
        assert config.eigh_eps == 1e-9
        # No assertion for hilbert_space_dims


class TestEarlyStoppingConfig:
    def test_early_stopping_minimal(self):
        config = EarlyStoppingConfig(monitor="val_loss")
        assert config.monitor == "val_loss"
        assert config.min_delta == 0.0001
        assert config.patience == 10
        assert config.mode == "min"
        assert config.verbose is False
        assert config.restore_best_weights is True

    def test_early_stopping_full(self):
        config = EarlyStoppingConfig(
            monitor="train_acc",
            min_delta=0.01,
            patience=20,
            mode="max",
            verbose=True,
            restore_best_weights=False
        )
        assert config.monitor == "train_acc"
        assert config.min_delta == 0.01
        assert config.patience == 20
        assert config.mode == "max"
        assert config.verbose is True
        assert config.restore_best_weights is False

class TestGradientClippingConfig:
    def test_gradient_clipping_minimal(self):
        config = GradientClippingConfig(max_norm=1.0)
        assert config.max_norm == 1.0
        assert config.norm_type == 2.0

    def test_gradient_clipping_full(self):
        config = GradientClippingConfig(max_norm=0.5, norm_type=1.0)
        assert config.max_norm == 0.5
        assert config.norm_type == 1.0

