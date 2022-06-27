import sys
import traceback
import os
import io

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

import textx.scoping.providers as scoping_providers
from textx import metamodel_from_file
from textx.scoping.tools import get_unique_named_object_in_all_models
from textx import register_language, clear_language_registrations

if __name__ == '__main__':
    
    mm_floorplan = metamodel_from_file('exsce_floorplan/exsce_floorplan.tx')
    mm_floorplan.register_scope_providers({
        "*.*": scoping_providers.FQNImportURI()
    })

    mm_variation = metamodel_from_file('exsce_floorplan/exsce_variations.tx')
    mm_variation.register_scope_providers({
        "*.*": scoping_providers.FQNImportURI()
    })

# formulate the evaluation wrt to the requirmements/interview
# system usibilty test sus
# 
# questionare?
# fomulate a research question around the effectiveness
