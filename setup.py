#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

extras_require = {
        'desktop': ['pynput', 'pyvjoy'],
        'rpi': ['gpiozero', 'RPi.GPIO', 'smbus', 'adafruit-circuitpython-ads1x15', 'PyYAML'],
        'dev': ['Flask', 'flask-cors']
    }

setup(
    author="Sean Barzilay",
    author_email='sesnbarzilay@gmail.com',
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    description="wifi_controller",
    entry_points={
        'console_scripts': [
            'wifi_controller=wifi_controller.cli:main',
            'config_server=wifi_controller.backend.fileServer:main'
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='wifi_controller',
    name='wifi_controller',
    packages=find_packages(include=['wifi_controller', 'wifi_controller.*']),
    extras_require=extras_require,
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/sbarzilay/wifi_controller',
    version='0.0.2-dev',
    zip_safe=False,
)
