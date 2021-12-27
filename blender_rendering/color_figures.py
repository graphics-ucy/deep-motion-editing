import sys
import os

sys.path.append("./utils")
sys.path.append("./")
import numpy as np
import bpy
import mathutils
import pdb
import colorsys

print('Executing script!')

bvh_materials_config = {
    'gt': (*colorsys.hsv_to_rgb(0.33, 1, 1), 1),

    'dqMSE': (*colorsys.hsv_to_rgb(0.833, 1, 1), 1),
    'dq': (*colorsys.hsv_to_rgb(0.745, 1, 1), 1),

    '6Dpos': (*colorsys.hsv_to_rgb(0.05, 1, 1), 1),
    'ortho6Dpos': (*colorsys.hsv_to_rgb(0.05, 1, 1), 1),

    'ortho6D': (*colorsys.hsv_to_rgb(0.025, 1, 1), 1),

    '6Doff': (*colorsys.hsv_to_rgb(0.075, 1, 1), 1),
    'ortho6Doff': (*colorsys.hsv_to_rgb(0.075, 1, 1), 1),

    '6D': (*colorsys.hsv_to_rgb(0.025, 1, 1), 1),

    'qMSE': (*colorsys.hsv_to_rgb(0.65, 1, 1), 1),
    'quatsFK': (*colorsys.hsv_to_rgb(0.62, 1, 1), 1),
    'quatsoff': (*colorsys.hsv_to_rgb(0.62, 1, 1), 1),
    'quatspos': (*colorsys.hsv_to_rgb(0.58, 1, 1), 1),
    'q': (*colorsys.hsv_to_rgb(0.65, 1, 1), 1),
    'quats': (*colorsys.hsv_to_rgb(0.65, 1, 1), 1),

    'undefined': (*colorsys.hsv_to_rgb(1, 1, 1), 1)
}


def retrieve_mat_color(bvh_name):
    for key in bvh_materials_config:
        if key == 'gt':
            if bvh_name.endswith(key+".bvh") or bvh_name.startswith(key):
                return bvh_materials_config[key]
        if bvh_name.startswith(key + "_"):
            return bvh_materials_config[key]
    return bvh_materials_config['undefined']


def add_material_for_character(character, name=""):
    # Get the material
    mat = character.active_material
    bsdf = mat.node_tree.nodes[0]
    bsdf.inputs[0].default_value = retrieve_mat_color(name)


if __name__ == '__main__':
    print('Coloring figures and floor...')

    # Change color of figures: Get all 'Hips_end_'
    characters = [obj for obj in bpy.data.objects if obj.name.startswith("Hips_end_")]
    for character in characters:
        add_material_for_character(character, character.name.replace("Hips_end_", ""))

    # Change color of floor:
    bpy.data.materials["floorMaterial"].node_tree.nodes["Checker Texture"].inputs[2].default_value = (
        *colorsys.hsv_to_rgb(0.7, 0.35, 0.55), 1)

    # Save and exit
    bpy.ops.wm.save_mainfile()
    bpy.ops.wm.quit_blender()
