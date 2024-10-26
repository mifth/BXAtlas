# Blender Add-on Template
# Contributor(s): Aaron Powell (aaron@aaronpowell.me)
#
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

import bpy
from bpy.types import Panel
from bpy.types import Operator, AddonPreferences
from bpy.props import *


class TP_AddonPreferences(AddonPreferences):

    bl_idname = __package__

    # test_col_prop : FloatVectorProperty(
    #     name="Color Tag 1",
    #     subtype='COLOR',
    #     default=(0.764286, 0.285096, 0.283878),
    #     min=0.0, max=1.0,
    #     description=""
    # )


    # def draw(self, context):
    #     layout = self.layout
    #     row = layout.row()
    #     row.label(text="Test")
    #     row = layout.column()
    #     row.prop(self, "test_col_prop")


class BXA_PT_Panel(Panel):
    bl_label = 'BXAtlas'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BXAtlas"

    colors_state = None


    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column()

        col = layout.operator("bxa.test", text="BXAtlas Test")

classes = (
    TP_AddonPreferences,
    BXA_PT_Panel,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)



def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


