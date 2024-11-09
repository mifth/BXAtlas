import bpy

import numpy as np

import ctypes
from ctypes import *

import traceback
import time

from .BXAtlas_CTypes.bxatlas_data import *
from . import bxatlas_utils


class ChartOptionsGroup(bpy.types.PropertyGroup):
    show_options: bpy.props.BoolProperty(default=True, name="")

    maxChartArea: bpy.props.FloatProperty(default=0,)
    maxBoundaryLength: bpy.props.FloatProperty(default=0,)

    normalDeviationWeight: bpy.props.FloatProperty(default=2,)
    roundnessWeight: bpy.props.FloatProperty(default=0.01,)
    straightnessWeight: bpy.props.FloatProperty(default=6,)
    normalSeamWeight: bpy.props.FloatProperty(default=4,)
    textureSeamWeight: bpy.props.FloatProperty(default=0.5,)

    maxCost: bpy.props.FloatProperty(default=2,)
    maxIterations: bpy.props.IntProperty(default=1, min=0,)

    useInputMeshUvs: bpy.props.BoolProperty(default=False,)
    fixWinding: bpy.props.BoolProperty(default=False,)


class PackOptionsGroup(bpy.types.PropertyGroup):
    show_options: bpy.props.BoolProperty(default=True, name="")

    maxChartSize: bpy.props.IntProperty(default=0, min=0,)
    padding: bpy.props.IntProperty(default=0, min=0,)
    texelsPerUnit: bpy.props.BoolProperty(default=0,)
    resolution: bpy.props.IntProperty(default=0, min=0,)
    bilinear: bpy.props.BoolProperty(default=True,)
    blockAlign: bpy.props.BoolProperty(default=False,)
    maxCbruteForceost: bpy.props.BoolProperty(default=False,)
    # createImage: bpy.props.BoolProperty(default=False,)
    rotateChartsToAxis: bpy.props.BoolProperty(default=True,)
    rotateCharts: bpy.props.BoolProperty(default=True,)


class BXA_OP_Generate(bpy.types.Operator):
    bl_idname = "bxa.generate"
    bl_label = "Generate"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_obj: bpy.types.Object = context.active_object

        if not active_obj:
            return {"CANCELLED"}
        
        active_obj.data.update()

        # bpy.ops.ed.undo_push()

        # Positions
        mesh_verts = np.empty(len(active_obj.data.vertices) * 3, dtype=np.float32)
        active_obj.data.vertices.foreach_get('co', mesh_verts)

        # PolyIndices
        # poly_indices = np.concatenate([np.array(poly.vertices, dtype=np.int32) for poly in active_obj.data.polygons])
        poly_indices = np.empty(len(active_obj.data.loop_triangles) * 3, dtype=np.int32)
        active_obj.data.polygons.foreach_get("vertices", poly_indices)

        # Get Polygons Loop Start
        np_loops_total = np.empty(len(active_obj.data.polygons), dtype=np.int32)
        active_obj.data.polygons.foreach_get("loop_total", np_loops_total)

        # Normals
        np_normals = None
        # np_normals = np.empty(len(active_obj.data.loops) * 3, dtype=np.float32)
        # active_obj.data.corner_normals.foreach_get("vector", np_normals)
        # np_normals = np.ctypeslib.as_ctypes(np_normals)

        # UVs
        np_uvs = None
        active_uv = active_obj.data.uv_layers.active

        if active_uv:
            # uvs = [uv.uv[:] for uv in active_uv]
            np_uvs = np.empty(len(active_obj.data.loops) * 2, dtype=np.float32)
            active_uv.uv.foreach_get("vector", np_uvs)
            np_uvs = np.ctypeslib.as_ctypes(np_uvs)

        # Load XAtlas
        bxatlas = bxatlas_utils.load_xatlas()

        b_data: DataFromPy = DataFromPy(
           np.ctypeslib.as_ctypes(mesh_verts),
           len(mesh_verts),

           np.ctypeslib.as_ctypes(poly_indices),
           len(poly_indices),

           np.ctypeslib.as_ctypes(np_loops_total),
           len(np_loops_total),

           np_normals,

           np_uvs,
        )

        bxatlas.GenerateXAtlas.argtypes = (POINTER(DataFromPy), )
        bxatlas.GenerateXAtlas.restype = ctypes.POINTER(DataToPy)

        try:
            start_time = time.time()

            xatlas_data: DataToPy = bxatlas.GenerateXAtlas(b_data)

            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time:.6f} seconds")
            
        except Exception as e:
            print("No Data From XAtlas!")
            print(e)
            del bxatlas
            del b_data
            xatlas_data = None
            bxatlas = None
            b_data = None

            return {"CANCELLED"}

        xatlas_contents = xatlas_data.contents

        np_new_uvs = np.ctypeslib.as_array(xatlas_contents.uvs, shape=(len(active_obj.data.loops) * 2,))

        if active_uv:
            active_uv.uv.foreach_set("vector", np_new_uvs)

        active_obj.data.update()

        # Clear
        del xatlas_data
        del bxatlas
        del b_data
        del xatlas_contents
        xatlas_data = None
        bxatlas = None
        b_data = None
        xatlas_contents = None

        return {"FINISHED"}


classes = (
    ChartOptionsGroup,
    PackOptionsGroup,
    BXA_OP_Generate,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.chart_options_group = bpy.props.PointerProperty( name="Chart Options Group", type=ChartOptionsGroup)
    bpy.types.Scene.pack_options_group = bpy.props.PointerProperty( name="Pack Options Group", type=PackOptionsGroup)
    

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.chart_options_group
    del bpy.types.Scene.pack_options_group