# OKR Visual Stimulation System

A PyQt6-based GUI application for measuring **Optomotor Response (OKR)** in animals using drifting grating stimuli and the staircase method.

## Overview

This system presents sinusoidal/square-wave grating stimuli on a secondary monitor and allows the experimenter to measure visual thresholds (contrast, spatial frequency, or speed) via an adaptive staircase procedure.

### Key Features

- Real-time control of contrast, spatial frequency, and grating speed
- Staircase method: stimulus difficulty adjusts automatically based on Hit/Miss responses
- Countdown timer for inter-trial interval management
- Automatic CSV data logging per session
- Gamma correction utility for monitor calibration
- 3D-printable hardware platform (STL files included)

## Hardware Requirements

| Component | Specification |
|-----------|--------------|
| Display monitor | 1920×1080, 60 Hz (for stimulus) |
| Monitor–eye distance | ~24 cm (adjustable in `config.py`) |
| OS | Windows 10/11 |

3D-printable platform files are provided in [`3D model/`](3D%20model/).

## Installation

```bash
pip install -r requirements.txt
```

> **Note:** PsychoPy may require additional setup. See the [PsychoPy installation guide](https://www.psychopy.org/download.html).

## Configuration

Edit [`OMR/config.py`](OMR/config.py) before first use:

```python
MONITOR_NAME         = 'YourMonitorName'   # PsychoPy monitor profile name
MONITOR_SIZE         = (45, 26.3)          # Physical screen size (cm)
MONITOR_DISTANCE     = 24                  # Viewing distance (cm)
MONITOR_REFRESH_RATE = 60                  # Hz
SAVE_DIRECTORY       = r'C:\path\to\data'  # Output directory for CSV files
```

### Gamma Correction

Run the gamma measurement utility to calibrate your monitor before experiments:

```bash
python OMR/gamma_correction.py
```

## Usage

```bash
cd OMR
python main.py
```

### GUI Overview

| Control | Description |
|---------|-------------|
| Contrast (%) | Stimulus contrast (0–100%) |
| Spatial frequency (c/d) | Cycles per degree of visual angle |
| Speed (d/s) | Grating drift speed in degrees/second |
| Show/Hide | Toggle stimulus visibility |
| Apply | Apply current parameter values to stimulus |
| Staircase step | Select which parameter the staircase adjusts |
| Timer (sec) | Countdown before auto-Miss |
| Termination (#Miss) | Number of misses to end a session |
| Animal ID | Prefix for output CSV filename |

### Staircase Response

Click inside the **Staircase method** panel:

- **Left click** → Hit (animal responded)
- **Right click** → Miss (no response)

### Output Data

CSV files are saved to `SAVE_DIRECTORY` with filenames: `<AnimalID>_<YYYYMMDDTHHmmSS>.csv`

| Column | Description |
|--------|-------------|
| `ct` | Contrast (%) |
| `sf` | Spatial frequency (c/d) |
| `spd` | Speed (d/s) |
| `hm` | Response: `h` (Hit) / `m` (Miss) |

## Citation

<!-- Add journal reference here once published -->

## License

<!-- Add license information -->
