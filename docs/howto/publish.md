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

## Harbor

The CI does not publish to Harbor: build the image locally, then use `make publish`, which pushes
`vre-odatis:master` to `registry.hpc.ifremer.fr/hpc-jupyterhub-dev/vre-odatis:master` (override
with `HARBOR_REGISTRY`/`HARBOR_OWNER`).
