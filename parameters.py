class Parameters:
    Nb_points = 1261
    Nb_HAPS_ant_ele = 16*16
    Nb_tbs = 48
    Nb_HAPS_users = 10
    Nb_null_points = 2
    Nb_ground_users = 30
    Mesh_type = 'square'
    Mesh_sample = 5 #km
    Mesh_rad = 100 #km
    TBS_generation_mode = 'circle_mesh'
    P_tr_HAPS = 120 #watts (whole array)
    P_tr_tbs = 20 #watts (whole array)
    TBS_max_gains = [P_tr_tbs]*Nb_tbs
    TBS_range = 5 #nb of closest tbs considered
    TBS_sector_size = 3