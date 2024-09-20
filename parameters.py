class Parameters:
    subcarrier_freq = 2000 #MHz
    Nb_points = 1261
    Nb_HAPS_ant_ele = 16*16
    Nb_tbs = 48
<<<<<<< HEAD
    Nb_HAPS_users = 10
    Nb_null_points = 2
=======
    Nb_HAPS_users = 4
    Nb_null_points = 4
>>>>>>> 8e1498c (commit better beamforming update)
    Nb_ground_users = 30
    Mesh_type = 'circle'
    Mesh_sample = 5 #km
    Mesh_rad = 100 #km
    user_height = 1 #m
    user_gain = -3 #dBi
    TBS_generation_mode = 'circle_mesh'
    P_tr_HAPS = 120 #watts (whole array)
    P_tr_tbs = 20 #watts (whole array)
    TBS_max_gain = 12 #dBi
    TBS_range = 1 #nb of closest tbs considered
    TBS_sector_size = 3
    TBS_elev_tilt = 1.15 #degree
    TBS_azi_3db = 70 #degree
    TBS_elev_3db = 30 #degree
    TBS_side_att = 25 #dB
    TBS_max_att = 20 #dB
