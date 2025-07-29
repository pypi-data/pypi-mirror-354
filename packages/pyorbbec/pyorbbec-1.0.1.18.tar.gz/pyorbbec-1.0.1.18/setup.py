# ******************************************************************************
#  Copyright (c) 2024 Orbbec 3D Technology, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http:# www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************

import os
import sys
import platform
import shutil

from setuptools import setup, find_packages

requires = [
    'pybind11==2.11.0',
    'pybind11-global==2.11.0',
    'opencv-python',
    'wheel',
    'numpy<2.0',  # see https://github.com/orbbec/pyorbbecsdk/issues/47
    'av',         # for h264 decoding
    'pygame',     # for visualization
    'pynput',     # for keyboard input
]

# platform tag
def get_platform_tag():
    if sys.platform.startswith('win'):
        return 'win_amd64'
    elif sys.platform.startswith('linux'):
        if sys.maxsize > 2**32 and 'aarch64' in sys.version.lower():
            return 'linux_aarch64'
        else:
            return 'manylinux_2_17_x86_64'
    else:
        raise ValueError(f"Unsupported platform: {sys.platform}")

# Platform
current_platform = platform.system().lower()

# Set package data according to platform
package_data = {
    'pyorbbecsdk': [],
}

# Windows
if current_platform == 'windows':
    package_data['pyorbbecsdk'].extend(['win_x64/*.pyd', 'win_x64/*.dll', 'win_x64/*.lib', 'win_x64/*.xml'])

# Linux
elif current_platform == 'linux':
    package_data['pyorbbecsdk'].extend(['linux_x64/*.so', 'linux_x64/*.so*', 'linux_x64/*.xml'])

setup(
    name="pyorbbec",
    version="1.0.1.18",
    description="Python interface to the Orbbec SDK.",
    long_description_content_type="text/markdown",
    author="orbbec",
    author_email="lijie@orbbec.com",
    url="https://orbbec.com.cn/",
    packages=find_packages(where="src", include=["pyorbbecsdk", "pyorbbecsdk.*"]),
    package_dir={"": "src"},
    options={
        'bdist_wheel': {
            'python_tag': 'py38',
            'plat_name': get_platform_tag(),
            'universal': False,
        }
    },
    python_requires=">=3.8",
    install_requires=requires,
    license="Apache-2.0",
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    
    package_data=package_data,
    include_package_data=True,
)
