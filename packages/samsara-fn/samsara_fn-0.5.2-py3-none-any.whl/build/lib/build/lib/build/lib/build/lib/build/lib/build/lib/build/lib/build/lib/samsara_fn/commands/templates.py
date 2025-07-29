import argparse
import os
from dataclasses import dataclass
import shutil
import fnmatch
from typing import Optional, List

from .utils import choices_from_artifacts, should_ignore

from samsara_fn.helptext import description, f
from samsara_fn.clilogger import logger


@dataclass
class TemplatesArgs:
    """Arguments for templates command."""

    template_name: str
    output_dir: str
    only: Optional[str] = None


def setup_templates_parser(subparsers: argparse._SubParsersAction) -> None:
    """Set up templates command parser."""
    templates_parser = subparsers.add_parser(
        "templates",
        help="generate predefined code templates for common Samsara Function patterns",
        description=description(f"""
        {f("Generate predefined code templates for common Samsara Function patterns.")}

        This command copies ready-to-use code templates to your specified directory,
        providing boilerplate implementations for common function patterns and best practices.
        These templates serve as starting points for developing Samsara Functions with
        specific functionality like secret management, AWS service interactions, and more.

        {f("Required arguments:", "yellow")}
        - {f("template_name", "bold")}: Specifies which template to generate.
        - {f("output_dir", "bold")}: Path to the directory where the template files will be copied.
          The directory will be created if it doesn't exist. Defaults to the current working directory. Files in an existing directory will be overwritten.

        {f("Optional arguments:", "green")}
        - {f("only", "bold")}: Comma-separated list of file patterns to copy. Only files matching
          these patterns will be copied from the template. Supports glob-style patterns with wildcards
          (e.g., {f('"*.py,requirements.txt,config/*.json"', "italic")}). If not specified, all files are copied.

        {f("Available Templates:", "green")}
        - {f("just-secrets:", "bold")} An example demonstrating how to securely access and use secrets
          in your Samsara Function. Includes proper credential management, secret retrieval via AWS SSM,
          and caching patterns for optimal performance.
        - {f("additional-python-dependencies:", "bold")} An example demonstrating how to use additional Python dependencies
          in your Samsara Function, to support packages which are not included in the default Python runtime.
        - {f("just-storage:", "bold")} An example demonstrating how to use the storage service in your Samsara Function.
          Includes proper credential management, storage retrieval via AWS S3, and caching patterns for optimal performance.

        {f("Important:", "yellow")} These templates are designed to work with the simulator's stubbed AWS services.
        The credential and secret management patterns will work seamlessly in both local development
        and production environments.

        {f("Example:", "green")}
        {f("samsara-fn templates just-secrets", "underline")}
        {f("samsara-fn templates just-secrets --output-dir ./my-function", "underline")}
        {f("samsara-fn templates just-secrets --only 'samsarafnsecrets.py' func-that-needs-secrets", "underline")}
        """),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    templates_parser.add_argument(
        "template_name",
        help="name of the template",
        choices=choices_from_artifacts(
            "templates",
            filter_func=lambda file: os.path.isdir(file),
            map_func=lambda file: os.path.basename(file),
        ),
    )

    templates_parser.add_argument(
        "output_dir",
        type=str,
        help="path to the directory to output the template to",
        metavar="output/dir",
    )

    templates_parser.add_argument(
        "--only",
        "-o",
        type=str,
        help="comma-separated list of file patterns to copy (supports glob patterns)",
        metavar="pattern1,pattern2",
    )


def map_templates_args(args: argparse.Namespace) -> TemplatesArgs:
    """Map templates arguments to TemplatesArgs."""
    return TemplatesArgs(
        template_name=args.template_name,
        output_dir=args.output_dir,
        only=args.only,
    )


def _parse_patterns(patterns_str: str) -> List[str]:
    """Parse comma-separated patterns and strip whitespace."""
    return [pattern.strip() for pattern in patterns_str.split(",") if pattern.strip()]


def _should_copy_item(item_name: str, patterns: List[str]) -> bool:
    """Check if an item should be copied based on the provided patterns."""
    if not patterns:
        return True

    for pattern in patterns:
        if fnmatch.fnmatch(item_name, pattern):
            return True

    return False


def _copy_directory_filtered(
    src_dir: str,
    dest_dir: str,
    patterns: List[str],
    gitignore_path: str,
    template_dir_path: str,
) -> int:
    """Recursively copy directory contents with pattern filtering."""
    os.makedirs(dest_dir, exist_ok=True)
    files_copied = 0

    for item in os.listdir(src_dir):
        source_path = os.path.join(src_dir, item)

        # Check gitignore first
        if should_ignore(gitignore_path, template_dir_path, source_path):
            continue

        # Get relative path for pattern matching
        rel_path = os.path.relpath(source_path, template_dir_path)

        # Check if item matches patterns
        if not _should_copy_item(rel_path, patterns):
            logger.debug(f"Skipped {rel_path} (doesn't match patterns)")
            continue

        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            logger.debug(f"Copied {rel_path}")
            files_copied += 1
        elif os.path.isdir(source_path):
            # For directories, we need to check if any files inside match the patterns
            # We'll copy the directory structure and let recursion handle the filtering
            files_copied += _copy_directory_filtered(
                source_path, dest_path, patterns, gitignore_path, template_dir_path
            )

            # Remove empty directories
            if os.path.exists(dest_path) and not os.listdir(dest_path):
                os.rmdir(dest_path)
                logger.debug(f"Removed empty directory {rel_path}")

    return files_copied


def handle_templates(args: TemplatesArgs) -> int:
    templates_dir = os.path.join(
        os.path.dirname(__file__),
        "..",
        "artifacts",
        "templates",
    )

    template_dir_path = os.path.join(
        templates_dir,
        f"{args.template_name}",
    )

    current_dir = os.getcwd()
    output_dir = current_dir
    if args.output_dir:
        output_dir = args.output_dir

    if not os.path.exists(template_dir_path):
        logger.error(
            f"Template '{args.template_name}' not found at {template_dir_path}"
        )
        return 2

    if not os.path.isdir(output_dir):
        logger.debug(f"Creating output directory {output_dir}")
        os.makedirs(output_dir, exist_ok=True)

    # Parse patterns if provided, otherwise use catch-all pattern
    has_custom_patterns = bool(args.only)
    patterns = _parse_patterns(args.only) if args.only else ["*"]
    if has_custom_patterns:
        logger.debug(f"Using file patterns: {patterns}")

    # Get the gitignore file from the templates directory
    # So that we don't copy the pycache files that are added at build time
    gitignore_path = os.path.join(
        templates_dir,
        "ignore.txt",  # there is an issue with dot files as artifacts
    )

    # Copy the template directory to the output directory with filtering
    try:
        files_copied = _copy_directory_filtered(
            template_dir_path, output_dir, patterns, gitignore_path, template_dir_path
        )

        logger.info(
            f"Successfully copied template '{args.template_name}' to {output_dir} ({files_copied} files)"
        )

    except Exception as e:
        logger.error(f"Error copying template: {e}")
        return 1

    return 0
