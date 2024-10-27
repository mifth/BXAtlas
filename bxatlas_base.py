import bpy

# import xatlas
import numpy as np

import os

import ctypes
from ctypes import *

import traceback

# import trimesh


class DataFromBlender(ctypes.Structure):
    _fields_ = [
        ("positions", POINTER(c_float)),
        ("positions_size", c_int32),

        ("indices", POINTER(c_int32)),
        ("indices_size", c_int32),

        ("loops_total", POINTER(c_ubyte)),
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
        # mesh: trimesh.Geometry = trimesh.load_mesh("D:/Projects/Test/Blender/box.obj")
        # print(mesh.vertices)

        active_obj: bpy.types.Object = context.active_object

        # Positions
        mesh_verts = np.zeros(len(active_obj.data.vertices) * 3, dtype=np.float32)
        active_obj.data.vertices.foreach_get('co', mesh_verts)
        # mesh_verts.shape = (len(active_obj.data.vertices), 3)
        print("mesh_verts: ", mesh_verts)

        # PolyIndices
        poly_indices = []
        for poly in active_obj.data.polygons:
            poly_indices += list(poly.vertices)

        poly_indices = np.ctypeslib.as_array(poly_indices, shape=(len(poly_indices),))

        # poly_indices = np.zeros(len(active_obj.data.loops), dtype=np.int32)
        # active_obj.data.polygons.foreach_get('vertices', poly_indices)
        print("poly_indices: ", poly_indices)

        # Get Polygons Loop Start
        np_loops_total = np.empty(len(active_obj.data.polygons), dtype=np.ubyte)
        active_obj.data.polygons.foreach_get("loop_total", np_loops_total)

        print("loops_total: ", np_loops_total)

        # Normals
        np_normals = np.empty(len(active_obj.data.loops) * 3, dtype=np.float32)
        active_obj.data.corner_normals.foreach_get("vector", np_normals)

        # UVs
        np_uvs = None
        active_uv = active_obj.data.uv_layers.active

        if active_uv:
            # uvs = [uv.uv[:] for uv in active_uv]
            np_uvs = np.empty(len(active_obj.data.loops) * 2, dtype=np.float32)
            active_uv.uv.foreach_get("vector", np_uvs)

        # Load XAtlas
        bxatlas = self.load_xatlas()

        b_data: DataFromBlender = DataFromBlender(
           np.ctypeslib.as_ctypes(mesh_verts),
           len(mesh_verts),

           np.ctypeslib.as_ctypes(poly_indices),
           len(poly_indices),

           np.ctypeslib.as_ctypes(np_loops_total),
           len(np_loops_total),

           np.ctypeslib.as_ctypes(np_normals),
           np.ctypeslib.as_ctypes(np_uvs),
        )

        bxatlas.my_test.argtypes = (POINTER(DataFromBlender), )
        bxatlas.my_test.restype = ctypes.POINTER(DataToBlender)

        xatlas_data: DataToBlender = bxatlas.my_test(b_data)
        xatlas_contents = xatlas_data.contents

        np_new_uvs = np.ctypeslib.as_array(xatlas_contents.uvs, shape=(len(active_obj.data.loops) * 2,))
        print("outArray Length:  ", len(np_new_uvs))
        print(np_new_uvs)

        if active_uv:
            active_uv.uv.foreach_set("vector", np_new_uvs)

        active_obj.data.update()

        # Clear
        del xatlas_data
        del bxatlas
        xatlas_data = None
        bxatlas = None

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