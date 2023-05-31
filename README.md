# MWAA Local

A local instance for working with MWAA.

This image will be built as `nicholasgriffinbbc/mwaa-local`, you can find it, deployed to the Docker Hub here:

https://hub.docker.com/r/nicholasgriffinbbc/mwaa-local

## Prerequisites

### Python

- Python 3.10 or higher
- Pip3 or higher

### Docker

- **macOS**: [Install Docker Desktop](https://docs.docker.com/desktop/).
- **Linux/Ubuntu**: [Install Docker Compose](https://docs.docker.com/compose/install/) and [Install Docker Engine](https://docs.docker.com/engine/install/).
- **Windows**: Windows Subsystem for Linux (WSL) to run the bash based command `mwaa-local-env`. Please follow [Windows Subsystem for Linux Installation (WSL)](https://docs.docker.com/docker-for-windows/wsl/) and [Using Docker in WSL 2](https://code.visualstudio.com/blogs/2020/03/02/docker-in-wsl2), to get started.

## Getting Started

First you'll need to clone the repo on your machine and access this folder with the following commands:

```bash
git clone https://github.com/nicholasgriffinbbc/mwaa-local
cd mwaa-local
```

### Building the Docker image

Nest you'll need to build the docker image for the MWAA instance.

> **Note**
> It will take several minutes to build this image locally

You can do that with the following command:

```bash
./mwaa-setup build-image
```

### Running Airflow

> **Note**
> It will take a couple minutes to start this image locally

Once it has built, you can start the airflow environment with the following command:

```bash
./mwaa-setup start
```

To stop this local environment, just press `Ctrl+C` on the terminal and wait until the runner and containers have stopped.

### Accessing airflow

Once started, the local Airflow instance should be available at: http://localhost:8080/.

By default, the credentials for the UI are:

- Username: `admin`
- Password: `test`

### Adding new DAGs

DAGs are stored and updated from the `dags/` folder. Initially, you should see a hello world DAG already set up here for you.

New DAGs should also be added to this folder.

### Adding code dependencies

If any new requirements are required, you should add them to the file `requirements/requirements.txt`.

You can test any new requirements with the command:

```bash
./mwaa-setup test-requirements
```

To package them, run the following script:

```bash
./mwaa-setup package-requirements
```

Any new plugins that you require can be added to the directory `plugins/`.

And if you require anything to run on startup of MWAA, you can adjust the file `startup_script/startup.sh`. Once edited, this can be tested with the following command:

```bash
./mwaa-setup test-startup-script
```
