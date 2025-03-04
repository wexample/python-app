from typing import cast, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_app.common.resolver.abstract_command_resolver import AbstractCommandResolver


class CommandResolverKernel:
    def _init_resolvers(self):
        from wexample_app.service.service_registry import ServiceRegistry
        cast(ServiceRegistry, self.register_services(
            'command_resolvers',
            self._get_command_resolvers()
        )).instantiate_all(kernel=self)

    def _get_command_resolvers(self) -> list[Type["AbstractCommandResolver"]]:
        return []
