import math
G=6.67430e-11; C=299792458.0; HBAR=1.054571817e-34
L=1.0e-40; RHO_CEIL=5.155e96*((1.616255e-35/L)**3); RHO0=1.0e-24
K=1.8734; GSTAR=1.2e-10; COUP=(K/RHO0)/(C*L)
M=1.0e10*1.98847e30
for r in (1e17, 1e20, 1e24):
    g=G*M/r**2
    rho=min(RHO0*(1+g/K),RHO_CEIL)
    e=(HBAR*C/L**4)/(RHO_CEIL*C**2)*(rho/RHO0)
    corr=sum(((-1)**(n+1))*e**n/math.factorial(n) for n in range(1,5))
    mult=1+COUP*corr
    print(f"r={r:.0e} g={g:.3e} accel_frac={g/(GSTAR+g):.3e} eps={e:.3e} corr={corr:.3e} mult={mult:.3e}")
