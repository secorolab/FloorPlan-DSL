import sys
from os.path import dirname, join
from textx import metamodel_from_file

class FloorPlan(object):
    """
    Floor plan model interpreter
    """

    def __init__(self, model):
        # instanciate all walls (boundary lines for each space)
        self.spaces = model.spaces
        
    def interpret(self):

        # locate all rooms according to the description w/o wall thickness

        # perform all boolean operations and merge spaces accordingly

        # consider the order integer of each room

        # space out the rooms for the offset

        # offset the walls to their desired width

        # determine the points for each area: i.e room, walls, doorways, windows

        # generate JSON-LD file with all this information 
        pass

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python {} <model>".format(sys.argv[0]))
    else:
        my_metamodel = metamodel_from_file('exsce_floorplan.tx')    
        my_model = my_metamodel.metamodel_from_file(sys.argv[1])
        floor_plan = FloorPlan(my_model)
        floor_plan.interpret()