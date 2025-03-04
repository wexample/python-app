from pydantic import PrivateAttr


class CommandLineKernel:
    _sys_argv: list[str] = PrivateAttr(default_factory=list)

    def _init_command_line_kernel(self):
        import sys

        self._sys_argv = sys.argv.copy()

    def exec_argv(self):
        """
        Main entrypoint from command line calls.
        May not be called by an internal script.
        """
        self.io.log('EXEC ARGV')
        self.io.log('WORKDIR ' + self.workdir.get_resolved())
        self.io.log('ENV ' + self.get_env_parameter("APP_ENV"))
        self.io.list(self._sys_argv)
        self.io.list(self._registries.keys())
        self.io.log(self.get_resolvers())
