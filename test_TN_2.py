import numpy as np
import pickle

from parameters import Parameters
from mesh import Points_Circle_Mesh, Points_Square_Mesh, Station_Circle_Mesh
from channels import TBS_channels
from base_stations import Base_Stations, Base_Station, Base_Station_Sector
from terrestrial import Terrestrial_Communication
import user_selection 
import plot

with open('TerCom_circle_mesh.pkl', 'rb') as file:
    TerCom = pickle.load(file)

Points_Mesh = Points_Circle_Mesh()
points = Points_Mesh.get_mesh_points()

ground_users = []
for i, usr_pos in enumerate(points):
    ground_users.append(np.array([i,usr_pos[0], usr_pos[1]]))
ground_users = np.array(ground_users)

Base_stations = TerCom.bss
tbs = Base_stations.get_tbs_positions()

plot.plot_mesh_point_station(points, tbs)

ground_users, Haps_users, Null_points = user_selection.select_users()

plot.plot_RSRP_from_tbs(points, TerCom.g)
print(TerCom.g.shape)