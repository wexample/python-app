from __future__ import annotations

from typing import TYPE_CHECKING, cast

import attrs
from wexample_helpers.classes.base_class import BaseClass
from wexample_app.common.abstract_kernel_child import AbstractKernelChild

if TYPE_CHECKING:
    from wexample_app.common.abstract_kernel import AbstractKernel
    from wexample_app.common.mixins.command_runner_kernel import CommandRunnerKernel
    from wexample_app.resolver.abstract_command_resolver import AbstractCommandResolver
    from wexample_app.response.abstract_response import AbstractResponse
    from wexample_app.runner.abstract_command_runner import AbstractCommandRunner
    from wexample_helpers.const.types import StringsMatch


@attrs.define(kw_only=True)
class CommandRequest(AbstractKernelChild, BaseClass):
    arguments: list[str | int] = attrs.field(factory=list)
    name: str
    path: str | None = attrs.field(default=None)
    type: str | None = attrs.field(default=None)
    _match: StringsMatch | None = attrs.field(default=None, init=False)
    _resolver: AbstractCommandResolver | None = attrs.field(default=None, init=False)
    _runner: AbstractCommandRunner | None = attrs.field(default=None, init=False)

    kernel: AbstractKernel = attrs.field()

    def __attrs_post_init__(self) -> None:
        from wexample_app.exception.command_runner_not_found_exception import (
            CommandRunnerNotFoundException,
        )
        from wexample_app.exception.command_type_not_found_exception import (
            CommandTypeNotFoundException,
        )

        AbstractKernelChild.__init__(self, kernel=self.kernel)

        self.type = self._guess_type()
        if self.type is None:
            raise CommandTypeNotFoundException(self.name)

        self.resolver = self._get_resolver()
        self.runner = self._guess_runner()
        if not self.runner:
            raise CommandRunnerNotFoundException(command_name=self.name)

        self.path = self.runner.build_command_path(request=self)

    @property
    def kernel(self) -> AbstractKernel | CommandRunnerKernel:
        from wexample_app.common.mixins.command_runner_kernel import CommandRunnerKernel

        # Enforce typing
        return cast(CommandRunnerKernel, super().kernel)

    @property
    def match(self) -> StringsMatch:
        return self._match

    @match.setter
    def match(self, value: StringsMatch) -> None:
        self._match = value

    @property
    def resolver(self) -> AbstractCommandResolver:
        return self._resolver

    @resolver.setter
    def resolver(self, value: AbstractCommandResolver) -> None:
        self._resolver = value

    @property
    def runner(self) -> AbstractCommandRunner:
        return self._runner

    @runner.setter
    def runner(self, value: AbstractCommandRunner) -> None:
        self._runner = value

    def execute(self) -> AbstractResponse:
        from wexample_app.exception.command_build_failed_exception import (
            CommandBuildFailedException,
        )
        from wexample_app.exception.command_runner_missing_exception import (
            CommandRunnerMissingException,
        )

        if self.runner is None:
            raise CommandRunnerMissingException(command_name=self.name)

        try:
            command = self.resolver.build_command(request=self)
            if command is None:
                raise CommandBuildFailedException(
                    command_name=self.name,
                    resolver_name=self.resolver.__class__.__name__,
                )

            return command.execute_request_and_normalize(self)
        except Exception as e:
            self.kernel.io.error(exception=e, fatal=True)

    def _get_resolver(self) -> AbstractCommandResolver:
        from wexample_app.exception.command_resolver_not_found_exception import (
            CommandResolverNotFoundException,
        )

        resolver = self.kernel.get_resolver(self.type)
        if resolver is None:
            raise CommandResolverNotFoundException(self.type)
        return resolver

    def _guess_runner(self) -> AbstractCommandRunner | None:
        for runner in self.kernel.get_runners().values():
            if runner.will_run(self):
                return runner
        return None

    def _guess_type(self) -> str | None:
        for resolver in self.kernel.get_resolvers().values():
            match = resolver.supports(request=self)
            if match is not None:
                self.match = match
                return resolver.get_type()
        return None
