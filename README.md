# Payload PCB

!TODO! PUT IMAGE HERE

## SUMMARY

The Payload PCB serves as an all-purpose control and interface board that contains the Raspberry Pi Pico (RP2040) designed to manage mission-critical sensors and electronics and communicate that information through its Micro USB connector to the LattePanda Sigma SBC.

## FEATURES

- Resettable PTC fuse and reverse voltage protection on +12V Molex Micro-Fit input.
- LTC2990 Quad I2C Voltage, Current, and Temperature Monitor,
- Traco TSR 2 Series +5V and +3V3 regulators: 96% eff, no heat sink required, built in filter caps, and short circuit protection.
- Outputs +12V, +5V, and +3V3 on Molex Micro-Fit.
- Status and error LEDs.
- Connections for both the Pico and an external device to CAN bus.
- 4x STEMMA QT / QWIIC connectors for COTS modules and peripherals.
- 2x custom expansion modules on two 6 pin 0.1" connectors each.
- 4x servo (PWM) outputs on Molex PicoBlades.
- 3x analog inputs on Molex Picoblades
- 2x digital outputs for relays.
- 2x digital inputs (active-low) for limit switches on manipulator linear rail.
- Micro USB port to connect to Seeeduino XIAO on manipulator.


## REPO

files
kicad 9
getting started


## DESIGN

schematic
layout
render of top
connector pinout
I2C mapping
firmware notes
known limitations

## CALCULATIONS

power budgeting
regulators
ptc fuse
trace width for power
trace width for impedance
adc voltage and bandwidth
