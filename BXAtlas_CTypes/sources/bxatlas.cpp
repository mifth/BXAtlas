#include "bxatlas.h"

using namespace std;

#include <iostream>
#include <stdio.h>
#include <fstream>

#include <xatlas.h>

// using namespace xatlas;

namespace bxatlas {

#if defined(_WIN32)
#  define DLL00_EXPORT_API __declspec(dllexport)
#else
#  define DLL00_EXPORT_API
#endif


struct DataFromBlender {
    float* positions = nullptr;
    int positions_size;

    uint32_t* indices = nullptr;
    int indices_size;

    uint32_t* loops_total = nullptr;
    int loops_total_size;

    float* normals = nullptr;
    float* uvs = nullptr;
};

struct DataToBlender {
    float* uvs = nullptr;
};

#if defined(__cplusplus)
extern "C" {
#endif

DLL00_EXPORT_API DataToBlender* my_test(const DataFromBlender* dataFromBlender);

#if defined(__cplusplus)
}
#endif

void RecordError(const std::runtime_error& e)
{
    std::ofstream logfile("d:/error_log.txt", std::ios::app);
    logfile << "Runtime error: " << e.what() << std::endl;
    logfile.close();
}

void RecordError2(const std::exception& e)
{
    std::ofstream logfile("d:/error_log.txt", std::ios::app);
    logfile << "Runtime error: " << e.what() << std::endl;
    logfile.close();
}

DataToBlender* my_test(const DataFromBlender* dataFromBlender)
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
        printf("----- XAtlasCPP is Done! \n");
    }
    catch (const std::runtime_error& e) {
        std::cerr << "Runtime error: " << e.what() << std::endl;
        RecordError(e);
        printf(e.what());
    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        RecordError2(e);
        printf(e.what());
    }
    catch (...) {
        std::cerr << "An unknown error occurred." << std::endl;
        printf("An unknown error occurred \n");
    }

    Destroy(atlas);

    return toBlender;
}

}