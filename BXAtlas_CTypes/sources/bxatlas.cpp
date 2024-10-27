#include "bxatlas.h"

using namespace std;

#include <iostream>
#include <stdio.h>

#include <xatlas.h>

// using namespace xatlas;

namespace bxatlas {

#if defined(_WIN32)
#  define DLL00_EXPORT_API __declspec(dllexport)
#else
#  define DLL00_EXPORT_API
#endif


extern "C" {

    struct DataFromBlender {
        float* positions = nullptr;
        int positions_size;

        int* indices = nullptr;
        int indices_size;

        uint8_t* loops_total = nullptr;
        int loops_total_size;

        float* normals = nullptr;
        float* uvs = nullptr;
    };

    struct DataToBlender {
        float* uvs = nullptr;
    };

    DLL00_EXPORT_API DataToBlender* my_test(const DataFromBlender* dataFromBlender)
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
        
		meshDecl.indexCount = dataFromBlender->indices_size;
		meshDecl.indexData = dataFromBlender->indices;
		meshDecl.indexFormat = xatlas::IndexFormat::UInt32;

        meshDecl.faceVertexCount = dataFromBlender->loops_total;
        meshDecl.faceCount = dataFromBlender->loops_total_size;

        xatlas::ChartOptions chartOptions = xatlas::ChartOptions();
        // chartOptions.useInputMeshUvs = true;
        xatlas::PackOptions packOptions = xatlas::PackOptions();

        try {
            xatlas::AddMeshError meshError = xatlas::AddMesh(atlas, meshDecl);

            if (meshError != xatlas::AddMeshError::Success) {
                // printf("\rError: %s\n", xatlas::StringForEnum(meshError));
            }

            xatlas::Generate(atlas, chartOptions, packOptions);
        }
        catch (const std::runtime_error& e) {
            std::cerr << "Runtime error: " << e.what() << std::endl;
            printf(e.what());
        }
        catch (const std::exception& e) {
            std::cerr << "Error: " << e.what() << std::endl;
            printf(e.what());
        }
        catch (...) {
            std::cerr << "An unknown error occurred." << std::endl;
            printf("An unknown error occurred");
        }

        // To Blender Struct
        DataToBlender* toBlender = new DataToBlender();

		for (uint32_t i = 0; i < atlas->meshCount; i++) 
        {
			const xatlas::Mesh& mesh = atlas->meshes[i];

            // printf("loops_total_size, indices_size, positions_size: %i, %i, %i\n" , 
            // dataFromBlender->loops_total_size, dataFromBlender->indices_size, dataFromBlender->positions_size);

            // printf("IndexCount, VertCount, MeshesCount, ChartsCount, loops_total_size: %i, %i, %i  %i, %i\n" , mesh.indexCount, mesh.vertexCount, 
            // atlas->meshCount, mesh.chartCount, dataFromBlender->loops_total_size);

            // To Blender UVs
            toBlender->uvs = new float[mesh.indexCount * 2];

            // printf("\rXxxx: %i  %i\n", mesh.vertexCount, mesh.indexCount);
            
            for (uint32_t j = 0; j < mesh.indexCount; j++)
            {
                // printf("j RequestedVertex: %i %i\n" , j ,mesh.indexArray[j]);
                // printf("IndexItem: %i\n" , mesh.indexArray[j]);

                const xatlas::Vertex &vert = mesh.vertexArray[mesh.indexArray[j]];

                toBlender->uvs[j * 2] = vert.uv[0] / atlas->width;
                toBlender->uvs[j * 2 + 1] = vert.uv[1] / atlas->height;

                // printf("\rError: %f %f\n", vert.uv[0], vert.uv[1]);
            }
        }

        Destroy(atlas);

        return toBlender;
    }

}

}