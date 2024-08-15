from textx import get_model, textx_isinstance
from textx.scoping.tools import get_unique_named_object


from floorplan_dsl.classes.fpm2.floorplan import Feature


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
