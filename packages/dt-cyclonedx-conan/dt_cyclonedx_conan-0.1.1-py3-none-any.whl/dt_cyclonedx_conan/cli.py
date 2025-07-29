import json
from argparse import ArgumentParser, Namespace
from pathlib import Path

from conans.client.command import Extender, OnceArgument, _add_common_install_arguments

from .cdx import CycloneDxBom
from .generate import generate_sbom


def get_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(description="SBOM Generator for conan v1")

    parser.add_argument(
        "path_or_reference",
        help="Path to a folder containing a recipe (conanfile.py or conanfile.txt) or to a recipe file. e.g., ./my_project/conanfile.txt",
    )

    group = parser.add_argument_group("SBOM options")
    group.add_argument(
        "--sbom-include-dev",
        action="store_true",
        help="Include development dependencies in the SBOM",
        dest="sbom_include_dev",
    )
    group.add_argument(
        "--sbom-main-component-type",
        action="store",
        help="Type of the main component",
        dest="sbom_main_type",
    )
    group.add_argument(
        "--sbom-main-component-name",
        action="store",
        help="Name of the main component",
        dest="sbom_main_name",
    )
    group.add_argument(
        "--sbom-main-component-version",
        action="store",
        help="Version of the main component, e.g., 2.1.0",
        dest="sbom_main_version",
    )
    group.add_argument(
        "--sbom-main-component-license",
        action="store",
        help="License of the main component, preferrably expressed as SPDX identifier, e.g., Apache-2.0",
        dest="sbom_main_license",
    )
    group.add_argument(
        "--sbom-main-component-purl",
        action="store",
        help="PURL identifier of the main component, e.g., pkg:conan/package-name@1.2.3",
        dest="sbom_main_purl",
    )
    group.add_argument(
        "--sbom-main-component-cpe",
        action="store",
        help="CPE identifier of the main component, e.g., cpe:2.3:a:openssl:openssl:3.2.1:*:*:*:*:*:*:*",
        dest="sbom_main_cpe",
    )
    group.add_argument(
        "--sbom-main-component-vcs-url",
        action="store",
        help="HTTPS URL of the remote repository",
        dest="sbom_main_vcs_url",
    )
    group.add_argument(
        "--sbom-output-file",
        action="store",
        metavar="FILE_PATH",
        default="-",
        required=False,
        help="Output file. If empty or '-', output will be sent to stdout",
        dest="sbom_output_file",
    )

    group = parser.add_argument_group("conan options")
    group.add_argument(
        "-if",
        "--install-folder",
        action=OnceArgument,
        help="Local folder containing conaninfo.txt and conanbuildinfo.txt files (from a previous conan install execution). "
        "Defaulted to current folder, unless --profile, -s or -o is specified. "
        "If you specify both install-folder and any setting/option it will raise an error.",
    )
    group.add_argument(
        "-db",
        "--dry-build",
        action=Extender,
        nargs="?",
        help="Apply the --build argument to output the information, as would be done by the install command",
    )
    _add_common_install_arguments(
        group,
        update_help="Will check if updates of the dependencies exist in the remotes (a new version that satisfies a"
        "version range, a new revision or a newer recipe if not using revisions).",
        build_help="Given a build policy, return an ordered list of packages that would be built from sources during the install command",
    )

    return parser


def print_bom(args: Namespace, bom: CycloneDxBom) -> None:
    output = json.dumps(bom, default=lambda o: o.__json__(), indent=2)

    if not args.sbom_output_file or args.sbom_output_file == "-":
        print(output)
    else:
        Path(args.sbom_output_file).write_text(f"{output}\n", encoding="utf-8")


def main() -> None:
    parser = get_arg_parser()
    args = parser.parse_args()

    output_bom = generate_sbom(args)
    print_bom(args, output_bom)


if __name__ == "__main__":
    main()  # pragma: no cover
