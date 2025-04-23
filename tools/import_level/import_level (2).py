bl_info = {
    "name": "Hobbit Level Importer",
    "description": "Import levels from The Hobbit (2003)",
    "author": "09beckerboy",
    "version": (1, 0),
    "blender": (4, 40, 0),
    "location": "View3D > Add > Mesh",
    "category": "3D View",
}



import os
import shutil
import bpy
import re
import json
from mathutils import Euler
import math
import time
from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, PropertyGroup)

level_dir = bpy.path.abspath("//")
start_time = time.time()

def find_many(instring, *substrings):
    pat = re.compile('|'.join([re.escape(s) for s in substrings]))
    match = pat.search(instring)
    if match is None:
        return -1
    else:
        return match.start() 

class OpenLevelOperator(bpy.types.Operator):
    bl_idname = "mesh.open_level"
    bl_label = "Open Level"
    def execute(self, context):
        models = 0
        # shutil.copy2("{0}\\exporttool.exe".format(level_dir), "{0}\\level_files\\exporttool.exe".format(level_dir))
        # shutil.copy2("{0}\\rgeom2obj.exe".format(level_dir), "{0}\\level_files\\rgeom2obj.exe".format(level_dir))
        # os.chdir("{0}/level_files".format(level_dir))
        # for file in os.listdir("{0}/level_files".format(level_dir)):
        #     if file.endswith(".EXPORT"): os.system(f'cmd /c "exporttool.exe -json -d {file}"')
        #     if file.endswith(".RGEOM"): os.system(f'cmd /c "rgeom2obj.exe {file} {file.split(".")[0]}.obj"')
        #     if file.endswith(".NPCGEOM"): os.system(f'cmd /c "rgeom2obj.exe {file} {file.split(".")[0]}.obj"')
        os.system("{0}/prep.py".format(level_dir))
        for file in os.listdir("{0}/level_files".format(level_dir)):
            if file.endswith(".EXPORT.json"):
                with open(os.path.join(level_dir, "level_files", file), 'r') as f:
                    file_json = json.load(f)
                    for thing in file_json:
                        if "rows" in thing and len(thing["rows"]) > 0:
                            model_name = None
                            model_pos = None
                            model_rot = None
                            model_scale = None
                            for key in thing["rows"][0].keys():
                                if key == "Resource:s" and model_name == None: model_name = thing["rows"][0].get("Resource:s", "")
                                if key == "GeometryResource:s" and model_name == None: model_name = thing["rows"][0].get("GeometryResource:s", "")
                                if key == "InitialPos:fff" and model_pos == None: model_pos = thing["rows"][0].get("InitialPos:fff", "")
                                if key == "Pos:fff" and model_pos == None: model_pos = thing["rows"][0].get("Pos:fff", "")
                                if key == "Position:fff" and model_pos == None: model_pos = thing["rows"][0].get("Position:fff", "")
                                if key == "Orientation:fff" and model_rot == None: model_rot = thing["rows"][0].get("Orientation:fff", "")
                                if key == "Orient:fff" and model_rot == None: model_rot = thing["rows"][0].get("Orient:fff", "")
                                if key == "Rotation:fff" and model_rot == None: model_rot = thing["rows"][0].get("Rotation:fff", "")
                                if key == "Scale:fff" and model_scale == None: model_scale = thing["rows"][0].get("Scale:fff", "")
                            if model_name is not None: print(model_name)
                            if model_pos is not None: print(model_pos)
                            if model_rot is not None: print(model_rot)
                            if model_scale is not None: print(model_scale)
                            if model_pos is not None: model_pos[2] = model_pos[2] * -1
                            if model_rot is not None: model_rot[2] = model_rot[2] + model_rot[1]
                            if model_rot is not None: model_rot[1] = 0
                            if model_rot is not None: model_rot[0] = 90 + model_rot[0]
                            if model_name is not None: model_file_path = "{0}\\level_files\\{1}.obj".format(level_dir, model_name.split(".")[0])
                            try:
                                for obj in bpy.data.objects:
                                    obj.tag = True
                                if model_name is not None: 
                                    bpy.ops.import_scene.obj(filepath=model_file_path)
                                    imported_objects = [obj for obj in bpy.data.objects if obj.tag is False]
                                    if model_pos is not None: bpy.data.objects[imported_objects[0].name].location = (model_pos[0], model_pos[2], model_pos[1])
                                    if model_rot is not None: bpy.data.objects[imported_objects[0].name].rotation_euler = (math.radians(model_rot[0]), math.radians(model_rot[1]), math.radians(model_rot[2]))
                                    if model_scale is not None: bpy.data.objects[imported_objects[0].name].scale = (model_scale[0], model_scale[2], model_scale[1])
                                    bpy.data.objects[imported_objects[0].name].transform_apply(location=True, rotation=True, scale=True)
                                    bpy.data.objects[imported_objects[0].name].location = bpy.data.objects[imported_objects[0].name].location
                                    models = models + 1
                            except Exception as e: print(e)
        #return models
        return {'FINISHED'}

#models = open_level()
#print("Imported {0} models in {1} seconds".format(models, time.time() - start_time))

class OBJECT_PT_ImportPanel(bpy.types.Panel):
    bl_label = "Hobbit Level Importer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "HLI"
    bl_context = "objectmode"   
    
    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        layout.prop(mytool, "level_dir")
        col = layout.column(align=True)
        col.operator("mesh.open_level", icon="MESH_CUBE")

classes = (
        OBJECT_PT_ImportPanel,
        OpenLevelOperator
        )
    

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()