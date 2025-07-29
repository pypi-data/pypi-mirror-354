# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# pyre-strict
import abc

from monarch._rust_bindings.monarch_hyperactor.actor import PythonMessage

from monarch._rust_bindings.monarch_hyperactor.alloc import (  # @manual=//monarch/monarch_extension:monarch_extension
    LocalAllocatorBase,
)

from monarch._rust_bindings.monarch_hyperactor.mailbox import Mailbox, PortId

from monarch._rust_bindings.monarch_hyperactor.proc import (  # @manual=//monarch/monarch_extension:monarch_extension
    ActorId,
    Alloc,
    AllocConstraints,
    AllocSpec,
    init_proc,
    Proc,
    Serialized,
)

from monarch._rust_bindings.monarch_hyperactor.shape import (  # @manual=//monarch/monarch_extension:monarch_extension
    Shape,
)


class Actor(abc.ABC):
    @abc.abstractmethod
    async def handle(self, mailbox: Mailbox, message: PythonMessage) -> None: ...

    async def handle_cast(
        self,
        mailbox: Mailbox,
        rank: int,
        coordinates: list[tuple[str, int]],
        message: PythonMessage,
    ) -> None:
        await self.handle(mailbox, message)


__all__ = [
    "init_proc",
    "Actor",
    "ActorId",
    "ActorHandle",
    "Alloc",
    "AllocSpec",
    "PortId",
    "Proc",
    "Serialized",
    "PickledMessage",
    "PickledMessageClientActor",
    "PythonMessage",
    "Mailbox",
    "PortHandle",
    "PortReceiver",
    "OncePortHandle",
    "OncePortReceiver",
    "Alloc",
    "AllocSpec",
    "AllocConstraints",
    "ProcMesh",
    "PythonActorMesh",
    "ProcessAllocatorBase",
    "Shape",
    "Selection",
    "LocalAllocatorBase",
]
