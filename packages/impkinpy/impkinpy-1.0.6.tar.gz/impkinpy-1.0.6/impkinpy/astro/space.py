import numpy as np 
import matplotlib.pyplot as plt

class Black_hole():
    def __init__(self):
        self.G = 6.67430e-11
        self.SB_const = 1.380649e-23
        self.proton_m = 1.6726e-27
    
    def black_hole(self, accretion_v: int | float, disk_r: int | float, hole_mass: int | float, H_He_Z_list: list[list[int]], **kwargs):
        t_list = []
        density_list = []
        vr_list = []
        r_list = []

        r_min = 3*(self.G*hole_mass/299792458**2)
        r = np.linspace(r_min, disk_r, 1000)

        Ah = 1
        Ahe = 4
        Az = 16

        sigma_H = H_He_Z_list[0][0]*(1+H_He_Z_list[0][1])/Ah
        sigma_He = H_He_Z_list[1][0]*(1+H_He_Z_list[1][1])/Ahe
        sigma_Z = H_He_Z_list[2][0]*(1+H_He_Z_list[2][1])/Az

        molecular_m = 1/(sigma_H+sigma_He+sigma_Z)
        alpha = 0

        for i in r:
            t = (3*self.G*hole_mass*accretion_v/(8*np.pi*self.SB_const*i**3))**(1/4)
            c_sound = np.sqrt(self.SB_const*t/(molecular_m*self.proton_m))
            angle_v = np.sqrt(self.G*hole_mass/i**3)
            disk_h = c_sound/angle_v
            if len(kwargs) == 0:
                    coeff = 0.3/disk_r
                    alpha += coeff
            else:
                for key, value in kwargs.items():
                    if key == "alpha":
                        alpha = value
                    if key == "viscosity":
                        viscosity = value
                        alpha = viscosity/(c_sound*disk_h)

            vK = np.sqrt(self.G*hole_mass/i)
            vr = -alpha*(disk_h/disk_r)**2*vK
            density = accretion_v/(4*np.pi*i*disk_h*abs(vr))

            r_list.append(i)
            density_list.append(density)
            vr_list.append(vr)
            t_list.append(t)

        return density_list, t_list, vr_list, r_list
    
    def plot_black_hole(self, func):
        density_list, t_list, vr_list, r_list = eval(func)
        plt.plot(r_list, density_list, "-r")
        plt.title("Density of disk on radius r from the black hole")
        plt.grid()
        plt.show()
        plt.plot(r_list, t_list, "-g")
        plt.title("Temperature of disk on radius r from the black hole")
        plt.grid()
        plt.show()
        plt.plot(r_list, vr_list, "-b")
        plt.title("Radial velocity of disk on radius r from the black hole")
        plt.grid()
        plt.show()




        
        


