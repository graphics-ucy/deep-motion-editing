import sys
import os

sys.path.append("./utils")
sys.path.append("./")
import numpy as np
import bpy
import mathutils
import pdb
import colorsys

# Just the names
group_names = [
    'gt', 'dqMSE', 'dq', '6Dpos', 'ortho6Dpos', 'ortho6D', '6Doff',
    'ortho6Doff', '6D', 'qMSE', 'quatsFK', 'quatsoff', 'quatspos',
    'q', 'undefined'
]

# Save the parent objects
groups = {}

# Save the characters
groups_characters = {}

def determine_group(bvh_name):
    for key in group_names:
        if key == 'gt':
            if bvh_name.endswith(key+".bvh") or bvh_name.startswith(key):
                return key
        if bvh_name.startswith(key + "_"):
            return key
    return 'undefined'


def add_in_group(key, character):
    # Initialize new group
    if key not in groups:
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0))
        parent_obj = bpy.data.objects['Empty']
        parent_obj.name = key
        groups[key] = parent_obj
        groups_characters[key] = []
        
    character.parent = groups[key]
    groups_characters[key].append(character)


def group_characters():
    # Get top level objects (characters)
    characters = [obj for obj in bpy.data.objects if obj.parent == None]
    for key in group_names:
        
        for character in characters:
            # Is it gt?
            if key == 'gt':
                if character.name.endswith(key+".bvh") or character.name.startswith(key):
                    add_in_group(key, character)
                    
            # It is something else
            if character.name.startswith(key + "_") and not (character.name.endswith("gt.bvh") 
            or character.name.startswith("gt")):
                add_in_group(key, character)
                

def position_characters():
    # For each group
    for key in groups_characters:
        x_offset = 10 # fwd
        y_offset = 7 # right
        (x,y,z) = (0, 0, 0)
        counter = 1
        for c in groups_characters[key]:
            # Change translation of object
            curr_loc = c.location
            c.location = curr_loc + mathutils.Vector((x, y, z))
                        
            if counter % 2 == 0 and counter != 0:
                x = x + x_offset
                y = 0
            else:
                y = y + y_offset

            counter = counter + 1


def disable_xyz_location():
    characters_hips = [obj for obj in bpy.data.objects if obj.name.startswith('Hips_end_')]
    for c in characters_hips:
        # x location
        c.animation_data.action.fcurves[0].mute = True
        # y location
        c.animation_data.action.fcurves[1].mute = True
        # z location
        c.animation_data.action.fcurves[2].mute = True

if __name__ == '__main__':
    print('Positioning figures...')
    group_characters()
    position_characters()
    disable_xyz_location()

    # Adjust camera
    cam = bpy.data.objects['Camera']
    cam.location = mathutils.Vector((95, 0, 31))
    cam.rotation_euler = mathutils.Vector((1.2257, 0, 1.5857))

    # Save and exit
    bpy.ops.wm.save_mainfile()
    bpy.ops.wm.quit_blender()
