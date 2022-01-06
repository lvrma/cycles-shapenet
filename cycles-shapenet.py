import bpy
from mathutils import Vector
import os
import glob
import subprocess

DB = 'C:\\Users\\lvrma\\shapenet'
OUT = 'C:\\Users\\lvrma\\output'

paths = glob.glob(DB + '/*/*/models')

for p in paths:
    obj_in = os.path.join(p, 'model_normalized.obj')

    out = p.replace(DB, OUT)
    out_gltf = os.path.join(out, 'model.gltf')
    out_obj = os.path.join(out, 'model_fixed.obj')

    cmd = 'obj2gltf -t -i ' + obj_in +' -o ' + out_gltf
    subprocess.run(cmd, shell=True, check=True, text=True)

    assets = [bpy.data.objects,
              bpy.data.meshes,
              bpy.data.textures,
              bpy.data.images,
              bpy.data.materials,
              bpy.data.collections];

    for dict in assets:
        for obj in dict:
            dict.remove(obj, do_unlink=True)

    scene = bpy.data.scenes[0]
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'

    bpy.ops.import_scene.gltf(filepath=out_gltf)

    part_names = []
    meshes = {}

    to_remove = []

	# delete identical meshes
    for idx, obj1 in enumerate(bpy.data.objects):
        for obj2 in bpy.data.objects[idx:]:
            if obj1 == obj2:
                continue

            mat1 = obj1.matrix_world
            mat2 = obj2.matrix_world

            vert1 = [mat1 @ v.co for v in obj1.data.vertices]
            vert2 = [mat2 @ v.co for v in obj2.data.vertices]

            if sorted(vert1) == sorted(vert2):
                for m in [obj1, obj2]:
                    nodes = m.active_material.node_tree.nodes
                    r, g, b, a = nodes['Principled BSDF'].inputs[0].default_value
                    if 'Image Texture' not in nodes and r >= 0.85 and g >= 0.85 and b >= 0.85:
                        if m not in to_remove:
                            to_remove.append(m)
                        break

    for obj in to_remove:
        bpy.data.objects.remove(obj)

    for obj1 in bpy.data.objects:
        if obj1.name not in part_names:
            meshes[obj1.name] = [obj1.name]

        for obj2 in bpy.data.objects:
            if obj1 is not obj2:
                if obj1.name in obj2.name and obj1.name in meshes:
                    meshes[obj1.name].append(obj2.name)
                    part_names.append(obj2.name)

    for mesh in meshes:
        tmp_vols = {}
        for m in meshes[mesh]:
            dims = bpy.data.objects[m].dimensions
            tmp_vols[str(m)] = float(dims[0] * dims[1] * dims[2])

        tmp_vols = sorted(tmp_vols.items(), key=lambda x:x[1])
        vols = {}
        for item in tmp_vols:
            vols[item[0]] = item[1]

    # sorted in smallest to largest volume
        meshes[mesh] = list(vols.keys())

    for mesh in meshes:
        tmp_mesh = meshes[mesh].copy()

    # filtering out white ones
        for m in tmp_mesh:
            nodes = bpy.data.objects[m].active_material.node_tree.nodes
            r, g, b, a = nodes['Principled BSDF'].inputs[0].default_value
            if 'Image Texture' not in nodes and r >= 0.85 and g >= 0.85 and b >= 0.85:
                bpy.data.objects[m].scale -= Vector((0.001, 0.001, 0.001))
                tmp_mesh.remove(m)

	# shifting to remove surface overlap, the smallest the portion, the more priority
        if len(tmp_mesh) >= 1:
            step = 0.0008 / len(tmp_mesh)
            scale_increase = 1.001
            for m in tmp_mesh:
                bpy.data.objects[m].scale = Vector((scale_increase, scale_increase, scale_increase))
                bpy.data.objects[m].select_set(True)
                bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
                bpy.data.objects[m].location *= Vector((scale_increase, scale_increase, scale_increase))

                scale_increase -= step

    for obj in bpy.data.objects:
        obj.select_set(True)

    bpy.ops.object.join()
    bpy.ops.export_scene.obj(filepath=out_obj)


paths = glob.glob(OUT + '/*/*/models')

for p in paths:
    out_gltf = os.path.join(p, 'model.gltf')
    os.remove(out_gltf)
