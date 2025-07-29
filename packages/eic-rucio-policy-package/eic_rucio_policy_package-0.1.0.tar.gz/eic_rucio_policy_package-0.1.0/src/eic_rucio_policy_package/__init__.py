SUPPORTED_VERSION = [">=37.0.0"]

def get_algorithms():
    from eic_rucio_policy_package.lfn2pfn import eicRSEDeterministicTranslation
    from eic_rucio_policy_package.extract_scope import eicScopeExtractionAlgorithm
    from eic_rucio_policy_package.non_deterministic_pfn import eicNonDeterministicPFNAlgorithm
    return {'lfn2pfn': {'eic': eicRSEDeterministicTranslation.lfn2pfn_eic},
            'scope': {'eic': eicScopeExtractionAlgorithm.extract_scope_eic},
            'non_deterministic_pfn': {
                'eic': eicNonDeterministicPFNAlgorithm.construct_non_deterministic_pfn_eic
                },
           }
