# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Random Material Assigner",
    "author" : "Ben Norris",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy 
from bpy.props import (BoolProperty, StringProperty, PointerProperty)
from bpy.types import (Panel, Operator, PropertyGroup)
from random import randint

class RandomMatProps(PropertyGroup):
    use_all : BoolProperty(name = "Use All Materials", description = "Should all materials be considered", default = True)
    mat_prefix : StringProperty(name = "", description = "A prefix to search for random materials", default = '')

def AssignRandomMats():
    #get props
    rm_props = bpy.context.scene.rmprop
    prefix = rm_props.mat_prefix
    use_all_bool = rm_props.use_all

    #make and fill mats list
    mats = []
    for mat in bpy.data.materials:
        if use_all_bool:
            mats.append(mat)
        else:
            if prefix in mat.name:
                mats.append(mat)

    #assign random mat from mats list to current obj
    for obj in bpy.context.selected_objects:
        rand = randint(0, len(mats) - 1)
        ob = bpy.context.scene.objects[obj.name]

        #if obj has material slots
        if ob.data.materials:
            ob.data.materials[0] = mats[rand]
        else:
            ob.data.materials.append(mats[rand])

#operator
class Random_Mat_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.random_mat_assigner"
    bl_label = "Random Material Assigner"
    bl_description = "Assigns random materials to selected objects"

    def execute(self, context):
        AssignRandomMats()
        return{'FINISHED'}

#ui
class Random_Mat_PT_Panel(bpy.types.Panel):
    bl_idname = "Random_Mat_PT_Panel"
    bl_label = "Random Material Assigner"
    bl_category = "Random Material Assigner"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column(align=False)
        #row = col.row(align=True)

        col.prop(scene.rmprop, "use_all")
        bool_all = scene.rmprop.use_all
        if not bool_all:
            col.label(text="Prefix to search with")
            col.prop(scene.rmprop, "mat_prefix")

        col.separator()
        col.operator('view3d.random_mat_assigner', text="Assign Random Mats!")

def register():
    bpy.utils.register_class(Random_Mat_OT_Operator)
    bpy.utils.register_class(Random_Mat_PT_Panel)
    bpy.utils.register_class(RandomMatProps)
    bpy.types.Scene.rmprop = PointerProperty(type=RandomMatProps)

def unregister():
    bpy.utils.unregister_class(Random_Mat_OT_Operator)
    bpy.utils.unregister_class(Random_Mat_PT_Panel)
    bpy.utils.unregister_class(RandomMatProps)
    del bpy.types.Scene.rmprop
