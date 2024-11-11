#include "bxatlas.h"

using namespace std;

#include <iostream>
#include <stdio.h>
#include <fstream>

#include <xatlas.h>

#include <cmath>
#include <vector>


namespace bxatlas {

#if defined(_WIN32)
#  define DLL00_EXPORT_API __declspec(dllexport)
#else
#  define DLL00_EXPORT_API
#endif

typedef struct ChartOptionsPy {
	float maxChartArea;
	float maxBoundaryLength;
	float normalDeviationWeight;
	float roundnessWeight;
	float straightnessWeight;
	float normalSeamWeight;
	float textureSeamWeight;
	float maxCost;
	uint32_t maxIterations;
	bool useInputMeshUvs;
	bool fixWinding;
}
ChartOptionsPy;

typedef struct PackOptionsPy {
	uint32_t maxChartSize;
	uint32_t padding;
	float texelsPerUnit;
	uint32_t resolution;
	bool bilinear;
	bool blockAlign;
	bool bruteForce;
	bool createImage;
	bool rotateChartsToAxis;
	bool rotateCharts;
}
PackOptionsPy;

typedef struct MeshDeclPy {
	float* vertexPositionData = nullptr;
	uint32_t vertexCount;

	uint32_t* indexData = nullptr;
	uint32_t indexCount;

	uint32_t* faceVertexCount = nullptr;
	uint32_t faceCount;

	float* vertexNormalData = nullptr;

	float* vertexUvData = nullptr;
} MeshDeclPy;

typedef struct DataFromPy {
	MeshDeclPy* meshesDeclPy = nullptr;
	uint32_t meshesDeclPyCount;
} DataFromPy;

typedef struct MeshDeclOutPy {
	float* vertexUvData = nullptr;
	uint32_t vertexUvDataCount;
	uint32_t meshID;
} MeshDeclOutPy;

typedef struct DataToPy {
	MeshDeclOutPy* meshDeclOutPy = nullptr;
	uint32_t meshDeclOutPyCount;
} DataToPy;

#if defined(__cplusplus)
extern "C" {
#endif

DLL00_EXPORT_API DataToPy* GenerateXAtlas(const DataFromPy* dataFromBlender, const ChartOptionsPy& chartOptionsPy,
	const PackOptionsPy& packOptionsPy, bool pack_only);
	DLL00_EXPORT_API void DeleteDataToPy(DataToPy* dataToPy);

#if defined(__cplusplus)
}
#endif

DataToPy* GenerateXAtlas(const DataFromPy* dataFromBlender, const ChartOptionsPy& chartOptionsPy,
	const PackOptionsPy& packOptionsPy, bool pack_only)
{
	xatlas::Atlas* atlas = xatlas::Create();

	xatlas::ChartOptions chartOptions = xatlas::ChartOptions();
	chartOptions.maxChartArea = chartOptionsPy.maxChartArea;
	chartOptions.maxBoundaryLength = chartOptionsPy.maxBoundaryLength;
	chartOptions.normalDeviationWeight = chartOptionsPy.normalDeviationWeight;
	chartOptions.roundnessWeight = chartOptionsPy.roundnessWeight;
	chartOptions.straightnessWeight = chartOptionsPy.straightnessWeight;
	chartOptions.normalSeamWeight = chartOptionsPy.normalSeamWeight;
	chartOptions.textureSeamWeight = chartOptionsPy.textureSeamWeight;
	chartOptions.maxCost = chartOptionsPy.maxCost;
	chartOptions.maxIterations = chartOptionsPy.maxIterations;
	chartOptions.useInputMeshUvs = chartOptionsPy.useInputMeshUvs;
	chartOptions.fixWinding = chartOptionsPy.fixWinding;

	xatlas::PackOptions packOptions = xatlas::PackOptions();
	packOptions.maxChartSize = packOptionsPy.maxChartSize;
	packOptions.padding = packOptionsPy.padding;
	packOptions.texelsPerUnit = packOptionsPy.texelsPerUnit;
	packOptions.resolution = packOptionsPy.resolution;
	packOptions.bilinear = packOptionsPy.bilinear;
	packOptions.blockAlign = packOptionsPy.blockAlign;
	packOptions.bruteForce = packOptionsPy.bruteForce;
	packOptions.createImage = packOptionsPy.createImage;
	packOptions.rotateChartsToAxis = packOptionsPy.rotateChartsToAxis;
	packOptions.rotateCharts = packOptionsPy.rotateCharts;


	// To Python Struct
	DataToPy* dataToPy = new DataToPy();

	try {
		printf("----- XAtlasCPP has Started! \n");

		std::vector<uint32_t> parsedMeshesIDs;

		// Run Mesh Decl Py
		for (uint32_t i = 0; i < dataFromBlender->meshesDeclPyCount; i++)
		{
			const MeshDeclPy& meshDeclPy = dataFromBlender->meshesDeclPy[i];

			xatlas::AddMeshError meshError;

			if (pack_only)
			{
				if (!meshDeclPy.vertexUvData) 
				{
					continue;
				}

				xatlas::UvMeshDecl uvMeshDecl;
				uvMeshDecl.indexCount = meshDeclPy.indexCount;
				uvMeshDecl.indexData = meshDeclPy.indexData;
				uvMeshDecl.indexFormat = xatlas::IndexFormat::UInt32;

				uvMeshDecl.vertexCount = meshDeclPy.indexCount;
				uvMeshDecl.vertexUvData = meshDeclPy.vertexUvData;
				uvMeshDecl.vertexStride = sizeof(float) * 2;

				meshError = xatlas::AddUvMesh(atlas, uvMeshDecl);
			}
			else
			{
				xatlas::MeshDecl meshDecl;
				meshDecl.vertexCount = meshDeclPy.vertexCount;
				meshDecl.vertexPositionData = meshDeclPy.vertexPositionData;
				meshDecl.vertexPositionStride = sizeof(float) * 3;

				meshDecl.indexCount = meshDeclPy.indexCount;
				meshDecl.indexData = meshDeclPy.indexData;
				meshDecl.indexFormat = xatlas::IndexFormat::UInt32;

				meshDecl.faceVertexCount = meshDeclPy.faceVertexCount;
				meshDecl.faceCount = meshDeclPy.faceCount;

				if (meshDeclPy.vertexNormalData)
				{
					meshDecl.vertexNormalData = meshDeclPy.vertexNormalData;
					meshDecl.vertexNormalStride = sizeof(float) * 3;
				}

				if (meshDeclPy.vertexUvData)
				{
					meshDecl.vertexUvData = meshDeclPy.vertexUvData;
					meshDecl.vertexUvStride = sizeof(float) * 2;
				}

				meshError = xatlas::AddMesh(atlas, meshDecl);
			}

			if (meshError != xatlas::AddMeshError::Success)
			{
				printf("Error to add mesh: %i,  %s\n", i, xatlas::StringForEnum(meshError));
			}
			else
			{
				parsedMeshesIDs.push_back(i);
			}
		}

		printf("----- XAtlasCPP Meshes are Added! \n");

		xatlas::Generate(atlas, chartOptions, packOptions);

		printf("----- XAtlasCPP Atlas is Generated! \n");

		dataToPy->meshDeclOutPy = new MeshDeclOutPy[parsedMeshesIDs.size()];
		dataToPy->meshDeclOutPyCount = static_cast<uint32_t>(parsedMeshesIDs.size());

		for (uint32_t i = 0; i < atlas->meshCount; i++) 
		{
			uint32_t realID = parsedMeshesIDs[i];

			const xatlas::Mesh& currentMesh = atlas->meshes[i];

			const MeshDeclPy& currentMeshDecl = dataFromBlender->meshesDeclPy[realID];

			// new mesh decl out
			dataToPy->meshDeclOutPy[i].meshID = realID;
			dataToPy->meshDeclOutPy[i].vertexUvDataCount = static_cast<uint32_t>(currentMeshDecl.indexCount * 2);

			dataToPy->meshDeclOutPy[i].vertexUvData = new float[currentMeshDecl.indexCount * 2]();  // () - zero values are initialized

			// To Blender UVs
			for (uint32_t j = 0; j < currentMesh.indexCount; j++)
			{
				uint32_t currentIndexArray = currentMesh.indexArray[j];
				if (currentIndexArray < currentMesh.vertexCount && currentIndexArray >= 0)
				{
					const xatlas::Vertex *vert = &currentMesh.vertexArray[currentIndexArray];

					if (std::isfinite(vert->uv[0]) && std::isfinite(vert->uv[1]))
					{
						dataToPy->meshDeclOutPy[i].vertexUvData[j * 2] = vert->uv[0] / static_cast<float>(atlas->width);
						dataToPy->meshDeclOutPy[i].vertexUvData[j * 2 + 1] = vert->uv[1] / static_cast<float>(atlas->height);
					}
				}
			}
		}
		
		printf("----- XAtlasCPP is Done! \n");
	}
	catch (const std::runtime_error& e) {
		std::cerr << "Runtime error: " << e.what() << std::endl;
		DeleteDataToPy(dataToPy);
		xatlas::Destroy(atlas);
		return nullptr;
	}
	catch (const std::exception& e) {
		std::cerr << "Error: " << e.what() << std::endl;
		DeleteDataToPy(dataToPy);
		xatlas::Destroy(atlas);
		return nullptr;
	}
	catch (...) {
		std::cerr << "An unknown error occurred." << std::endl;
		DeleteDataToPy(dataToPy);
		xatlas::Destroy(atlas);
		return nullptr;
	}

	xatlas::Destroy(atlas);

	return dataToPy;
}

void DeleteDataToPy(DataToPy* dataToPy)
{
	if (dataToPy)
    {
        // Loop through each MeshDeclOutPy and delete vertexUvData
        for (uint32_t i = 0; i < dataToPy->meshDeclOutPyCount; ++i)
        {
            delete[] dataToPy->meshDeclOutPy[i].vertexUvData;
        }

        delete[] dataToPy->meshDeclOutPy;

		delete dataToPy;
		dataToPy = nullptr;

		printf("----- XAtlasCPP Data is Cleaned Up! \n");
	}
}

}