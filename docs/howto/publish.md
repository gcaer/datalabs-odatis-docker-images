# How to publish the vre-odatis image

## GitLab CI

The repository is hosted both on GitHub and on the Ifremer GitLab
(`odatis-public/vre/datalabs-odatis-docker-images`). Pushing a Git tag `X.Y.Z` (or `vX.Y.Z`)
to GitLab makes the CI build the image from `vreodatis/` and push it to the GitLab registry as
`gitlab-registry.ifremer.fr/odatis-public/vre/datalabs-odatis-docker-images/vre-odatis:X.Y.Z`
(and `:latest`). No image is built on a branch push.

```bash
git remote add gitlab https://gitlab.ifremer.fr/odatis-public/vre/datalabs-odatis-docker-images.git
git push gitlab master
git tag 0.1.0
git push gitlab 0.1.0           # triggers the build and the publication
git push origin master --tags   # keeps GitHub up to date
```

The CI uses the Ifremer component `pipeline-generic-container-image@1.1.17` (`.gitlab-ci.yml`).
Its build job is overridden so that it only runs on a release tag.

```{warning}
Do not include another Ifremer component (e.g. `pipeline-documentation-sphinx@~latest`) in the
same pipeline: its `workflow:` replaces the one of the image component, and the image is then
published as `X-Y-Z` instead of `X.Y.Z`.
```

## Use on Datarmor (Apptainer)

The published image is converted to a `.sif` and run on Datarmor by
[jupyter-configs](https://gitlab.ifremer.fr/odatis-public/vre/jupyter-configs):

```bash
make pull-system/vre-odatis TAG=0.2.0   # → apptainer/system/vre-odatis-0.2.0.sif
make run/vre-odatis
```

## Harbor

The CI does not publish to Harbor: build the image locally, then use `make publish`, which pushes
`vre-odatis:master` to `registry.hpc.ifremer.fr/hpc-jupyterhub-dev/vre-odatis:master` (override
with `HARBOR_REGISTRY`/`HARBOR_OWNER`).
