# CORE EMU Dockerfile

A Dockercontainer to run [CORE](https://github.com/coreemu/core) preconfigured with DTN softwares and the ability to be used as a [MACI](https://github.com/AlexanderFroemmgen/maci) worker.

If CORE complains about missing `ebtables`, your kernel modules might not be available inside the container. To fix this issue, execute `modprobe ebtables` on your host and restart the container.

```bash
# Build the container
docker-compose build core

# Start the container with the available $DISPLAY environment variable..
docker-compose up core

# ..or a specific one
DISPLAY=docker.for.mac.localhost:0 docker-compose up core
DISPLAY=:3 docker-compose up core

# If your host system uses the X window system (like on a GNU/Linux), you might
# want to allow local connections.
# Enable those _before_ starting the container:
xhost +local:root
# And disable those again:
xhost -local:root
```

## Test local development

If you want to check your latest changes, you might want to bind mount your
dtn7 directory over the overlay.

```sh
# Bind mound
sudo mount --bind /your/dtn7/directory dtn7

# Clean up
sudo umount dtn7
```

## Running experiments

This repository is also meant as a plugin for [maci-docker-compose](https://github.com/umr-ds/maci-docker-compose), which creates the MACI environment and allows multiple workers to connect to it.

```sh
# clone maci-docker-compose
git clone --recursive https://github.com/umr-ds/maci-docker-compose

# remove the default maci_data folder
cd maci-docker-compose
rm -rf maci_data

# clone the evaluation repository
git clone https://github.com/dtn7/networkeval maci_data

# start the MACI backend
docker-compose up -d

# run a local worker, to connect to the local MACI backend
cd maci_data
DISPLAY= BACKEND=localhost docker-compose run core

# The MACI backend is running on http://localhost:63658
# Running docker on macOS, it can be tricky to connect the worker to the backend, therefore the hostname docker.for.mac.localhost can be used
DISPLAY= BACKEND=docker.for.mac.localhost docker-compose run core
```

## Related Work

- <https://github.com/umr-ds/maci-serval_core_worker>
- <https://github.com/D3f0/coreemu_vnc>
