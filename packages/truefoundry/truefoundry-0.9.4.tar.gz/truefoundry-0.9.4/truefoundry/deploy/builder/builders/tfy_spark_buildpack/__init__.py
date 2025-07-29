import os
import shutil
from tempfile import TemporaryDirectory
from typing import List, Optional

from truefoundry.deploy._autogen.models import DockerFileBuild, SparkBuildSpec
from truefoundry.deploy.builder.builders import dockerfile
from truefoundry.deploy.builder.builders.tfy_spark_buildpack.dockerfile_template import (
    generate_dockerfile_content,
)
from truefoundry.deploy.builder.utils import has_python_package_manager_conf_secret

__all__ = ["generate_dockerfile_content", "build"]


def _convert_to_dockerfile_build_config(
    build_configuration: SparkBuildSpec,
    dockerfile_path: str,
    mount_python_package_manager_conf_secret: bool = False,
) -> DockerFileBuild:
    dockerfile_content = generate_dockerfile_content(
        build_configuration=build_configuration,
        mount_python_package_manager_conf_secret=mount_python_package_manager_conf_secret,
    )
    with open(dockerfile_path, "w", encoding="utf8") as fp:
        fp.write(dockerfile_content)

    return DockerFileBuild(
        type="dockerfile",
        dockerfile_path=dockerfile_path,
        build_context_path=build_configuration.build_context_path,
    )


def build(
    tag: str,
    build_configuration: SparkBuildSpec,
    extra_opts: Optional[List[str]] = None,
):
    if not build_configuration.spark_version:
        raise ValueError(
            "`spark_version` is required for `tfy-spark-buildpack` builder"
        )
    mount_python_package_manager_conf_secret = (
        has_python_package_manager_conf_secret(extra_opts) if extra_opts else False
    )
    
    # Copy execute_notebook.py to the build context
    execute_notebook_src = os.path.join(os.path.dirname(__file__), "execute_notebook.py")
    execute_notebook_dst = os.path.join(build_configuration.build_context_path, "execute_notebook.py")
    
    # Track if we copied the file to clean it up later
    copied_execute_notebook = False
    if not os.path.exists(execute_notebook_dst):
        shutil.copy2(execute_notebook_src, execute_notebook_dst)
        copied_execute_notebook = True
    
    try:
        with TemporaryDirectory() as local_dir:
            docker_build_configuration = _convert_to_dockerfile_build_config(
                build_configuration,
                dockerfile_path=os.path.join(local_dir, "Dockerfile"),
                mount_python_package_manager_conf_secret=mount_python_package_manager_conf_secret,
            )
            dockerfile.build(
                tag=tag,
                build_configuration=docker_build_configuration,
                extra_opts=extra_opts,
            )
    finally:
        # Clean up the copied file if we copied it
        if copied_execute_notebook and os.path.exists(execute_notebook_dst):
            try:
                os.remove(execute_notebook_dst)
            except OSError:
                pass  # Ignore errors when cleaning up
