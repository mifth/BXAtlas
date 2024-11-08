#include "bxatlas.h"

using namespace std;

#include <iostream>
#include <stdio.h>
#include <fstream>

#include <xatlas.h>

#include <cmath>


namespace bxatlas {

#if defined(_WIN32)
#  define DLL00_EXPORT_API __declspec(dllexport)
#else
#  define DLL00_EXPORT_API
#endif

typedef struct DataFromBlender {
	float* positions = nullptr;
	int positions_size;

	uint32_t* indices = nullptr;
	int indices_size;

	uint32_t* loops_total = nullptr;
	int loops_total_size;

	float* normals = nullptr;

	float* uvs = nullptr;
} DataFromBlender;

typedef struct DataToBlender {
	float* uvs = nullptr;
} DataToBlender;

#if defined(__cplusplus)
extern "C" {
#endif

DLL00_EXPORT_API DataToBlender* RunXAtlas(const DataFromBlender* dataFromBlender);

#if defined(__cplusplus)
}
#endif

DataToBlender* RunXAtlas(const DataFromBlender* dataFromBlender)
{
	xatlas::Atlas* atlas = xatlas::Create();

	xatlas::MeshDecl meshDecl = xatlas::MeshDecl();
	meshDecl.vertexCount = dataFromBlender->positions_size;
	meshDecl.vertexPositionData = dataFromBlender->positions;
	meshDecl.vertexPositionStride = sizeof(float) * 3;

	if (dataFromBlender->normals) {
		meshDecl.vertexNormalData = dataFromBlender->normals;
		meshDecl.vertexNormalStride = sizeof(float) * 3;
	}

	if (dataFromBlender->uvs) {
		meshDecl.vertexUvData = dataFromBlender->uvs;
		meshDecl.vertexUvStride = sizeof(float) * 2;
	}
	
	meshDecl.indexFormat = xatlas::IndexFormat::UInt32;
	meshDecl.indexCount = dataFromBlender->indices_size;
	meshDecl.indexData = dataFromBlender->indices;

	meshDecl.faceVertexCount = dataFromBlender->loops_total;
	meshDecl.faceCount = dataFromBlender->loops_total_size;

	// To Blender Struct
	DataToBlender* toBlender = new DataToBlender();

	xatlas::ChartOptions chartOptions = xatlas::ChartOptions();
	// chartOptions.useInputMeshUvs = true;
	xatlas::PackOptions packOptions = xatlas::PackOptions();

	try {
		printf("----- XAtlasCPP has Started! \n");

		xatlas::AddMeshError meshError = xatlas::AddMesh(atlas, meshDecl);

		if (meshError != xatlas::AddMeshError::Success) {
			printf("\rError: %s\n", xatlas::StringForEnum(meshError));
			return toBlender;
		}

		printf("----- XAtlasCPP Meshes are Added! \n");

		xatlas::Generate(atlas, chartOptions, packOptions);

		printf("----- XAtlasCPP Atlas is Generated! \n");

		for (uint32_t i = 0; i < atlas->meshCount; i++) 
		{
			const xatlas::Mesh& mesh = atlas->meshes[i];

			// To Blender UVs
			const uint32_t indices_size_uint = static_cast<uint32_t>(dataFromBlender->indices_size);
			toBlender->uvs = new float[dataFromBlender->indices_size * 2];
			for (uint32_t j = 0; j < indices_size_uint; j++)
			{
				toBlender->uvs[j * 2] = 0.0f;
				toBlender->uvs[j * 2 + 1] = 0.0f;
			}
			for (uint32_t j = 0; j < mesh.indexCount; j++)
			{
				uint32_t currentIndexArray = mesh.indexArray[j];
				if (currentIndexArray < mesh.vertexCount && currentIndexArray >= 0) {
					const xatlas::Vertex *vert = &mesh.vertexArray[currentIndexArray];
					if (std::isfinite(vert->uv[0]) && std::isfinite(vert->uv[1])) {
						toBlender->uvs[j * 2] = vert->uv[0] / static_cast<float>(atlas->width);
						toBlender->uvs[j * 2 + 1] = vert->uv[1] / static_cast<float>(atlas->height);
					}
				}
			}
			// printf("Out IndexCount %i %i \n", mesh.indexCount, dataFromBlender->indices_size);
		}
		printf("----- XAtlasCPP is Done! \n");
	}
	catch (const std::runtime_error& e) {
		std::cerr << "Runtime error: " << e.what() << std::endl;
		delete toBlender;
		xatlas::Destroy(atlas);
		return nullptr;
	}
	catch (const std::exception& e) {
		std::cerr << "Error: " << e.what() << std::endl;
		delete toBlender;
		xatlas::Destroy(atlas);
		return nullptr;
	}
	catch (...) {
		std::cerr << "An unknown error occurred." << std::endl;
		delete toBlender;
		xatlas::Destroy(atlas);
		return nullptr;
	}

	xatlas::Destroy(atlas);

	return toBlender;
}

}