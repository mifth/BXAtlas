# import bpy

# import xatlas
# import numpy as np


# import trimesh

# class BXA_OP_Test(bpy.types.Operator):
#     bl_idname = "bxa.test"
#     bl_label = "Test"
#     bl_options = {'REGISTER', 'UNDO'}

#     def execute(self, context):
#         # mesh: trimesh.Geometry = trimesh.load_mesh("D:/Projects/Test/Blender/box.obj")
#         # print(mesh.vertices)

#         active_obj: bpy.types.Object = context.active_object

#         # Get Verts
#         mesh_verts = np.zeros(len(active_obj.data.vertices) * 3, dtype=np.float64)
#         active_obj.data.vertices.foreach_get('co', mesh_verts)
#         mesh_verts.shape = (len(active_obj.data.vertices), 3)

#         poly_indeces = np.zeros(len(active_obj.data.loop_triangles) * 3, dtype=np.int32)
#         active_obj.data.loop_triangles.foreach_get('vertices', poly_indeces)
#         poly_indeces.shape = (len(active_obj.data.loop_triangles), 3)

#         poly_loops = np.zeros(len(active_obj.data.loop_triangles) * 3, dtype=np.int32)
#         active_obj.data.loop_triangles.foreach_get('loops', poly_loops)
#         poly_loops.shape = (len(active_obj.data.loop_triangles), 3)

#         mesh_normals = np.zeros(len(active_obj.data.vertices) * 3, dtype=np.float64)
#         active_obj.data.vertices.foreach_get('normal', mesh_normals)
#         mesh_normals.shape = (len(active_obj.data.vertices), 3)

#         atlas = xatlas.Atlas()
#         atlas.add_mesh(mesh_verts, poly_indeces, mesh_normals)

#         chart_options = xatlas.ChartOptions()
#         chart_options.normal_deviation_weight = 0.5
#         chart_options.roundness_weight = 0.5
#         chart_options.straightness_weight = 0.5
#         chart_options.normal_seam_weight = 0.5
#         chart_options.texture_seam_weight = 0.5
#         chart_options.max_cost = 0.5
#         chart_options.fix_winding = True

#         pack_options = xatlas.PackOptions()
#         pack_options.padding = 5
#         pack_options.create_image = False
        
#         atlas.generate(chart_options, pack_options, True)
        
#         xatlas_vmapping, xatlas_indices, xatlas_uvs = atlas[0]

#         active_uv = active_obj.data.uv_layers.active

#         if active_uv:
#             for i, poly_indices in enumerate(xatlas_indices):
#                 poly_loop_ids = poly_loops[i]

#                 for j in range(len(poly_loop_ids)):
#                     active_uv.data[poly_loop_ids[j]].uv = xatlas_uvs[poly_indices[j]]


#         # print(mesh_verts)
#         # print(poly_indeces)
#         # print(poly_loops)
#         # print(vmapping)
#         # print(xatlas_indices)
#         # print(xatlas_uvs)
#         # print("-----------------")

#         del atlas
#         del chart_options
#         del pack_options


#         # # print(len(mesh.vertices), len(mesh.faces))
#         # print(len(vmapping), len(indices), len(uvs))
#         # # print(mesh.vertices)
#         # # print(mesh.faces)
#         # print(vmapping)
#         # print(indices)
#         # print(uvs)

#         # del mesh

#         return {"FINISHED"}


# classes = (
#     BXA_OP_Test,
# )


# def register():
#     from bpy.utils import register_class
#     for cls in classes:
#         register_class(cls)

#     # bpy.types.Scene.tmp_properties = PointerProperty( name="Designer Utils Variables", type=TP_PG_Props, description="Designer Utils Properties" )
    

# def unregister():
#     from bpy.utils import unregister_class
#     for cls in reversed(classes):
#         unregister_class(cls)

#     # del bpy.types.Scene.tmp_properties