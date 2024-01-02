
# FAQ

I'm currently working on a scaled down model that fits on a desk. It has ~64 vertical cylinders housing rotating turbines and connected by various drains and vents.

Before I expand myself into the world of CAD and mechanical engineering, though, I think it prudent to share this.

> Where is that described? Maybe I'm misreading the diagrams?

I didn't want to go into implementation details, but I will try to diagram that today and get back to you.

> Are you including the inefficiencies in the water pumps, trompe, everything else? With 64 cylinders that much surface area is likely to have lots of friction

I'm hoping for significant friction.  A perfectly efficient engine could be hard to stop.  There is a lot of energy stored in a glass of ice water on a warm day.

> I could be mistaken, but I keep thinking this looks like "a sterling engine with extra steps", and none of those steps are going to improve efficiency? Or were you getting extra energy input that I'm missing?

A [Stirling cycle](https://en.wikipedia.org/wiki/Stirling_cycle) is (ΔT = 0, ΔQ < 0 | ΔT > 0, ΔQ > 0 | ΔT = 0, ΔQ > 0 | ΔT < 0, ΔQ < 0).  You could implement one with a (trompe @ $T_C$ -> copper loop @ $T_H$ -> airlift pump @ $T_H$ -> copper loop @ $T_C$) loop. The [alpha configuration](https://github.com/trstovall/engine/blob/main/pv_diagram_alpha.png) I documented is very similar. It is a (trompe (water @ $T_C$, air @ $T_H$) -> airlift pump @ (water @ $T_H$, air @ $T_C$)) loop, and it also follows the Stirling cycle, albeit isobaric instead of isochoric.  The isochoric and isobaric phases are inefficient, especially for air.

The [beta configuration](https://github.com/trstovall/engine/blob/main/pv_diagram_beta.png) combines the Stirling cycle with the [Brayton cycle](https://en.wikipedia.org/wiki/Brayton_cycle), (ΔT > 0, ΔQ = 0 | ΔT > 0, ΔQ > 0 | ΔT < 0, ΔQ = 0 | ΔT < 0, ΔQ < 0) cycle, to form the [Carnot cycle](https://en.wikipedia.org/wiki/Carnot_cycle), (ΔT = 0, ΔQ < 0 | ΔT > 0, ΔQ = 0 | ΔT = 0, ΔQ > 0 | ΔT < 0, ΔQ = 0).  My design is a (trompe (isothermal) @ $T_C$ -> compressor (isentropic) -> (isothermal) airlift pump @ $T_H$ -> expander (isentropic)) loop.

> do you have specific examples of the input and output forces? It's a heat delta? Or where are the mechanical inputs/outputs exactly?

The heat engine converts a heat delta into work.  Each parcel of the working gas is a heat sponge.  The sponge is sqeezed by the isothermal compression phase and expanded by the isothermal expansion phase.  The temperature differential is maintained by cooling the cold water and / or heating the hot water.  Mechanically, the pump and compressor do negative work while turbine and compressor do positive work.

> How much heat delta is needed to start seeing the effect?

Ideally none.  How much voltage is needed to drive electrons through a wire?  Reality is implementation specific.

> what level of energy conversion do you see possible through this system (now or in future designs)? Milliwatts, Watts, kilowatts, no limit?

There is no limit.

The [Pressure-Volume diagram](https://github.com/trstovall/engine/blob/main/pv_diagram_beta.png) illustrates the various calculations for each journey through the cycle by 1 mole of air starting at ($T_C$ = $0^{\circ}$C, 1 bar), goes to ($T_H$ = $100^{\circ}$C, 3 bar) and emits net output of 576.28 J.  If the system cycles 1 mole of air per second, then the power should be 576.28 W.

Ideal efficiency is $100\% * (1 - T_C/T_H) = 26.81\%$.  Of course, parasitic losses must be considered.  However, real world efficiencies over 20% should be expected for that configuration.

It should be straightforward to both scale down or scale up the system.
