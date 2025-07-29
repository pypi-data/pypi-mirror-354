import shlex
from typing import Dict, List, Optional

from mako.template import Template

from truefoundry.common.constants import ENV_VARS, PythonPackageManager
from truefoundry.deploy._autogen.models import SparkBuildSpec
from truefoundry.deploy.builder.constants import (
    PIP_CONF_BUILDKIT_SECRET_MOUNT,
    PIP_CONF_SECRET_MOUNT_AS_ENV,
    UV_CONF_BUILDKIT_SECRET_MOUNT,
    UV_CONF_SECRET_MOUNT_AS_ENV,
)
from truefoundry.deploy.v2.lib.patched_models import (
    _resolve_requirements_path,
)

# TODO (chiragjn): Switch to a non-root user inside the container

DEFAULT_PYTHON_IMAGE_REPO = "apache/spark"

_POST_PYTHON_INSTALL_TEMPLATE = """
% if apt_install_command is not None:
RUN ${apt_install_command}
% endif
% if requirements_path is not None:
COPY ${requirements_path} ${requirements_destination_path}
% endif
% if python_packages_install_command is not None:
RUN ${package_manager_config_secret_mount} ${python_packages_install_command}
% endif
COPY . /app
WORKDIR /app
USER spark
"""

DOCKERFILE_TEMPLATE = Template(
    """
FROM ${spark_image_repo}:${spark_version}
USER root
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*
COPY execute_notebook.py /app/execute_notebook.py
"""
    # + _POST_PYTHON_INSTALL_TEMPLATE
)

ADDITIONAL_PIP_PACKAGES = ['papermill']

def generate_apt_install_command(apt_packages: Optional[List[str]]) -> Optional[str]:
    packages_list = None
    if apt_packages:
        packages_list = " ".join(p.strip() for p in apt_packages if p.strip())
    if not packages_list:
        return None
    apt_update_command = "apt update"
    apt_install_command = f"DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends {packages_list}"
    clear_apt_lists_command = "rm -rf /var/lib/apt/lists/*"
    return " && ".join(
        [apt_update_command, apt_install_command, clear_apt_lists_command]
    )


def generate_pip_install_command(
    requirements_path: Optional[str],
    pip_packages: Optional[List[str]],
    mount_pip_conf_secret: bool = False,
) -> Optional[str]:
    upgrade_pip_command = "python -m pip install -U pip setuptools wheel"
    envs = []
    if mount_pip_conf_secret:
        envs.append(PIP_CONF_SECRET_MOUNT_AS_ENV)

    command = ["python", "-m", "pip", "install", "--use-pep517", "--no-cache-dir"]
    args = []
    if requirements_path:
        args.append("-r")
        args.append(requirements_path)

    if pip_packages:
        args.extend(pip_packages)

    if not args:
        return None

    final_pip_install_command = shlex.join(envs + command + args)
    final_docker_run_command = " && ".join(
        [upgrade_pip_command, final_pip_install_command]
    )
    return final_docker_run_command


def generate_uv_pip_install_command(
    requirements_path: Optional[str],
    pip_packages: Optional[List[str]],
    mount_uv_conf_secret: bool = False,
) -> Optional[str]:
    upgrade_pip_command = "python -m pip install -U pip setuptools wheel"
    uv_mount = f"--mount=from={ENV_VARS.TFY_PYTHON_BUILD_UV_IMAGE_URI},source=/uv,target=/usr/local/bin/uv"
    envs = [
        "UV_LINK_MODE=copy",
        "UV_PYTHON_DOWNLOADS=never",
        "UV_INDEX_STRATEGY=unsafe-best-match",
    ]
    if mount_uv_conf_secret:
        envs.append(UV_CONF_SECRET_MOUNT_AS_ENV)

    command = ["uv", "pip", "install", "--no-cache-dir"]

    args = []

    if requirements_path:
        args.append("-r")
        args.append(requirements_path)

    if pip_packages:
        args.extend(pip_packages)

    if not args:
        return None

    uv_pip_install_command = shlex.join(envs + command + args)
    shell_commands = " && ".join([upgrade_pip_command, uv_pip_install_command])
    final_docker_run_command = " ".join([uv_mount, shell_commands])

    return final_docker_run_command


def generate_dockerfile_content(
    build_configuration: SparkBuildSpec,
    package_manager: str = ENV_VARS.TFY_PYTHON_BUILD_PACKAGE_MANAGER,
    mount_python_package_manager_conf_secret: bool = False,
) -> str:
    # TODO (chiragjn): Handle recursive references to other requirements files e.g. `-r requirements-gpu.txt`
    requirements_path = _resolve_requirements_path(
        build_context_path=build_configuration.build_context_path,
        requirements_path=build_configuration.requirements_path,
    )
    requirements_destination_path = (
        "/tmp/requirements.txt" if requirements_path else None
    )
    if not build_configuration.spark_version:
        raise ValueError(
            "`spark_version` is required for `tfy-spark-buildpack` builder"
        )
    
    # Handle pip packages - SparkBuildSpec pip_packages is Optional[List[str]], so we need to handle None
    pip_packages = build_configuration.pip_packages or []
    
    if package_manager == PythonPackageManager.PIP.value:
        python_packages_install_command = generate_pip_install_command(
            requirements_path=requirements_destination_path,
            pip_packages=pip_packages + ADDITIONAL_PIP_PACKAGES,
            mount_pip_conf_secret=mount_python_package_manager_conf_secret,
        )
    elif package_manager == PythonPackageManager.UV.value:
        python_packages_install_command = generate_uv_pip_install_command(
            requirements_path=requirements_destination_path,
            pip_packages=pip_packages + ADDITIONAL_PIP_PACKAGES,
            mount_uv_conf_secret=mount_python_package_manager_conf_secret,
        )
    else:
        raise ValueError(f"Unsupported package manager: {package_manager}")

    apt_install_command = generate_apt_install_command(
        apt_packages=build_configuration.apt_packages
    )
    template_args = {
        "spark_image_repo": ENV_VARS.TFY_SPARK_BUILD_SPARK_IMAGE_REPO,
        "spark_version": build_configuration.spark_version,
        "apt_install_command": apt_install_command,
        "requirements_path": requirements_path,
        "requirements_destination_path": requirements_destination_path,
        "python_packages_install_command": python_packages_install_command,
    }

    if mount_python_package_manager_conf_secret:
        if package_manager == PythonPackageManager.PIP.value:
            template_args["package_manager_config_secret_mount"] = (
                PIP_CONF_BUILDKIT_SECRET_MOUNT
            )
        elif package_manager == PythonPackageManager.UV.value:
            template_args["package_manager_config_secret_mount"] = (
                UV_CONF_BUILDKIT_SECRET_MOUNT
            )
        else:
            raise ValueError(f"Unsupported package manager: {package_manager}")
    else:
        template_args["package_manager_config_secret_mount"] = ""

    dockerfile_content = DOCKERFILE_TEMPLATE.render(**template_args)
    return dockerfile_content
