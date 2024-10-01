import numpy as np

from parameters import Parameters
from base_stations import Base_Stations
from channels import TBS_channels

class Terrestrial_Communication:
    def __init__(self, ground_users, base_stations: Base_Stations ) -> None:
        self.bss = base_stations
        self.g_users = ground_users
        self.channels = TBS_channels()
        self.Nb_points = Parameters.Nb_points
        self.Nb_tbs = Parameters.Nb_tbs
        self.Nb_sec = Parameters.TBS_sector_size
        self.radiat_ptn = np.zeros([self.Nb_points, self.Nb_tbs, self.Nb_sec])
        self.path_loss = np.zeros([self.Nb_points, self.Nb_tbs, self.Nb_sec])
        self.fading = np.zeros([self.Nb_points, self.Nb_tbs, self.Nb_sec], dtype=np.complex64)
        self.g = np.zeros([self.Nb_points, self.Nb_tbs, self.Nb_sec], dtype=np.complex64)

    def set_tn(self):
        list_bs = self.bss.tbs_list
        for bs_idx, bs in enumerate(list_bs):
            sec_list = bs.sector_list
            tilt = Parameters.TBS_elev_tilt
            azi_3db = Parameters.TBS_azi_3db
            elev_3db = Parameters.TBS_elev_3db
            sd_att = Parameters.TBS_side_att
            max_att = Parameters.TBS_max_att
            max_gain = Parameters.TBS_max_gain
            height = bs.h
            for sec_idx, sec in enumerate(sec_list):
                sec_usrs = sec.sec_pot_users
                usrs_dir = sec.pot_users_dir
                for usr_idx in range(len(sec_usrs)):
                    az = usrs_dir[usr_idx][0]
                    el = usrs_dir[usr_idx][1]
                    v_radiat = -min(12*((el+tilt)/elev_3db)**2, sd_att)
                    h_radiat = -min(12*(az/azi_3db)**2, max_att)
                    radiat = -min(-(v_radiat+h_radiat), max_att)
                    gain_db = max_gain + radiat + Parameters.user_gain
                    gain = 10**(gain_db/20)
                    self.radiat_ptn[int(sec_usrs[usr_idx][0]), bs_idx, sec_idx] = gain
                    self.path_loss[int(sec_usrs[usr_idx][0]), bs_idx, sec_idx] = self.channels.cost231hata(height*1000, Parameters.user_height, Parameters.subcarrier_freq, bs.xy, sec_usrs[usr_idx][1:3], 1)
                    print(self.channels.cost231hata(height*1000, Parameters.user_height, Parameters.subcarrier_freq, bs.xy, sec_usrs[usr_idx][1:3], 1))
        x = np.random.normal(0, 1, [self.Nb_points, self.Nb_tbs, self.Nb_sec])
        y = np.random.normal(0, 1, [self.Nb_points, self.Nb_tbs, self.Nb_sec])
        self.fading = (x + 1j * y) / np.sqrt(2)
        self.g = self.path_loss * self.radiat_ptn * self.fading


