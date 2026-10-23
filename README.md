# datalabs-odatis-docker-images

System image of the ODATIS VRE (`vre-odatis`): JupyterLab with its extensions and the tools of the
VRE (VNC desktop, code-server, QGIS, OTB, eodag, Apptainer...). It is a fork of
[CNES datalabs-docker-images](https://github.com/CNES/datalabs-docker-images) and is built on
`cnes/base-image`, whose `ONBUILD` instructions install the files of `vreodatis/`.

The Python kernels and the VRE configuration (kernels, launcher entries) are not in this image:
see [jupyter-kernels](https://gitlab.ifremer.fr/odatis-public/vre/jupyter-kernels) and
[jupyter-configs](https://gitlab.ifremer.fr/odatis-public/vre/jupyter-configs).

## Content of `vreodatis/`

| File | Role |
|---|---|
| `environment.yml`, `pixi.toml` | conda packages of the `notebook` environment (edit both) |
| `conda-lock.yml` | locked environment installed by the build (`make conda-lock`) |
| `apt.txt` | system packages (merged with the base layers by `make apt`) |
| `resources/<tool>/install.sh` | installation of an additional tool, run at build time |
| `start` | startup script, runs the `/usr/local/bin/start-notebook-*` scripts |
| `Dockerfile` | `FROM cnes/base-image` + default environment variables |

## Make commands

```bash
make conda-lock   # solve pixi.toml with pixi, then write conda-lock.yml
make apt          # merge apt.txt with the base layers
make build        # build vre-odatis:master
make docker       # build vre-odatis:master and run the tests
make run          # JupyterLab on http://127.0.0.1:8888 (./work mounted)
make shell        # shell in the image (USER_ARG="--user root" to be root)
make publish      # push vre-odatis:master to Harbor (registry.hpc.ifremer.fr/hpc-jupyterhub-dev)
make update       # update the base layer files
```

A change in `environment.yml`/`pixi.toml` is only taken into account after `make conda-lock`.

## Release

Pushing a tag `X.Y.Z` to GitLab builds the image and publishes it as
`gitlab-registry.ifremer.fr/odatis-public/vre/datalabs-odatis-docker-images/vre-odatis:X.Y.Z`
(and `:latest`). See [How to publish the image](docs/howto/publish.md).

On Datarmor, the image is pulled as an Apptainer `.sif` and run by
[jupyter-configs](https://gitlab.ifremer.fr/odatis-public/vre/jupyter-configs)
(`make pull-system/vre-odatis TAG=X.Y.Z`, `make run/<vre>`).
