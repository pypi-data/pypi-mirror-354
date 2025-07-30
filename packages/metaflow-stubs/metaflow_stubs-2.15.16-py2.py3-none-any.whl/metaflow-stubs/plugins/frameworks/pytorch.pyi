######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.16                                                                                #
# Generated on 2025-06-10T23:43:51.593175                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.parallel_decorator

from ...metaflow_current import current as current
from ..parallel_decorator import ParallelDecorator as ParallelDecorator

class PytorchParallelDecorator(metaflow.plugins.parallel_decorator.ParallelDecorator, metaclass=type):
    def task_decorate(self, step_func, flow, graph, retry_count, max_user_code_retries, ubf_context):
        ...
    def setup_distributed_env(self, flow):
        ...
    ...

def setup_torch_distributed(master_port = None):
    """
    Set up environment variables for PyTorch's distributed (DDP).
    """
    ...

