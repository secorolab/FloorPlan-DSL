import bpy
import bmesh
import os

def create_mesh(collection, name, vertices, faces):
    me = bpy.data.meshes.new(name)
    me.from_pydata(vertices, [], faces)
    me.update()

    bm = bmesh.new()
    bm.from_mesh(me, face_normals=True) 

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

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
    bpy.ops.object.modifier_apply(modifier="boolean")

def export(_format, path, name):

    if _format == 'stl':
        name = "{name}.stl".format(name=name)
        bpy.ops.export_mesh.stl(filepath=os.path.join(path, name))