from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# https://stackoverflow.com/questions/30223161/how-to-increase-the-size-of-an-axis-stretch-in-a-3d-plot
def resize(ax: Axes3D, scale_x: float, scale_y: float, scale_z: float):
    scale_x = float(scale_x)
    scale_y = float(scale_y)
    scale_z = float(scale_z)

    scale=np.diag([scale_x, scale_y, scale_z, 1.0])
    scale=scale*(1.0/scale.max())
    scale[3,3]=1.0

    def short_proj():
        return np.dot(Axes3D.get_proj(ax), scale)

    ax.get_proj=short_proj