######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.14.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-09T21:12:38.831118                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import typing


class SerializationHandler(object, metaclass=type):
    def serialze(self, *args, **kwargs) -> typing.Union[str, bytes]:
        ...
    def deserialize(self, *args, **kwargs) -> typing.Any:
        ...
    ...

