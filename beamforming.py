import numpy as np
from parameters import Parameters


class HAPS_Beamforming:
    def __init__(self) -> None:
        pass

    def simple_zero_forcing_beamforming(self, HAPS_channels, HAPS_users):
        HAPS_users_channels = np.array(HAPS_channels[HAPS_users])
        N_HU = len(HAPS_users)
        print("The number of HAPS users is : ", N_HU)
        W_bf =  np.dot(self.herm_transpose(HAPS_users_channels), np.linalg.inv(np.dot(HAPS_users_channels, self.herm_transpose(HAPS_users_channels))))
        for usr in range(W_bf.shape[1]):
            w_vec = W_bf[:, usr]
            w_usr_sum = np.sqrt(abs(sum(w_vec*np.conjugate(w_vec))))
            W_bf[:,usr] = W_bf[:,usr] / w_usr_sum
        return W_bf

    def two_stage_zero_forcing_nullforming(self, HAPS_channels, HAPS_users, Null_points) :
        HAPS_users_channels = np.array(HAPS_channels[HAPS_users])
        Null_points_channels = np.array(HAPS_channels[Null_points])
        N_HU = len(HAPS_users)
        N_NP = len(Null_points)
        M = Parameters.Nb_HAPS_ant_ele - N_NP
        print("The number of HAPS users is : ", N_HU)
        print("The number of null points is : ", N_NP)
        U,S,Vh = np.linalg.svd(Null_points_channels)
        null_vectors = Vh[N_NP:]
        W_nf = self.herm_transpose(null_vectors[np.random.choice(len(null_vectors), size=M)])
        H_tilde = np.dot(HAPS_users_channels, W_nf)
        W_bf = np.dot(self.herm_transpose(H_tilde),np.linalg.inv(np.dot(H_tilde,self.herm_transpose(H_tilde))))
        W_zf = np.dot(W_nf, W_bf)
        #W_zf_amp = np.abs(W_zf)
        #W_zf_phase = np.angle(W_zf)
        #W_zf = np.exp(1j * W_zf_phase)/W_zf_amp
        for usr in range(W_zf.shape[1]):
            w_vec = W_zf[:, usr]
            w_usr_sum = np.sqrt(abs(sum(w_vec*np.conjugate(w_vec))))
            W_zf[:,usr] = W_zf[:,usr] / w_usr_sum
        return W_zf, W_nf

    def herm_transpose(self, matrix):
        return np.conjugate(matrix.T, dtype=np.complex64)
    
    #def get_RSRP
