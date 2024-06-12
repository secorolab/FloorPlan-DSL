import unittest
import os

# Application imports
from textx import metamodel_for_language


class FloorPlanDSLMethods(unittest.TestCase):

    def test_valid_model(self):
        try:
            my_metamodel = metamodel_for_language("exsce-floorplan-dsl")
            model_path = os.path.join(
                os.getcwd(), "models", "examples", "hospital.floorplan"
            )
            my_model = my_metamodel.model_from_file(model_path)
        except:
            assert False
        else:
            assert True


class VariationDSLMethods(unittest.TestCase):

    def test_valid_model(self):
        try:
            my_metamodel = metamodel_for_language("exsce-variation-dsl")
            model_path = os.path.join(
                os.getcwd(), "models", "examples", "hospital.variation"
            )
            my_model = my_metamodel.model_from_file(model_path)
        except:
            assert False
        else:
            assert True


if __name__ == "__main__":
    unittest.main()
