import bpy

import numpy as np

import os

import ctypes
from ctypes import *

import traceback
import time


class DataFromBlender(ctypes.Structure):
    _fields_ = [
        ("positions", POINTER(c_float)),
        ("positions_size", c_int32),

        ("indices", POINTER(c_int32)),
        ("indices_size", c_int32),

        ("loops_total", POINTER(c_int32)),
        ("loops_total_size", c_int32),

        ("normals", POINTER(c_float)),

        ("uvs", POINTER(c_float)),
        ]
    
class DataToBlender(ctypes.Structure):
    _fields_ = [
        ("uvs", POINTER(c_float)),
        ]

class BXA_OP_Test(bpy.types.Operator):
    bl_idname = "bxa.test"
    bl_label = "Test"
    bl_options = {'REGISTER', 'UNDO'}

    def load_xatlas(self):
        if os.name == "nt":  # Windows
            bxatlas = ctypes.CDLL("D:/Repositories/My_Repositories/addons/BXAtlas/BXAtlas_CTypes/build/Release/BXAtlas.dll")
        # else:  # Linux/macOS
        #     lib = ctypes.CDLL("./libexample.so")

        return bxatlas

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
        bxatlas = self.load_xatlas()

        b_data: DataFromBlender = DataFromBlender(
           np.ctypeslib.as_ctypes(mesh_verts),
           len(mesh_verts),

           np.ctypeslib.as_ctypes(poly_indices),
           len(poly_indices),

           np.ctypeslib.as_ctypes(np_loops_total),
           len(np_loops_total),

           np_normals,

           np_uvs,
        )

        bxatlas.RunXAtlas.argtypes = (POINTER(DataFromBlender), )
        bxatlas.RunXAtlas.restype = ctypes.POINTER(DataToBlender)

        try:
            start_time = time.time()

            xatlas_data: DataToBlender = bxatlas.RunXAtlas(b_data)

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
    BXA_OP_Test,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # bpy.types.Scene.tmp_properties = PointerProperty( name="Designer Utils Variables", type=TP_PG_Props, description="Designer Utils Properties" )
    

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    # del bpy.types.Scene.tmp_properties