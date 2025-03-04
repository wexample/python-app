from typing import cast, Type, TYPE_CHECKING, Optional, Dict

from wexample_app.runner.abstract_command_runner import AbstractCommandRunner

if TYPE_CHECKING:
    from wexample_app.resolver.abstract_command_resolver import AbstractCommandResolver


class CommandRunnerKernel:
    def _init_resolvers(self):
        from wexample_app.service.service_registry import ServiceRegistry
        cast(ServiceRegistry, self.register_services(
            'command_resolvers',
            self._get_command_resolvers()
        )).instantiate_all(kernel=self)

    def _init_runners(self):
        from wexample_app.service.service_registry import ServiceRegistry
        cast(ServiceRegistry, self.register_services(
            'command_runners',
            self._get_command_runners()
        )).instantiate_all(kernel=self)

    def _get_command_resolvers(self) -> list[Type["AbstractCommandResolver"]]:
        return []

    def _get_command_runners(self) -> list[Type["AbstractCommandRunner"]]:
        from wexample_app.runner.python_command_runner import PythonCommandRunner

        return [
            # Default runner.
            PythonCommandRunner
        ]

    def get_resolver(self, type: str) -> Optional["AbstractCommandResolver"]:
        return cast(
            "AbstractCommandResolver",
            self.get_service_registry('command_resolvers').get(key=type)
        )

    def get_resolvers(self) -> Dict[str, "AbstractCommandResolver"]:
        return cast(
            Dict[str, "AbstractCommandResolver"],
            self.get_service_registry('command_resolvers').all_instances()
        )

    def get_runner(self, type: str) -> Optional[AbstractCommandRunner]:
        return cast(
            AbstractCommandRunner,
            self.get_service_registry('command_runners').get(key=type)
        )

    def get_runners(self) -> Dict[str, AbstractCommandRunner]:
        return cast(
            Dict[str, AbstractCommandRunner],
            self.get_service_registry('command_runners').all_instances()
        )
