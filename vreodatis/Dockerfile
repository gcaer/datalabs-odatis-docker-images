# ONBUILD instructions in base-image/Dockerfile are used to
# perform certain actions based on the presence of specific
# files (such as conda-linux-64.lock, start) in this repo.
# Refer to the base-image/Dockerfile for documentation.
ARG PANGEO_BASE_IMAGE_TAG=master
FROM cnes/base-image:${PANGEO_BASE_IMAGE_TAG}

# Shared VRE configuration on the Ifremer storage, added to what the image ships:
# - kernels: Jupyter looks for kernel specs in ${JUPYTER_PATH}/kernels/<name>/kernel.json
# - app launcher: jp_app_launcher*.yml (+ its images/) in ${JUPYTER_APP_LAUNCHER_PATH}
ENV JUPYTER_PATH=/scale/project/data-terra/intranet/odatis/vre-odatis \
    JUPYTER_APP_LAUNCHER_PATH=/scale/project/data-terra/intranet/odatis/vre-odatis/app_launcher
