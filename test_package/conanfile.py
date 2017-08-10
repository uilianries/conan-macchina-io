from conans import ConanFile, RunEnvironment, tools
import os


class MacchinaioTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    user = os.getenv("CONAN_USERNAME", "uilianries")
    channel = os.getenv("CONAN_CHANNEL", "testing")
    requires = "macchina.io/0.7.0@%s/%s" % (user, channel)

    def imports(self):
        self.copy("macchina", dst="bin", src="bin")

    def test(self):
        env_build = RunEnvironment(self)
        with tools.environment_append(env_build.vars):
            with tools.chdir("bin"):
                assert(os.path.isfile("macchina"))
                #self.run("./macchina")
