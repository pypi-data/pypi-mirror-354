import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfinv
import massfunc as mf
from scipy.integrate import quad,quad_vec
from joblib import Parallel, delayed
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
h = cosmo.h
rhoc = cosmo.rhocrit.value
rhom = cosmo.rhom

class Bubble:
    def __init__(self,zeta=40,b0=1.0,b1=1.0):
        self.zeta = zeta
        self.b0 = b0
        self.b1 = b1

    def B(self,m,z):
        sig2 = cosmo.sigma2_interpolation(m)
        m_min = cosmo.virialm(Tvir=1e4,mu=0.61,z=z)
        sig2_min = cosmo.sigma2_interpolation(m_min)
        K_zeta = erfinv(1.0 - self.zeta**-1)
        b0 = cosmo.deltac(z) - np.sqrt(2)*K_zeta*np.sqrt(sig2_min)
        b1 = K_zeta/np.sqrt(2.0*sig2_min)
        return self.b0 + self.b1*sig2 , b0

    def MassFunc_Liner(self,m,z):
        sig2 =  cosmo.sigma2_interpolation(m)
        sigm = np.sqrt(sig2)
        b0 = self.B(m,z)[1]
        b = self.B(m,z)[0]
        dsig_dm = abs( cosmo.dsig2dm_interpolation(m) ) / (2.0*sigm)
        return np.sqrt(2.0/np.pi) * rhom/m *dsig_dm * b0/sig2 * np.exp( -b**2/(2*sig2) )


    def Radius_Lagrangian(self,m):
        return (3.0*m / (4.0*np.pi*rhom))**(1.0/3.0)

    def Valume_Bubble(self,m):
        return (3.0/4.0)*np.pi*self.Radius_Lagrangian(m)**3 

    def Q_bubble_diff(self,m,z):
        return self.MassFunc_Liner(m,z) * self.Valume_Bubble(m)

    def Q_bubble(self,m,z):
        m_min = self.zeta*cosmo.M_vir(Tvir=1e4,mu=0.61,z=z)
        mlist = np.logspace(np.log10(m_min),np.log10(m),12)
        ans = np.zeros_like(z,dtype=float)
        for i in range(len(mlist)-1):
            ans += quad_vec(self.Q_bubble_diff,mlist[i],mlist[i+1],args=(z,),epsrel=1e-5)[0]
        return ans

    def QVdndlnr(self,m,z):
        Q_bar = self.Q_bubble(1e18,z)
        return Q_bar**-1 *3*m**2 /rhom *self.MassFunc_Liner(m,z)

class Barrier:

    def __init__(self,fesc=0.2, qion=20000.0,z_v=12.0,nrec=3,xi=100.0):
        self.fesc = fesc
        self.qion = qion
        self.z = z_v
        self.nrec = nrec
        self.xi = xi

    # def delta_L(self,deltar):
    #     return (1.68647 - 1.35/(1 + deltar)**(2/3) - 1.12431/(1 + deltar)**(1/2) + 0.78785/(1 + deltar)**(0.58661)) / cosmo.Dz(self.z)

    def dndm(self,M,Mv,deltav):
        sig1 = cosmo.sigma2_interpolation(M)-cosmo.sigma2_interpolation(Mv)
        del1 = cosmo.deltac(self.z) - deltav
        return Mv/M /np.sqrt(2*np.pi) * abs(cosmo.dsig2dm_interpolation(M))*del1/sig1**(3/2) * np.exp(-del1**2/(2*sig1))

    def Nion_diff(self,m,Mv,deltaR):
        fstar = cosmo.fstar(m)
        # fstar = 0.05
        return self.fesc*self.qion/m_H *fstar* omega_b/omega_m *m*self.dndm(m,Mv,deltaR)

    def Nion(self,Mv,delta_R):
        m_min = cosmo.M_vir(0.61,1e4,self.z)
        m_slice = np.linspace(m_min, Mv, 12)
        ans = np.zeros_like(delta_R)
        for i in range(len(m_slice)-1):
            ans += quad_vec(self.Nion_diff, m_slice[i],m_slice[i+1], args=(Mv,delta_R,))[0]
        return ans

    def N_H(self,deltaR):
        return 1/m_H * omega_b/omega_m * rhom *(1+cosmo.delta_L(deltaR,self.z)) 

    def Calcul_deltaVM_EQ(self,deltaR,Mv):
        return self.Nion(Mv,deltaR) - (1+self.nrec)*self.N_H(deltaR)

    def Calcul_deltaVM(self,Mv):
        result = root_scalar(self.Calcul_deltaVM_EQ, args=(Mv,), bracket=[0.05, 1.7], method='bisect')
        return result.root

    def Calcul_deltaVM_Parallel(self,Mv_array):
        results = Parallel(n_jobs = -1)(delayed(self.Calcul_deltaVM)(Mv) for Mv in Mv_array)
        return np.array(results)
    
    def N_xi_diff(self,M,Mv,deltaR):
        return self.xi/m_H * omega_b/omega_m *M*cosmo.dndmeps(M,Mv,deltaR,self.z)
    
    def N_xi(self,Mv,delta_R):
        m_min = cosmo.M_vir(0.61,1e4,self.z)
        m_slice = np.linspace(m_min, Mv, 12)
        ans = np.zeros_like(delta_R)
        for i in range(len(m_slice)-1):
            ans += quad_vec(self.N_xi_diff, m_slice[i],m_slice[i+1], args=(Mv,delta_R))[0]
        return ans
    
    def Calcul_deltaVM_Minihalo_EQ(self,deltaR,Mv):
        return self.Nion(Mv,deltaR) - (1+self.nrec)*self.N_H(deltaR) - self.N_xi(Mv,deltaR)
    
    def Calcul_deltaVM_Minihalo(self,Mv):
        result = root_scalar(self.Calcul_deltaVM_Minihalo_EQ, args=(Mv,), bracket=[0.05, 1.7], method='bisect')
        return result.root
    
    def Calcul_deltaVM_Minihalo_Parallel(self,Mv_array):
        results = Parallel(n_jobs = -1)(delayed(self.Calcul_deltaVM_Minihalo)(Mv) for Mv in Mv_array)
        return np.array(results)


    
    

if __name__ == "__main__":
    bbl = Bubble(zeta=30)
    bar = Barrier(fesc=0.2, qion=20000.0, z_v=12.0, nrec=3, xi=100.0)
    print(bar.Nion(1e16, 0.1))
    # zs = np.linspace(6,12,1000)
    # Qff = Parallel(n_jobs=-1)(delayed(bbl.Q_bubble)(1e16,z) for z in zs)
    # # Qff = np.array([bbl.Q_bubble(1e16,z) for z in zs])
    # pd.DataFrame({'z':zs,'Qff':Qff}).to_csv('Qff_cpu.csv',index=False)
    print(bbl.Q_bubble(1e16,16))