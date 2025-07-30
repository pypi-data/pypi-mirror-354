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
import shutil
from glob import glob

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.sdist import sdist


class PrebuiltExtension(Extension):
    def __init__(self, name, lib_dir=''):
        super().__init__(name, sources=[])  # No sources to compile
        self.lib_dir = os.path.abspath(lib_dir)


class CustomBuildExt(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        # Check if the lib directory exists and contains files
        if not os.path.isdir(ext.lib_dir) or not os.listdir(ext.lib_dir):
            raise FileNotFoundError(
                f"Directory '{ext.lib_dir}' is empty or does not exist. "
                "Please compile the necessary components with CMake as described in the README."
            )

        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        os.makedirs(extdir, exist_ok=True)  # Ensure the destination path exists
        self.copy_all_files(ext.lib_dir, extdir)

    def copy_all_files(self, source_dir, destination_dir):
        os.makedirs(destination_dir, exist_ok=True)  # Ensure the entire destination directory structure exists

        for item in os.listdir(source_dir):
            source_path = os.path.join(source_dir, item)
            destination_path = os.path.join(destination_dir, item)

            if os.path.islink(source_path):
                link_target = os.readlink(source_path)
                if os.path.exists(destination_path):
                    os.remove(destination_path)
                os.symlink(link_target, destination_path)
                print(f"Preserved symbolic link {destination_path} -> {link_target}")
            elif os.path.isdir(source_path):
                self.copy_all_files(source_path, destination_path)
            else:
                shutil.copy2(source_path, destination_path)
                print(f"Copied {source_path} to {destination_path}")


# 自定义sdist命令，确保库文件被包含
class CustomSdist(sdist):
    def make_release_tree(self, base_dir, files):
        # 调用原始sdist方法创建基础发布树
        super().make_release_tree(base_dir, files)
        
        # 复制install/lib目录到发布树
        lib_source = 'install/lib'
        lib_dest = os.path.join(base_dir, 'install/lib')
        
        if os.path.exists(lib_source):
            os.makedirs(os.path.dirname(lib_dest), exist_ok=True)
            if os.path.exists(lib_dest):
                shutil.rmtree(lib_dest)
            shutil.copytree(lib_source, lib_dest)
            print(f"Added {lib_source} to sdist")


# 获取所有需要包含的库文件
def get_lib_files():
    lib_files = []
    if os.path.exists('install/lib'):
        for root, _, files in os.walk('install/lib'):
            for file in files:
                lib_files.append(os.path.join(root, file))
    return lib_files


setup(
    name='pyorbbec',
    version='1.0.1.23',
    author='zhonghong',
    author_email='zhonghong@orbbec.com',
    description='pyorbbecsdk is a python wrapper for the OrbbecSDK',
    long_description='',
    ext_modules=[PrebuiltExtension('pyorbbec', 'install/lib')],
    cmdclass={
        'build_ext': CustomBuildExt,
        'sdist': CustomSdist,
    },
    zip_safe=False,
    # 包含所有库文件
    package_data={
        '': get_lib_files(),
    },
    # 确保MANIFEST.in文件包含库文件
    include_package_data=True,
)
