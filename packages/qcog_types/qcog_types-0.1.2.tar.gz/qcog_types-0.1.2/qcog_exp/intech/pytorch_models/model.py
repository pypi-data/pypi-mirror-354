from typing import Any, Callable, Literal, NotRequired, TypedDict, Unpack
import torch  # type: ignore
from qcog_torch.layers.general import PytorchGeneralHSM  # type: ignore
from qcog_torch.layers.pauli import PytorchPauliHSM  # type: ignore
from qcog_torch.layers.general_full_energy import PytorchGeneralHSMFullEnergy  # type: ignore
from qcog_torch.layers.weighted import WeightedLayer  # type: ignore
import pandas as pd  # type: ignore
from torch.utils.data import Dataset, DataLoader  # type: ignore
from qcog_torch import nptype  # type: ignore
from qcog_exp.intech.pytorch_models.resolve_dataset import resolve_dataset # type: ignore
from qcog_exp.intech.pytorch_models.split_dataset import split_dataset # type: ignore
from qcog_exp.intech.pytorch_models.hyperparameters import (  # type: ignore
    ModelHyperparameters,
    GeneralHSModelHyperparameters,
    PauliHSModelHyperparameters,
)
import logging

# Initialize logger at module level
logger = logging.getLogger(__name__)
# Required exports --------------------------------------------------------+
# The following exports are used by the API to determine the version       |
# of the train and predict functions.                                      |
#                                                                          |
# Hyperparameters will eventually be used to generate a package for        |
# the client that will be used to validate and type hint the parameters    |
# -------------------------------------------------------------------------+

TRAIN_VERSION = "v0.0.1"
PREDICT_VERSION = "v0.0.1"

# -------------------------------------------------------------------------+

ColumnName = str
Function = Literal["to_datetime"]
ApplyTransform = dict[ColumnName, Function]

# Create a union type for all supported hyperparameter types
SupportedHyperparameters = GeneralHSModelHyperparameters | PauliHSModelHyperparameters | ModelHyperparameters


class DataFrameDataset(Dataset):
    """DataFrame Dataset."""

    def __init__(self, df: pd.DataFrame, target: str, device: str):
        """
        Initialize a dataset from a dataframe

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with data to use
        target: str
            Target variable name which must be a column in df
        device: str
            Device for torch
        """
        target_data = df[[target]].values.astype(nptype(), copy=True)
        inputs_data = df.drop([target], axis=1).values.astype(nptype(), copy=True)
        self.target = torch.tensor(target_data).to(device=device)
        self.inputs = torch.tensor(inputs_data).to(device=device)

    def __len__(self) -> int:
        """Get the length of the dataset."""
        return len(self.target)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        """Get an item from the dataset."""
        return self.inputs[idx, :], self.target[idx, :]


StateDict = dict[str, Any]


class Checkpoint(TypedDict):
    model_state_dict: StateDict
    timestamp: str
    current_epoch: int
    other_states: dict[str, Any] | None
    optimizer_state_dict: dict[str, Any] | None
    hyperparameters: dict[str, Any] | None
    metrics: dict[str, Any] | None


class SaveCheckpointKwargs(TypedDict):
    """
    Kwargs for the save_checkpoint method.

    model_state_dict: The model state dictionary when the checkpoint was saved.
    current_epoch: The current epoch when the checkpoint was saved.
    other_states: Other states to save (e.g, loss, optimizers, etc.)
    optimizer_state_dict: The optimizer state dictionary when the checkpoint was saved.
    hyperparameters: The hyperparameters of the experiment.
    metrics: The metrics of the experiment at the time the checkpoint was saved.
    """
    model_state_dict: dict[str, Any]
    current_epoch: int
    other_states: dict[str, Any] | None
    hyperparameters: dict[str, Any] | None
    metrics: dict[str, Any] | None


class TrainContext(TypedDict):
    status_id: str  # The train identifier
    save_checkpoint: NotRequired[Callable[[Unpack[SaveCheckpointKwargs]], None]]
    load_last_checkpoint: NotRequired[Callable[[], Checkpoint | None]]
    dataset_bucket: str
    dataset_format: str


