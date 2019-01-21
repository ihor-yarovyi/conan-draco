from conans import ConanFile, tools, CMake
import os
from os import path

class DracoConan(ConanFile):
    """
    Conan package for the draco library https://github.com/google/draco
    """
    name = "draco"
    version = "1.3.4"
    license = "Apache-2.0"
    description = "Draco is a library for compressing and decompressing 3D geometric meshes and point clouds. It is intended to improve the storage and transmission of 3D graphics."
    url = "https://github.com/ableigdev/conan-draco.git"
    homepage = "https://google.github.io/draco/"
    generators = "cmake"
    
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared" : [True, False],
        "enable_ccache" : [True, False],
        "enable_distcc" : [True, False],
        "enable_extra_speed" : [True, False],
        "enable_extra_warnings" : [True, False],
        "enable_goma" : [True, False],
        "enable_js_glue" : [True, False],
        "enable_mesh_compression" : [True, False],
        "enable_point_cloud_compression" : [True, False],
        "enable_predictive_edgebreaker" : [True, False],
        "enable_standard_edgebreaker" : [True, False],
        "enable_backwards_compatibility" : [True, False],
        "enable_decoder_attribute_deduplication" : [True, False],
        "enable_tests" : [True, False],
        "enable_wasm" : [True, False],
        "enable_werror" : [True, False],
        "enable_wextra" : [True, False],
        "ignore_empty_build_type" : [True, False],
        "build_unity_plugin" : [True, False],
        "build_animation_encoding" : [True, False],
        "build_for_gltf" : [True, False],
        "build_maya_plugin" : [True, False]
    }

    default_options = {
        "shared" : False,
        "enable_ccache" : False,
        "enable_distcc" : False,
        "enable_extra_speed" : False,
        "enable_extra_warnings" : False,
        "enable_goma" : False,
        "enable_js_glue" : True,
        "enable_mesh_compression" : True,
        "enable_point_cloud_compression" : True,
        "enable_predictive_edgebreaker" : True,
        "enable_standard_edgebreaker" : True,
        "enable_backwards_compatibility" : True,
        "enable_decoder_attribute_deduplication" : False,
        "enable_tests" : False,
        "enable_wasm" : False,
        "enable_werror" : False,
        "enable_wextra" : False,
        "ignore_empty_build_type" : False,
        "build_unity_plugin" : False,
        "build_animation_encoding" : False,
        "build_for_gltf" : False,
        "build_maya_plugin" : False
    }
    
    ZIP_NAME = "%s.tar.gz" % version
    UNZIPPED_FOLDER = "draco-%s" % version
    FILE_URL = "https://github.com/google/draco/archive/%s" % ZIP_NAME
    
    def source(self):
        tools.download(self.FILE_URL, self.ZIP_NAME)
        tools.untargz(self.ZIP_NAME)
        os.unlink(self.ZIP_NAME)
    
    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["ENABLE_CCACHE"] = self.options.enable_ccache
        cmake.definitions["ENABLE_DISTCC"] = self.options.enable_distcc
        cmake.definitions["ENABLE_EXTRA_SPEED"] = self.options.enable_extra_speed
        cmake.definitions["ENABLE_EXTRA_WARNINGS"] = self.options.enable_extra_warnings
        cmake.definitions["ENABLE_GOMA"] = self.options.enable_goma
        cmake.definitions["ENABLE_JS_GLUE"] = self.options.enable_js_glue
        cmake.definitions["ENABLE_MESH_COMPRESSION"] = self.options.enable_mesh_compression
        cmake.definitions["ENABLE_POINT_CLOUD_COMPRESSION"] = self.options.enable_point_cloud_compression
        cmake.definitions["ENABLE_PREDICTIVE_EDGEBREAKER"] = self.options.enable_predictive_edgebreaker
        cmake.definitions["ENABLE_STANDARD_EDGEBREAKER"] = self.options.enable_standard_edgebreaker
        cmake.definitions["ENABLE_BACKWARDS_COMPATIBILITY"] = self.options.enable_backwards_compatibility
        cmake.definitions["ENABLE_DECODER_ATTRIBUTE_DEDUPLICATION"] = self.options.enable_decoder_attribute_deduplication
        cmake.definitions["ENABLE_TESTS"] = self.options.enable_tests
        cmake.definitions["ENABLE_WASM"] = self.options.enable_wasm
        cmake.definitions["ENABLE_WERROR"] = self.options.enable_werror
        cmake.definitions["ENABLE_WEXTRA"] = self.options.enable_wextra
        cmake.definitions["IGNORE_EMPTY_BUILD_TYPE"] = self.options.ignore_empty_build_type
        cmake.definitions["BUILD_UNITY_PLUGIN"] = self.options.build_unity_plugin
        cmake.definitions["BUILD_ANIMATION_ENCODING"] = self.options.build_animation_encoding
        cmake.definitions["BUILD_FOR_GLTF"] = self.options.build_for_gltf
        cmake.definitions["BUILD_MAYA_PLUGIN"] = self.options.build_maya_plugin

        return cmake

    def cmake_args(self):
        args = ['-DCMAKE_INSTALL_PREFIX="%s"' % self.package_folder]

        return ' '.join(args)

    def build(self):
        # Make build dir
        build_dir = self.try_make_dir(os.path.join(".", "build"))

        # Change to build dir
        os.chdir(build_dir)
        cmake = self.configure_cmake()
        src_dir = path.join(self.build_folder, self.UNZIPPED_FOLDER)
        self.run('cmake "%s" %s %s' % (src_dir, cmake.command_line, self.cmake_args()))
        self.run('cmake --build . --target install %s' % cmake.build_config)

    def package_info(self):
        self.cpp_info.libs = ["draco"]

    def try_make_dir(self, name_of_the_dir):
        try:
            os.mkdir(name_of_the_dir)
            return name_of_the_dir
        except OSError:
            #dir already exist
            pass

    
    