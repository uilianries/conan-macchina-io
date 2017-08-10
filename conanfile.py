from tempfile import mkdtemp
from os import path
from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.util.config_parser import get_bool_from_text

class MacchinaioConan(ConanFile):
    name = "macchina.io"
    version = "0.7.0"
    settings = "os", "compiler", "build_type", "arch"
    description = "Package for Macchina.io"
    author = "Uilian Ries <uilianries@gmail.com>"
    url = "https://github.com/macchina-io/macchina.io"
    license = "https://github.com/macchina-io/macchina.io/blob/develop/LICENSE"
    options = {"shared": [True, False], "v8snapshot": [True, False]}
    requires = "OpenSSL/1.0.2l@conan/stable"
    default_options = "shared=True", "v8snapshot=True"
    install_dir = mkdtemp(prefix="%s-%s" % (name, version))

    def source(self):
        tools.get("https://github.com/macchina-io/macchina.io/archive/macchina-%s-release.tar.gz" % self.version)

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            with tools.chdir("macchina.io-macchina-%s-release" % self.version):
                openssl_dir = "OPENSSL_DIR=%s" % ''.join(self.deps_cpp_info["OpenSSL"].lib_paths)
                target = "DEFAULT_TARGET=%s_%s" % ("shared" if self.options.shared else "static", str(self.settings.build_type).lower())
                nosnapshot = "V8_NOSNAPSHOT=%s" % ("0" if self.options.v8snapshot else "1")
                target_install_dir = "INSTALLDIR=%s" % self.install_dir
                env_build.make(args=['-s', openssl_dir, target, nosnapshot,'all'])
                env_build.make(args=['-s', openssl_dir, target, nosnapshot, target_install_dir, "install"])

    def package(self):
        self.copy(pattern="LICENSE", dst=".", src=".")
        self.copy(pattern="*", dst="include", src=path.join(self.install_dir, "include"))
        self.copy(pattern="*", dst="etc", src=path.join(self.install_dir, "etc"))
        self.copy(pattern="*", dst="bin", src=path.join(self.install_dir, "bin"))
        self.copy(pattern="*", dst="bundles", src=path.join(self.install_dir, "lib", "bundles"))
        self.copy(pattern="*.so*", dst="lib", src=path.join(self.install_dir, "lib"))
        self.copy(pattern="*.a", dst="lib", src=path.join(self.install_dir, "lib"))

    def package_info(self):
        self.cpp_info.libs = self.collect_libs()
