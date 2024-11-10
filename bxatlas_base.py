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
    texelsPerUnit: bpy.props.FloatProperty(default=0, min=0,)
    resolution: bpy.props.IntProperty(default=0, min=0,)
    bilinear: bpy.props.BoolProperty(default=True,)
    blockAlign: bpy.props.BoolProperty(default=False,)
    bruteForce: bpy.props.BoolProperty(default=False,)
    # createImage: bpy.props.BoolProperty(default=False,)
    rotateChartsToAxis: bpy.props.BoolProperty(default=True,)
    rotateCharts: bpy.props.BoolProperty(default=True,)


class BXA_OP_Generate(bpy.types.Operator):
    bl_idname = "bxa.generate"
    bl_label = "Generate"
    bl_options = {'REGISTER', 'UNDO'}

    pack_only: bpy.props.BoolProperty(
        name="Packing Only",
        default=False,
        description="Enable packing only mode"
    )

    def execute(self, context):
        # bpy.ops.ed.undo_push()

        decl_meshes_py = []

        sel_objs = context.selected_objects

        if not sel_objs:
            return {"CANCELLED"}

        final_objects = []
        mesh_decls_py = []
        GetMeshDecls(sel_objs, final_objects, mesh_decls_py)

        if not final_objects:
            return {"CANCELLED"}

        mesh_decls_py_ptr = (MeshDeclPy * len(mesh_decls_py))()
        for i, mesh_decl in enumerate(mesh_decls_py):
            mesh_decls_py_ptr[i] = mesh_decl

        chart_gr = context.scene.chart_options_group
        pack_gr = context.scene.pack_options_group

        # Load XAtlas
        bxatlas = bxatlas_utils.load_xatlas()

        # ChartOptionsPy
        chart_opt: ChartOptionsPy = ChartOptionsPy()
        chart_opt.maxChartArea = chart_gr.maxChartArea
        chart_opt.maxBoundaryLength = chart_gr.maxBoundaryLength
        chart_opt.normalDeviationWeight = chart_gr.normalDeviationWeight
        chart_opt.roundnessWeight = chart_gr.roundnessWeight
        chart_opt.straightnessWeight = chart_gr.straightnessWeight
        chart_opt.normalSeamWeight = chart_gr.normalSeamWeight
        chart_opt.textureSeamWeight = chart_gr.textureSeamWeight
        chart_opt.maxCost = chart_gr.maxCost
        chart_opt.maxIterations = ctypes.c_uint32(chart_gr.maxIterations)
        chart_opt.useInputMeshUvs = chart_gr.useInputMeshUvs
        chart_opt.fixWinding = chart_gr.fixWinding

        # PackOptionsPy
        pack_opt: PackOptionsPy = PackOptionsPy()
        pack_opt.maxChartSize = ctypes.c_uint32(pack_gr.maxChartSize)
        pack_opt.padding = ctypes.c_uint32(pack_gr.padding)
        pack_opt.texelsPerUnit = pack_gr.texelsPerUnit
        pack_opt.resolution = ctypes.c_uint32(pack_gr.resolution)
        pack_opt.bilinear = pack_gr.bilinear
        pack_opt.blockAlign = pack_gr.blockAlign
        pack_opt.bruteForce = pack_gr.bruteForce
        pack_opt.createImage = False
        pack_opt.rotateChartsToAxis = pack_gr.rotateChartsToAxis
        pack_opt.rotateCharts = pack_gr.rotateCharts

        # Data From Python
        b_data: DataFromPy = DataFromPy(
            mesh_decls_py_ptr,
            ctypes.c_uint32(len(mesh_decls_py)),
        )

        xatlas_data: DataToPy = None

        try:
            start_time = time.time()

            bxatlas.GenerateXAtlas.argtypes = (POINTER(DataFromPy), POINTER(ChartOptionsPy), POINTER(PackOptionsPy), c_bool)
            bxatlas.GenerateXAtlas.restype = POINTER(DataToPy)

            xatlas_data = bxatlas.GenerateXAtlas(b_data, byref(chart_opt), byref(pack_opt), self.pack_only)

            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time:.6f} seconds")

            xatlas_contents = xatlas_data.contents
            
        except Exception as e:
            print("No Data From XAtlas!")
            print(e)

            # Clear
            del xatlas_data
            del bxatlas
            del b_data
            del mesh_decls_py_ptr
            xatlas_data = None
            bxatlas = None
            b_data = None

            return {"CANCELLED"}

        mesh_decls_out = xatlas_contents.meshDeclOutPy

        for i in range(xatlas_contents.meshDeclOutPyCount):
            mesh_decl_out: MeshDeclOutPy = xatlas_contents.meshDeclOutPy[i]

            current_obj = final_objects[mesh_decl_out.meshID]
            
            np_new_uvs = np.ctypeslib.as_array(mesh_decl_out.vertexUvData, 
                                               shape=(len(current_obj.data.loops) * 2,))

            active_uv = current_obj.data.uv_layers.active

            if active_uv:
                active_uv.uv.foreach_set("vector", np_new_uvs)

            current_obj.data.update()

        # Clear
        del xatlas_data
        del bxatlas
        del b_data
        del mesh_decls_py_ptr
        xatlas_data = None
        bxatlas = None
        b_data = None

        return {"FINISHED"}


def GetMeshDecls(sel_objs: list, final_objects: list, mesh_decls_py: list):
    for obj in sel_objs:
        # obj.data.update()

        # Positions
        mesh_verts = np.empty(len(obj.data.vertices) * 3, dtype=np.float32)
        obj.data.vertices.foreach_get('co', mesh_verts)

        mesh_verts_num = len(mesh_verts)

        # PolyIndices
        # poly_indices = np.concatenate([np.array(poly.vertices, dtype=np.int32) for poly in active_obj.data.polygons])
        poly_indices = np.empty(len(obj.data.loop_triangles) * 3, dtype=np.uint32)
        obj.data.polygons.foreach_get("vertices", poly_indices)

        poly_indices_num = len(poly_indices)

        # Get Polygons Loop Start
        loops_total = np.empty(len(obj.data.polygons), dtype=np.uint32)
        obj.data.polygons.foreach_get("loop_total", loops_total)

        loops_total_num = len(loops_total)

        # Normals
        normals = None
        # normals = np.empty(len(obj.data.loops) * 3, dtype=np.float32)
        # obj.data.corner_normals.foreach_get("vector", normals)
        # normals = np.ctypeslib.as_ctypes(normals)

        # UVs
        uvs = None
        active_uv = obj.data.uv_layers.active

        if active_uv:
            # uvs = [uv.uv[:] for uv in active_uv]
            uvs = np.empty(len(obj.data.loops) * 2, dtype=np.float32)
            active_uv.uv.foreach_get("vector", uvs)
            print(uvs)
            uvs = np.ctypeslib.as_ctypes(uvs)

        mesh_decl_py = MeshDeclPy(
            np.ctypeslib.as_ctypes(mesh_verts),
            ctypes.c_uint32(mesh_verts_num),

            np.ctypeslib.as_ctypes(poly_indices),
            ctypes.c_uint32(poly_indices_num),

            np.ctypeslib.as_ctypes(loops_total),
            ctypes.c_uint32(loops_total_num),

            normals,
            uvs,
        )

        final_objects.append(obj)
        mesh_decls_py.append(mesh_decl_py)


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