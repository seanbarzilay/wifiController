import os
import setuptools

#: The runtime requirements
RUNTIME_PACKAGES = ['pynput']

#: Additional requirements used during setup
SETUP_PACKAGES = [
    'setuptools-lint >=0.5',
    'sphinx >=1.3.1']

#: Packages requires for different environments
EXTRA_PACKAGES = {}


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wifi_controller",
    version="0.0.1",
    author="Sean Barzilay",
    author_email="senbarzilay@gmail.com",
    description="Wifi Controller",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seanbarzilay/wifiController",
    install_requires=RUNTIME_PACKAGES,
    setup_requires=RUNTIME_PACKAGES + SETUP_PACKAGES,
    extras_require=EXTRA_PACKAGES,
    packages=setuptools.find_packages(
        os.path.join(
            os.path.dirname(__file__),
            'lib')),
    package_dir={'': 'wifi_controller'},
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
