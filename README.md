BXAtlas is an attempt to use XAtlas in Blender 4.1+.

Features:
- UVs generation works.
- Quads and NGons support is added. This pull request is applied.
- Fixes of a cross-product calculation. This pull request is applied.
- Fixes of PiecewiseParam. This pull request is applied.
- CTypes linked addon.

![image](https://github.com/user-attachments/assets/b94f33a1-146d-4ea1-8f35-27ef7f9af263)

Installation:
- Go to the BXAtlas_CTypes folder and compile C++ code. CMake/GCC. The BXAtlas dll/so file should be built at "BXAtlas_CTypes/build/Release/BXAtlas.dll"
- Copy the addon (the entire root folder) to Blender addons and enable the addon.
- Select an object in ObjectMode.
- Go to UV panel and press the Generate button.

Unfortunately, the project is finished to 50% because of having some issues with the XAtlas library itself.

Problems:
- AddUVMesh() breaks UVs.
- useInputMeshUVs variable breaks UVs.
