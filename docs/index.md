# ODATIS VRE system image

This repository builds `vre-odatis`, the system image of the ODATIS VRE: JupyterLab with its
extensions and the tools of the VRE. It is a fork of
[CNES datalabs-docker-images](https://github.com/CNES/datalabs-docker-images), built on
`cnes/base-image`. The pages inherited from the upstream project (Binder, DockerHub images) describe
the CNES images.

The kernels and the configuration of each VRE live in other repositories:
[jupyter-kernels](https://gitlab.ifremer.fr/odatis-public/vre/jupyter-kernels) and
[jupyter-configs](https://gitlab.ifremer.fr/odatis-public/vre/jupyter-configs).

# How do I...?

```{toctree}
:maxdepth: 2
howto/publish.md
howto/launch.md
howto/custom-image.md
howto/conda-env.md
contributing.md
```

# Topic explainers

```{toctree}
:maxdepth: 2
topic/design.md
topic/environment-variables.md
```
