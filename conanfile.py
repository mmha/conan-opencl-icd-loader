# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class OpenCLICDLoaderConan(ConanFile):
    name = "opencl-icd-loader"
    version = "20190411"
    description = "The OpenCL ICD Loader"
    topics = ("opencl")
    url = "https://github.com/bincrafters/conan-opencl-icd-loader"
    homepage = "https://github.com/KhronosGroup/OpenCL-ICD-Loader"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "Apache-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    requires = "opencl-headers/20190412@bincrafters/stable"

    def source(self):
        source_url = "https://github.com/KhronosGroup/OpenCL-ICD-Loader"
        commit = "66ecca5dce2c4425a48bdb0cf0de606e4da43ab5"
        checksum = "3af9efaf9ebc68e1fb18b7904ec71004a9e71cf074e2ce70b719382b65f2b609"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, commit), sha256=checksum)
        extracted_dir = "OpenCL-ICD-Loader-" + commit

        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["OPENCL_INCLUDE_DIRS"] = ";".join(self.deps_cpp_info["opencl-headers"].include_paths)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        libdir = os.path.join(self.build_folder, self._build_subfolder, "lib")
        self.copy(pattern="OpenCL.dll", dst="bin", src=libdir, keep_path=False)
        self.copy(pattern="OpenCL.lib", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="libOpenCL.a", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="libOpenCL.so*", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="libOpenCL.dylib", dst="lib", src=libdir, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
