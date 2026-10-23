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

## Shared kernels and app launcher (vre-odatis)

The `vreodatis` image sets two variables in its `Dockerfile` so that configuration shared on the
Ifremer storage is picked up at runtime, in addition to what is installed in the image:

* `JUPYTER_PATH=/scale/project/data-terra/intranet/odatis/vre-odatis`: every kernel spec stored as
  `/scale/project/data-terra/intranet/odatis/vre-odatis/kernels/<name>/kernel.json` shows up in the
  JupyterLab launcher.
* `JUPYTER_APP_LAUNCHER_PATH=/scale/project/data-terra/intranet/odatis/vre-odatis/app_launcher`:
  `jp_app_launcher*.yml` files in this folder (with their `images/` folder, referenced as
  `./images/...`) define the entries of the launcher. The image itself ships no app launcher
  entry: they are all managed in this shared folder.

If a folder does not exist (e.g. when running the image outside the Ifremer infrastructure), it is
simply ignored.
