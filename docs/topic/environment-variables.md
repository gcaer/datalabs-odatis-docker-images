# Environment variables

The runtime environment sets two variables by default

1. `$PANGEO_ENV`: name of the conda environment.
2. `$PANGEO_SCRATCH`: a URL like `gcs://pangeo-scratch/username/` that
   points to a cloud storage bucket for temporary storage. This is set
   if the variable `$PANGEO_SCRATCH_PREFIX` and `JUPYTERHUB_USER`
   are detected. The prefix should be like `s3://pangeo-scratch`.

Every script named `start-notebook*.sh` will be executed at runtime if they are in the `/usr/local/bin` folder. They can be copied there from an `install.sh` script. This is useful if you need to setup more environment variables for the runtime. 
Here's an exemple of how it works : 

`resources/application/install.sh`:
```bash
#!/bin/bash

# Copy the start-notebook file
cp resources/application/start-notebook-application.sh /usr/local/bin

# Make sure the file can be executed 
chmod +x /usr/local/bin/start-notebook-application.sh
```

`resources/application/start-notebook-application.sh`:
```bash
#!/bin/bash

export SOME_VARIABLE="some value"
```

## Kernels and app launcher of the VRE

Two variables tell JupyterLab where the configuration of the VRE is stored, outside the image:

* `JUPYTER_PATH`: Jupyter looks for kernels in `${JUPYTER_PATH}/kernels/<name>/kernel.json`.
* `JUPYTER_APP_LAUNCHER_PATH`: folder of the `jp_app_launcher*.yml` files (with their `images/`
  folder, referenced as `./images/...`) that define the entries of the launcher. The image itself
  ships no launcher entry.

The `Dockerfile` gives them default values on the Ifremer storage
(`/scale/project/data-terra/intranet/odatis/vre-odatis` and `.../vre-odatis/app_launcher`). On
Datarmor, [jupyter-configs](https://gitlab.ifremer.fr/odatis-public/vre/jupyter-configs)
overrides them for each VRE with its `vre/<vre>/.env` file (`apptainer run --env-file`), so the
same image can serve several VREs with different kernels and launchers.

If a folder does not exist (e.g. when running the image outside the Ifremer infrastructure), it is
simply ignored.
