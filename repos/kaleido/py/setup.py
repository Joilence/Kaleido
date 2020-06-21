import setuptools
import os
import shutil
from setuptools import setup, Command
import glob
import distutils.util

here = os.path.dirname(os.path.abspath(__file__))

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    CLEAN_FILES = './build ./dist ./*.pyc ./*.tgz ./*.egg-info'.split(' ')

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        global here

        for path_spec in self.CLEAN_FILES:
            # Make paths absolute and relative to this path
            abs_paths = glob.glob(os.path.normpath(os.path.join(here, path_spec)))
            for path in [str(p) for p in abs_paths]:
                if not path.startswith(here):
                    # Die if path in CLEAN_FILES is absolute + outside this directory
                    raise ValueError("%s is not a path inside %s" % (path, here))
                print('removing %s' % os.path.relpath(path))
                shutil.rmtree(path)


class CopyExecutable(Command):
    description = "Copy Kaleido executable directory into package"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        shutil.rmtree(os.path.join(here, 'kaleido', 'executable'), ignore_errors=True)
        shutil.copytree(
            os.path.join(here, '..', '..', 'build', 'kaleido'),
            os.path.join(here, 'kaleido', 'executable')
        )


class PackageWheel(Command):
    description = "Build Wheel Package"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.run_command("clean")
        self.run_command("copy_executable")
        cmd_obj = self.distribution.get_command_obj('bdist_wheel')

        # Use current platform as plat_name, but replace linux with manylinux2014
        cmd_obj.plat_name = distutils.util.get_platform().replace("linux-", "manylinux2014-")
        cmd_obj.python_tag = 'py2.py3'
        self.run_command("bdist_wheel")

setup(
    name="kaleido",
    version="0.0.1a3",
    packages=["kaleido", "kaleido.scopes"],
    package_data={'kaleido': package_files("kaleido/executable")},
    cmdclass=dict(
        copy_executable=CopyExecutable, clean=CleanCommand, package=PackageWheel
    )
)