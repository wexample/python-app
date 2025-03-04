from typing import cast, Type, TYPE_CHECKING, Optional, Dict, Union

from wexample_app.runner.abstract_command_runner import AbstractCommandRunner

if TYPE_CHECKING:
    from wexample_app.resolver.abstract_command_resolver import AbstractCommandResolver
    from wexample_app.service.mixins.service_container_mixin import ServiceContainerMixin


class CommandRunnerKernel:
    def _init_resolvers(self: Union["CommandRunnerKernel", "ServiceContainerMixin"]):
        cast("ServiceRegistry", self.register_services(
            'command_resolvers',
            self._get_command_resolvers()
        )).instantiate_all(kernel=self)

    def _init_runners(self: ["CommandRunnerKernel", "ServiceContainerMixin"]):
        cast("ServiceRegistry", self.register_services(
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

    def get_resolver(self: "ServiceContainerMixin", type: str) -> Optional["AbstractCommandResolver"]:
        return cast(
            "AbstractCommandResolver",
            self.get_service_registry('command_resolvers').get(key=type)
        )

    def get_resolvers(self: "ServiceContainerMixin") -> Dict[str, "AbstractCommandResolver"]:
        return cast(
            Dict[str, "AbstractCommandResolver"],
            self.get_service_registry('command_resolvers').all_instances()
        )

    def get_runner(self: "ServiceContainerMixin", type: str) -> Optional[AbstractCommandRunner]:
        return cast(
            AbstractCommandRunner,
            self.get_service_registry('command_runners').get(key=type)
        )

    def get_runners(self: "ServiceContainerMixin") -> Dict[str, AbstractCommandRunner]:
        return cast(
            Dict[str, AbstractCommandRunner],
            self.get_service_registry('command_runners').all_instances()
        )
