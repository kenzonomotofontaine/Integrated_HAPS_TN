import numpy as np

from parameters import Parameters
from mesh import Points_Circle_Mesh, Points_Square_Mesh
import channels

if Parameters.Mesh_type == 'circle':
    Mesh = Points_Circle_Mesh()

elif Parameters.Mesh_type == 'square':
    Mesh = Points_Square_Mesh()

else:
    print("No mesh type specified!")

points = Mesh.get_mesh_points()
input = str([[points[i][0]*1000, points[i][1]*1000, 0] for i in range(len(points))])
output = channels.positions_from_python_to_matlab(input)
f = open("Channels_txt/copy_to_matlab.txt", "a")
f.write(output)
f.close()