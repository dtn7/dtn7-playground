# CORE EMU Dockerfile / dtn7-playground
A Dockercontainer to run [CORE](https://github.com/coreemu/core) preconfigured
with DTN7-Go for extendet CI tests if DTN7-Go.

## Requirements
If CORE complains about missing `ebtables`, your kernel modules might not be
available inside the container. To fix this issue, execute `modprobe ebtables`
on your host and restart the container.

## Local development
This container has two modes: GUI based and headless. For local development, it
makes sense to run the GUI version, but it is also possible to start the
execution of the test headless.

### General
First you have to build the container.

```bash
docker-compose build
```

### GUI
To start the container in GUI mode, you have to set the DISPLAY variable as an
environment variable. This can be done during the startup process. You also may
want to allow local X connections before on Linux with `xhost +local:root` and
disable afterwards with `xhost -local:root`

```bash
# Linux
DISPLAY=:3 docker-compose up
# macOS
DISPLAY=docker.for.mac.localhost:0 docker-compose up
```

This will start up the CORE GUI. You can now fiddle around, test various things
and run multiple emulated virtual nodes.

### Headless
When the container is executed headless with the following command, the tests
will be started automatically.

```bash
# Linux
DISPLAY= docker-compose up
```

The results of the experiment will be stored in the `results` folder.

#### Configuration
The experiments require three parameters: the size of the payloads to be sent,
how many bundles should be sent per node and how long the experiment should be
executed. These parameters are set in the `experiment_settings.env` file and
will set the parameters as environment variables in the Docker container.

## Github Actions execution
As this setup is meant to be used for extended Github Actions tests, the entire
setup is done in the main DTN7-Go repository.

## See also
- <https://github.com/umr-ds/maci-serval_core_worker>
- <https://github.com/D3f0/coreemu_vnc>
- <https://github.com/dtn7/adhocnow2019-evaluation>
