
import matplotlib.pyplot as plt
from math import log

def V(p, T):
    return 8.314 * T / p

def P(v, T):
    return 8.314 * T / v

def isotherm(v1, v2, T):
    return tuple(
        list(x) for x in zip(*[
            (v, P(v, T))
            for v in [((100-i) * v1 + i * v2) / 100. for i in range(101)]
        ])
    )

def P_adiabat(p1, t1, t2):
    return (t2 / t1 * p1 ** (2. / 7)) ** (7. / 2)

def V_adiabat(v1, p1, p2):
    return v1 * (p2 / p1) ** (-5. / 7)

def PV_adiabat(p1, t1, t2):
    p0, t0, v0 = p1, t1, V(p1, t1)
    for t in [((100-i) * t1 + i * t2) / 100. for i in range(101)]:
        p = P_adiabat(p0, t0, t)
        v = V_adiabat(v0, p0, p)
        yield v, p
        v0, p0, t0 = v, p, t

def adiabat(p1, t1, t2):
    return tuple(
        list(x) for x in zip(*list(PV_adiabat(p1, t1, t2)))
    )

p1, p2 = 100_000, 200_000   # Pascals
tc, th = 273, 373           # Kelvin

v1 = V(p1, tc)              # 0.02269722 m^3 ideal gas per mole
v2 = V(p2, tc)              # 0.01134861 m^3
p3 = P_adiabat(p2, tc, th)
v3 = V_adiabat(v2, p2, p3)
# p1 ** (2. / 7) = (t1 / t2) * p2 ** (2. / 7)
p4 = ((th / tc) * p1 ** (2. / 7)) ** (7. / 2)
v4 = V(p4, th)              # 0.03101122 m^3

c1 = isotherm(v1, v2, tc)   # isothermal compression
# c2 = [v2, v3], [p2, p2]     # isobaric expansion
c2 = adiabat(p2, tc, th)    # adiabatic compression
c3 = isotherm(v3, v4, th)   # isothermal expansion
# c4 = [v4, v1], [p1, p1]     # isobaric compression
c4 = adiabat(p4, th, tc)    # adiabatic expansion

c1 = [x*1000 for x in c1[0]], [x/1000. for x in c1[1]]
c2 = [x*1000 for x in c2[0]], [x/1000. for x in c2[1]]
c3 = [x*1000 for x in c3[0]], [x/1000. for x in c3[1]]
c4 = [x*1000 for x in c4[0]], [x/1000. for x in c4[1]]

w1 = 8.314 * tc * log(v1 / v2)          # isothermal compression work
w2 = (5. / 2) * (p3 * v3 - p2 * v2)     # adiabatic compression work
w_in = w1 + w2
w3 = 8.314 * th * log(v4 / v3)          # isothermal expansion work
w4 = (5. / 2) * (p4 * v4 - p1 * v1)     # adiabatic compression work
w_out = w3 + w4
w = w_out - w_in

efficiency = 100. * w / w3

plt.plot(*(
    c1 + ('blue',)
    + c2 + ('orange',)
    + c3 + ('red',)
    + c4 + ('green',)
))
plt.axis((4, 25, 50, 650))
plt.xlabel('Volume (L)')
plt.ylabel('Pressure (kPa)')
plt.title('Pressure - Volume (mole of ideal gas)')
plt.text(v1 * 1000, p1 / 1000. + 1, '1')
plt.text(v2 * 1000, p2 / 1000. + 1, '2')
plt.text(v3 * 1000, p3 / 1000. + 1, '3')
plt.text(v4 * 1000, p4 / 1000. + 1, '4')
plt.text(11, 130, r'$T_C = 0^{\circ} C$')
plt.text(11, 100, f'$Q_C = {round(w1, 2)}$ J')
plt.text(8, 450, r'$T_H = 100^{\circ} C$')
plt.text(8, 420, f'$Q_H = {round(w3, 2)}$ J')
plt.text(5, 250, f'$W_{{IN}} = {round(w_in, 2)}$ J')
plt.text(13, 250, f'$W_{{OUT}} = {round(w_out, 2)}$ J')
plt.text(17, 510, f'β configuration')
plt.text(17, 480, f'$efficiency = {round(efficiency, 2)}$%')
plt.text(17, 450, f'$W = {round(w, 2)}$ J')
plt.show()

