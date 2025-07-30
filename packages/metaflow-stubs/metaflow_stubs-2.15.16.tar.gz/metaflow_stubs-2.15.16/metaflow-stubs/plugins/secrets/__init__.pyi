######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.16                                                                                #
# Generated on 2025-06-10T23:43:51.567570                                                            #
######################################################################################################

from __future__ import annotations

import abc
import typing
if typing.TYPE_CHECKING:
    import abc

from . import secrets_decorator as secrets_decorator
from . import inline_secrets_provider as inline_secrets_provider

class SecretsProvider(abc.ABC, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None) -> typing.Dict[str, str]:
        """
        Retrieve the secret from secrets backend, and return a dictionary of
        environment variables.
        """
        ...
    ...

