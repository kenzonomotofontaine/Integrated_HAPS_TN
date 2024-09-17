import numpy as np
import matplotlib.pyplot as plt

from parameters import Parameters
from mesh import Points_Circle_Mesh, Station_Circle_Mesh


def plot_mesh_point_station(points, tbs, save=''):
    x_coords_p, y_coords_p = zip(*points)
    x_coords_tbs, y_coords_tbs, z_coords_tbs = zip(*tbs)
    plt.figure(figsize=(8, 8))
    plt.scatter(x_coords_p, y_coords_p, c='blue', marker='o')
    plt.scatter(x_coords_tbs, y_coords_tbs, c='purple', marker='o')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(-110, 110)
    plt.ylim(-110, 110)
    plt.xlabel('Position $x$ [km]')
    plt.ylabel('Position $y$ [km]')
    plt.grid(True)
    plt.title('2D Radial Mesh Grid')
    if save != '':
        plt.savefig(save)
    plt.show()

def plot_tbs_pathloss(points, pathloss_tbs, save=''):
    x, y = zip(*points)
    x = np.array(x)
    y = np.array(y)
    fig= plt.figure(figsize=(8, 8))
    ax = plt.subplot()
    sc = plt.scatter(x, y, c=np.min(pathloss_tbs, axis=1), cmap='viridis', s=60)
    plt.colorbar(sc, ax=ax, label='Value')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(-110, 110)
    plt.ylim(-110, 110)
    plt.xlabel('Position $x$ [km]')
    plt.ylabel('Position $y$ [km]')
    plt.grid(True)
    plt.title('Pathloss in the Terrestrial Network')
    if save != '':
        plt.savefig(save)
    plt.show()

def plot_HAPS_user_null_selection(points, H_users, Null_points, save=''):
    x_coords, y_coords = zip(*points)
    plt.figure(figsize=(8, 8))
    plt.scatter([x_coords[i] for i in range(len(x_coords)) if i not in H_users], [y_coords[i] for i in range(len(y_coords)) if i not in H_users], c='blue', marker='o')
    plt.scatter([x_coords[i] for i in H_users], [y_coords[i] for i in H_users], c='red', marker='o')
    plt.scatter([x_coords[i] for i in Null_points], [y_coords[i] for i in Null_points], c='green', marker='o')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(-110, 110)
    plt.ylim(-110, 110)
    plt.xlabel('Position $x$ [km]')
    plt.ylabel('Position $y$ [km]')
    plt.grid(True)
    plt.title('HAPS users and HAPS null-points selection')
    if save != '':
        plt.savefig(save)
    plt.show()

def plot_HAPS_Beam_Pattern(W, user=-1, save=''):
    if user == -1:
        W_one = np.sum(W.transpose(), axis=0).reshape(int(np.sqrt(Parameters.Nb_HAPS_ant_ele)),int(np.sqrt(Parameters.Nb_HAPS_ant_ele)))
    else:
        W_one = W.transpose()[user].reshape(int(np.sqrt(Parameters.Nb_HAPS_ant_ele)),int(np.sqrt(Parameters.Nb_HAPS_ant_ele)))
    padded_function_output = np.pad(W_one, ((28, 28), (28, 28)), mode='constant', constant_values=0)
    fourier_transform = np.fft.fft2(padded_function_output)
    fourier_transform_shifted = np.fft.fftshift(fourier_transform)
    magnitude = np.abs(fourier_transform_shifted)
    magnitude /= np.max(magnitude)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    x = np.fft.fftshift(np.fft.fftfreq(magnitude.shape[1]))  # Frequency coordinates for x-axis
    y = np.fft.fftshift(np.fft.fftfreq(magnitude.shape[0]))  # Frequency coordinates for y-axis
    x, y = np.meshgrid(x, y)
    ax.plot_surface(x, y, magnitude, cmap='viridis')
    ax.set_xlabel('Frequency X')
    ax.set_ylabel('Frequency Y')
    ax.set_zlabel('Normalized Magnitude')
    ax.set_title('Fourier Transform')
    if save != '':
        plt.savefig(save)
    plt.show()

