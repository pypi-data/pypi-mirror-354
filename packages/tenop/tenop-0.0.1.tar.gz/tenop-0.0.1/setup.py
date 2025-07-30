from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess


class Compile(install):
  def run(self):
    subprocess.run(["./compile.sh"], check=True)
    super().run()

setup(
  name = "tenop",
  version = "0.0.1",
  url="https://github.com/0xhilSa/tenop",
  author = "Sahil Rajwar",
  license = "MIT",
  description = "A lightweight & minimalist tensor computation library with CUDA backend",
  long_description = open("README.md").read(),
  long_description_content_type = "text/markdown",
  packages = find_packages(),
  package_data = {"tenop.engine": ["*.so", "*.pyi"]},
  include_package_data = True,
  cmdclass = {"install": Compile},
  zip_safe = False,
  classifiers = [
    "Programming Language :: Python :: 3",
    "Operating System :: POSIX :: Linux",
  ],
)
