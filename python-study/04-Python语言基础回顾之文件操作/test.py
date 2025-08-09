from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.tri import Triangulation

# 绘制莫比乌斯带
# 由于它是一条二维带，因此需要两个内在维度。theta维度取值范围是0～2pi，宽度维度w取值范围是-1～1
theta = np.linspace(0, 2 * np.pi, 30)
w = np.linspace(-0.25, 0.25, 8)
w, theta = np.meshgrid(w, theta)
phi = 0.5 * theta
# x-y平面内的半径
r = 1 + w * np.cos(phi)

x = np.ravel(r * np.cos(theta))
y = np.ravel(r * np.sin(theta))
z = np.ravel(w * np.sin(phi))

# 要画出莫比乌斯带，还必须保证三角部分是正确的。最好的方法是首先用基本参数化方法定义三角部分，然后用Matplotlib将
# 这个三角剖分映射到莫比乌斯带的三维空间里

tri = Triangulation(np.ravel(w), np.ravel(theta))
ax = plt.axes(projection='3d')
ax.plot_trisurf(x, y, z, triangles=tri.triangles, cmap='viridis', linewidth=0.2)
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(-1, 1)