def train(
    context: TrainContext,
    dataset_path: str,
    *,
    params: dict[str, Any],
):
    hyperparameters_dict: dict = params.get("hyperparameters", {})

    if not hyperparameters_dict:
        raise ValueError("Hyperparameters must be provided")

    # Determine the HSM model type to parse the correct hyperparameters
    hsm_model_type = hyperparameters_dict.get("hsm_model")
    hyperparameters: SupportedHyperparameters
    if hsm_model_type == "general":
        hyperparameters = GeneralHSModelHyperparameters.model_validate(hyperparameters_dict)
    elif hsm_model_type == "pauli":
        hyperparameters = PauliHSModelHyperparameters.model_validate(hyperparameters_dict)
    elif hsm_model_type == "general_fullenergy":
        # General Full Energy model uses GeneralHSModelHyperparameters for its structure
        hyperparameters = GeneralHSModelHyperparameters.model_validate(hyperparameters_dict)
    else:
        raise ValueError(f"hsm_model type '{hsm_model_type}' is not explicitly handled or is missing. Available types are: general, pauli, general_fullenergy")

    # Extract hooks to save and extract checkpoints
    save_checkpoint_hook = context.get("save_checkpoint", None)
    load_last_checkpoint_hook = context.get("load_last_checkpoint", None)

    # Extract dataset information from the context
    dataset_bucket = context.get("dataset_bucket", "s3")
    dataset_format = context.get("dataset_format", "csv")

    # Check if there is a checkpoint
    checkpoint: Checkpoint | None = None

    if load_last_checkpoint_hook:
        checkpoint = load_last_checkpoint_hook()

    # Initialize checkpoint-related variables
    epochs_completed: int = 0
    optimizer_state_dict: dict[str, Any] | None = None
    model_state_dict: dict[str, Any] | None = None

    if checkpoint:
        epochs_completed = checkpoint.get("epochs", 0)
        optimizer_state_dict = checkpoint.get("optimizer_state_dict")
        model_state_dict = checkpoint.get("model_state_dict")
        # It's important that hyperparameters for resuming a run are consistent.
        # The current logic re-validates params from the input, then potentially loads a checkpoint.
        # If HPs changed between runs, this could be an issue.
        # For now, we assume the input `params` are the source of truth for HPs,
        # and the checkpoint only provides state.

    # Use validated hyperparameters
    torch.manual_seed(hyperparameters.seed if hyperparameters.seed is not None else 42)

    # Device setup from hyperparameters - Correctly use the validated device from Pydantic model
    device = hyperparameters.device
    logger.info(f"Using device: {device}")
    logger.info(f"Dataset path: {dataset_path}")

    dataset = resolve_dataset(dataset_path, dataset_bucket, dataset_format)
    # Use split from the typed hyperparameter object
    train_df, test_df = split_dataset(dataset, test_size=hyperparameters.split)

    # Derive operator counts from the data for training
    data_derived_input_operator_count = train_df.shape[1] - 1 # Assuming target is one column
    data_derived_output_operator_count = 1 # Assuming single output

    # Update hyperparameters with data-derived counts if they are specific to the model type
    # This ensures that the correct counts used for training are saved for prediction.
    if isinstance(hyperparameters, (GeneralHSModelHyperparameters, PauliHSModelHyperparameters)):
        hyperparameters.input_operator_count = data_derived_input_operator_count
        hyperparameters.output_operator_count = data_derived_output_operator_count
    # For ModelHyperparameters base class, these attributes might not exist.
    # Consider adding them to ModelHyperparameters or handling this more generally if all models need them.

    train_dataset = DataFrameDataset(df=train_df, target=hyperparameters.target, device=device)
    test_dataset = DataFrameDataset(df=test_df, target=hyperparameters.target, device=device)
    train_dataloader = DataLoader(
        train_dataset,
        batch_size=hyperparameters.batch_size,
        shuffle=True,
        num_workers=hyperparameters.num_workers,
        pin_memory=hyperparameters.pin_memory
    )
    test_dataloader = DataLoader(
        test_dataset,
        batch_size=test_df.shape[0], # Consider making this configurable
        shuffle=False, # Usually false for testing
        num_workers=hyperparameters.num_workers,
        pin_memory=hyperparameters.pin_memory
    )

    # Model instantiation based on hsm_model type
    hsm_layer: PytorchGeneralHSM | PytorchPauliHSM | PytorchGeneralHSMFullEnergy
    if hyperparameters.hsm_model == "general":
        # Type checking ensures this is GeneralHSModelHyperparameters
        assert isinstance(hyperparameters, GeneralHSModelHyperparameters)
        hsm_layer = PytorchGeneralHSM(
            input_operator_count=data_derived_input_operator_count, # Use data-derived
            output_operator_count=data_derived_output_operator_count, # Use data-derived
            hilbert_space_dims=hyperparameters.hilbert_space_dims,
            initialization_mean_per_operator=hyperparameters.initialization_mean_per_operator,
            initialization_std_per_operator=hyperparameters.initialization_std_per_operator,
            beta=hyperparameters.beta,
            input_operators=hyperparameters.input_operators,
            output_operators=hyperparameters.output_operators,
            complex=hyperparameters.complex,
            eigh_eps=hyperparameters.eigh_eps,
            device=device,
        )
    elif hyperparameters.hsm_model == "pauli":
        # Type checking ensures this is PauliHSModelHyperparameters
        assert isinstance(hyperparameters, PauliHSModelHyperparameters)
        # hilbert_space_dims = 2**hyperparameters.qubits_count # This is handled internally by PytorchPauliHSM
        hsm_layer = PytorchPauliHSM(
            input_operator_count=data_derived_input_operator_count, # Use data-derived
            output_operator_count=data_derived_output_operator_count, # Use data-derived
            qubits_count=hyperparameters.qubits_count,
            input_operator_pauli_weight=hyperparameters.input_operator_pauli_weight,
            output_operator_pauli_weight=hyperparameters.output_operator_pauli_weight,
            input_pauli_coeffs=hyperparameters.input_pauli_coeffs,
            output_pauli_coeffs=hyperparameters.output_pauli_coeffs,
            eigh_eps=hyperparameters.eigh_eps,
            device=device,
        )
    elif hyperparameters.hsm_model == "general_fullenergy":
        # Type checking ensures this is GeneralHSModelHyperparameters
        assert isinstance(hyperparameters, GeneralHSModelHyperparameters)
        hsm_layer = PytorchGeneralHSMFullEnergy(
            input_operator_count=data_derived_input_operator_count, # Use data-derived
            output_operator_count=data_derived_output_operator_count, # Use data-derived
            hilbert_space_dims=hyperparameters.hilbert_space_dims,
            device=device,
        )
    else:
        # This case should ideally be caught by the initial hyperparameter validation
        raise ValueError(f"Unsupported hsm_model type: {hyperparameters.hsm_model}")


    model = WeightedLayer(hsm_layer=hsm_layer, device=device)

    # Display information about the model
    logger.info(f"Model: {model}")
    logger.info(f"Model named parameters: {[(name, param.shape) for name, param in model.named_parameters()]}")

    # Load the checkpoint if it exists
    if model_state_dict: # Check if model_state_dict was loaded from checkpoint
        model.load_state_dict(model_state_dict)

    # Optimizer setup
    opt_config = hyperparameters.optimizer_config
    optimizer_cls = getattr(torch.optim, opt_config.type)

    param_groups = []
    if opt_config.group_params:
        # Create a set of all parameter names for easier lookup
        # all_param_names = {name for name, _ in model.named_parameters()} # This variable was unused

        # Assign parameters to groups
        assigned_param_names = set()
        for group_spec in opt_config.group_params:
            group_params_list = []
            for name, param in model.named_parameters():
                if any(substr in name for substr in group_spec.param_name_contains) and name not in assigned_param_names:
                    group_params_list.append(param)
                    assigned_param_names.add(name)
            if group_params_list:
                 param_groups.append({"params": group_params_list, **group_spec.params})
            else:
                logger.warning(f"Optimizer group with 'param_name_contains': {group_spec.param_name_contains} did not match any parameters.")

        # Add remaining parameters with default settings
        default_params_list = [param for name, param in model.named_parameters() if name not in assigned_param_names]
        if default_params_list:
            param_groups.append({"params": default_params_list, **opt_config.default_params})
        elif not param_groups: # Handle case where no groups were defined and no default params matched
             param_groups.append({"params": model.parameters(), **opt_config.default_params})

    else: # No group_params defined, use default_params for all model parameters
        param_groups = [{"params": model.parameters(), **opt_config.default_params}]

    optimizer = optimizer_cls(param_groups)

    logger.info(f"Optimizer: {optimizer}")
    logger.info(f"Optimizer State Dict (initial): {optimizer.state_dict()}")

    if optimizer_state_dict: # Check if optimizer_state_dict was loaded from checkpoint
        optimizer.load_state_dict(optimizer_state_dict)

    # Loss function setup
    loss_fn_config = hyperparameters.loss_fn_config
    if isinstance(loss_fn_config.type, str):
        # TODO: Handle fully qualified path for custom loss functions
        loss_fn_cls = getattr(torch.nn, loss_fn_config.type)
        loss_fn = loss_fn_cls(**loss_fn_config.params)
    elif callable(loss_fn_config.type):
        loss_fn = loss_fn_config.type() # Assumes callable takes no params or uses its own defaults
    else:
        raise TypeError(f"Unsupported loss_fn_config.type: {type(loss_fn_config.type)}")


    # Scheduler setup (optional)
    scheduler = None
    if hyperparameters.scheduler_config:
        sch_config = hyperparameters.scheduler_config
        # TODO: Handle fully qualified path for custom schedulers
        scheduler_cls = getattr(torch.optim.lr_scheduler, sch_config.type)
        scheduler = scheduler_cls(optimizer, **sch_config.params)

    # Early stopping setup (optional)
    if hyperparameters.early_stopping_config:
        es_config = hyperparameters.early_stopping_config
        # This is a conceptual placeholder. Actual implementation requires a callback mechanism.
        # For simplicity, we'll track best_score and patience manually in the loop.
        # A more robust solution would involve a class or more complex logic.
        best_val_metric = float('inf') if es_config.mode == "min" else float('-inf')
        epochs_no_improve = 0
        best_model_state_dict = None
        logger.info(f"Early stopping enabled: monitor='{es_config.monitor}', patience={es_config.patience}")


    # Training loop
    for epoch in range(hyperparameters.epochs - epochs_completed):
        actual_epoch = epoch + epochs_completed
        model.train(True)
        epoch_train_loss = 0.0
        num_train_batches = 0
        for batch, (X, y) in enumerate(train_dataloader):
            pred = model(X)
            loss = loss_fn(pred, y)
            epoch_train_loss += loss.item()
            num_train_batches +=1
            # print(f"Epoch {actual_epoch}[{batch}]: Loss {loss.item():.4f}") # More granular logging

            if loss is not None:
                optimizer.zero_grad()
                loss.backward()
                if hyperparameters.gradient_clipping_config:
                    clip_config = hyperparameters.gradient_clipping_config
                    torch.nn.utils.clip_grad_norm_(
                        model.parameters(),
                        max_norm=clip_config.max_norm,
                        norm_type=clip_config.norm_type
                    )
                optimizer.step()

        avg_epoch_train_loss = epoch_train_loss / num_train_batches if num_train_batches > 0 else 0.0
        logger.info(f"Epoch {actual_epoch} Training Loss: {avg_epoch_train_loss:.4f}")

        # Validation step (conceptual - needs actual validation data and metric calculation)
        model.eval()
        epoch_val_loss = 0.0 # Placeholder for actual validation metric
        num_val_batches = 0
        with torch.no_grad():
            for X_val, y_val in test_dataloader: # Using test_dataloader for now, ideally a separate val_dataloader
                pred_val = model(X_val)
                val_loss_item = loss_fn(pred_val, y_val).item() # Assuming same loss_fn for validation
                epoch_val_loss += val_loss_item
                num_val_batches +=1

        avg_epoch_val_loss = epoch_val_loss / num_val_batches if num_val_batches > 0 else 0.0
        logger.info(f"Epoch {actual_epoch} Validation Loss: {avg_epoch_val_loss:.4f}")


        # Scheduler step
        if scheduler:
            if hyperparameters.scheduler_config and hyperparameters.scheduler_config.type == "ReduceLROnPlateau":
                # ReduceLROnPlateau typically uses a validation metric
                # TODO: Handle other metrics if logged differently
                metric_to_monitor_scheduler = hyperparameters.scheduler_config.params.get("monitor", "val_loss")
                if metric_to_monitor_scheduler == "val_loss":
                    scheduler.step(avg_epoch_val_loss)
                else:
                    raise NotImplementedError("ReduceLROnPlateau only supports val_loss as a metric at the moment")
            elif hyperparameters.scheduler_config and hyperparameters.scheduler_config.interval == "epoch":
                scheduler.step()
            # Step-based schedulers would be handled inside the batch loop (not implemented here for simplicity)


        # Early stopping check
        if hyperparameters.early_stopping_config:
            es_config = hyperparameters.early_stopping_config
            current_metric_val = avg_epoch_val_loss # Assuming monitoring val_loss

            # TODO: Adapt this if es_config.monitor is different (e.g. "train_loss", or a custom metric)
            # This requires a more flexible way to get the monitored metric.
            # For now, we assume es_config.monitor is effectively 'val_loss' as calculated above.

            improved = False
            if es_config.mode == "min":
                if current_metric_val < best_val_metric - es_config.min_delta: # Add type check for current_metric_val
                    best_val_metric = current_metric_val
                    improved = True
            else: # mode == "max"
                if current_metric_val > best_val_metric + es_config.min_delta: # Add type check for current_metric_val
                    best_val_metric = current_metric_val
                    improved = True

            if improved:
                epochs_no_improve = 0
                if es_config.restore_best_weights:
                    best_model_state_dict = model.state_dict()
                    logger.info(f"EarlyStopping: New best model found at epoch {actual_epoch} with {es_config.monitor}: {best_val_metric:.4f}")
            else:
                epochs_no_improve += 1
                logger.info(f"EarlyStopping: No improvement for {epochs_no_improve} epochs. Patience: {es_config.patience}")

            if epochs_no_improve >= es_config.patience:
                logger.info(f"EarlyStopping: Stopping training at epoch {actual_epoch} as {es_config.monitor} did not improve for {es_config.patience} epochs.")
                if es_config.restore_best_weights and best_model_state_dict:
                    logger.info("EarlyStopping: Restoring best model weights.")
                    model.load_state_dict(best_model_state_dict)
                break # Exit training loop

        # Save the checkpoint
        if save_checkpoint_hook:
            save_checkpoint_hook(
                # model.state_dict(),
                # {
                #     "epochs": actual_epoch + 1,
                #     "optimizer_state_dict": optimizer.state_dict(),
                #     "loss": avg_epoch_train_loss, # Save average train loss for the epoch
                #     "hyperparameters": hyperparameters.model_dump(), # Save validated and typed HPs
                # },
                model_state_dict=model.state_dict(),
                current_epoch=actual_epoch + 1,
                other_states={
                    "optimizer_state_dict": optimizer.state_dict(),
                    "loss": avg_epoch_train_loss, # Save average train loss for the epoch
                },
                hyperparameters=hyperparameters.model_dump(), # Save validated and typed HPs
                metrics={
                    "loss": avg_epoch_train_loss, # Save average train loss for the epoch
                },
            )

    # Test
    model.eval()
    num_batches = len(test_dataloader)
    test_loss = 0.0
    with torch.no_grad():
        for X, y in test_dataloader:
            pred = model(X)
            test_loss += loss_fn(pred, y).item()

    test_loss /= num_batches

    return {
        "metrics": {
            "test_loss": test_loss,
        }
    }


