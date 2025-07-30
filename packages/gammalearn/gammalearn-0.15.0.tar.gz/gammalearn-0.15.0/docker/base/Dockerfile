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
USER $MAMBA_USER

# Copy the pinned dependencies file. It is generated in the first CI stage and made an artifact
ARG PROD_PINNED_DEPENDENCIES_FILE
COPY ${PROD_PINNED_DEPENDENCIES_FILE} .

# Install environment in base env
# This is the installation recommanded by micromamba's docker doc
# https://micromamba-docker.readthedocs.io/en/latest/quick_start.html
# (First remove everything from base env)
RUN eval "$(micromamba shell hook --shell bash)" && \
    micromamba install --yes -n base -f ${PROD_PINNED_DEPENDENCIES_FILE} && \
    micromamba clean --all --yes
