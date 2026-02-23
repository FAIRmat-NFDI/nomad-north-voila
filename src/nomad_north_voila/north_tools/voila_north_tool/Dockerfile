ARG IMAGE_TAG=lab-4.5.4
ARG BASE_IMAGE=quay.io/jupyter/datascience-notebook
ARG UV_VERSION=0.9
ARG PLUGIN_NAME=nomad-north-voila

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv_stage

FROM ${BASE_IMAGE}:${IMAGE_TAG} AS base

# https://github.com/hadolint/hadolint/wiki/DL4006
# https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

COPY --from=uv_stage /uv /uvx /bin/

USER root

# Define environment variables
# With pre-existing NB_USER="jovyan" and NB_UID=100, NB_GID=1000
ENV HOME=/home/${NB_USER}
ENV CONDA_DIR=/opt/conda

ARG PLUGIN_NAME

RUN apt-get update \
 && apt-get install --yes --quiet --no-install-recommends \
      libmagic-dev \
 && rm -rf /var/lib/apt/lists/* \
 && rm -rf /tmp/*

 # Needed to build jupyter-lab
 # Add NodeSource APT repo for Debian-base distributions repository
RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash -

# Install Node.js from the Debian-based distributions repository
RUN apt-get install nodejs -y \
       && npm install -g configurable-http-proxy@^4.2.0 \
       # clean cache and logs
       && rm -rf /var/lib/apt/lists/* /var/log/* /var/tmp/* ~/.npm

USER ${NB_USER}
# To open voila preview on side panel in jupyterlab
RUN npm i @voila-dashboards/jupyterlab-preview


# uv env
ENV UV_PROJECT_ENVIRONMENT=${CONDA_DIR} \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1 \
    UV_SYSTEM_PYTHON=1

COPY --chown=${NB_USER}:${NB_GID} . ${HOME}/${PLUGIN_NAME}

WORKDIR ${HOME}/${PLUGIN_NAME}

# https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --group north --inexact --no-install-project

WORKDIR ${HOME}
RUN rm -rf ${HOME}/${PLUGIN_NAME}

RUN jupyter server extension enable voila

RUN jupyter lab build --dev-build=False --minimize=False

# After build remove node_modules and package-lock.json to reduce image size, as they are not needed at runtime
RUN rm -rf ${HOME}/node_modules package-lock.json package.json

RUN fix-permissions "/home/${NB_USER}" \
    && fix-permissions "${CONDA_DIR}"

EXPOSE 8888

RUN touch ${HOME}/.hushlogin