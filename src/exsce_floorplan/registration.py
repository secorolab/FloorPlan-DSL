'''
Registration of languages with TextX registration API
'''
# dependencies
import sys
from os.path import abspath, dirname, join, realpath
from textx import LanguageDesc, GeneratorDesc, metamodel_from_file
import textx.scoping.providers as scoping_providers
import textx.scoping as scoping

dir_path = dirname(realpath(__file__))
sys.path.append(dir_path)

# Classes for FloorPlan DSL and Variation DSL
from floor_plan.classes.space import Space
from floor_plan.classes.polytope import (
                        Circle, 
                        Polygon, 
                        Rectangle, 
                        VerticalPolygon,
                        VerticalRectangle
                        ) 
from floor_plan.classes.wall_opening import WallOpening
from floor_plan.classes.floor_feature import FloorFeature

from variation.classes.distribution import (
    UniformDistribution,
    DiscreteDistribution,
    NormalDistribution
)

# object processors for FloorPlan DSL
from floor_plan.processors.processors import (
    opening_obj_processors,
    feature_obj_processor,
    unique_names_processor
)

from variation.processors.processors import discrete_distribution_obj_processor

from variation.exsce_variations import variation_floorplan_generator 

def exsce_floorplan_metamodel():
    "exsce_floorplan language"

    current_dir = dirname(__file__)
    path = join(current_dir, 'floor_plan', 'grammar', 'exsce_floorplan.tx')
    mm_floorplan = metamodel_from_file(path, classes=[Space, 
                                                        Rectangle, 
                                                        Polygon, 
                                                        Circle,
                                                        VerticalRectangle,
                                                        WallOpening,
                                                        FloorFeature])
    mm_floorplan.register_obj_processors({
        'WallOpening': opening_obj_processors,
        'FloorFeature': feature_obj_processor,
        'FloorPlan' : unique_names_processor
    }) 
    mm_floorplan.register_scope_providers({
        "*.*": scoping_providers.FQNImportURI()
    })

    return mm_floorplan

def exsce_variation_metamodel():

    current_dir = dirname(__file__)
    path = join(current_dir, 'variation', 'grammar', 'exsce_variation.tx')
    mm_variation = metamodel_from_file(path, classes=[UniformDistribution,
                                                        DiscreteDistribution,
                                                        NormalDistribution])
    mm_variation.register_obj_processors({
        'DiscreteDistribution' : discrete_distribution_obj_processor
    })
    mm_variation.register_scope_providers({
        "*.*": scoping_providers.FQNImportURI()
    })

    return mm_variation

floorplan_lang = LanguageDesc(
    'exsce-floorplan-dsl',
    pattern='*.floorplan',
    description='A language to model indoor environments',
    metamodel=exsce_floorplan_metamodel
)

variation_lang = LanguageDesc(
    'exsce-variation-dsl',
    pattern="*.variation",
    description='A language to variate models from ExSce',
    metamodel=exsce_variation_metamodel
)

variation_floorplan_gen = GeneratorDesc(
    language='exsce-variation-dsl',
    target='exsce-floorplan-dsl',
    description='Generate variations of indoor environments from .floorplan models',
    generator=variation_floorplan_generator
)