# Copyright 2024 CS GROUP - https://www.csgroup.eu
# All rights reserved
# This file is provided under MIT license. See LICENSE file.

"""
Return config on servers

See https://jupyter-server-proxy.readthedocs.io/en/latest/server-process.html
for more information.
"""
import getpass
import os
import shutil
import shlex
import subprocess


def setup_rstudio():
    def _get_rsession_env(port):
        # Detect various environment variables rsession requires to run
        # Via rstudio's src/cpp/core/r_util/REnvironmentPosix.cpp
        cmd = [
            "R",
            "--slave",
            "--vanilla",
            "-e",
            'cat(paste(R.home("home"),R.home("share"),R.home("include"),R.home("doc"),getRversion(),sep=":"))',
        ]

        r_output = subprocess.check_output(cmd)
        (
            R_HOME,
            R_SHARE_DIR,
            R_INCLUDE_DIR,
            R_DOC_DIR,
            version,
        ) = r_output.decode().split(":")

        return {
            "R_DOC_DIR": R_DOC_DIR,
            "R_HOME": R_HOME,
            "R_INCLUDE_DIR": R_INCLUDE_DIR,
            "R_SHARE_DIR": R_SHARE_DIR,
            "RSTUDIO_DEFAULT_R_VERSION_HOME": R_HOME,
            "RSTUDIO_DEFAULT_R_VERSION": version,
        }

    def _get_rsession_cmd(port):
        # Other paths rsession maybe in
        other_paths = [
            # When rstudio-server deb is installed
            "/usr/lib/rstudio-server/bin/rsession",
            # When just rstudio deb is installed
            "/usr/lib/rstudio/bin/rsession",
        ]
        if shutil.which("rsession"):
            executable = "rsession"
        else:
            for op in other_paths:
                if os.path.exists(op):
                    executable = op
                    break
            else:
                raise FileNotFoundError("Can not find rsession in PATH")

        return [
            executable,
            "--standalone=1",
            "--program-mode=server",
            "--log-stderr=1",
            "--session-timeout-minutes=0",
            "--user-identity=" + getpass.getuser(),
            "--www-port=" + str(port),
        ]

    return {
        "command": _get_rsession_cmd,
        "environment": _get_rsession_env,
        "launcher_entry": {
            "title": "RStudio",
            "icon_path": os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "icons", "rstudio.svg"
            ),
        },
        "new_browser_tab": True,
    }


def setup_codeserver():
    # Make sure codeserver is in $PATH
    def _codeserver_command(unix_socket):
        full_path = shutil.which("code-server")
        if not full_path:
            raise FileNotFoundError("Can not find code-server in $PATH")
        working_dir = os.getenv("CODE_WORKINGDIR", None)
        if working_dir is None:
            working_dir = os.path.expanduser("~")
        if working_dir is None:
            working_dir = os.getenv("JUPYTER_SERVER_ROOT", ".")

        return [
            full_path,
            # Unix socket in a private (0700) temporary folder created by
            # jupyter-server-proxy: only the user can reach code-server, and
            # Jupyter already authenticates the requests, so no password.
            "--socket=" + unix_socket,
            "--socket-mode=600",
            "--auth",
            "none",
            "--disable-telemetry",
            "--extensions-dir",
            os.path.join(os.path.join(working_dir, ".vscode"), "extensions"),
            working_dir,
        ]

    return {
        "command": _codeserver_command,
        "unix_socket": True,
        "timeout": 20,
        "launcher_entry": {
            "title": "VS Code IDE",
            "icon_path": os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "icons", "vscode.svg"
            ),
        },
        "new_browser_tab": True,
    }


def setup_novnc():
    def _novnc_command(port):

        vnc_command = " ".join(shlex.quote(p) for p in ([
            "vncserver",
            "-rfbport", str(port),
            "-verbose",
            "-xstartup", "/usr/bin/dbus-launch /usr/local/bin/vre-xstartup",
            "-geometry", "1680x1050",
            "-fg"
        ]))

        return [
            "websockify", "-v",
            "--web", "/opt/noVNC",
            "--heartbeat", "30",
            str(port),
            "--",
            "/bin/sh", "-c", f"{vnc_command}"
        ]
    
    novnc_token = os.getenv("NOVNC_TOKEN")
    if not novnc_token:
        raise TypeError("NOVNC_TOKEN not set")
    
    return {
        "command": _novnc_command,
        "timeout": 20,
        "launcher_entry": {
            "title": "Desktop",
            "icon_path": os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "icons", "xfce.svg"
            ),
            "path_info": "desktop/vnc.html?autoconnect=true&password=" + novnc_token 
        },
        "mappath": {"/": "/vnc.html"},
        "new_browser_tab": True,
    }
