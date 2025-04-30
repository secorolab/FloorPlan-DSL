"""
Registration of languages with TextX registration API
"""

import sys
from os.path import dirname, join, realpath

import textx.scoping.providers as scoping_providers
from textx import LanguageDesc, GeneratorDesc, metamodel_from_file

from floorplan_dsl.generators.fpm import jsonld_floorplan_generator
from floorplan_dsl.generators.variations import variation_floorplan_generator

# Classes for FloorPlan DSL and Variation DSL
from floorplan_dsl.classes.variation.distribution import (
    UniformDistribution,
    DiscreteDistribution,
    NormalDistribution,
)

import floorplan_dsl.classes.fpm2.floorplan as fpm
import floorplan_dsl.classes.fpm2.geometry as geom
import floorplan_dsl.classes.fpm2.qudt as qudt
import floorplan_dsl.classes.fpm2.variables as var

import floorplan_dsl.processors.validation.fpm2 as validation
import floorplan_dsl.processors.semantics.fpm2 as sem2
import floorplan_dsl.processors as proc2
import floorplan_dsl.scoping.fpm2 as scope2

# object processors for FloorPlan DSL
from floorplan_dsl.processors.validation.variation import (
    discrete_distribution_obj_processor,
)

dir_path = dirname(realpath(__file__))
sys.path.append(dir_path)


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
            geom.Point,
            geom.Frame,
            geom.PointCoordinate,
            geom.Rectangle,
            geom.Circle,
            geom.SimplePolygon,
            var.VariableReference,
            qudt.Length,
            qudt.Angle,
            geom.PoseCoordinate,
            geom.PositionCoordinate,
            geom.EulerAngles,
            geom.Polyhedron,
            geom.Face,
        ],
    )
    floorplan_mm.register_obj_processors(
        {
            "Space": proc2.space_processor,
            "Feature": proc2.feature_processor,
            "WallOpening": proc2.opening_processor,
            "Wall": proc2.wall_processor,
            "Angle": sem2.process_angle_units,
            "AngleVariable": sem2.process_angle_units,
            "LengthValue": validation.validate_length_value,
            "AngleValue": validation.validate_angle_value,
        }
    )
    floorplan_mm.register_scope_providers(
        {
            "WallFrame.space": scope2.space_location_scope_provider,
            "SpaceFrame.space": scope2.space_location_scope_provider,
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


fpv2_lang = LanguageDesc(
    "fpm",
    pattern="*.fpm",
    description="A language to model floor plans (v2)",
    metamodel=fpv2_metamodel,
)

variation_lang = LanguageDesc(
    "fpm-variation",
    pattern="*.variation",
    description="A language to describe variations of floorplan models",
    metamodel=variation_metamodel,
)

variation_floorplan_gen = GeneratorDesc(
    language="fpm-variation",
    target="fpm",
    description="Generate variations of indoor environments from .fpm models",
    generator=variation_floorplan_generator,
)

json_ld_floorplan_gen = GeneratorDesc(
    language="fpm",
    target="json-ld",
    description="Generate composable models in json-ld",
    generator=jsonld_floorplan_generator,
)
