"""
Registration of languages with TextX registration API
"""

# dependencies
import sys
from os.path import dirname, join, realpath

import textx.scoping.providers as scoping_providers
from textx import LanguageDesc, GeneratorDesc, metamodel_from_file

from floorplan_dsl.generators.fpm import (
    jsonld_floorplan_generator,
    v1_to_v2_converter,
)
from floorplan_dsl.generators.variations import variation_floorplan_generator
from floorplan_dsl.parser.classes.fpm1.floor_feature import FloorFeature
from floorplan_dsl.parser.classes.fpm1.polytope import (
    Circle,
    Polygon,
    Rectangle,
    VerticalRectangle,
)
from floorplan_dsl.parser.classes.fpm1.position import Position, PoseDescription

# Classes for FloorPlan DSL and Variation DSL
from floorplan_dsl.parser.classes.fpm1.space import Space
from floorplan_dsl.parser.classes.fpm1.wall_opening import WallOpening
from floorplan_dsl.parser.classes.variation.distribution import (
    UniformDistribution,
    DiscreteDistribution,
    NormalDistribution,
)

import floorplan_dsl.parser.classes.fpm2.floorplan as fpm
import floorplan_dsl.parser.classes.fpm2.geometry as geom
import floorplan_dsl.parser.classes.fpm2.qudt as qudt
import floorplan_dsl.parser.classes.fpm2.variables as var

import floorplan_dsl.parser.processors.fpm2 as proc2

# object processors for FloorPlan DSL
from floorplan_dsl.parser.processors.fpm1 import unique_names_processor
from floorplan_dsl.parser.processors.variation import (
    discrete_distribution_obj_processor,
)

dir_path = dirname(realpath(__file__))
sys.path.append(dir_path)


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
    floorplan_mm = metamodel_from_file(
        path,
        classes=[
            fpm.Space,
            fpm.Wall,
            fpm.Column,
            fpm.Divider,
            fpm.Window,
            fpm.Entryway,
            fpm.Frame,
            geom.PointCoordinate,
            geom.Rectangle,
            geom.Circle,
            geom.Polygon,
            var.VariableReference,
            qudt.Length,
            qudt.Angle,
        ],
    )
    floorplan_mm.register_obj_processors(
        {
            "Space": proc2.space_obj_processor,
            "Feature": proc2.feature_obj_processor,
            "WallOpening": proc2.opening_obj_processor,
        }
    )
    floorplan_mm.register_scope_providers(
        {
            "WallFrame.space": proc2.space_location_scope_provider,
            "SpaceFrame.space": proc2.space_location_scope_provider,
        }
    )
    floorplan_mm.auto_init_attributes = False
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
    language="floorplan-v2",
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
