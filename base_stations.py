from parameters import Parameters
from mesh import Station_Circle_Mesh, Station_Circle_Mesh_Poisson

import numpy as np

class Base_Stations:
    def __init__(self, ground_users) -> None:
        self.generation_mode = Parameters.TBS_generation_mode
        self.Nb_tbs = Parameters.Nb_tbs
        self.tbs_list = []
        self.max_gain = Parameters.TBS_max_gain
        self.sector_size = Parameters.TBS_sector_size
        self.ground_users = ground_users # is a np array of form [idx of user point, x, y]
        self.tbs_range = Parameters.TBS_range

    def set_base_stations_positions(self): 
        if self.generation_mode == 'circle_mesh':
            mesh = Station_Circle_Mesh()
            self.tbs_positions = mesh.get_mesh_stations() # 3D points
        elif self.generation_mode == 'circle_poisson':
            mesh = Station_Circle_Mesh_Poisson()
            self.tbs_positions = mesh.get_mesh_stations()
        self.Nb_tbs = mesh.Nb_points

    
    def set_base_stations(self):
        self.set_base_stations_positions()
        closest_tbs = np.zeros((self.ground_users.shape[0], int(self.tbs_range)))
        for usr in range(self.ground_users.shape[0]):
            distances_to_bs = np.linalg.norm(self.tbs_positions[:,:2].reshape(32,2) - self.ground_users[usr][1:], axis=1) # 2D distance
            closest_tbs[usr] = np.array(distances_to_bs.argsort()[:self.tbs_range])
        tbs_pot_users = [[] for _ in range(self.Nb_tbs)]
        for usr in range(closest_tbs.shape[0]):
            idx = closest_tbs[usr].astype(int)
            for i in idx:
                tbs_pot_users[i].append(self.ground_users[usr])
        for i in range(self.Nb_tbs):
            bs = Base_Station(self.tbs_positions[i,2], self.tbs_positions[i,0:2], self.max_gain, self.sector_size, tbs_pot_users[i])
            self.tbs_list.append(bs)
        
    def get_tbs_positions(self):
        return self.tbs_positions
        
    def update_pot_users(self):
        closest_tbs = np.zeros(self.ground_users.shape[0])
        for usr in range(self.ground_users.shape[0]):
            distances_to_bs = np.linalg.norm(self.tbs_positions[1:3] - self.ground_users[usr][1:]) # 2D distance
            closest_tbs[usr] = distances_to_bs.argsort()[:self.tbs_range]
        tbs_pot_users = [[] for _ in range(self.Nb_tbs)]
        for usr in range(closest_tbs.shape[0]):
            idx = closest_tbs[usr].astype(int)
            for i in idx:
                tbs_pot_users[i].append(self.ground_users[usr])
        for i, bs in enumerate(self.tbs_list):
            bs.update_bs_pot_users(tbs_pot_users[i])
            bs.update_sec_pot_users()
            


class Base_Station:
    def __init__(self, height, bs_xy, max_gain, sector_size, bs_pot_users: list) -> None:
        self.xy = bs_xy
        self.h = height
        self.max_gain = max_gain
        self.bs_pot_users = bs_pot_users
        self.sec_size = sector_size
        self.sector_list = []
        self.set_sectors()

    def set_sectors(self):
        dir_unit = 360 / self.sec_size
        user_azi_directions = self.get_user_azi_directions()
        user_elev_directions = self.get_user_elev_directions()
        for sec_idx in range(self.sec_size):
            dir_deg = -180+dir_unit*sec_idx
            sec_pot_users = []
            sec_pot_users_dir = []
            for i in range(user_azi_directions.shape[0]):
                if dir_deg - dir_unit/2 <= user_azi_directions[i] <= dir_deg + dir_unit/2 or 360+dir_deg - dir_unit/2 <= user_azi_directions[i] <= 360+dir_deg + dir_unit/2:
                    sec_pot_users.append(self.bs_pot_users[i])
                    sec_pot_users_dir.append((user_azi_directions[i] - dir_deg, user_elev_directions[i]))
            sector = Base_Station_Sector(dir_deg, dir_unit, sec_pot_users, sec_pot_users_dir)
            self.sector_list.append(sector)

    def get_user_azi_directions(self):
        return np.angle([(usr[1]-self.xy[0]) + (usr[2]-self.xy[1])*1j for usr in self.bs_pot_users], deg=True)
    
    def get_user_elev_directions(self):
        return 90 + np.angle([(((usr[1]-self.xy[0])**2 + (usr[2]-self.xy[1])**2)**0.5 -self.xy[0]) + (Parameters.user_height - self.h)*1j for usr in self.bs_pot_users], deg=True)

    def update_sec_pot_users(self):
        user_azi_directions = self.get_user_azi_directions()
        user_elev_directions = self.get_user_elev_directions()
        for sec in self.sector_list:
            sec_pot_users = []
            sec_pot_users_dir = []
            for i in range(user_azi_directions.shape[0]):
                if sec.az_dir_deg - sec.az_range/2 <= user_azi_directions[i] <= sec.az_dir_deg + sec.az_range/2 or 360+sec.az_dir_deg - sec.az_range/2 <= user_azi_directions[i] <= 360+sec.az_dir_deg + sec.az_range/2:
                    sec_pot_users.append(self.bs_pot_users[i])
                    sec_pot_users_dir.append((user_azi_directions[i] - sec.az_dir_deg, user_elev_directions[i]))
            sec.update_sec_pot_users(sec_pot_users, sec_pot_users_dir)

    def update_bs_pot_users(self, new_pot_users):
        self.bs_pot_users = new_pot_users



class Base_Station_Sector:
    def __init__(self, azimuth_dir_deg, azimuth_range, sec_pot_users: list, pot_users_dir) -> None:
        self.az_dir_deg = azimuth_dir_deg
        self.az_range = azimuth_range
        self.sec_pot_users = sec_pot_users
        self.pot_users_dir = pot_users_dir

    def update_sec_pot_users(self, new_pot_users, new_pot_users_dir):
        self.sec_pot_users = new_pot_users
        self.pot_users_dir = new_pot_users_dir