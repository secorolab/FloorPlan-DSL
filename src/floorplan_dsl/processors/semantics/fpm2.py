def process_location(element):
    element.process_location()


def space_obj_processor(space):
    process_location(space)
    space.wall_pose_coords = space.get_wall_poses()
    space.pose = space.get_pose_coord_wrt_location()


def feature_obj_processor(feature):
    process_location(feature)
    feature.pose = feature.get_pose_coord_wrt_location()


def opening_obj_processor(opening):
    process_location(opening)
    opening.pose = opening.get_pose_coord_wrt_location()
