# Docker

[Direct Linux build of local files]: #direct-linux-build
[Build local srcML on a Linux distribution]: #build-srcml-on-a-linux-distribution
[Debug srcML on a Linux distribution]: #debug-srcml-on-a-linux-distribution
[Architecture]: #architecture
[Approaches]: #approaches

srcML uses Docker images to build, package, and test on Linux. 

If your host is not Linux (macOS or Windows), or you want to debug or build srcML on another distribution or version, the easiest way is to use these docker images.

We currently support multiple versions of Ubuntu, Fedora, and OpenSUSE. For the complete list, see the variable `distributions` in the file _docker-bake.override.hcl_.

* [Direct Linux build of local files]
* [Build srcML on a Linux distribution]
* [Debug srcML on a Linux distribution]
* [Architecture]
* [Approaches]

**Note** All commands shown below must be entered in the root of the source directory, _srcML_. They cannot be used from the build directory.

## Direct Linux Build

The build environment docker images provide all the necessary software to build, generate packages, and test for a specific Linux distribution. You can directly use the image with docker:

```console
docker run -v "${PWD}":/srcML --workdir /Build -it srcml/ubuntu:24.04
```

This puts you in a shell in the /Build directory in a container with your current changes where you can enter your build commands.

The direct `docker run` command is quite complex, and this is only the start of configuration. To make it much easier you can use services defined in `docker compose`. See [Build srcML on a Linux distribution].

## Build srcML on Linux

As an alternative to `docker run`, srcML has a set of services configured in `docker compose`. Like the `docker run` in [Direct Linux Build], the build will occur in a _build_ directory inside the docker container, and will not cause any change to your host directory.

You may already know the cmake `--workflow` and `--preset`. These automate the configuration of cmake, building, packaging, installation, and testing. The default operation is to run the workflow `ci-<platform>`. For each platform, these presets define all the settings necessary for the above. E.g., for Ubuntu:

```console
cmake --workflow --preset ci-ubuntu
```

Fortunately, we do not have to figure out all those settings, as `docker compose` already has this configured.

### Build srcML on all supported Linux distributions:

This command simultaneously starts srcML builds for all supported Linux distributions:

```console
docker compose up
```

That will probably overwhelm your machine, so we have separate _services_ (in the docker-compose terminology) to limit this to specific distributions or categories. E.g., to build srcML on Ubuntu:24.04

```console
docker compose up ubuntu_24_04
```

Note the underscore, `'_'`, in place of the `':'` and `'.'`.

To build and package srcML for all Ubuntu distributions you can use _profiles_:

```console
docker compose --profile ubuntu up
```

All Linux services are organized into Docker Compose profiles. They include a default profile, e.g., `package`; Linux distributions, e.g., `ubuntu`, `fedora`, and `opensuse`, and age, e.g., `latest`, `earliest`.

## Debug srcML on Linux

The command from above:

```console
docker compose up ubuntu_24_04
```

ran the automated workflow preset. However, you can interact with the container:

```console
docker compose up ubuntu_24_04 /bin/bash
```

This gives you a shell into the container. You can enter any command, but the source files (and directory) are read-only. A good first step is to use the configure preset:

```console
root@04285c4739e5:/srcML\# cmake --preset ci-ubuntu
```

From there you can go to the _/srcML-Build_ directory and enter commands.

As you change the source code on the host, the change is reflected in the container's _/srcML_ directory.

## Use the Build Image Directly

You can also directly use the build image. The following mimics the `docker compose up ubuntu_24_04 /bin/bash` using `docker run`:

```console
docker run -v "${PWD}:/srcML:ro --workdir /srcML -it srcml/ubuntu:24.04
```

You are then in a shell in the directory /srcML and can enter commands.

## Approaches
The images can be used to build in two different ways:

* **Build in a Docker Container** You can use a build environment Docker image with everything installed to build and package srcML. This is easily connected to your current repository working copy and is good for development and debugging. This uses `docker-compose` and the configuration in the file _compose.yml_.

* **Build in Docker Image** You can create a new Docker image where srcML is built and packaged as the Docker image is created. This uses `docker buildx bake` and the configuration is in the files _docker-bake.hcl_ and _docker-bake.override.hcl_.

To maintain the build images for above:

* **Create build Images** You can create a Docker image with the build environment. This is only needed if there are new needed packages or updates to CMake.

## Architecture

The default architecture for a docker container is your host machine's architecture, i.e., `linux/amd64` or `linux/arm64`. To build on the non-default architecture, set the environment variable `PLATFORM`. E.g., To build for x86 while on  an ARM architecture, you can set the environment variable:

```console
export PLATFORM="linux/amd64"
docker compose up ubuntu_24_04
```

Or run the command with the environment set:

```console
PLATFORM="linux/amd64" docker compose up ubuntu_24_04
```

## Configuration Files

The configuration for Docker is in the following files:

* _compose.yml_ Main docker-compose configuration
* _compose.override.yml_ Maintenance docker-compose configuration
* _docker-bake.hcl_ Base docker bake configuration
* _docker-bake.override.hcl_ The docker bake configuration for supported Linux distributions

In addition, the directory tree at _docker_ contains the dockerfiles for each supported platform:

* _docker/ubuntu/Dockerfile_
* _docker/fedora/Dockerfile_
* _docker/opensuse/Dockerfile_

## Supported Linux Distributions


## Build in a Docker Container

A Docker Compose file, `compose.yml`, is in the root directory and allows execution on all the Linux distributions for packaging. They use build environments available for supported Linux distributions, e.g., srcml/ubuntu:24.04. The Dockerfiles are in the directory `docker` with a subdirectory for each platform.

The build environment images are built and maintained using `docker buildx bake`. This configuration is in the files _docker-bake.hcl_ and _docker-bake.override.hcl_. Using `bake` you can also build packages and test them.


## Maintain Docker Images

The following commands apply to all Docker images. To selectively do any of the following, see the variations above.


If the Dockerfiles change, a new one is added, or a previous one is updated, the image needs to be rebuilt. To build all docker images (after Dockerfile change):

```console
docker compose build
```

To push all docker images to Docker Hub (if you have permission):

```console
docker compose push
```
