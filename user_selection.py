import numpy as np
import matplotlib as plt
import random as rd

from parameters import Parameters


def select_users(G_user=[], H_user=[], Null=[], plot=False):
    if G_user != []:
        G_users = G_user
    else:
        G_users = rd.sample(range(Parameters.Nb_points), Parameters.Nb_ground_users)
    if H_user != []:
        H_users = H_user
    else:
        H_users = rd.sample([i for i in range(Parameters.Nb_points) if i not in G_users], Parameters.Nb_HAPS_users)
    if Null != []:
        Null_points = Null
    else:
        Null_points = rd.sample([i for i in range(Parameters.Nb_points) if i not in H_users], Parameters.Nb_null_points)
    return G_users, H_users, Null_points