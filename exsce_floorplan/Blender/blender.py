import bpy
import bmesh

def create_mesh(collection, name, vertices, faces):
    me = bpy.data.meshes.new(name)
    me.from_pydata(vertices, [], faces)
    me.update()

    bm = bmesh.new()
    bm.from_mesh(me, face_normals=True) 

    bm.to_mesh(me)
    bm.free()
    me.update()

    obj = bpy.data.objects.new(name, me)
    collection.objects.link(obj)

def create_collection(name):
    collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(collection)
    return collection

def clear_scene():
    for obj in bpy.context.scene.objects:
        obj.select_set(True)
        bpy.ops.object.delete()

def boolean_operation_difference(obj_name, cutter_name):
    # select the object
    obj = bpy.data.objects[obj_name]
    # configure modifier
    boolean = obj.modifiers.new(name="boolean", type='BOOLEAN')
    boolean.object = bpy.data.objects[cutter_name]
    boolean.operation = "DIFFERENCE"
    # apply modifier
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="boolean")

def export(name):
    bpy.ops.export_mesh.stl(filepath="output/{name}_enviornment.stl".format(name=name))