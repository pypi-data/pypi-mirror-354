import argparse
import os
from dataclasses import dataclass
import zipfile
import re

from .utils import should_ignore

from samsara_fn.helptext import description, f
from samsara_fn.clilogger import logger


@dataclass
class BundleArgs:
    """Arguments for bundle command."""

    directory: str
    ignore_file: str
    include_all: bool
    output_dir: str


def setup_bundle_parser(subparsers: argparse._SubParsersAction) -> None:
    """Set up bundle command parser."""
    bundle_parser = subparsers.add_parser(
        "bundle",
        help="bundle a source directory into a zip file",
        description=description(f"""
        {f("Create a deployment-ready zip file from a source directory.")}

        This command packages your function code and dependencies into a zip file suitable
        for use with the {f("samsara-fn init", "underline")} command. It applies intelligent filtering
        to exclude common development artifacts and potentially sensitive files, helping you
        create clean, secure deployment packages.

        {f("Usage with Init Command:", "green")}
        The generated zip file can be directly used as the {f("--zipFile", "italic")} argument when
        initializing a function with {f("samsara-fn init", "underline")}. This creates a complete
        workflow: bundle your source code, then initialize it as a local function for testing.

        {f("Required arguments:", "yellow")}
        - {f("dir", "bold")}: Path to the directory containing your function code to bundle.

        {f("Optional arguments:", "green")}
        - {f("ignore_file", "bold")}: Path to a custom ignore file for filtering. If not specified, uses the default ignore patterns that exclude {f("__pycache__", "italic")} directories and common hidden/system files.
        - {f("include_all", "bold")}: Include all files without any filtering. Use with caution as this bypasses security warnings for sensitive files.
        - {f("output_dir", "bold")}: Directory where the zip file will be created. Defaults to the current working directory.

        Key actions performed:
        - Walks through all files in the specified directory.
        - Applies filtering based on ignore patterns (unless {f("--include-all", "italic")} is specified).
        - Warns about potentially sensitive files (e.g., {f(".env", "italic")}, {f("*.key", "italic")}, {f("*secret*", "italic")}) and large files (configurable via {f("SAMSARA_SIMULATOR_LARGE_FILE_SIZE_MB", "bright_white")} environment variable, defaults to 1.0 MB).
        - Creates a zip file named {f("<directory_name>.zip", "bright_white")} in the specified output location.
        - Provides a summary of files added, skipped, and warnings generated.

        {f("Security Considerations:", "yellow")}
        The command automatically detects and warns about files that might contain sensitive information:
        - Environment files ({f(".env", "italic")}, {f(".env.*", "italic")})
        - Key files ({f("*.key", "italic")}, {f("*.pem", "italic")}, {f("*.p12", "italic")}, {f("*.pfx", "italic")})
        - Configuration files that might contain credentials
        - SSH and AWS credential directories

        {f("Important:", "yellow")} 
        Review all warnings carefully before using the generated zip file.
        If sensitive or large files are flagged, you can either remove them from your source directory
        and re-run the bundle command, or create a custom ignore file (in {f(".gitignore", "italic")} format)
        using the {f("--ignore-file", "italic")} option to exclude them from bundling.

        {f("Example:", "green")}
        {f("samsara-fn bundle ./my-function", "underline")}
        {f("samsara-fn bundle ./my-function --output-dir ./dist", "underline")}
        {f("samsara-fn bundle ./my-function --ignore-file ./.bundleignore", "underline")}
        
        {f("Complete Workflow Example:", "green")}
        {f("samsara-fn bundle ./my-function", "underline")}
        {f("samsara-fn init my-function --zipFile ./my-function.zip --handler main.handler", "underline")}
        """),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    bundle_parser.add_argument(
        "directory",
        help="path to the directory to bundle",
    )

    bundle_parser.add_argument(
        "--include-all",
        "-a",
        action="store_true",
        help="include all files in the directory, without suggested filtering",
    )

    bundle_parser.add_argument(
        "--ignore-file",
        "-i",
        help="path to the ignore file to use for filtering",
        metavar="/path/ignore.txt",
    )

    bundle_parser.add_argument(
        "--output-dir",
        "-o",
        help="path to the directory where the zip file will be created",
        metavar="/path",
    )


def map_bundle_args(args: argparse.Namespace) -> BundleArgs:
    """Map bundle arguments to BundleArgs."""
    return BundleArgs(
        directory=args.directory,
        ignore_file=args.ignore_file,
        include_all=args.include_all,
        output_dir=args.output_dir,
    )


def get_large_file_threshold() -> float:
    """Get the large file size threshold in MB from environment variable or default."""
    try:
        return float(os.environ.get("SAMSARA_SIMULATOR_LARGE_FILE_SIZE_MB", "1.0"))
    except ValueError:
        logger.warning(
            "Invalid SAMSARA_SIMULATOR_LARGE_FILE_SIZE_MB value, using default 1.0 MB"
        )
        return 1.0


def is_potentially_sensitive_file(file_path: str) -> bool:
    """Check if a file might contain sensitive information."""
    sensitive_patterns = [
        r".*\.env$",
        r".*\.env\..*",
        r".*secret.*",
        r".*password.*",
        r".*\.key$",
        r".*\.pem$",
        r".*\.p12$",
        r".*\.pfx$",
        r".*config.*\.json$",
        r".*credentials.*",
        r".*\.aws/.*",
        r".*\.ssh/.*",
    ]

    filename = os.path.basename(file_path).lower()
    for pattern in sensitive_patterns:
        if re.match(pattern, filename):
            return True
    return False


def should_warn_about_file(file_path: str, max_size_mb: float) -> tuple[bool, str]:
    """Check if we should warn about a file and return the reason."""
    try:
        if is_potentially_sensitive_file(file_path):
            return (
                True,
                "Potentially sensitive file, are you sure you need to include it?",
            )

        file_size = os.path.getsize(file_path)
        size_mb = file_size / (1024 * 1024)

        if size_mb > max_size_mb:
            return (
                True,
                f"File is large ({size_mb:.1f}MB), are you sure you need to include it?",
            )

    except OSError:
        return True, "Cannot access file"

    return False, ""


def handle_bundle(args: BundleArgs) -> int:
    """Handle the bundle command."""
    ignore_file_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "artifacts",
        "bundle",
        "ignore.txt",
    )

    if args.ignore_file:
        ignore_file_path = args.ignore_file
        if not os.path.isfile(ignore_file_path):
            logger.error(f"Ignore file '{ignore_file_path}' does not exist")
            return 1

        logger.info(f"Using custom ignore file: {ignore_file_path}")

    if not os.path.isdir(args.directory):
        logger.error(f"Directory '{args.directory}' does not exist")
        return 1

    # Get configurable file size threshold
    max_file_size_mb = get_large_file_threshold()
    logger.debug(f"Large file threshold: {max_file_size_mb} MB")

    # Create output zip file name
    dir_name = os.path.basename(os.path.abspath(args.directory))
    zip_filename = f"{dir_name}.zip"

    zip_path = os.path.join(os.getcwd(), zip_filename)
    if args.output_dir:
        if not os.path.isdir(args.output_dir):
            logger.debug(f"Creating output directory {args.output_dir}")
            os.makedirs(args.output_dir, exist_ok=True)

        zip_path = os.path.join(args.output_dir, zip_filename)

    # Remove existing zip file if it exists
    if os.path.exists(zip_path):
        os.remove(zip_path)
        logger.info(f"Removed existing {zip_filename}")

    files_added = 0
    files_skipped = 0
    warnings_count = 0
    total_dir_size = 0  # Track total size of files being bundled

    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Walk through all files in the directory
            for root, _dirs, files in os.walk(args.directory):
                for file in files:
                    file_path = os.path.join(root, file)

                    # Add to total directory size before any filtering
                    try:
                        total_dir_size += os.path.getsize(file_path)
                    except OSError:
                        # Skip files we can't access
                        pass

                    # Check if file should be ignored (unless include_all is set)
                    if not args.include_all and should_ignore(
                        ignore_file_path, args.directory, file_path
                    ):
                        files_skipped += 1
                        logger.debug(f"{file_path}: Skipped (ignored)")
                        continue

                    # Check for warnings about the file
                    should_warn, reason = should_warn_about_file(
                        file_path, max_file_size_mb
                    )
                    if should_warn:
                        warnings_count += 1
                        logger.warning(f"{file_path}: Bundled with warning: {reason}")
                    else:
                        logger.debug(f"{file_path}: Bundled")

                    # Calculate relative path for the zip archive
                    arcname = os.path.relpath(file_path, args.directory)

                    # Add file to zip
                    try:
                        zipf.write(file_path, arcname)
                        files_added += 1
                    except Exception as e:
                        logger.error(f"Failed to add {file_path}: {str(e)}")
                        return 1

        # Calculate sizes in MB
        dir_size_mb = total_dir_size / (1024 * 1024)
        zip_size_mb = os.path.getsize(zip_path) / (1024 * 1024)

        # Calculate unzipped size by reading zip file info
        unzipped_size = 0
        with zipfile.ZipFile(zip_path, "r") as zipf:
            for info in zipf.infolist():
                if not info.is_dir():  # Only count files, not directories
                    unzipped_size += info.file_size
        unzipped_size_mb = unzipped_size / (1024 * 1024)

        # Summary
        logger.info(
            f"Bundle created: {zip_filename} ({files_added} files, {files_skipped} skipped, {warnings_count} warnings) ({dir_size_mb:.1f} MB raw, {zip_size_mb:.1f} MB zipped, {unzipped_size_mb:.1f} MB unzipped)"
        )

        return_code = 0
        MAX_ZIPPED_SIZE_MB = 14.5
        if zip_size_mb > MAX_ZIPPED_SIZE_MB:
            logger.error(
                f"The zipped bundle is too large and will not be able to be uploaded to Samsara Functions (max {MAX_ZIPPED_SIZE_MB} MB)"
            )
            return_code = 1

        MAX_UNZIPPED_SIZE_MB = 200
        if unzipped_size_mb > MAX_UNZIPPED_SIZE_MB:
            logger.error(
                f"The unzipped bundle is too large and will not be able to be uploaded to Samsara Functions (max {MAX_UNZIPPED_SIZE_MB} MB)"
            )
            return_code = 1

        logger.info("Run 'samsara-fn --verbose bundle' to see more details.")

        return return_code

    except Exception as e:
        logger.error(f"Failed to create bundle: {str(e)}")
        return 1
