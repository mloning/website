---
title: "Electrical Engineering of EEG"
date: 2026-02-01T16:55:39+01:00
draft: true
---
## Introduction

I have recently worked more on EEG ([Electroencephalography](https://en.wikipedia.org/wiki/Electroencephalography)) sensing technology and EEG data.
EEG is a method to record the electrical activity of the brain.
It's typically non-invasive, with the EEG sensors being placed on head of the subject.

This requires electrodes and related hardware and electronics that is extremely senstive to pick up the faint electrical signals of the brain, filter out the electrical noise, and convert them into something that can by analysed.

The hardware involves a number of components:

- the EEG sensors, called electrodes
- differential amplifier, boosting the signals of interest while cancelling out the noise
- signal filters
- analog-to-digital converter (ADC)

## Electrical brain signals

- the brain's voltage comes from dipoles
- when thousands of neurons in one area fire together, they move enough ions to create a positive charge in one region and negative charge in another.
- the EEG electrode captures that shift in voltage as those ions react with the electrode material
- individual neurons don't have enough power to be seen from outside the skull, however, many neurons are structured in a way that makes their activity measurable

### Brain as a battery

- in electrical engineering and electrochemistry, a unit cell is the smallest functional building blocks of a system
- in a standard battery, we have a unit cell with a cathode (+) and an anode (-)
- in the brain, the pyramidal neuron is the unit cell
  - when the neuron is active, it moves ions (Na+,K+) across its membrane
  - this creates a separation of charge: the top of the neuron becomes negative and the bottom becomes positive
  - this is a Current Dipole, which is the fundamental "battery" component of the EEG signal
- a single neuron produces a voltage so small it's almost immeasurable
- neurons in the cortex are all lined up in the same direction (perpendicular to the surface)
- they act like batteries connected in parallel
- when thousands of them fire in synchrony, their currents add up and become measurable
- the brain tissue, cerebrospinal fluid, and blood are highly conductive (low resistance)
- the skull is a high-resistance barrier (insulator), it acts like a massive resistor which is why the signal drops from millivolts inside the brain to microvolts on the scalp
- most batteries are DC (Direct Current); the brain, however, is an AC source (Alternating Current).
  - neurons are constantly flipping their polarity or pulsing at specific frequencies (e.g. 8–12 Hz for Alpha waves)
  - If the brain were a steady DC battery, your EEG would just be a flat line; we only see a signal because the neurons are constantly charging and discharging
- TODO what are resistors and capacitors?
- a real battery has a fixed amount of chemical energy; the brain is rechargeable on a millisecond scale by the metabolic pumping of ions back across cell membranes

## Electrodes

- conductive, galvanic sensors requiring physical, conductive contact with signal source (also see contactless capacitative sensing)
- usually wet electrodes using a conductive gel but can also be dry
- act as transducers, converting physical energy into electrical, in this case, ionic current from the brain into electron current in the wire
- brain uses ions, charged particles, e.g. Na+, K+, Cl- for communication
- electrodes measure the flow of ions on the head and convert it into electron current in the wire via chemical reactions
- the chemical reactions at the electrode tip create its own inherent electrical fluctuations
- half-cell because you cannot have a flow of electricity with only one electrode
- the cell isn't complete until you connect that electrode through the amplifier to a second electrode (i.e. the reference)
- the voltage you measure is the difference between these two half-cells (i.e. half-cell potential)
- properties
  - sensitivity, how much electrical output is generated for physical input
  - stability (small inherent chemical offset and fluctuations)
- impedance, "resistance" between electrode and skin (contact quality)
- usually silver (Ag) or silver chloride (AgCl)
  - non polarizable
  - almost zero resistance
  - little inherent electrical offset and fluctuations, staying at constant voltage
- measure voltage
  - also known as (electrical) potential difference, electric pressure, or electric tension
  - the difference in electric potential between two points

- typical voltage scales
  - Power lines, 100K+ V
  - Wall outlet, 110–230 V
  - AA battery, 1.5 V
  - EEG brain signal, 0.00001-0.0001 V, i.e. 10–100 μV (micro volts)

## Connections

3 types of connections

- ground
- reference electrode
- electrode of interest

Without a ground connection, the amplifier's sensitive electronics can become overwhelmed by static electricity on your skin.
Without a reference, the amplifier has no way to subtract out the environmental noise.

## Impedance

- low impedance is critical because higher impedance makes it harder to measure brain signals
- measured in Ohm (Ω)
- should usually be below 5kΩ
- Ohm’s Law: V = IR where V is the voltage ("pressure" or "tension"), I the current and R the resistance
- the higher the current or resistance, the higher the voltage
- to find the resistance (impedance) R, we need to know the voltage (V) and the current (I)

## Differential amplifier and referencing

- body acts like an antenna for environmental electrical noise, e.g. 50 or 60Hz from power lines in the walls around us
- differential amplifier takes in two signals and subtracts them, subtracting out the signal that's common to both, called [common mode rejection](https://en.wikipedia.org/wiki/Differential_amplifier#Common_mode)
- noise is assumed to be the same in both signals, the reference and the electrode of interest, cancelling out the noise from the electrode and leaving unique brain signal at the electrode position
- ideally, same environmental noise but no brain signal
- ideally, reference electrode is as close to the electrode(s) of interest as possible while at the same time as far away from the brain (signal source of interest) as possible, e.g. ear lope or nose

## Operational amplifiers, gain and clipping

- since brain waves are so tiny (10–100μV), they are hard to captured and processed by a computer.
- the amplifier multiplies the signal until it is large enough to be processed digitally
- usually the signal is boosted by a factor of 1,000 to 100,000 (gain), moving it from the scale of microvolts (μV) to volts (V)
- voltage_out = voltage_in \* gain
- TODO amplifier stages (pre-amplifier, main amplifier, inherent noise)
- gain usually measured on a logarithmic scale in terms of decibels (dB)
- for example, a gain of 10 is 20dB, a gain of 1,000 is 60dB, a gain of 100,000 is 100dB
- every amplifier has a limit, usually the voltage of its own power supply (e.g. ±5V)
- if the amplifier is powered by 5V, it physically cannot produce a 6V signal; the 5V mark is called the "rail"
- if the gain is too high, the signal will hit the ceiling, this is called clipping
- dynamic range

## Analog-to-digital converter (ADC)

- The continuous brain signal is chopped up into digital numbers which can be processed by a computer.
- properties
  - sampling rate, typically between 250 and 1000 Hz (samples per second)
  - precision
  - TODO what's a typical digital precision?

## How to measure impedance

- can be measured by injecting a tiny, known signal into the electrode circuit (AC) at a specific frequency that won't interfere with the brain data
- measure the resulting voltage at the electrodes
- Using Ohm's Law, since the current (I) is known and the voltage (V) is measured, the system calculates the impedance (Z) using Z=I/V
- TODO why is the current known? what's the unit of current?
- TODO why use AC and not DC?

## Noise

- environmental
- physiological from body movements, e.g. blinks, eye movements, jaw movements

## Signal processing

- hardware or software to filter out unwanted frequencies
- high-pass filter to remove DC offset or slow drift
- low-pass filter to remove high-frequency components from muscle movements ([EMG](https://en.wikipedia.org/wiki/Electromyography))

Resources 
- Bioelectromagnetism: History, Foundations and Applications
- https://www.bem.fi
- Medical Instrumentation: Application and Design
