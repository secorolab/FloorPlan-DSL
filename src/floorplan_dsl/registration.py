"""
Registration of languages with TextX registration API
"""

# dependencies
import sys
from os.path import abspath, dirname, join, realpath
from textx import LanguageDesc, GeneratorDesc, metamodel_from_file
import textx.scoping.providers as scoping_providers
import textx.scoping as scoping

dir_path = dirname(realpath(__file__))
sys.path.append(dir_path)

# Classes for FloorPlan DSL and Variation DSL
from floorplan_dsl.floor_plan.classes.space import Space
from floorplan_dsl.floor_plan.classes.polytope import (
    Circle,
    Polygon,
    Rectangle,
    VerticalPolygon,
    VerticalRectangle,
)
from floorplan_dsl.floor_plan.classes.wall_opening import WallOpening
from floorplan_dsl.floor_plan.classes.floor_feature import FloorFeature
from floorplan_dsl.floor_plan.classes.position import Position, PoseDescription

from floorplan_dsl.variation.classes.distribution import (
    UniformDistribution,
    DiscreteDistribution,
    NormalDistribution,
)

# object processors for FloorPlan DSL
from floorplan_dsl.floor_plan.processors.processors import unique_names_processor

from floorplan_dsl.variation.processors.processors import (
    discrete_distribution_obj_processor,
)

from floorplan_dsl.variation.exsce_variations import variation_floorplan_generator

from floorplan_dsl.floor_plan.generators import (
    jsonld_floorplan_generator,
    v1_to_v2_converter,
)


def floorplan_metamodel():
    "floorplan language"

    current_dir = dirname(__file__)
    path = join(current_dir, "grammar/fpm1", "floorplan.tx")
    mm_floorplan = metamodel_from_file(
        path,
        classes=[
            Space,
            Rectangle,
            Polygon,
            Circle,
            VerticalRectangle,
            WallOpening,
            FloorFeature,
            Position,
            PoseDescription,
        ],
    )
    mm_floorplan.register_obj_processors(
        {
            "FloorPlan": unique_names_processor,
        }
    )
    mm_floorplan.register_scope_providers({"*.*": scoping_providers.FQNImportURI()})

    return mm_floorplan


def fpv2_metamodel():
    current_dir = dirname(__file__)
    path = join(current_dir, "grammar/fpm2", "floorplan.tx")
    floorplan_mm = metamodel_from_file(path)
    floorplan_mm.auto_init_attributes = False
    floorplan_mm.register_obj_processors(
        {
            "FloorPlan": unique_names_processor,
        }
    )
    # floorplan_mm.register_scope_providers({"*.*": scoping_providers.FQN()})
    return floorplan_mm


def variation_metamodel():

    current_dir = dirname(__file__)
    path = join(current_dir, "grammar/variation", "floorplan_variation.tx")
    mm_variation = metamodel_from_file(
        path, classes=[UniformDistribution, DiscreteDistribution, NormalDistribution]
    )
    mm_variation.register_obj_processors(
        {"DiscreteDistribution": discrete_distribution_obj_processor}
    )
    mm_variation.register_scope_providers({"*.*": scoping_providers.FQNImportURI()})

    return mm_variation


floorplan_lang = LanguageDesc(
    "floorplan-v1",
    pattern="*.floorplan",
    description="A language to model indoor environments",
    metamodel=floorplan_metamodel,
)

fpv2_lang = LanguageDesc(
    "floorplan-v2",
    pattern="*.fpm2",
    description="A language to model floor plans (v2)",
    metamodel=fpv2_metamodel,
)

variation_lang = LanguageDesc(
    "floorplan-variation",
    pattern="*.variation",
    description="A language to variate models from ExSce",
    metamodel=variation_metamodel,
)

variation_floorplan_gen = GeneratorDesc(
    language="floorplan-variation",
    target="floorplan-v2",
    description="Generate variations of indoor environments from .floorplan models",
    generator=variation_floorplan_generator,
)

json_ld_floorplan_gen = GeneratorDesc(
    language="floorplan-v1",
    target="json-ld",
    description="Generate composable models in json-ld",
    generator=jsonld_floorplan_generator,
)

floorplan_v1_to_v2_gen = GeneratorDesc(
    language="floorplan-v1",
    target="floorplan-v2",
    description="Convert from floorplan models from v1 to v2",
    generator=v1_to_v2_converter,
)
