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
	("maxChartSize", c_uint32),
	("padding", c_uint32),
	("texelsPerUnit", c_float),
	("resolution", c_uint32),
	("bilinear", c_bool),
	("blockAlign", c_bool),
	("bruteForce", c_bool),
	("createImage", c_bool),
	("rotateChartsToAxis", c_bool),
	("rotateCharts", c_bool),
    ]

    _defaults_ = { "createImage" : False,
    }

class MeshDeclPy(ctypes.Structure):
    _fields_ = [
        ("vertexPositionData", POINTER(c_float)),
        ("vertexCount", c_uint32),

        ("indexData", POINTER(c_uint32)),
        ("indexCount", c_uint32),

        ("faceVertexCount", POINTER(c_uint32)),
        ("faceCount", c_uint32),

        ("vertexNormalData", POINTER(c_float)),

        ("vertexUvData", POINTER(c_float)),
        ]
    
class DataFromPy(ctypes.Structure):
    _fields_ = [
        ("meshesDeclPy", POINTER(MeshDeclPy)),
        ("meshesDeclPyCount", c_uint32),
        ]

class MeshDeclOutPy(ctypes.Structure):
    _fields_ = [
        ("vertexUvData", POINTER(c_float)),
        ("vertexUvDataCount", c_uint32),
        ("meshID", c_uint32),
        ]

class DataToPy(ctypes.Structure):
    _fields_ = [
        ("meshDeclOutPy", POINTER(MeshDeclOutPy)),
        ("meshDeclOutPyCount", c_uint32),
        ]