def plot_received_signal_from_HAPS(W: np.array, HAPS_channels, points, HAPS_users, Null_points, user=-1, save=''):
    if user == -1:
        W_one = np.sum(W, axis=1)
    else:
        W_one = W[:,user]
    Rec_Sig = np.dot(HAPS_channels, W_one)
    x, y = zip(*points)
    x = np.array(x)
    y = np.array(y)
    value = np.abs(np.array(Rec_Sig.real.flatten().tolist()))

    fig= plt.figure(figsize=(8, 8))
    ax = plt.subplot()
    sc = plt.scatter(x, y, c=value, cmap='viridis', s=60)
    plt.colorbar(sc, ax=ax, label='Value')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(-110, 110)
    plt.ylim(-110, 110)
    plt.xlabel('Position $x$ [km]')
    plt.ylabel('Position $y$ [km]')
    plt.grid(True)
    plt.title('Received Signal Amplitude for the same carrier frequency used')
    if save != '':
        plt.savefig(save)
    plt.show()
    print("Received Signal Amplitude at HAPS users : ", value[HAPS_users])
    print("Received Signal Amplitude at Null points : ", value[Null_points])


def plot_weights(W: np.array, save=''):
    N_ele = int(np.sqrt(W.shape[0]))
    N_even = N_ele/2
    d_e = 1/2
    antenna_elements = np.array([[(-N_even*d_e+d_e*(i+1/2) , -N_even*d_e+d_e*(j+1/2)) for j in range(N_ele)] for i in range(N_ele)])
    value = np.sum(np.abs(W), axis=1)

    fig= plt.figure(figsize=(8, 8))
    ax = plt.subplot()
    sc = plt.scatter([[antenna_elements[i][j][0] for i in range(N_ele)] for j in range(N_ele)], [[antenna_elements[i][j][1] for i in range(N_ele)] for j in range(N_ele)], c=value, cmap='viridis', s=60)
    plt.colorbar(sc, ax=ax, label='Value')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True)
    if save != '':
        plt.savefig(save)
    plt.show()

def plot_RSRP_from_HAPS(W: np.array, HAPS_channels, points, HAPS_users, Null_points, user=-1, save=''):
    if user == -1:
        W_one = np.sum(W, axis=1)
    else:
        W_one = W[:,user]
    Rec_Sig = np.dot(HAPS_channels, W_one)
    Sig_Pow = np.square(np.abs(Rec_Sig))*Parameters.P_tr_HAPS
    #Sig_Amp = np.abs(np.array(Rec_Sig.real.flatten().tolist()))
    RSRP_dbm = 10*np.log10(Sig_Pow*1000)
    
    x, y = zip(*points)
    x = np.array(x)
    y = np.array(y)
    value = RSRP_dbm

    fig= plt.figure(figsize=(8, 8))
    ax = plt.subplot()
    sc = plt.scatter(x, y, c=value, cmap='viridis', s=60)
    plt.colorbar(sc, ax=ax, label='Value')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(-110, 110)
    plt.ylim(-110, 110)
    plt.xlabel('Position $x$ [km]')
    plt.ylabel('Position $y$ [km]')
    plt.grid(True)
    plt.title('RSRP in dBm for each user')
    plt.savefig('rsrsp2')
    if save != '':
        plt.savefig(save)
    plt.show()
    print("Received Signal Amplitude at HAPS users : ", value[HAPS_users])
    print("Received Signal Amplitude at Null points : ", value[Null_points])

def plot_RSRP_from_tbs(points, users_gain, ground_users=range(Parameters.Nb_points), tbs=[], save=''):
    if tbs != []:
        users_gain = users_gain[:,tbs,:]
    x, y = zip(*points[ground_users])
    x = np.array(x)
    y = np.array(y)
    
    Rec_pow = np.max((np.square(np.absolute(users_gain[ground_users]))*Parameters.P_tr_tbs).reshape(len(ground_users),-1), axis=1)
    print(Rec_pow)
    print("RecPow",Rec_pow.shape, "lenground",len(ground_users) )
    RSRP_dBm = 10*np.log10(Rec_pow*1000)

    fig= plt.figure(figsize=(8, 8))
    ax = plt.subplot()
    sc = plt.scatter(x, y, c=RSRP_dBm, cmap='viridis', s=60)
    plt.colorbar(sc, ax=ax, label='RSRP (dBm)')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(-110, 110)
    plt.ylim(-110, 110)
    plt.xlabel('Position $x$ [km]')
    plt.ylabel('Position $y$ [km]')
    plt.grid(True)
    plt.title('RSRP in dBm in the Terrestrial Network')
    if save != '':
        plt.savefig(save)
    plt.show()