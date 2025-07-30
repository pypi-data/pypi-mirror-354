# scintiPulses

![scintiPulses logo](scintiPulses_logo.jpg)

**Simulate scintillation detector signals with photodetector effects, noise sources, and digitization modeling.**

`scintiPulses` is a Python package for simulating high-fidelity photodetector outputs from scintillation detectors. It models the full signal chain from energy deposition to digitized output, incorporating physical, electronic, and digitization effects.

---

## ✨ Features

- 📈 Realistic pulse shapes from energy depositions in scintillators  
- ⏱️ Time-dependent fluorescence (prompt and delayed components)  
- 🔬 Quantum shot noise and after-pulse simulation  
- 🌡️ Thermionic (dark) noise and Johnson-Nyquist noise  
- ⚙️ Analog filtering stages (RC preamplifier and CR fast amplifier)  
- 🧮 Digitization with low-pass filtering, quantization, and saturation

---

## 📦 Installation

Install via pip:

```bash
pip install scintiPulses
```

---

## 🚀 Usage Example

```python
import numpy as np
import matplotlib.pyplot as plt
from scintiPulses import scintiPulses

# Sample energy deposition (in keV)
Y = 100 * np.ones(1000)

# Run simulation
t, v0, v1, v2, v3, v4, v5, v6, v7, v8, y0, y1 = scintiPulses(
    Y,
    tN=20e-6,
    arrival_times=False,
    fS=1e8,
    tau1=250e-9,
    tau2=2000e-9,
    p_delayed=0,
    lambda_=1e6,
    L=1,
    C1=1,
    sigma_C1=0,
    I=-1,
    tauS=10e-9,
    electronicNoise=False,
    sigmaRMS=0.00,
    afterPulses=False,
    pA=0.5,
    tauA=10e-6,
    sigmaA=1e-7,
    digitization=False,
    fc=4e7,
)

# Plot the final output signal
plt.plot(t, v8)
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.title("Simulated Scintillation Pulse")
plt.grid(True)
plt.show()
```

---

## ⚙️ Parameters

| Parameter         | Type        | Default Value | Description                                                  |
|------------------|-------------|----------------|--------------------------------------------------------------|
| `Y`              | array-like  | None           | Sample energy deposition (in keV)                            |
| `tN`             | float       | 20e-6          | Total simulation time (in seconds)                           |
| `arrival_times`  | bool        | False          | Flag to indicate if arrival times are provided               |
| `fS`             | float       | 1e8            | Sampling frequency (in Hz)                                   |
| `tau1`           | float       | 250e-9         | Decay time constant for prompt component (in seconds)        |
| `tau2`           | float       | 2000e-9        | Decay time constant for delayed component (in seconds)       |
| `p_delayed`      | float       | 0              | Probability of delayed component                             |
| `lambda_`        | float       | 1e6            | Rate parameter for Poisson process (in Hz)                   |
| `L`              | float       | 1              | Inductance (in Henry)                                        |
| `C1`             | float       | 1              | Capacitance (in Farad)                                       |
| `sigma_C1`       | float       | 0              | Standard deviation of capacitance (in Farad)                 |
| `I`              | float       | -1             | Current (in Ampere)                                          |
| `tauS`           | float       | 10e-9          | Decay time constant for scintillation (in seconds)           |
| `electronicNoise`| bool        | False          | Flag to indicate if electronic noise is included             |
| `sigmaRMS`       | float       | 0.00           | RMS value of electronic noise                                |
| `afterPulses`    | bool        | False          | Flag to indicate if after-pulses are included                |
| `pA`             | float       | 0.5            | Probability of after-pulse occurrence                        |
| `tauA`           | float       | 10e-6          | Decay time constant for after-pulse (in seconds)             |
| `sigmaA`         | float       | 1e-7           | Standard deviation of after-pulse (in seconds)               |
| `digitization`   | bool        | False          | Flag to indicate if digitization is included                 |
| `fc`             | float       | 4e7            | Cut-off frequency for low-pass filter (in Hz)                |

## ⚙️ Outputs:

- 📈 v0 - Idealized light emission
- 📈 v1 - Shot noise from quantized photons
- 📈 v2 - After-pulses added (Optional)
- 📈 v3 - Thermoionic dark noise (Optional)
- 📈 v4 - PMT voltage signal
- 📈 v5 - Thermal noise added (Optional)
- 📈 v6 - Post-RC filter (preamp) (Optional)
- 📈 v7 - Post-CR filter (fast amplifier) (Optional)
- 📈 v8 - Final digitized signal (Optional)
