# Brief: Mossgauge

Mossgauge is an invented open-hardware project. The maker writes:

Mossgauge is a desk air-quality monitor that people build from a kit. It measures CO2, temperature and humidity and shows them on a small e-paper screen. It has no app, no account and no cloud. A USB-C cable powers it, and one button cycles through the views.

I make three things: a circuit board, a 3D-printed case in two halves, and the firmware. The board is designed in KiCad, and a fabrication house assembles the surface-mount parts. Buyers solder the sensor header themselves, so every kit needs an assembly guide they can follow with a basic soldering iron. The case must print on a common hobby printer without supports. The firmware is written in Rust for an RP2040 microcontroller. A buyer updates it by dragging a file onto the USB drive the board shows.

The first batch is 200 kits. The parts for one kit must cost under 45 EUR. The CO2 reading must stay within 50 ppm plus 5 percent of a reference meter. The CO2 sensor is often out of stock, so I need a bill of materials that names a second source for every part.

The kit ships to the EU and the UK first, so it needs CE and UKCA marking and must meet RoHS. Everything is open source: CERN-OHL-S for the hardware and MIT for the firmware.

I work alone, with coding agents for the firmware and the documents. A friend reviews the board layout before each order.
