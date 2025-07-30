# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import logging
import re
from pathlib import Path
from typing import List, Optional
from packaging.version import parse
from ruamel.yaml import YAML
import os
import multiprocessing

from shrike.build.core.command_line import Command

log = logging.getLogger(__name__)


class Register(Command):
    def __init__(self):
        super().__init__()

    def validate_branch(self) -> None:
        """
        Check whether the current source branch name matches the configured
        regular expression of branch name. Fail if it doesn't match.
        """
        log.info(f"Expected branch: {self.config.compliant_branch}")
        log.info(f"Current branch: {self.config.source_branch}")
        if re.match(self.config.compliant_branch, self.config.source_branch):
            log.info(f"Current branch matches configured regular expression.")
        else:
            raise ValueError(
                f"Current branch name doesn't match configured name pattern."
            )

    def find_signed_component_specification_files(self, dir=None) -> List[str]:
        """
        Find all signed component (AML format) generated in the `prepare` step. Return the
        absolute paths of these components in the format of a list of string.
        """
        if dir is None:
            dir = self.config.working_directory

        signed_component_spec_files = []
        # Find the path of spec files in the '.build' folders
        for spec_path in Path(dir).glob(f'{Path(self.config.component_specification_glob).parent}/.build/{Path(self.config.component_specification_glob).name}'):

            # Check whether the component is signed by examining catalog files
            if (
                spec_path.parent.joinpath("catalog.json").exists()
                and spec_path.parent.joinpath("catalog.json.sig").exists()
            ):
                signed_component_spec_files.append(os.path.abspath(spec_path))
                log.info(f"Found a signed component for AML: {spec_path}")
            elif spec_path.parent.joinpath(".build.cat").exists():
                log.info(f"Found a signed component for Aether: {spec_path}")
            else:
                log.warning(f"Found an unsigned component: {spec_path}")
            log.info(str(spec_path.parent.joinpath("catalog.json")))

        if len(signed_component_spec_files) == 0:
            log.info("Cannot find any signed components for AML.")
        else:
            log.info(
                f"Found {len(signed_component_spec_files)} signed components for AML."
            )

        return signed_component_spec_files

    def list_registered_component(self) -> None:
        """
        Log all registered component in the attached workspace by using az ml command.
        """
        list_registered_component_success = self.execute_azure_cli_command(
            f"ml component list -o table", ignore_blowfish=True, ignore_pkg_resources=True
        )
        if not list_registered_component_success:
            self.register_error(f"Error when listing registered components.")

    def register_all_signed_components(self, files: List[str], registry: Optional[str] = None) -> None:
        """
        Run register_component_with_status() in parallel with nb_cores threads
        """
        if files:
            nb_cores = self.nb_cores

            if nb_cores == 1 and not self.config.force_parallelism:
                log.info(f"Batch register with one thread.")
                for component in files:
                    self.register_component_with_status(component, registry)
            else:
                log.info(f"Batch register with multiple threads. {nb_cores} threads.")
                files_with_registry = [(f, registry) for f in files]
                pool = multiprocessing.Pool(processes=nb_cores)
                pool.starmap(self.register_component_with_status, files_with_registry)
                pool.close()
                pool.join()

    def register_component_with_status(self, component, registry: Optional[str] = None) -> None:
        """
        For one of the signed component specification file, run `az ml component create`,
        and register the status (+ register error if registration failed).
        """
        register_command = self.register_component_command(component, registry)

        register_component_success = self.execute_azure_cli_command(
            command=register_command,
            stderr_is_failure=False,
            fail_if_version_exists=self.config.fail_if_version_exists,
            ignore_pkg_resources=True,
        )
        if register_component_success:
            log.info(f"Component {component} is registered.")
            self.register_component_status(component, "register", "succeeded")
        else:
            self.register_component_status(component, "register", "failed")
            self.register_error(f"Error when registering component {component}.")

    def register_component_command(self, component, registry: Optional[str] = None):
        register_command = f"ml component create --file {component}"
        set_default_version = False
        component_raw_version = self.read_component_version(component)

        if self.config.all_component_version:
            register_command += f" --version {self.config.all_component_version}"
            component_raw_version = self.config.all_component_version
            log.info(
                f"Overwrite the component version with the specified value {self.config.all_component_version}"
            )

        if registry:
            register_command += f" --registry {registry}"

        try:
            component_version = parse(str(component_raw_version))
            set_default_version = (
                component_version.base_version == str(component_raw_version)
            )
        except:
            log.error(f"{component_raw_version} is not a valid version number.")
        if set_default_version:
            log.info(
                f"Component {component} version {component_raw_version} is production-ready. Setting as default."
            )
            register_command += f" --label default"
        else:
            log.info(
                f"Component {component} version {component_raw_version} is not production-ready. NOT setting as default."
            )

        log.info(f"Register command is {register_command}")
        return register_command

    def read_component_version(self, yaml_file: str) -> str:
        yaml = YAML(typ="safe")
        with open(yaml_file, "r") as file:
            spec = yaml.load(file)
        try:
            version = spec["version"]
            log.info(f"Component {yaml_file} has version {version}.")
            return version
        except KeyError:
            log.warning(
                "Component does not have version attribute, attempting to read module version."
            )
            return spec["amlModuleIdentifier"]["moduleVersion"]

    def run_with_config(self):
        """
        Running component registration logic.
        """
        self.telemetry_logging(command="register")

        self.validate_branch()
        self.ensure_component_cli_installed()

        component_path = self.find_signed_component_specification_files()
        if len(component_path) > 0:
            for workspace_id in self.config.workspaces:
                log.info(f"Start registering signed components in {workspace_id}")
                self.attach_workspace(workspace_id)

                log.info("List of components in workspace before current registration.")
                self.list_registered_component()

                self.register_all_signed_components(files=component_path)

                log.info("List of components in workspace after current registration.")
                self.list_registered_component()
            for registry in self.config.registries:
                log.info(f"Start registering signed components in {registry}")
                self.register_all_signed_components(files=component_path, registry=registry)


if __name__ == "__main__":
    Register().run()
