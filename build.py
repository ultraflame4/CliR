"""Build script."""
import os
import platform
import subprocess
import sys

from setuptools import Extension
from setuptools.errors import CCompilerError, ExecError, PlatformError
from setuptools.command.build_ext import build_ext
from pathlib import Path


class CMakeExtension(Extension):
    def __init__(self, name, cmakelist_dir: Path, **kwa):
        Extension.__init__(self, name, sources=[], **kwa)
        self.cmakelist_dir = cmakelist_dir.absolute()


extensions = [
    CMakeExtension("CliRenderer.ext", Path("ext")),
]


class BuildFailed(Exception):
    pass


class ExtBuilder(build_ext):
    def run(self):
        try:
            build_ext.run(self)
        except (PlatformError, FileNotFoundError):
            pass

    def build_extension(self, ext):

        if not isinstance(ext, CMakeExtension):
            build_ext.build_extension(self, ext)
            return

        try:
            out = subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError("Cannot find CMake executable! Is cmake in path?")

        extdir = Path(self.get_ext_fullpath(ext.name)).absolute().parent
        print("EXT DIR",extdir)
        build_type = 'Debug' if self.debug == 'ON' else 'Release'
        cmake_args = [
            f"-DCMAKE_BUILD_TYPE={build_type}",
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{build_type.upper()}={extdir}",
            f"-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_{build_type.upper()}={self.build_temp}",
            f"-DPYTHON_EXECUTABLE={sys.executable}"
        ]

        if platform.system() == 'Windows':
            plat = ('x64' if platform.architecture()[0] == '64bit' else 'Win32')
            cmake_args += [
                # These options are likely to be needed under Windows
                "-DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=TRUE"
                f"-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_{build_type.upper()}={extdir}"
            ]
            # Assuming that Visual Studio and MinGW are supported compilers
            if self.compiler.compiler_type == 'msvc':
                cmake_args += [
                    f"-DCMAKE_GENERATOR_PLATFORM={plat}"
                ]
            else:
                cmake_args += [
                    '-G', 'Ninja'
                ]

            if not Path(self.build_temp).exists():
                os.makedirs(self.build_temp)
            # Cmake Config
            subprocess.check_call(['cmake', ext.cmakelist_dir] + cmake_args,
                                  cwd=self.build_temp)

            subprocess.check_call(['cmake', '--build', '.', '--config', build_type], cwd=self.build_temp)
def build(setup_kwargs):
    setup_kwargs.update({"ext_modules": extensions, "cmdclass": {"build_ext": ExtBuilder}})
