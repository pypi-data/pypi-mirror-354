FROM mambaorg/micromamba:debian-slim

# micromamba dockerfile makes use of SHELL. If it is overwritten
# the auto-activate might not work
# https://micromamba-docker.readthedocs.io/en/latest/advanced_usage.html#use-of-the-shell-command-within-a-dockerfile

# Note: if defining entrypoints one must make sure to not overwrite the
# micromamba entrypoint, otherwise the base environment won't be loaded.
# https://micromamba-docker.readthedocs.io/en/latest/advanced_usage.html#use-of-the-entrypoint-command-within-a-dockerfile

# We need git and ssh for setuptools scm to automatically detect version
USER root
RUN apt update && apt upgrade -y && apt install -y git git-lfs && apt clean && apt autoremove
# We need to change the permissions on /opt/conda so that other users will be able to modify the environment
# this is required to let the developers entering the container with their own "uid" to be able to install/modify
# dependencies. 
RUN chown -R $MAMBA_USER /opt/conda
USER $MAMBA_USER

# Copy the development pinned dependencies file. It is generated in the first CI stage and made an artifact
ARG DEV_PINNED_DEPENDENCIES_FILE
COPY ${DEV_PINNED_DEPENDENCIES_FILE} .

# Install environment in base env
# This is the installation recommanded by micromamba's docker doc
# https://micromamba-docker.readthedocs.io/en/latest/quick_start.html
# (First remove everything in base env)
RUN eval "$(micromamba shell hook --shell bash)" && \
    micromamba install --yes -n base -f ${DEV_PINNED_DEPENDENCIES_FILE} && \
    micromamba clean --all --yes && chmod -R o+w /opt/conda/*
