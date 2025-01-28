import os
import bpy
from bpy import context
import re
from mathutils import Euler

script_dir = "C:/Users/09beckerboy/Documents/Hobbit Modding/HMCT/tools/Objects/Models" #Use / instead of \

def purge_orphans():
    if bpy.app.version >= (3, 0, 0):
        bpy.ops.outliner.orphans_purge(
            do_local_ids=True, do_linked_ids=True, do_recursive=True
        )
    else:
        # call purge_orphans() recursively until there are no more orphan data blocks to purge
        result = bpy.ops.outliner.orphans_purge()
        if result.pop() != "CANCELLED":
            purge_orphans()


def clean_scene():
    """
    Removing all of the objects, collection, materials, particles,
    textures, images, curves, meshes, actions, nodes, and worlds from the scene
    """
    if bpy.context.active_object and bpy.context.active_object.mode == "EDIT":
        bpy.ops.object.editmode_toggle()

    for obj in bpy.data.objects:
        obj.hide_set(False)
        obj.hide_select = False
        obj.hide_viewport = False

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    collection_names = [col.name for col in bpy.data.collections]
    for name in collection_names:
        bpy.data.collections.remove(bpy.data.collections[name])

    # in the case when you modify the world shader
    world_names = [world.name for world in bpy.data.worlds]
    for name in world_names:
        bpy.data.worlds.remove(bpy.data.worlds[name])
    # create a new world data block
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]

    purge_orphans()

def find_many(instring, *substrings):
    pat = re.compile('|'.join([re.escape(s) for s in substrings]))
    match = pat.search(instring)
    if match is None:
        return -1
    else:
        return match.start() 

for root, dirs, files in os.walk(script_dir):
    for file in files:
        if file.endswith(".fbx"):
            model_file_path = os.path.join(root, file)
            try:
                clean_scene()
                for obj in bpy.data.objects:
                    obj.tag = True
                #bpy.ops.wm.obj_import(filepath=model_file_path)
                bpy.ops.import_scene.fbx(filepath=model_file_path)
                print("Imported {}".format(model_file_path))
                imported_objects = [obj for obj in bpy.data.objects if obj.tag is False]
                print("Set imported objects")
                for obj in context.scene.objects:
                    obj.select_set(False)
                print("Deselected object")
                for obj in context.visible_objects:
                    if not (obj.hide_get() or obj.hide_render):
                        obj.select_set(True)
                print("IDK")

                for area in bpy.context.screen.areas:
                    if area.type == 'VIEW_3D':
                        for region in area.regions:
                            if region.type == 'WINDOW':
                                #override = {'area': area, 'region': region, 'edit_object': bpy.context.edit_object}
                                with bpy.context.temp_override(area=area, region=region, edit_object=bpy.context.edit_object):
                                    bpy.ops.view3d.view_all(center=True) #Doesn't work, override deprecated
                print("Set View")
                output_file = "{0}/{1}.png".format(root, file.split(".")[0])

                for obj in context.scene.objects:
                    for material in obj.data.materials:
                        material.use_backface_culling = True
                    obj.select_set(False)
                print("Set Backface Culling to True")

                #bpy.ops.view3d.toggle_shading(type='MATERIAL')

                # Set the viewport resolution
                context.scene.render.resolution_x = 1024
                context.scene.render.resolution_y = 1024
                print("Set viewport resolution")

                # Set the output format
                context.scene.render.image_settings.file_format = "PNG"
                print("Set output to png")

                # Render the viewport and save the result
                bpy.ops.render.opengl(write_still=True)
                bpy.data.images["Render Result"].save_render(output_file)
                print("Saved render as {}".format(output_file))
            except Exception as e: print(e)