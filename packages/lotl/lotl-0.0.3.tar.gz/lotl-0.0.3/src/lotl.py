import ninjalib
import numpy as np
from stl import mesh

class lotl:
    def __init__(self,model):
        self.model = model

    def half(self):
        model = mesh.Mesh.from_file(self.model)
        triangles = model.vectors
        center = np.array(ninjalib.ninjalib(triangles.reshape(-1, 3)).center())
        left_mask = np.any(triangles[:, :, 0] < center[0], axis=1)
        right_mask = ~left_mask

        left_mesh = mesh.Mesh(np.zeros(np.sum(left_mask), dtype=mesh.Mesh.dtype))
        left_mesh.vectors[:] = triangles[left_mask]

        right_mesh = mesh.Mesh(np.zeros(np.sum(right_mask), dtype=mesh.Mesh.dtype))
        right_mesh.vectors[:] = triangles[right_mask]
        left_mesh.save("left.stl")
        right_mesh.save("right.stl")
        return True
