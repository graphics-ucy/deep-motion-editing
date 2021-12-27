import sys
import bpy

sys.path.append("./blender_rendering")
from options import Options
from load_bvh import load_bvh
from scene import make_scene, add_material_for_character, add_rendering_parameters
import os
import glob
import re

def initialise_scene(args):
    # Import first bvh & scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    scene = make_scene()
    bpy.ops.object.select_all(action='DESELECT')
    add_rendering_parameters(bpy.context.scene, args, scene[1])


def bvh_import(bvh_path):
    # Load bvh
    filename = os.path.basename(bvh_path)
    character = load_bvh(bvh_path)
    
    # EXPETIONAL FOR MIXAMO
    # Blender naming restrictions: Remove spaces & max len 63
    filename = filename.replace(" ","")
    ending_name = filename.split("_")[-1]
    if ending_name.find("out") == -1 and ending_name.find("gt") == -1:
    	ending_name = ""
    filename = re.sub("(out.bvh)|(gt.bvh)", '', filename)
    filename = filename.split("_m_",1)[0]
    filename = filename + ending_name
    print("Renaming figure to: %s" % filename)
    
    add_material_for_character(character, bvh_name=filename)
    # Create parent
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0))
    # Load child and parent object instances
    parent_obj = bpy.data.objects['Empty']
    child_obj = bpy.data.objects["Hips_end_%s" % filename]
    # Rename parent & set child
    parent_obj.name = filename
    child_obj.parent = parent_obj
    # Move to parent to child's collection
    current_collection = parent_obj.users_collection[0]
    target_collection = child_obj.users_collection[0]
    target_collection.objects.link(parent_obj)
    current_collection.objects.unlink(parent_obj)


if __name__ == '__main__':
    args = Options(sys.argv).parse()
    dir_path = args.dir_path
    bvh_files = glob.glob("%s/*.bvh" % dir_path)
    print(bvh_files)
    initialise_scene(args)

    for bvh in bvh_files:
        print(bvh)
        bvh_import(bvh)

    save_path = "%s/%s.blend" % (dir_path, os.path.basename(os.path.normpath(dir_path)))
    bpy.ops.wm.save_as_mainfile(filepath=save_path)
    print("Done! Saved in %s !" % save_path)
    bpy.ops.wm.quit_blender()
