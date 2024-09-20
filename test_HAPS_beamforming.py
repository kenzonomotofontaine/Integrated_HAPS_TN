import numpy as np

from parameters import Parameters
from mesh import Points_Circle_Mesh, Points_Square_Mesh
from channels import HAPS_channels
from beamforming import HAPS_Beamforming
import user_selection 
import plot

Points_Mesh = Points_Circle_Mesh()
points = Points_Mesh.get_mesh_points()

HC = HAPS_channels()
H_channels = HC.get_HAPS_channels_from_txt("Channels_txt/channels_16ele_1261users.txt")

_, HAPS_users, Null_points = user_selection.select_users(H_user=[0], Null=[1,2,3,4,5,6])

H_Beam = HAPS_Beamforming()
W_zf, W_nf = H_Beam.two_stage_zero_forcing_nullforming(HAPS_channels=H_channels, HAPS_users=HAPS_users, Null_points=Null_points)
#W_zf = H_Beam.simple_zero_forcing_beamforming(H_channels, HAPS_users)
print(W_zf.shape)
plot.plot_weights(W_zf)
plot.plot_HAPS_user_null_selection(points, HAPS_users, Null_points)
plot.plot_HAPS_Beam_Pattern(W_zf)
plot.plot_received_signal_from_HAPS(W_zf, H_channels, points, HAPS_users, Null_points)
plot.plot_RSRP_from_HAPS(W_zf, H_channels, points, HAPS_users, Null_points)
