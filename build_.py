import shutil
from pathlib import Path

import skbuild

import skbuild.constants


def build(setup_kwargs):
    print("BUILDING C EXTENSIONS!")
    skbuild.setup(
        **setup_kwargs,
        script_args=["build_ext"],
        cmake_source_dir="ext"
    )
    ext_path = Path(skbuild.constants.CMAKE_INSTALL_DIR()) / "clir_cpp"
    pylib_path = Path("CliRenderer")
    shutil.copytree(ext_path, pylib_path, dirs_exist_ok=True)


if __name__ == "__main__":
    build({})
