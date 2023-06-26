def get_proper_value(variable):
    return variable.value.value if variable.ref is None else variable.ref.name

def pose_json(pose):
    return {
        'translation' : {
            'x' : pose.translation.x.value,
            'y' : pose.translation.y.value,
            'z' : pose.translation.z.value if not pose.translation.z is None else 0 
        },
        'rotation' : pose.rotation.value
    }

def shape_json(shape):

    context = {
        'type' : shape.__class__.__name__
    }

    if context['type'] == 'Rectangle':
        context['width'] = shape.w
        context['length'] = shape.l 
    elif context['type'] == 'VerticalRectangle':
        context['width'] = shape.w 
        context['height'] = shape.h
    elif context['type'] == 'Polygon':
        context['points'] = shape.points

    return context

def floor_feature_json(feature):
    return {
        'name' : feature.name,
        'shape' : shape_json(feature.shape),
        'divider' : feature.divider,
        'column' : feature.column,
        'height' : get_proper_value(feature.height),
        'from' : feature.location.from_frame,
        'pose' : pose_json(feature.location.pose)
    }

def space_json(space):
    return {
        'name' : space.name,
        'location' : {
            'pose' : pose_json(space.location.pose),
            'from' : {
                'world' : space.location.from_frame.world,
                'ref' : space.location.from_frame.ref,
                'index' : space.location.from_frame.index
            },
            'to' : {
                'index' : space.location.to_frame.index
            },
            'spaced' : space.location.spaced,
            'not_aligned' : space.location.aligned
        },
        'floor_features': [floor_feature_json(f) for f in space.floor_features],
        'shape' : shape_json(space.shape),
        'wall_thickness' : space.wall_thickness,
        'wall_height' : space.wall_height
    }

def wall_opening_json(wall_opening):

    return {
        'entryway' : wall_opening.entryway,
        'window'  : wall_opening.window,
        'name' : wall_opening.name,
        'in' : {
            'wall_a' : wall_opening.wall_a,
            'wall_b' : wall_opening.wall_b
        },
        'shape' : shape_json(wall_opening.shape),
        'pose' : pose_json(wall_opening.pose)
    }

def default_json(default):
    return {
        'wall_thickness' : default.wall_thickness,
        'wall_height' : default.wall_height
    }

def variable_json(variable):
    return {
        'type':variable.__class__.__name__,
        'name' : variable.name,
        'value' : variable.value.value
    }

def get_floorplan_as_json(flp_model):
    
    # convert the original model into a context dictionary
    context = {
        'floorplan_name' : flp_model.name,
        'name' : flp_model.name,
        'variables' : [variable_json(variable) for variable in flp_model.variables],
        'spaces' : [space_json(space) for space in flp_model.spaces],
        'wall_openings' : [wall_opening_json(wall_opening) for wall_opening in flp_model.wall_openings],
        'default' : default_json(flp_model.default)
    }
    return context
