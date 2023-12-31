
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

p1, p2 = 100_000, 200_000     # Pascals
tc, th = 273, 373           # Kelvin

v1 = V(p1, tc)              # 0.02269722 m^3 ideal gas per mole
v2 = V(p2, tc)              # 0.01134861 m^3
v3 = V(p2, th)              # 0.01550561 m^3
v4 = V(p1, th)              # 0.03101122 m^3

c1 = isotherm(v1, v2, tc)   # isothermal compression
c2 = [v2, v3], [p2, p2]     # isobaric expansion
c3 = isotherm(v3, v4, th)   # isothermal expansion
c4 = [v4, v1], [p1, p1]     # isobaric compression

c1 = [x*1000 for x in c1[0]], [x/1000. for x in c1[1]]
c2 = [x*1000 for x in c2[0]], [x/1000. for x in c2[1]]
c3 = [x*1000 for x in c3[0]], [x/1000. for x in c3[1]]
c4 = [x*1000 for x in c4[0]], [x/1000. for x in c4[1]]

w_in = 8.314 * tc * log(v1 / v2)
w_out = 8.314 * th * log(v4 / v3)
q_h = 29.1 * (th - tc) + w_out
w = p2 * (v3 - v2) + w_out - p1 * (v4 - v1) - w_in

efficiency = 100. * w / (w_in + q_h)

plt.plot(*(
    c1 + ('blue',)
    + c2 + ('orange',)
    + c3 + ('red',)
    + c4 + ('green',)
))
plt.axis((10, 33, 80, 220))
plt.xlabel('Volume (L)')
plt.ylabel('Pressure (kPa)')
plt.title('Pressure - Volume (mole of ideal gas)')
plt.text(v1 * 1000., p1 / 1000. + 1, '1')
plt.text(v2 * 1000., p2 / 1000. + 1, '2')
plt.text(v3 * 1000., p2 / 1000. + 1, '3')
plt.text(v4 * 1000., p1 / 1000. + 1, '4')
plt.text(12, 140, r'$T_C = 0^{\circ} C$')
plt.text(12, 135, f'$W_C = {round(w_in, 2)}$ J')
plt.text(12, 130, f'$Q_C = {round(w_in, 2)}$ J?')
plt.text(25, 140, r'$T_H = 100^{\circ} C$')
plt.text(25, 135, f'$W_H = {round(w_out, 2)}$ J')
plt.text(25, 130, f'$Q_H = {round(q_h, 2)}$ J')
plt.text(25, 200, f'α configuration')
plt.text(25, 195, f'$W = {round(w, 2)}$ J')
plt.text(25, 190, f'$efficiency = {round(efficiency, 2)}$%')
plt.show()