class PredictContext(TypedDict):
    pass


def predict(
    context: PredictContext,
    checkpoint: Checkpoint,
    *,
    params: dict[str, Any],
) -> pd.DataFrame:
    # Load hyperparameters from checkpoint
    hyperparameters_dict = checkpoint.get("hyperparameters")
    if not hyperparameters_dict:
        raise ValueError("Hyperparameters must be provided in the checkpoint")

    # Determine the HSM model type to parse the correct hyperparameters object
    hsm_model_type = hyperparameters_dict.get("hsm_model")
    hyperparameters_obj: SupportedHyperparameters
    if hsm_model_type == "general":
        hyperparameters_obj = GeneralHSModelHyperparameters.model_validate(hyperparameters_dict)
    elif hsm_model_type == "pauli":
        hyperparameters_obj = PauliHSModelHyperparameters.model_validate(hyperparameters_dict)
    elif hsm_model_type == "general_fullenergy":
        hyperparameters_obj = GeneralHSModelHyperparameters.model_validate(hyperparameters_dict)
    else:
        # If the hsm_model_type from checkpoint is unknown, we attempt to fall back to base ModelHyperparameters
        # or raise an error if that's not suitable / hsm_model_type is truly unrecognized.
        logger.warning(
            f"hsm_model type '{hsm_model_type}' in checkpoint is not explicitly handled or is missing. "
            f"Falling back to ModelHyperparameters for prediction. Model rehydration might be incomplete if model-specific params are needed."
        )
        # It's safer to raise an error if the specific model type can't be determined for rehydration
        # as Pytorch*HSM layers require specific counts.
        # However, the user might have a case where ModelHyperparameters is sufficient.
        # For now, let's try to validate with ModelHyperparameters as a last resort before erroring.
        try:
            hyperparameters_obj = ModelHyperparameters.model_validate(hyperparameters_dict)
        except Exception as e:
            raise ValueError(f"Unsupported or invalid hsm_model type '{hsm_model_type}' in checkpoint for prediction. Error: {e}")


    dataset_bucket = str(context.get("dataset_bucket", "s3"))
    dataset_format = str(context.get("dataset_format", "csv"))

    device = hyperparameters_obj.device # Use device from loaded and validated hyperparameters object

    # Rehydrate the model based on hsm_model type stored in the hyperparameter object itself
    hsm_layer: PytorchGeneralHSM | PytorchPauliHSM | PytorchGeneralHSMFullEnergy
    if hyperparameters_obj.hsm_model == "general":
        assert isinstance(hyperparameters_obj, GeneralHSModelHyperparameters)
        input_op_count = hyperparameters_obj.input_operator_count
        output_op_count = hyperparameters_obj.output_operator_count

        hsm_layer = PytorchGeneralHSM(
            input_operator_count=input_op_count,
            output_operator_count=output_op_count,
            hilbert_space_dims=hyperparameters_obj.hilbert_space_dims,
            initialization_mean_per_operator=hyperparameters_obj.initialization_mean_per_operator,
            initialization_std_per_operator=hyperparameters_obj.initialization_std_per_operator,
            beta=hyperparameters_obj.beta,
            input_operators=hyperparameters_obj.input_operators,
            output_operators=hyperparameters_obj.output_operators,
            complex=hyperparameters_obj.complex,
            eigh_eps=hyperparameters_obj.eigh_eps,
            device=device,
        )
    elif hyperparameters_obj.hsm_model == "pauli":
        assert isinstance(hyperparameters_obj, PauliHSModelHyperparameters)
        hsm_layer = PytorchPauliHSM(
            input_operator_count=hyperparameters_obj.input_operator_count,
            output_operator_count=hyperparameters_obj.output_operator_count,
            qubits_count=hyperparameters_obj.qubits_count,
            input_operator_pauli_weight=hyperparameters_obj.input_operator_pauli_weight,
            output_operator_pauli_weight=hyperparameters_obj.output_operator_pauli_weight,
            input_pauli_coeffs=hyperparameters_obj.input_pauli_coeffs,
            output_pauli_coeffs=hyperparameters_obj.output_pauli_coeffs,
            eigh_eps=hyperparameters_obj.eigh_eps,
            device=device,
        )
    elif hyperparameters_obj.hsm_model == "general_fullenergy":
        assert isinstance(hyperparameters_obj, GeneralHSModelHyperparameters)
        hsm_layer = PytorchGeneralHSMFullEnergy(
            input_operator_count=hyperparameters_obj.input_operator_count,
            output_operator_count=hyperparameters_obj.output_operator_count,
            hilbert_space_dims=hyperparameters_obj.hilbert_space_dims,
            device=device,
        )
    else:
        raise ValueError(f"Unsupported hsm_model type in checkpoint: {hyperparameters_obj.hsm_model}")

    model = WeightedLayer(hsm_layer=hsm_layer, device=device)

    # Display information about the model
    logger.info(f"Model: {model}")
    logger.info(f"Model named parameters: {[(name, param.shape) for name, param in model.named_parameters()]}")

    model_state_dict = checkpoint.get("model_state_dict")
    if not model_state_dict:
        raise ValueError("model_state_dict not found in checkpoint")
    model.load_state_dict(model_state_dict)


    dataset_path = params.get("dataset_path", None)

    if dataset_path is None:
        raise ValueError("Dataset path must be provided")

    dataset = resolve_dataset(dataset_path, dataset_bucket, dataset_format)
    X = dataset.df_ref()

    model.eval()

    with torch.no_grad():
        pred = model(X)

    return {"predictions": pred}


