import glob
import shutil
import subprocess
import os
import sys


def install_dependencies_to_path(
    dependency_path: str, requirements_file: str
) -> subprocess.CompletedProcess:
    """
    Install dependencies to the given path with pip using --target flag.
    Remove all files in the given path before installation.
    """
    if os.path.exists(dependency_path):
        shutil.rmtree(dependency_path)

    return subprocess.run(
        ["pip", "install", "-r", requirements_file, "--target", dependency_path],
        check=True,
    )


def clean_up_depedency_path(dependency_path: str):
    """
    Remove files that are not needed in the dependency directory:
    - binary files
    - dist-info files (leaves METADATA)
    - egg-info files (leaves PKG-INFO)
    """
    shutil.rmtree(os.path.join(dependency_path, "bin"))

    for dist_info in glob.glob(os.path.join(dependency_path, "*.dist-info")):
        for file in os.listdir(dist_info):
            if file.endswith("WHEEL"):
                platform_tag = get_package_platform_tag(os.path.join(dist_info, file))
                if platform_tag != "py3-none-any":
                    package_name = os.path.basename(dist_info).split("-")[0]
                    print(
                        "\033[31m"
                        f"platform-warning: package '{package_name}' is not platform-agnostic (wheel tag '{platform_tag}'). You can proceed with testing it in the simulator, but for production you need to run the dependency installing script on a machine with x86_64 architecture. See the template README for more details."
                        "\033[0m",
                        file=sys.stderr,
                    )

            if not file.endswith("METADATA"):
                remove(os.path.join(dist_info, file))

    for egg_info in glob.glob(os.path.join(dependency_path, "*.egg-info")):
        for file in os.listdir(egg_info):
            if not file.endswith("PKG-INFO"):
                remove(os.path.join(egg_info, file))


def remove(path: str):
    if os.path.isfile(path):
        os.remove(path)
    else:
        shutil.rmtree(path)


def get_package_platform_tag(wheel_file_path: str):
    wheel_file_lines = []
    with open(wheel_file_path, "r") as f:
        wheel_file_lines = f.readlines()

    for line in wheel_file_lines:
        line = line.strip()
        if line.startswith("Tag: "):
            # Extract the part after "Tag: "
            return line[5:]  # len("Tag: ") = 5

    # Return None if no Tag line was found
    return None


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    lib_dir = os.path.join(current_dir, "..", "lib")

    install_dependencies_to_path(
        dependency_path=lib_dir,
        requirements_file=os.path.join(current_dir, "requirements.txt"),
    )

    clean_up_depedency_path(lib_dir)
