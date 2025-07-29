import sys
from argparse import Namespace
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

from conans import ConanFile
from conans.client.command import Command as ConanCommand
from conans.client.conan_api import Conan, ProfileData
from conans.client.graph.graph import DepsGraph, Node
from conans.client.output import ConanOutput
from conans.errors import ConanException, ConanMigrationError
from conans.model.ref import ConanFileReference

from .cdx import (
    Component,
    CycloneDxBom,
    Dependency,
    ExternalReference,
    License,
    Metadata,
    Property,
)
from .utils import find_git_origin_url, get_dynatrace_versions


def get_conan_info(arguments: Namespace) -> Tuple[DepsGraph, ConanFile]:
    try:
        conan_api = Conan(output=ConanOutput(sys.stderr, sys.stderr, color=False))
    except ConanMigrationError:
        sys.exit(1)
    except ConanException as e:
        sys.stderr.write(f"Error in Conan initialization: {e}")
        sys.exit(1)

    return ConanCommand(conan_api)._conan.info(
        arguments.path_or_reference,
        remote_name=arguments.remote,
        settings=arguments.settings_host,
        options=arguments.options_host,
        env=arguments.env_host,
        profile_names=arguments.profile_host,
        conf=arguments.conf_host,
        profile_build=ProfileData(
            profiles=arguments.profile_build,
            settings=arguments.settings_build,
            options=arguments.options_build,
            env=arguments.env_build,
            conf=arguments.conf_build,
        ),
        update=arguments.update,
        install_folder=arguments.install_folder,
        build=arguments.dry_build,
        lockfile=arguments.lockfile,
    )


# traverses the dependency graph to find prod dependencies, i.e., deps that mention others in their [requires] section
def get_package_dependencies(include_dev: bool, deps_graph_nodes: Set[Node]) -> Set[str]:
    package_dep_node_ids: Set[str] = set()

    if not include_dev:
        visited_node_ids: Set[str] = set()
        nodes_to_visit: Set[Node] = set(node for node in deps_graph_nodes if not list(node.ancestors))
        while nodes_to_visit:
            node = nodes_to_visit.pop()
            node_id = str(node.id)
            if node_id in visited_node_ids:
                continue

            visited_node_ids.add(node_id)
            package_dep_node_ids.add(node_id)

            for dependency in node.dependencies:
                if node.graph_lock_node and str(dependency.dst.id) in node.graph_lock_node.requires:
                    nodes_to_visit.add(dependency.dst)

    return package_dep_node_ids


def build_purl(name: str, version: Optional[str], ref: Optional[ConanFileReference] = None) -> str:
    qualifiers: Dict[str, str] = {}
    # if ref and ref.revision:
    #    qualifiers["rrev"] = ref.revision

    version = f"@{version}" if version else ""
    qualifiers_str = f"?{'&'.join([f'{key}={value}' for key, value in qualifiers.items()])}" if qualifiers else ""

    return f"pkg:conan/{name}{version}{qualifiers_str}"


def extract_component_from_node(node: Node, node_is_root: bool, arguments: Namespace) -> Component:
    conanfile: Optional[ConanFile] = node.conanfile

    # default component values
    bom_type = "library"
    conan_name: Optional[str] = node.ref.name if node.ref else None
    conan_version: Optional[str] = node.ref.version if node.ref else None
    conan_license: Union[str, tuple, list, None] = conanfile.license if conanfile else None
    conan_url: Optional[str] = conanfile.url if conanfile else None
    conan_homepage: Optional[str] = conanfile.homepage if conanfile else None
    purl: Optional[str] = None
    cpe: Optional[str] = None

    # main component
    if node_is_root:
        # strip a potential .local suffix
        if conan_version and conan_version.endswith(".local"):
            conan_version = conan_version[:-6]

        # explicit overrides
        if arguments.sbom_main_type:
            bom_type = arguments.sbom_main_type
        if arguments.sbom_main_name:
            conan_name = arguments.sbom_main_name
        if arguments.sbom_main_version:
            conan_version = arguments.sbom_main_version
        if arguments.sbom_main_license:
            conan_license = arguments.sbom_main_license
        if arguments.sbom_main_purl:
            purl = arguments.sbom_main_purl
        if arguments.sbom_main_cpe:
            cpe = arguments.sbom_main_cpe
        if arguments.sbom_main_vcs_url:
            conan_url = arguments.sbom_main_vcs_url

    if not conan_name:
        conan_name = Path(node.path).parent.name if node_is_root and node.path else str(node.id)

    dt_versions = get_dynatrace_versions(conan_version)
    properties: List[Property] = []
    if dt_versions["full"] and dt_versions["base"] != dt_versions["full"]:
        properties.append(Property(name="dynatrace:version", value=dt_versions["full"]))

    if not purl:
        purl = build_purl(conan_name, dt_versions["base"], node.ref)

    if not conan_url:
        conan_url = find_git_origin_url(arguments.path_or_reference)

    if conan_license and not isinstance(conan_license, (tuple, list)):
        conan_license = [conan_license]
    licenses: List[License] = [License(name=x) for x in conan_license] if conan_license else []

    external_references: List[ExternalReference] = []
    if conan_url:
        external_references.append(ExternalReference(type="vcs", url=conan_url))
    if conan_homepage:
        external_references.append(ExternalReference(type="website", url=conan_homepage))
    if node.remote and node.remote.url:
        external_references.append(ExternalReference(type="distribution", url=node.remote.url))

    return Component(
        bom_ref=purl,
        type=bom_type,
        name=conan_name,
        version=dt_versions["base"],
        author=conanfile.author if conanfile else None,
        description=conanfile.description if conanfile else None,
        licenses=licenses,
        external_references=external_references,
        purl=purl,
        cpe=cpe,
        properties=properties,
    )


def extract_dependency_from_node(
    bom_ref: str, node: Node, sbom_include_dev: bool, package_dep_node_ids: Set[str]
) -> Dependency:
    node_dep = Dependency(ref=bom_ref)

    for dependency in node.dependencies:
        dep_dst: Node = dependency.dst
        if not sbom_include_dev and str(dep_dst.id) not in package_dep_node_ids:
            continue

        dep_dst_name = dep_dst.ref.name if dep_dst.ref else str(dep_dst.id)
        dep_dst_version = dep_dst.ref.version if dep_dst.ref else None
        dt_versions = get_dynatrace_versions(dep_dst_version)
        purl = build_purl(dep_dst_name, dt_versions["base"], dep_dst.ref)

        node_dep.depends_on.append(purl)

    return node_dep


def generate_sbom(arguments: Namespace) -> CycloneDxBom:
    deps_graph, _ = get_conan_info(arguments)
    deps_graph_nodes: Set[Node] = deps_graph.nodes
    package_dep_node_ids = get_package_dependencies(arguments.sbom_include_dev, deps_graph_nodes)

    bom = CycloneDxBom()

    for node in deps_graph_nodes:
        node_is_root = not list(node.ancestors)
        # check whether to skip dev dependencies
        if not arguments.sbom_include_dev and not node_is_root and str(node.id) not in package_dep_node_ids:
            continue

        component = extract_component_from_node(node, node_is_root, arguments)
        if node_is_root:
            bom.metadata = Metadata(component=component)
        else:
            bom.components.append(component)

        bom.add_dependency(
            extract_dependency_from_node(component.bom_ref, node, arguments.sbom_include_dev, package_dep_node_ids)
        )

    return bom