if __name__ == "__main__":
    import dotenv  # type: ignore
    import logging # Import logging

    # Configure logging to show INFO level messages
    logging.basicConfig(level=logging.INFO)

    dotenv.load_dotenv()

    result = train(
        context={
            "status_id": "test",
            "dataset_bucket": "local",
            "dataset_format": "csv",
        },
        dataset_path="test_dataset.csv",
        params={
            "hyperparameters": {
                "hsm_model": "general",
                "epochs": 1000,  # Increased to test early stopping
                "batch_size": 5,  # Smaller batch size for test dataset
                "seed": 24,
                "target": "scaled_demedian_forward_return_22d",
                "device": "cpu",  # Use CPU for testing
                "num_workers": 0,
                "pin_memory": False,
                "split": 0.2,  # 80/20 train/test split
                # GeneralHSModel specific - these will be updated by data_derived_input/output_operator_count in train
                "input_operator_count": 5,
                "output_operator_count": 1,
                "hilbert_space_dims": 4,
                "complex": True,
                "optimizer_config": {
                    "type": "Adam",
                    "default_params": {"lr": 1e-3},
                    "group_params": [
                        {
                            "param_name_contains": ["input_diag"],
                            "params": {"lr": 1e-4, "weight_decay": 0}
                        }
                    ]
                },
                "loss_fn_config": {
                    "type": "MSELoss",
                    "params": {}
                },
                "scheduler_config": {
                    "type": "StepLR",
                    "params": {"step_size": 3, "gamma": 0.5},
                    "interval": "epoch"
                },
                "early_stopping_config": {
                    "monitor": "val_loss",
                    "patience": 3,
                    "mode": "min",
                    "min_delta": 0.0001,
                    "verbose": True,
                    "restore_best_weights": True
                },
                "gradient_clipping_config": {
                    "max_norm": 1.0,
                    "norm_type": 2.0
                }
            },
        },
    )
    print("\nTraining Results:")
    print(f"Test Loss: {result['metrics']['test_loss']:.6f}")