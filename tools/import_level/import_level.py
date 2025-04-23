import os
import shutil
import bpy
import re
import json
from mathutils import Euler
import math
import time

script_dir = "Path/To/The/Scripts/Folder/Because/Blender/Doesn't/Like/To/Set/It/Correctly" #Use / instead of \
start_time = time.time()

def find_many(instring, *substrings):
    pat = re.compile('|'.join([re.escape(s) for s in substrings]))
    match = pat.search(instring)
    if match is None:
        return -1
    else:
        return match.start()

models = 0

def open_level():
    global models
    scale = float(input("What scale would you like to use? (Recommended - 0.017): "))
    #input("Run prep.py, then press enter")
    os.system("prep.py")
    for file in os.listdir("{0}/level_files".format(script_dir)):
        if file.endswith(".EXPORT.json"):
            layer_name = file.split(".")[0]
            object_list = []
            with open(os.path.join(script_dir, "level_files", file), 'r') as f:
                file_json = json.load(f)
                global models
                for thing in file_json:
                    if thing["name"] == "RigidInstance" or thing["name"] == "NPC":
                        if "rows" in thing and len(thing["rows"]) > 0:
                            model_name = None
                            model_file_name = None
                            model_pos = None
                            model_rot = None
                            model_scale = None
                            for key in thing["rows"][0].keys():
                                if key == "Name:s" and model_name == None: model_name = thing["rows"][0].get("Name:s", "")
                                if key == "GeometryResource:s" and model_file_name == None: model_file_name = thing["rows"][0].get("GeometryResource:s", "")
                                if key == "Pos:fff" and model_pos == None: model_pos = thing["rows"][0].get("Pos:fff", "")
                                if key == "Position:fff" and model_pos == None: model_pos = thing["rows"][0].get("Position:fff", "")
                                if key == "Orient:fff" and model_rot == None: model_rot = thing["rows"][0].get("Orient:fff", "")
                                if key == "Rotation:fff" and model_rot == None: model_rot = thing["rows"][0].get("Rotation:fff", "")
                                if key == "Scale:fff" and model_scale == None: model_scale = thing["rows"][0].get("Scale:fff", "")
                            def fix_size(x): return x*scale
                            if model_file_name is not None: print(model_file_name)
                            if model_pos is not None: print(model_pos)
                            if model_rot is not None: print(model_rot)
                            if model_scale is not None: print(model_scale)
                            if model_pos is not None: model_pos[2] = model_pos[2] * -1
                            if model_rot is not None: model_rot[2] = model_rot[2] + model_rot[1]
                            if model_rot is not None: model_rot[1] = 0
                            if model_rot is not None: model_rot[0] = 90 + model_rot[0]
                            if model_scale is not None: new_model_scale = list(map(fix_size, model_scale))
                            if model_pos is not None: new_model_pos = list(map(fix_size, model_pos))
                            new_model_rot = model_rot
                            if model_file_name is not None: model_file_path = "{0}\\level_files\\{1}.obj".format(script_dir, model_file_name.split(".")[0])
                            try:
                                for obj in bpy.data.objects:
                                    obj.tag = True
                                if model_file_name is not None: 
                                    bpy.ops.wm.obj_import(filepath=model_file_path) #bpy.ops.import_scene.obj
                                    imported_objects = [obj for obj in bpy.data.objects if obj.tag is False]
                                    if new_model_pos is not None: bpy.data.objects[imported_objects[0].name].location = (new_model_pos[0], new_model_pos[2], new_model_pos[1])
                                    if new_model_rot is not None: bpy.data.objects[imported_objects[0].name].rotation_euler = (math.radians(new_model_rot[0]), math.radians(new_model_rot[1]), math.radians(new_model_rot[2]))
                                    if new_model_scale is not None: bpy.data.objects[imported_objects[0].name].scale = (new_model_scale[0], new_model_scale[2], new_model_scale[1])
                                    bpy.data.objects[imported_objects[0].name].name = model_name
                                    bpy.data.objects[imported_objects[0].name].transform_apply(location=True, rotation=True, scale=True)
                                    bpy.data.objects[imported_objects[0].name].location = bpy.data.objects[imported_objects[0].name].location
                                    #collection.objects.link(bpy.data.objects[model_name])
                                    #bpy.data.collections[collection].objects.link(imported_objects[0])
                                    #bpy.context.scene.collection.objects.unlink(bpy.data.objects[model_name])
                                    object_list.append(imported_objects[0])
                                    models += 1
                            except Exception as e: print(e)
                    if thing["name"] == "PlaySurface":
                        if "rows" in thing and len(thing["rows"]) > 0:
                            model_name = None
                            model_file_name = None
                            model_pos = None
                            model_rot = None
                            model_scale = None
                            for key in thing["rows"][0].keys():
                                if key == "Name:s" and model_name == None: model_name = thing["rows"][0].get("Name:s", "")
                                if key == "Resource:s" and model_file_name == None: model_file_name = thing["rows"][0].get("Resource:s", "")
                            if model_file_name is not None: model_file_path = "{0}\\level_files\\{1}.obj".format(script_dir, model_file_name.split(".")[0])
                            try:
                                for obj in bpy.data.objects:
                                    obj.tag = True
                                if model_file_name is not None: 
                                    bpy.ops.wm.obj_import(filepath=model_file_path) #bpy.ops.import_scene.obj
                                    imported_objects = [obj for obj in bpy.data.objects if obj.tag is False]
                                    bpy.data.objects[imported_objects[0].name].location = (0, 0, 0)
                                    bpy.data.objects[imported_objects[0].name].rotation_euler = (math.radians(90), math.radians(0), math.radians(0))
                                    bpy.data.objects[imported_objects[0].name].scale = (0.017, 0.017, 0.017)
                                    bpy.data.objects[imported_objects[0].name].name = model_name
                                    bpy.data.objects[imported_objects[0].name].transform_apply(location=True, rotation=True, scale=True)
                                    bpy.data.objects[imported_objects[0].name].location = bpy.data.objects[imported_objects[0].name].location
                                    #collection.objects.link(bpy.data.objects[model_name])
                                    #bpy.data.collections[collection].objects.link(imported_objects[0])
                                    #bpy.context.scene.collection.objects.unlink(bpy.data.objects[model_name])
                                    object_list.append(imported_objects[0])
                                    models += 1
                            except Exception as e: print(e)
                    if thing["name"] == "Light":
                        if "rows" in thing and len(thing["rows"]) > 0:
                            light_pos = None
                            light_kind = None
                            light_name = None
                            light_color = None
                            light_intensity = None
                            for key in thing["rows"][0].keys():
                                if key == "Name:s" and light_name == None: light_name = thing["rows"][0].get("Name:s", "")
                                if key == "Pos:fff" and light_pos == None: light_pos = thing["rows"][0].get("Pos:fff", "")
                                if key == "Kind:d" and light_kind == None: light_kind = thing["rows"][0].get("Kind:d", "")
                                if key == "Color:dddd" and light_color == None: light_color = thing["rows"][0].get("Color:dddd", "")
                                if key == "Intensity:f" and light_intensity == None: light_intensity = thing["rows"][0].get("Intensity:f", "")
                            def fix_size(x): return x*0.017
                            if light_pos is not None: light_pos[2] = light_pos[2] * -1
                            if light_pos is not None: new_light_pos = list(map(fix_size, light_pos))
                            try:
                                light_data = bpy.data.lights.new(name=light_name, type='POINT')
                                light_data.energy = light_intensity * 10
                                light_data.color = [light_color[0], light_color[1], light_color[2]]
                                light_object = bpy.data.objects.new(name=light_name, object_data=light_data)
                                #collection.objects.link(light_object)
                                #bpy.context.scene.collection.objects.unlink(light_object)
                                object_list.append(light_object)
                                light_object.location = (new_light_pos[0], new_light_pos[2], new_light_pos[1])
                                models += 1
                            except Exception as e: print(e)
            collection = bpy.data.collections.new(layer_name)
            bpy.context.scene.collection.children.link(collection)
            for obj in object_list:
                collection.objects.link(obj)
                #bpy.context.scene.collection.objects.unlink(obj)
            
open_level()
print("Imported {0} models in {1} seconds".format(len(bpy.context.scene.objects), time.time() - start_time))