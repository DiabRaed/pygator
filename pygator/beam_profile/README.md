# How to Use

# How to Use

## Table of Contents
- [Installing PySpin](#installing-pyspin)
- [Running Scripts](#running-scripts)
- [Beam Profile with Propagation](#beam-profile-with-propagation)
  - [Command-Line Arguments](#command-line-arguments)
- [Live Fitting (No Data Saving)](#live-fitting-no-data-saving)
- [Live Camera](#live-camera)
- [Command Reference](#quick-command-reference)



## Installing PySpin
To install the PySpin wrapper, follow the instructions in  
[README_FLIR](./README_FLIR_installation.md).

⚠️ **Do NOT install with**:
```bash
pip install pyspin
```
This is a different package and will not work.

---

## Running Scripts
It’s most convenient to run scripts from the command prompt. The exact command depends on your installation method.

**From Git:**
```bash
python script.py --keyword_arguments keyword_values
```

**From pip:**
```bash
python -m pygator.beam_profile.script --keyword_arguments keyword_values
```

---

## Beam Profile with Propagation
Performs live 2D Gaussian fitting of the beam and displays results with overlays.  
Unlike `live_camera_fit.py`, this script can record beam waist data (`wx`, `wy`) as a function of propagation distance `z`.

**From Git:**
```bash
python beam_profile_fit.py --roi-size 400 --downsample 2 --exposure auto --gain auto --pixel-size 6.9 --output my_beam_scan.csv --mode heatmap
```

**From pip:**
```bash
python -m pygator.beam_profile.beam_profile_fit --roi-size 400 --downsample 2 --exposure auto --gain auto --pixel-size 6.9 --output my_beam_scan.csv --mode heatmap
```

**Controls:**
- `r` → start/stop recording frames
- `R` → calculates average of beam radii and standard deviations at some point z of all recorded frames
- `n` → command to record the distance the camera has moved from the previous point. Takes values in inches. Once entered, repeat `r` and `R` to record the next data point.
- `f` → save recorded data to CSV (`--output`) and display the fit. The fit is done with pygator.module.fit_beam_profile_ODR
- `q` → quit  

After saving the `.csv` file, you can fit the beam profile manually using:
- `pygator.module.fit_beam_profile_ODR`
- `pygator.module.fit_beam_profile_curve_fit`
This is the exact fit shown after pressing `f`.  
See example in  
[beam_profile_FLIR](../../Tests/beam_profile_FLIR.py).

---

### Command-Line Arguments
- **`--roi-size`**: side length of square ROI (pixels). Example: `400` → 400×400 px.  
- **`--downsample`**: default `2`.  

  Downsampling uses:
  ```python
  cropped = cv2.resize(
      cropped,
      (cropped.shape[1] // downsample, cropped.shape[0] // downsample),
      interpolation=cv2.INTER_AREA
  )
  ```
  - `downsample=2` → averages 2×2 blocks  
  - `downsample=4` → averages 4×4 blocks  

- **`--pixel-size`**: camera pixel size in µm (default: 6.9).  
- **`--output`**: name of CSV file to save (in current directory).  
- **`--mode`**: `"heatmap"` or `"gray"` (default: `"gray"`).  

**Saved CSV includes:**
- `z [m]` → propagation distance  
- `wx [m]`, `wy [m]` → horizontal/vertical beam waists  
- `wx_std [m]`, `wy_std [m]` → standard deviations (stability estimate)  

If the beam cannot be fit (too faint/absent), that frame is skipped.  
If the camera disconnects, progress is saved automatically to `outputfilename_backed_up.csv`.

---

## Live Fitting (No Data Saving)
Simple 2D Gaussian fitting of the beam at a single spot (no data saved).

**From Git:**
```bash
python live_camera_fit.py --mode heatmap --roi-size 350 --downsample 2 --exposure 10000 --gain 0
```

**From pip:**
```bash
python -m pygator.beam_profile.live_camera_fit --mode heatmap --roi-size 350 --downsample 2 --exposure 10000 --gain 0
```

---

## Live Camera
Displays the beam in real time (like Spinnaker software, but simplified).

**From Git:**
```bash
python live_camera.py --mode heatmap --roi-size 350 --downsample 2 --exposure 10000 --gain 0
```

**From pip:**
```bash
python -m pygator.beam_profile.live_camera --mode heatmap --exposure 10000 --gain 0
```



## Quick Command Reference

| Script              | From Git                                                                 | From pip                                                                                   |
|---------------------|---------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| **Beam Profile Fit** | `python beam_profile_fit.py --roi-size 400 --downsample 2 --exposure auto --gain auto --pixel-size 6.9 --output my_beam_scan.csv --mode heatmap` | `python -m pygator.beam_profile.beam_profile_fit --roi-size 400 --downsample 2 --exposure auto --gain auto --pixel-size 6.9 --output my_beam_scan.csv --mode heatmap` |
| **Live Camera Fit**  | `python live_camera_fit.py --mode heatmap --roi-size 350 --downsample 2 --exposure 10000 --gain 0` | `python -m pygator.beam_profile.live_camera_fit --mode heatmap --roi-size 350 --downsample 2 --exposure 10000 --gain 0` |
| **Live Camera**      | `python live_camera.py --mode heatmap --roi-size 350 --downsample 2 --exposure 10000 --gain 0` | `python -m pygator.beam_profile.live_camera --mode heatmap --exposure 10000 --gain 0` |

---