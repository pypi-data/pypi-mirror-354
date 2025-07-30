import numpy as np
import matplotlib.pyplot as plt
import massfunc as mf
import astropy.units as u
from scipy.integrate import quad,quad_vec
from scipy.optimize import fsolve,root_scalar
import pandas as pd
from joblib import Parallel, delayed

cosmo = mf.SFRD()
m_H = (cosmo.mHu.to(u.M_sun)).value #M_sun
omega_b = cosmo.omegab
omega_m = cosmo.omegam
rhom = cosmo.rhom

class Barrier:

    def __init__(self,fesc=0.2, qion=20000.0,z_v=12.0,nrec=3,xi=100.0):
        self.fesc = fesc
        self.qion = qion
        self.z = z_v
        self.nrec = nrec
        self.xi = xi
        self.M_min = cosmo.M_vir(0.61,1e4,self.z)  # Minimum halo mass for ionization

    def Nion_diff(self,m,Mv,deltaR):
        fstar = cosmo.fstar(m)
        return self.fesc*self.qion/m_H *fstar* omega_b/omega_m *m*cosmo.dndmeps(m,Mv,deltaR,self.z)

    def Nion(self,Mv,delta_R):
        return quad_vec(self.Nion_diff, self.M_min, Mv, args=(Mv,delta_R),epsrel=1e-5)[0]

    def N_H(self,deltaR):
        return 1/m_H * omega_b/omega_m * rhom *(1+deltaR) 

    def N_xi_diff(self,M,Mv,deltaR):
        return self.xi/m_H * omega_b/omega_m *M*cosmo.dndmeps(M,Mv,deltaR,self.z)
    
    def N_xi(self,Mv,delta_R):
        return quad_vec(self.N_xi_diff, self.M_min, Mv, args=(Mv,delta_R),epsrel=1e-5)[0]
    
    def Calcul_deltaVM_EQ(self,deltaR,Mv):
        return self.Nion(Mv,deltaR) - (1+self.nrec)*self.N_H(deltaR)

    def Calcul_deltaVM(self,Mv):
        result = root_scalar(self.Calcul_deltaVM_EQ, args=(Mv,), bracket=[0.05, 1.7], method='bisect')
        return result.root

    def Calcul_deltaVM_Parallel(self,Mv_array):
        results = Parallel(n_jobs = -1)(delayed(self.Calcul_deltaVM)(Mv) for Mv in Mv_array)
        return np.array(results)
    
    def Calcul_deltaVM_Minihalo_EQ(self,deltaR,Mv):
        return self.Nion(Mv,deltaR) - (1+self.nrec)*self.N_H(deltaR) - self.N_xi(Mv,deltaR)
    
    def Calcul_deltaVM_Minihalo(self,Mv):
        result = root_scalar(self.Calcul_deltaVM_Minihalo_EQ, args=(Mv,), bracket=[0.05, 1.7], method='bisect')
        return result.root
    
    def Calcul_deltaVM_Minihalo_Parallel(self,Mv_array):
        results = Parallel(n_jobs = -1)(delayed(self.Calcul_deltaVM_Minihalo)(Mv) for Mv in Mv_array)
        return np.array(results)