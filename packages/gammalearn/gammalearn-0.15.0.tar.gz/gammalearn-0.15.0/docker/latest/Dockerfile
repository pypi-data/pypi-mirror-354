ARG BASE_IMAGE_LOCATION

FROM ${BASE_IMAGE_LOCATION}

# micromamba dockerfile makes use of SHELL. If it is overwritten
# the auto-activate might not work
# https://micromamba-docker.readthedocs.io/en/latest/advanced_usage.html#use-of-the-shell-command-within-a-dockerfile

# Note: if defining entrypoints one must make sure to not overwrite the
# micromamba entrypoint, otherwise the base environment won't be loaded.
# https://micromamba-docker.readthedocs.io/en/latest/advanced_usage.html#use-of-the-entrypoint-command-within-a-dockerfile

# Install package in base environment using pip
COPY . /opt/gammalearn
RUN micromamba run -n base pip install --no-deps /opt/gammalearn

# Remove package sources
USER root
RUN rm -fr /opt/gammalearn
USER $MAMBA_USER
