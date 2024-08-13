from textx import get_model, textx_isinstance
from textx.scoping.tools import get_unique_named_object


from floorplan_dsl.parser.classes.fpm2.floorplan import Feature


def space_location_scope_provider(frame, attr, attr_ref):
    m = get_model(frame)
    name = attr_ref.obj_name

    if name == "this":
        if textx_isinstance(frame.parent.parent, Feature):
            return frame.parent.parent.parent
        else:
            return frame.parent.parent
    else:
        return get_unique_named_object(m, name)


def process_location(element):
    element.process_location()


def space_obj_processor(space):
    process_location(space)
    space.wall_pose_coords = space.get_wall_poses()
    space.pose = space.get_pose_coord_wrt_location()


def feature_obj_processor(feature):
    process_location(feature)


def opening_obj_processor(opening):
    process_location(opening)
