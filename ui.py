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
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "BXAtlas"

    colors_state = None

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column()

        col = layout.operator("bxa.generate", text="Generate")

        col = layout.column()

        box = col.box()
        box.label(text="Chart Options")
        chart_options = context.scene.chart_options_group
        
        box.prop(chart_options, "show_options", icon="TRIA_DOWN" if chart_options.show_options else "TRIA_RIGHT", emboss=False)

        if chart_options.show_options:
            box.prop(chart_options, "maxChartArea", text="maxChartArea")
            box.prop(chart_options, "maxBoundaryLength", text="maxBoundaryLength")

            box.prop(chart_options, "normalDeviationWeight", text="normalDeviationWeight")
            box.prop(chart_options, "roundnessWeight", text="roundnessWeight")
            box.prop(chart_options, "straightnessWeight", text="straightnessWeight")
            box.prop(chart_options, "normalSeamWeight", text="normalSeamWeight")
            box.prop(chart_options, "textureSeamWeight", text="textureSeamWeight")

            box.prop(chart_options, "maxCost", text="maxCost")
            box.prop(chart_options, "maxIterations", text="maxIterations")

            box.prop(chart_options, "useInputMeshUvs", text="useInputMeshUvs")
            box.prop(chart_options, "fixWinding", text="fixWinding")

        col = layout.column()

        box = col.box()
        box.label(text="Pack Options")
        pack_options = context.scene.pack_options_group
        box.prop(pack_options, "show_options", icon="TRIA_DOWN" if pack_options.show_options else "TRIA_RIGHT", emboss=False)

        if pack_options.show_options:
            box.prop(pack_options, "maxChartSize", text="maxChartSize")
            box.prop(pack_options, "padding", text="padding")
            box.prop(pack_options, "texelsPerUnit", text="texelsPerUnit")
            box.prop(pack_options, "resolution", text="resolution")
            box.prop(pack_options, "bilinear", text="bilinear")
            box.prop(pack_options, "blockAlign", text="blockAlign")
            box.prop(pack_options, "maxCbruteForceost", text="maxCbruteForceost")
            # box.prop(pack_options, "createImage", text="createImage")
            box.prop(pack_options, "rotateChartsToAxis", text="rotateChartsToAxis")
            box.prop(pack_options, "rotateCharts", text="rotateCharts")

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


