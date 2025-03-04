from pydantic import PrivateAttr

from wexample_app.const.globals import ENV_VAR_NAME_APP_ENV


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
        self.io.properties(
            title="General",
            properties={
                "Location": self.workdir.get_resolved(),
                "Environment": self.get_env_parameter(ENV_VAR_NAME_APP_ENV),
                "Arguments": self._sys_argv[2:],
            }
        )

        self.io.properties(
            title="Resolvers",
            properties=self.get_resolvers()
        )

        self.io.properties(
            title="Runners",
            properties=self.get_runners()
        )
