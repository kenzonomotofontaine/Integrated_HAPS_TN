import numpy as np
import re

from parameters import Parameters

class HAPS_channels:
    def __init__(self) -> None:
        self.Nb_points = Parameters.Nb_points
        self.Nb_ant_ele = Parameters.Nb_HAPS_ant_ele
        self.Nb_tbs = Parameters.Nb_tbs

    def get_HAPS_channels_from_txt(self, filename):
        HAPS_channels_txt = open(filename,'r')
        HAPS_channels_txt = HAPS_channels_txt.read()
        HAPS_channels_txt = HAPS_channels_txt.replace("i", "j")
        HAPS_channels_txt = HAPS_channels_txt.replace(",", "")
        HAPS_channels_one_one = re.split(r'(?<=j)', HAPS_channels_txt)[:-1]
        HAPS_channels = np.array([complex(HAPS_channels_one_one[i]) for i  in range(len(HAPS_channels_one_one))]).reshape((self.Nb_points, self.Nb_ant_ele))
        #for usr in range(self.Nb_points):
            #for i in range(0,int(np.sqrt(self.Nb_ant_ele)),2):
                #print(i)
            #np.random.shuffle(HAPS_channels[usr])
        #np.random.shuffle(HAPS_channels)
        #        HAPS_channels[usr][i:int(np.sqrt(self.Nb_ant_ele))*(i+1)] = np.flip(HAPS_channels[usr][i:int(np.sqrt(self.Nb_ant_ele))*(i+1)])
        return HAPS_channels

def positions_from_python_to_matlab(input):
    output = input.replace("],", "]@")
    output = output.replace(",",";")
    output = output.replace("@", ",")
    return output



class TBS_channels:
    def __init__(self) -> None:
        self.Nb_points = Parameters.Nb_points
        self.Nb_tbs = Parameters.Nb_tbs

    def cost231hata(self, hb, hu, f, ph, pu, area):
        n = 0
        d = np.linalg.norm(ph-pu)
        ahMS = (1.1 * np.log10(f) - 0.7) * hu - (1.56 * np.log10(f) - 0.8)
        if area == 1: #medium sized city
            C = 0
        if area == 2: # metropolitain centres
            C = 3
        L50dB = 46.3 + 33.9 * np.log10(f) - 13.82 * np.log10(hb) - ahMS + (44.9 - 6.55 * np.log10(hb)) * np.log(d) + C
        C_h = 0.8 + (1.1*np.log10(f) - 0.7)*hu -1.56*np.log(f)
        L_u = 69.55 + 26.16*np.log10(f) -13.82*np.log10(hb) - C_h + (44.9 - 6.55*np.log10(hb))*np.log10(d) #urban
        L_su = L_u - 2*(np.log10(f/28))**2 -5.4 #suburban
        L_o = L_u - 4.78*(np.log10(f))**2 + 18.33*np.log10(f) -40.94  #open
        return 10**(-L_o/20)
        #return L50dB
    
    def get_cost231hata_pathloss_to_points(self, tbs, points):
        """tbs and points being the arrays of tbs and points locations."""
        pathloss_tbs = np.zeros([self.Nb_points, self.Nb_tbs], np.float64)
        for u in range(self.Nb_points):
            for h in range(len(tbs)):
                pathloss_tbs[u][h] = self.cost231hata(50,1,2400,tbs[h], points[u], 1) #+ 50*(rd.random()-0.5)
        return np.array(pathloss_tbs)