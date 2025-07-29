import re
from setuptools import setup

with open("requirements.txt", "r") as f:
    req = f.read().splitlines()

with open("README.MD", "r") as f:
    ldr = f.read()

with open('mbbankchecker/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

setup(
    name='MBbankchecker',
    version=version,
    description='bankchecker base on MBBank of The DT',
    author='JussKynn',
    packages=["mbbankchecker", "mbbankchecker.wasm_helper"],
    install_requires=req,
    include_package_data=True
)
