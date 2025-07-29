from typing import Optional

import rucio.common.utils


class eicNonDeterministicPFNAlgorithm(rucio.common.utils.NonDeterministicPFNAlgorithms):
    """
    eic specific non-deterministic PFN algorithm
    """

    def __init__(self):
        super().__init__()

    @classmethod
    def _module_init_(cls) -> None:
        """
        Registers the included non-deterministic PFN algorithms
        """
        cls.register('eic', cls.construct_non_deterministic_pfn_eic)

    @staticmethod
    def construct_non_deterministic_pfn_eic(dsn: str, scope: Optional[str], filename: str) -> str:
        """
        Defines relative PFN for  specific replicas.
        This method contains the convention.
        To be used for non-deterministi.
        DSN  contains /
        """

        fields = dsn.split("/")
        nfields = len(fields)
        if nfields == 0:
            return '/other/%s' % (filename)
        else:
            return '%s/%s' % (dsn, filename)
        
eicNonDeterministicPFNAlgorithm._module_init_()