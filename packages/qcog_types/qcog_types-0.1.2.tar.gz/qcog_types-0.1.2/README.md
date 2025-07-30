# Deploy new Experiment


# Deploy new Environment

Currently, the process for deploying a new environment is completely manual
and should be run from a local machine that has Admin access to the AWS account.

## Steps

1. Create a new folder in the `docker-environments` directory
2. Create a new Dockerfile in the new folder.
3. Add all the files that are needed for the new environment.
4. Run `scripts/build-docker-env.sh` to build the new environment.

**Gemfury Access**

If the docker build requires access to private repositories, you will need to
provide the credentials to the build script.

We assume that the credentials are used through the `uv` tool.

You can declare a new index for a private package by adding the following to the `pyproject.toml` file:

```toml
[tool.uv.sources]
<my_private_package> = { index = "gemfury" }

[[tool.uv.index]]
name = "gemfury"
url = "https://pypi.fury.io/qognitive"
authenticate = "always"
explicit=true
```

Credentials are passed as environment variables to the build script.

```bash
export UV_INDEX_GEMFURY_USERNAME=<your-username>
export UV_INDEX_GEMFURY_PASSWORD=<your-password>
```

## Command example
```bash
./scripts/build-docker-env.sh py3.12 0.0.1 dev
```

This will build the docker image and push it to the ECR repository.


# Deploy experiment types