import numpy as np
import pickle

from parameters import Parameters
from mesh import Points_Circle_Mesh, Points_Square_Mesh, Station_Circle_Mesh
from channels import TBS_channels
from base_stations import Base_Stations, Base_Station, Base_Station_Sector
from terrestrial import Terrestrial_Communication
import user_selection 
import plot


Points_Mesh = Points_Circle_Mesh()
points = Points_Mesh.get_mesh_points()

ground_users = []
for i, usr_pos in enumerate(points):
    ground_users.append(np.array([i,usr_pos[0], usr_pos[1]]))
ground_users = np.array(ground_users)

Base_stations = Base_Stations(ground_users)
Base_stations.set_base_stations()
tbs = Base_stations.get_tbs_positions()

print(len(Base_stations.tbs_list[1].sector_list[1].sec_pot_users))
#plot.plot_mesh_point_station(points, tbs)

TerCom = Terrestrial_Communication(ground_users, Base_stations)
TerCom.set_tn()
with open('TerCom_circle_mesh_1ngbtbs.pkl','wb') as file:
    pickle.dump(TerCom, file)
plot.plot_RSRP_from_tbs(points, TerCom.g,save='RSRP_tbs')
