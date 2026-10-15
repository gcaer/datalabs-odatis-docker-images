#!/bin/bash
# Copyright 2024 CS GROUP - https://www.csgroup.eu
# Copyright 2024 CNES - https://cnes.fr
# All rights reserved
# This file is provided under MIT license. See LICENSE file.
set -e

# Jupyter App Launcher: "Odatis Expertise Center" section in the JupyterLab Launcher
# (same location as the odatis-base image: /usr/local/share/jupyter is in jupyter_path)
APP_LAUNCHER_DIR=/usr/local/share/jupyter/jupyter_app_launcher
mkdir -p ${APP_LAUNCHER_DIR}
cp resources/app_launcher/jp_app_launcher.yml ${APP_LAUNCHER_DIR}/
cp -r resources/app_launcher/images ${APP_LAUNCHER_DIR}/
chmod -R a+rX ${APP_LAUNCHER_DIR}
