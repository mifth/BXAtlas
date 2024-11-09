import ctypes
from ctypes import *

class ChartOptionsPy(ctypes.Structure):
    _fields_ = [
        ("maxChartArea", c_float),
        ("maxBoundaryLength", c_float),

        ("normalDeviationWeight", c_float),
        ("roundnessWeight", c_float),
        ("straightnessWeight", c_float),
        ("normalSeamWeight", c_float),
        ("textureSeamWeight", c_float),

        ("maxCost", c_float),
        ("maxIterations", c_uint32),

        ("useInputMeshUvs", c_bool),
        ("fixWinding", c_bool),
    ]

class PackOptionsPy(ctypes.Structure):
    _fields_ = [
	("maxChartSize", POINTER(c_uint32)),
	("padding", POINTER(c_uint32)),
	("texelsPerUnit", POINTER(c_bool)),
	("resolution", POINTER(c_uint32)),
	("bilinear", POINTER(c_bool)),
	("blockAlign", POINTER(c_bool)),
	("bruteForce", POINTER(c_bool)),
	# ("createImage", POINTER(c_bool)),
	("rotateChartsToAxis", POINTER(c_bool)),
	("rotateCharts", POINTER(c_bool)),
    ]

class DataFromPy(ctypes.Structure):
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
    
class DataToPy(ctypes.Structure):
    _fields_ = [
        ("uvs", POINTER(c_float)),
        ]