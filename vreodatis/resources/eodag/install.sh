#!/bin/bash
# This file is provided under MIT license. See LICENSE file.
set -e

# EODAG providers directory = built-in providers (symlinks) + Ifremer STAC catalogs.
# EODAG_PROVIDERS_CFG_DIR replaces the built-in directory, hence the symlinks.
EODAG_PROVIDERS_DIR=/srv/conda/etc/eodag/providers
BUILTIN_DIR=$(${NB_PYTHON_PREFIX}/bin/python -c "import eodag.config as c; print(c.DEFAULT_PROVIDERS_DIR)")

mkdir -p ${EODAG_PROVIDERS_DIR}
ln -sf ${BUILTIN_DIR}/*.yml ${EODAG_PROVIDERS_DIR}/
cp resources/eodag/ifremer.yml ${EODAG_PROVIDERS_DIR}/
chmod -R a+rX /srv/conda/etc/eodag

cp resources/eodag/start-notebook-eodag.sh /usr/local/bin
chmod +x /usr/local/bin/start-notebook-eodag.sh
