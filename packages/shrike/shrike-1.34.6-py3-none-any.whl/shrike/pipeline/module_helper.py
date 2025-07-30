# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""
Pipeline helper class to create pipelines loading modules from a flexible manifest.
"""


from azure.ml.component import Component
from azure.ml.component._core._component_definition import ComponentDefinition
from dataclasses import dataclass, field
import os
import logging
from typing import Optional, List, Tuple
from packaging.specifiers import SpecifierSet
from packaging.version import Version, InvalidVersion

from shrike.pipeline.aml_connect import current_workspace


log = logging.getLogger(__name__)


@dataclass
class module_reference:
    key: Optional[str] = (
        None  # use as internal key to reference module (if None, use name)
    )
    name: Optional[str] = None  # None if module exists only locally?
    source: Optional[str] = None  # This config is deprecated. Please do not use.
    yaml: Optional[str] = None
    version: Optional[str] = None
    from_workspace: Optional[bool] = (
        False  # If set to True and it's a remote component, shrike will only attempt to load it from workspace (not from registry or feed)
    )


@dataclass
class module_manifest:
    manifest: List[module_reference] = field(default_factory=list)
    feeds: List[str] = field(default_factory=list)
    registries: List[str] = field(default_factory=list)


@dataclass
class module_loader_config:  # pylint: disable=invalid-name
    """Config for the AMLModuleLoader class"""

    use_local: Optional[str] = None
    use_local_except_for: Optional[bool] = None
    force_default_module_version: Optional[str] = None
    force_all_module_version: Optional[str] = None
    local_steps_folder: str = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "tests",
            "tests_pipeline",
            "sample",
            "steps",
        )
    )
    use_remote_when_component_not_in_manifest: Optional[bool] = False
    loading_order: Optional[str] = "registry, feed, workspace"


class AMLModuleLoader:
    """Helper class to load modules from within an AMLPipelineHelper."""

    def __init__(self, config):
        """Creates module instances for AMLPipelineHelper.

        Args:
            config (DictConfig): configuration options
        """
        self.use_local_except_for = (
            config.module_loader.use_local_except_for
            if "use_local_except_for" in config.module_loader
            else None
        )
        if "use_local" not in config.module_loader:
            self.use_local = []
        elif config.module_loader.use_local is None:
            self.use_local = []
        elif config.module_loader.use_local == "*":
            self.use_local = "*"
        elif isinstance(config.module_loader.use_local, str):
            self.use_local = [
                x.strip() for x in config.module_loader.use_local.split(",")
            ]
            if not _check_use_local_syntax_valid(self.use_local):
                raise ValueError(
                    f'Invalid value for `use_local`. Please follow one of the four patterns: \n1) use_local="", all modules are remote\n2) use_local="*", all modules are local\n3) use_local="MODULE_KEY_1, MODULE_KEY_2", only MODULE_KEY_1, MODULE_KEY_2 are local, everything else is remote\n4) use_local="!MODULE_KEY_1, !MODULE_KEY_2", all except for MODULE_KEY_1, MODULE_KEY_2 are local'
                )
            self.use_local_except_for = self.use_local[0].startswith("!")

        self.force_default_module_version = (
            config.module_loader.force_default_module_version
            if "force_default_module_version" in config.module_loader
            else None
        )
        self.force_all_module_version = (
            config.module_loader.force_all_module_version
            if "force_all_module_version" in config.module_loader
            else None
        )
        self.local_steps_folder = config.module_loader.local_steps_folder
        self.use_remote_when_component_not_in_manifest = (
            config.module_loader.use_remote_when_component_not_in_manifest
            if "use_remote_when_component_not_in_manifest" in config.module_loader
            else None
        )
        self.module_cache = {}

        self.feeds: List[str] = []
        self.registries: List[str] = []

        self.loading_order = (
            [x.strip().lower() for x in config.module_loader.loading_order.split(",")]
            if "loading_order" in config.module_loader
            else ["registry", "feed", "workspace"]
        )

        # internal manifest built from yaml config
        self.modules_manifest = {}
        self.load_config_manifest(config)

        initialization_info_string = (
            "AMLModuleLoader initialized ("
            f"use_local={self.use_local}"
            f", force_default_module_version={self.force_default_module_version}"
            f", force_all_module_version={self.force_all_module_version}"
            f", local_steps_folder={self.local_steps_folder}"
            f", use_remote_when_component_not_in_manifest={self.use_remote_when_component_not_in_manifest}"
            f", manifest={list(self.modules_manifest.keys())}"
            f", loading_order={self.loading_order}"
            ")"
        )
        log.info(initialization_info_string)

    def load_config_manifest(self, config):
        """Fills the internal module manifest based on config object"""
        for entry in config.modules.manifest:
            if entry.key:
                module_key = entry.key
            elif entry.name:
                module_key = entry.name
            else:
                raise Exception(
                    "In module manifest, you have to provide at least key or name."
                )

            self.modules_manifest[module_key] = entry

        for feed in config.modules.get("feeds", []):
            self.feeds.append(feed)

        for registry in config.modules.get("registries", []):
            self.registries.append(registry)

    def is_local(self, module_name):
        """Tests is module is in local list"""
        if self.use_local == "*":
            return True
        if self.use_local_except_for:
            return "!" + module_name not in self.use_local
        else:
            return module_name in self.use_local

    def module_in_cache(self, module_cache_key):
        """Tests if module in internal cache (dict)"""
        return module_cache_key in self.module_cache

    def get_from_cache(self, module_cache_key):
        """Gets module class from internal cache (dict)"""
        log.debug(f"Using cached module {module_cache_key}")
        return self.module_cache.get(module_cache_key, None)

    def put_in_cache(self, module_cache_key, module_class):
        """Puts module class in internal cache (dict)"""
        self.module_cache[module_cache_key] = module_class

    def verify_manifest(self, modules_manifest):
        """Tests a module manifest schema"""
        errors = []

        for k, module_entry in modules_manifest.items():
            # TODO: merge error checking code with processing code so we do all this in one pass
            if self.is_local(k):
                if "yaml_spec" not in module_entry:
                    errors.append(
                        f"{k}: You need to specify a yaml_spec for your module to use_local=['{k}']"
                    )
                elif not os.path.isfile(
                    module_entry["yaml_spec"]
                ) and not os.path.isfile(
                    os.path.join(self.local_steps_folder, module_entry["yaml_spec"])
                ):
                    errors.append(
                        "{}: Could not find yaml spec {} for use_local=['{}']".format(
                            k, module_entry["yaml_spec"], k
                        )
                    )
            else:
                if "remote_module_name" not in module_entry:
                    errors.append(
                        f"{k}: You need to specify a name for your module to use_local=False"
                    )
                if "namespace" not in module_entry:
                    errors.append(
                        f"{k}: You need to specify a namespace for your module to use_local=False"
                    )
                if ("version" not in module_entry) and (
                    self.force_default_module_version or self.force_all_module_version
                ):
                    errors.append(
                        f"{k}: You need to specify a version for your module to use_local=False, or use either force_default_module_version or force_all_module_version in config"
                    )

        return errors

    def load_local_module(self, module_spec_path):
        """Creates one module instance.

        Args:
            module_spec_path (str): path to local module yaml spec

        Returns:
            object: module class loaded
        """
        module_cache_key = module_spec_path
        if self.module_in_cache(module_cache_key):
            return self.get_from_cache(module_cache_key)

        log.info("Building module from local code at {}".format(module_spec_path))
        if not os.path.isfile(module_spec_path):
            module_spec_path = os.path.join(self.local_steps_folder, module_spec_path)
        loaded_module_class = Component.from_yaml(yaml_file=module_spec_path)
        self.put_in_cache(module_cache_key, loaded_module_class)

        return loaded_module_class

    def solve_module_version_and_load(
        self, module_name, module_version, module_cache_key, registry=None
    ):
        """Loads module class if exists

        Args:
            module_name (str): name of the module to load
            module_version (str): version of the module to load
            module_cache_key (str): cache key of the module after loading
            registy (str): registry name if loading from a registry
        """
        module_version = solve_module_version(
            module_name,
            module_version,
            workspace=current_workspace() if registry is None else None,
            registry=registry,
        )

        loaded_module_class = Component.load(
            current_workspace(),
            name=module_name,
            version=module_version,
            registry=registry,
        )

        self.put_in_cache(module_cache_key, loaded_module_class)
        return loaded_module_class

    def load_prod_module_helper(
        self,
        module_name,
        module_version,
        module_cache_key,
        module_namespace=None,
        loading_order=None,
    ):
        """Loads module from available sources

        Args:
            module_name (str): name of the module to load
            module_version (str): version of the module to load
            module_cache_key (str): cache key of the module after loading
            module_namespace (str): namespace of the module if applicable
            loading_order (list[str]): custom loading order, if not specified loading order from config is used
        """

        if loading_order is None:
            loading_order = self.loading_order

        for source in loading_order:
            if source == "registry":
                log.info(f"Attempting to load {module_name} from registries...")
                for registry in self.registries:
                    try:
                        log.info(
                            f"Loading component {module_name} from registry {registry}"
                        )

                        loaded_module_class = self.solve_module_version_and_load(
                            module_name, module_version, module_cache_key, registry
                        )
                        return loaded_module_class

                    except BaseException as e:
                        log.debug(f"Exception: {e}")

            elif source == "feed":
                log.info(f"Attempting to load {module_name} from feeds...")
                for feed in self.feeds:
                    try:
                        log.info(f"Loading component {module_name} from feed {feed}")

                        module_name = f"azureml.feed://{feed}/{module_name}"

                        loaded_module_class = self.solve_module_version_and_load(
                            module_name, module_version, module_cache_key
                        )
                        return loaded_module_class

                    except BaseException as e:
                        log.debug(f"Exception: {e}")

            elif source == "workspace":
                log.info(f"Attempting to load {module_name} from workspace...")
                try:
                    # try without namespace first
                    return self.solve_module_version_and_load(
                        module_name, module_version, module_cache_key
                    )
                except BaseException as e:
                    log.debug(f"Exception: {e}")

                if module_namespace is not None:
                    log.info(
                        f"    Trying to load module {module_name} with namespace {module_namespace}."
                    )
                    module_name = module_namespace + "://" + module_name

                    try:
                        return self.solve_module_version_and_load(
                            module_name, module_version, module_cache_key
                        )
                    except BaseException as e:
                        log.debug(f"Exception: {e}")

            else:
                raise ValueError(
                    f"Loading order contains incorrect key {source}. Please use a comma-separated str to order 'registry', 'feed', and 'workspace'."
                )

        raise ValueError(
            f"Module {module_name} with version {module_version} not found in neither of the following sources: {loading_order}."
        )

    def load_prod_module(
        self, module_name, module_version, from_workspace=False, module_namespace=None
    ):
        """Creates one module instance.

        Args:
            module_name (str) : module name
            module_version (str) : module version
            from_workspace (bool) : attempt to load from workspace only

        Returns:
            object: module class loaded
        """
        if self.force_all_module_version:
            module_version = self.force_all_module_version
        else:
            module_version = module_version or self.force_default_module_version

        module_cache_key = f"{module_name}:{module_version}"
        if self.module_in_cache(module_cache_key):
            return self.get_from_cache(module_cache_key)

        log.info(
            f"Loading remote module {module_cache_key} (name={module_name}, version={module_version}, namespace={module_namespace})"
        )

        if from_workspace:
            return self.load_prod_module_helper(
                module_name,
                module_version,
                module_cache_key,
                module_namespace,
                loading_order=["workspace"],
            )
        return self.load_prod_module_helper(
            module_name, module_version, module_cache_key, module_namespace
        )

    def get_module_manifest_entry(
        self, module_key, modules_manifest=None
    ) -> Tuple[dict, Optional[str], bool]:
        """Gets a particular entry in the module manifest.

        Args:
            module_key (str): module key from the manifest
            modules_manifest (dict): manifest from required_modules() [DEPRECATED]

        Returns:
            module_entry (dict): module manifest entry (if no entry for this module key in the manifest, only the module key is returned)
            module_namespace (str | None): module namespace for legacy modules
            is_in_manifest (bool): true if the module key can be found in the manifest
        """
        if module_key in self.modules_manifest:
            module_entry = self.modules_manifest[module_key]
            module_namespace = None
            is_in_manifest = True
        elif modules_manifest and module_key in modules_manifest:
            log.warning(
                f"We highly recommend substituting the `required_modules` method by the modules.manifest configuration."
            )
            module_entry = modules_manifest[module_key]
            # map to new format
            module_entry["yaml"] = module_entry["yaml_spec"]
            module_entry["name"] = module_entry["remote_module_name"]
            module_namespace = module_entry.get("namespace", None)
            is_in_manifest = True
        else:
            module_entry = {}
            module_entry["name"] = module_key
            module_namespace = None
            is_in_manifest = False
            if not (self.use_remote_when_component_not_in_manifest):
                log.warning(
                    f"Module key '{module_key}' could not be found in modules.manifest configuration or in required_modules() method. If you want to try and load it from the workspace, set 'module_loader.use_remote_when_component_not_in_manifest' to True in the config."
                )

        return module_entry, module_namespace, is_in_manifest

    def load_module(self, module_key, modules_manifest=None):
        """Loads a particular module from the manifest.

        Args:
            module_key (str): module key from the manifest
            modules_manifest (dict): manifest from required_modules() [DEPRECATED]

        Returns:
            object: module class loaded
        """
        module_entry, module_namespace, is_in_manifest = self.get_module_manifest_entry(
            module_key, modules_manifest
        )
        if is_in_manifest:
            if self.is_local(module_key):
                loaded_module = self.load_local_module(module_entry["yaml"])
            else:
                loaded_module = self.load_prod_module(
                    module_entry["name"],
                    module_entry["version"],
                    from_workspace=(
                        module_entry["from_workspace"]
                        if "from_workspace" in module_entry
                        else False
                    ),
                    module_namespace=module_namespace,
                )
        else:
            log.warning(
                f"The component '{module_key}' cannot be found in the manifest. Attempting to load the remote copy."
            )
            loaded_module = self.load_prod_module(module_entry["name"], None)
        return loaded_module

    def load_modules_manifest(self, modules_manifest):
        """Creates module instances from modules_manifest.

        Args:
            modules_manifest (dict): manifest of modules to load

        Returns:
            dict: modules loaded, keys are taken from module_manifest.

        Raises:
            Exception: if loading module has an error or manifest is wrong.
        """
        log.info(f"Loading module manifest (use_local={self.use_local})")
        test_results = self.verify_manifest(modules_manifest)
        if test_results:
            raise Exception(
                "Loading modules from manifest raised errors:\n\nMANIFEST: {}\n\nERRORS: {}".format(
                    modules_manifest, "\n".join(test_results)
                )
            )

        loaded_modules = {}
        for module_key in modules_manifest:
            log.info(f"Loading module {module_key} from manifest")
            loaded_modules[module_key] = self.load_module(module_key, modules_manifest)

        return loaded_modules


def solve_module_version(module_name, module_version, workspace=None, registry=None):

    if module_version is None:
        return module_version

    try:
        module_version_PEP440 = Version(module_version)
        if str(module_version_PEP440) != module_version:
            log.warning(
                "We suggest adopting PEP440 versioning for your component {module_name}!"
            )

    except InvalidVersion as e:
        log.info(f"{module_version} is a version constraint. Try to solve it...")

        spec = SpecifierSet(module_version)
        if registry:
            components = ComponentDefinition.list(
                registry_name=registry, name=module_name
            )
        elif workspace:
            components = ComponentDefinition.list(workspace=workspace, name=module_name)

        versions = []
        for component in components:
            version = component.version
            version_PEP440 = Version(version)
            if str(version_PEP440) != version:
                log.warning(
                    f"Version {version} does not follow PEP440 versioning, skipping ..."
                )
            else:
                versions.append(version_PEP440)

        compatible_versions = list(spec.filter(versions))
        if compatible_versions:
            module_version = max(compatible_versions)
            log.info(f"Solved version for {module_name} is {module_version}.")

        else:
            raise ValueError(
                f"No version exists for the constraint {module_version}. Existing versions: {versions}"
            )

    return str(module_version)


def _check_use_local_syntax_valid(use_local_list) -> bool:
    use_local_except_for = True if use_local_list[0].startswith("!") else False
    if use_local_except_for:
        for module_key in use_local_list:
            if not module_key.startswith("!"):
                return False
    else:
        for module_key in use_local_list:
            if module_key.startswith("!"):
                return False
    return True
