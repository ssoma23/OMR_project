# OMR Visual Stimulation System

GUI application for measuring **Optomotor Response (OMR)** in animals using drifting grating stimuli and the staircase method.

## Overview

This system presents square-wave grating stimuli on a secondary monitor and allows the experimenter to measure visual thresholds (contrast, spatial frequency, or speed) via an adaptive staircase procedure.

### Key Features

- Real-time control of contrast, spatial frequency, and grating speed
- Staircase method: stimulus difficulty adjusts based on Hit/Miss responses
- Automatic CSV data logging per session
- Gamma correction utility for monitor calibration
- 3D-printable hardware platform (STL files included)

## Hardware Requirements

| Component                                     | Specification                   |
| --------------------------------------------- | ------------------------------- |
| Laptop computer or desktop computer + monitor | For stimulus control            |
| 4 monitors                                    | For stimulus presentation       |
| HDMI splitter (4 out)                         | For duplicating stimulus window |

Worked with Windows 10/11. May work with Linux too.

3D-printable platform files are provided in [`3D model/`](3D%20model/).

## Installation

1. Install Anaconda/miniconda first

2. Create OMR environment
```bash
conda create -n omr python==3.10
```
> **Note:** Psychopy requires python 3.8/3.10 (7/23/2026)

3. Activate OMR environment
```bash
conda activate omr
```

4. Install modules
```bash
pip install -r requirements.txt
```
> **Note:** PsychoPy may require additional setup. See the [PsychoPy installation guide](https://www.psychopy.org/download.html).

## Configuration

### Connection
```bash
Computer
└── HDMI splitter
    ├── Monitor 1
    ├── Monitor 2
    ├── Monitor 3
    └── Monitor 4
```
Set multiple display mode to "extend"

Edit [`OMR/config.py`](OMR/config.py) before first use:
```python
MONITOR_RESOLUTION   = (1920, 1080) # pix
MONITOR_SIZE         = (45, 26.3)   # Physical size (cm)
MONITOR_DISTANCE     = 24           # Distance (cm) from monitor to animal
MONITOR_REFRESH_RATE = 60           # Hz
```
> **Note:** Monitors for stimulus presentation

### Gamma Correction

Run the gamma measurement utility to calibrate your monitor before experiments:
```bash
cd OMR

# measurement
python -c "import gamma_correction; gamma_correction.measure()"
```
Blank screen will appear. Measure the screen brightness (using photometer etc.) and input it in command prompt window.
Check minimum brightness (m), maximum brightness (M), and gamma value (gamma), and use them in the following command.
```bash
# evaluate
python -c "import gamma_correction; gamma_correction.evaluate(m, M, gamma)"
```
If the evaluation result is OK, you can update "MONITOR_GAMMA" in config.py.
'''python
MONITOR_GAMMA        = None
'''
> **Note:** If you encounter "OSError: The hardware look-up table function (GetDeviceGammaRamp) failed", you have to set the gamma value through the GPU setting, instead of config.py.

## Usage

```bash
cd OMR
python main.py
```
> **Tip:** If you want to use sinusoidal grating instead of square one, change "sqr" to "sin" in "stm = visual.GratingStim(win, size = 120, texRes = 512, tex = 'sqr')" (L44)
'''python
stm = visual.GratingStim(win, size = 120, texRes = 512, tex = 'sin')
'''

### GUI Overview

Top part (for instant preview and setting initial parameters)
| Control                 | Description                                         |
| ----------------------- | --------------------------------------------------- |
| Contrast (%)            | Stimulus contrast (0–100%)                          |
| Spatial frequency (c/d) | Grating finess in cycles per degree of visual angle |
| Speed (d/s)             | Grating drift speed in degrees per second           |
| Show/Hide               | Toggle stimulus visibility                          |
| Apply                   | Apply current parameter values to stimulus          |

Bottom part (for staircase method)
| Control                      | Description                                                                                                         |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Contrast step (%)            | Increment/decrement step of contrast. Select one of contrast step, spatial frequency step, and speed step.          |
| Spatial frequency step (c/d) | Increment/decrement step of spatial frequency. Select one of contrast step, spatial frequency step, and speed step. |
| Speed step (%)               | Increment/decrement step of speed. Select one of contrast step, spatial frequency step, and speed step.             |
| Timer (sec)                  | Countdown before auto-Miss                                                                                          |
| Termination (#Miss)          | Number of misses to end a staircase session                                                                         |
| Save directry                | Path for CSV auto-saving                                                                                            |
| Animal ID                    | Prefix for output CSV filename                                                                                      |
| Start                        | Start a staircase method session                                                                                    |
| Stop                         | Stop a staircase method session                                                                                     |

### Staircase Response

Click inside the **Staircase method** panel (right part of GUI):

- **Left click** → Hit (animal responded)
- **Right click** → Miss (no response)

### Output Data

CSV files are saved to `SAVE_DIRECTORY` with filenames: `<AnimalID>_<YEAR><MONTH><DAY>T<HOUR><MINUTE><SECOND>.csv`

| Column | Description                      |
| ------ | -------------------------------- |
| `ct`   | Contrast (%)                     |
| `sf`   | Spatial frequency (c/d)          |
| `spd`  | Speed (d/s)                      |
| `hm`   | Response: `h` (Hit) / `m` (Miss) |

Lines correspond to trials.

## Citation

If you use this software in your research, please cite:

Suematsu N, Ikeda T, Aoki T, Asayama M, Horii T, Hoshino A, Tanaka H, Soma S (2026).
An open-source platform for measuring optomotor responses in mice.
*Journal of Physiological Sciences*, 76(3), 100113.
https://doi.org/10.1016/j.jphyss.2026.100113

```bibtex
@article{suematsu2026omr,
  title   = {An open-source platform for measuring optomotor responses in mice},
  author  = {Suematsu, Naofumi and Ikeda, Toshihide and Aoki, Takanori and Asayama, Moe and Horii, Takuro and Hoshino, Atsushi and Tanaka, Hiroshi and Soma, Shogo},
  journal = {Journal of Physiological Sciences},
  volume  = {76},
  number  = {3},
  pages   = {100113},
  month   = {nov},
  year    = {2026},
  doi     = {10.1016/j.jphyss.2026.100113},
  url     = {https://doi.org/10.1016/j.jphyss.2026.100113}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.