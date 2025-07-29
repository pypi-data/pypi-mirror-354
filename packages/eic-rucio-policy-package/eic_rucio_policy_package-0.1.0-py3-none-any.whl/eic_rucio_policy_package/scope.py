from typing import TYPE_CHECKING, Optional

import rucio.common.utils

if TYPE_CHECKING:
    from collections.abc import Sequence

class eicScopeExtractionAlgorithm(rucio.common.utils.ScopeExtractionAlgorithms):
    def __init__(self) -> None:
        """
        Initialises scope extraction algorithm object
        """
        super().__init__()

    @classmethod
    def _module_init_(cls) -> None:
        """
        Registers the included scope extraction algorithms
        """
        cls.register('eic', cls.extract_scope_eic)

    @staticmethod
    def extract_scope_eic(did: str, scopes: Optional['Sequence[str]']) -> 'Sequence[str]':
        """
        scope extraction algorithm, based on the EIC scope extraction algorithm.
        :param did: The DID to extract the scope from.
        :returns: A tuple containing the extracted scope and the DID.
        """
        if did.find(':') > -1:
            scope, _ , name = did.partition(':')
            if name.endswith('/'):
                name = name[:-1]
            if scope.startswith('user') or scope.startswith('group'):
                username = scope.split('.')[1]
                if name.startswith(f"/{username}"):
                    return scope, name
                else:
                    raise RucioException(f"For scope {scope}, name should start with /{username}.")
            return scope, name
        else:
            raise RucioException(f"Invalid DID format: {did}")

eicScopeExtractionAlgorithm._module_init_()