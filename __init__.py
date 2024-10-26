
import bpy

from . import bxatlas_base, ui


bl_info = {
        "name": "BXAtlas",
        "description": "BXAtlas",
        "author": "mifth",
        "version": (0, 1, 0),
        "blender": (3, 9, 0),
        "location": "3D Viewport",
        "warning": "",
        "wiki_url": "",
        "tracker_url": "",
        "category": "Tools"
            }


classes = (
    bxatlas_base,
    ui,
)


def register():
    for cls in classes:
        cls.register()


def unregister():
    for cls in classes:
        cls.unregister()


if __name__ == "__main__":
    register()



