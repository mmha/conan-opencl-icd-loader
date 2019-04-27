# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class KhronosOpenCLICDLoaderConan(ConanFile):
    name = "khronos-opencl-icd-loader"
    version = "20190412"
    description = "The OpenCL ICD Loader"
    topics = ("conan", "opencl", "opencl-icd-loader", "build-system", "icd-loader")
    url = "https://github.com/bincrafters/conan-khronos-opencl-icd-loader"
    homepage = "https://github.com/KhronosGroup/OpenCL-ICD-Loader"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "Apache-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "0001-static-library.patch"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"fPIC": [True, False], "shared": [True, False]}
    default_options = {"fPIC": True, "shared": False}
    requires = "khronos-opencl-headers/20190412@bincrafters/stable"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        commit = "66ecca5dce2c4425a48bdb0cf0de606e4da43ab5"
        sha256 = "3af9efaf9ebc68e1fb18b7904ec71004a9e71cf074e2ce70b719382b65f2b609"
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, commit), sha256=sha256)
        extracted_dir = "OpenCL-ICD-Loader-" + commit
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        tools.patch(base_path=self._source_subfolder, patch_file="0001-static-library.patch")
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["pthread", "dl"])
        elif self.settings.os == "Windows" and \
             self.settings.compiler == "Visual Studio":
            self.cpp_info.libs.append("cfgmgr32")
