How to use

### Installing PySpin

To install PySpin wrapper, follow the instruction in 

[README_FLIR](./README_FLIR_installation.md)


Do NOT install pyspin with 

```
pip install pyspin
```
This is not the wrapper we need.


### Running Scripts
It's most convenient to run all scripts using the command prompt.
Depending on installation method, the command line changes. 

If you install pygator through Git, go to the folder of the script and run 

```
python script.py --keyword_arguments keyword_values
```

If you install pygator with pip, the command line is 

```
python -m pygator.beam_profile.script --keyword_arguments keyword_values
```

### Beam Profile with Propagation

Git:
```
python beam_profile_fit.py --roi-size 400 --downsample 2 --exposure auto --gain auto --pixel-size 6.9 --output my_beam_scan.csv --mode heatmap
```

Pip:
```
python -m pygator.beam_profile.beam_profile_fit --roi-size 400 --downsample 2 --exposure auto --gain auto --pixel-size 6.9 --output my_beam_scan.csv --mode heatmap
```

Performs live 2D Gaussian fitting of the beam and displays the result with overlays. Unlike live_camera_fit.py, this script allows recording beam waist data (wx, wy) as a function of propagation distance z.
Press r to start/stop recording data.
Press f to save the recorded data to the specified CSV file (--output).
Press q to quit.


Once you are done with the scan and saved the .csv file, you can use pygator.module.fit_beam_profile_ODR or pygator.module.fit_beam_profile_curve_fit to perform the fitting and return the q-parameters. See example beam_profile_FLIR in Tests found here 

[beam_profile_FLIR](../../Tests/beam_profile_FLIR.py)




--roi-size: is the region of interest. It's a square shape around the highest peak with a size equal to the number of pixels. In this example it's a square of 400 pixel side length. 

--downsample: default to 2
What Happens with Downsampling in the Code

When we downsample like this:
```
cropped = cv2.resize(cropped, (cropped.shape[1] // downsample, cropped.shape[0] // downsample),
                     interpolation=cv2.INTER_AREA)
```

we’re using:

📉 cv2.INTER_AREA interpolation

This does approximate area-based resampling, which is similar to averaging pixels together — especially when downsampling by integer factors like 2 or 4.

So, for example:

If downsample=2, OpenCV effectively averages 2×2 pixel blocks into one pixel.

If downsample=4, it uses 4×4 blocks, and so on.

This isn’t a naive pixel-wise average but a resampling algorithm that gives similar results with more accurate interpolation.
 
--pixel-size is the camera's pixel size in microns. Default to 6.9 µm

--output is the name of the CSV file to be saved, if chosen. This is saved in the current working directory. 

--mode either "heatmap" or "gray" (default). This is just a display preference and does not affect the fitting at all.

Saved CSV includes:
z [m]: propagation distance (from stage or user input)
wx [m]: horizontal beam waist (meters)
wy [m]: vertical beam waist (meters)
wx_std [m], wy_std [m]: standard deviations over recent frames (stability estimate)
If the beam cannot be fit (too faint / absent), the frame is skipped with a warning.
If the camera disconnects unexpectedly, any recorded data up to that point is saved automatically to a backup CSV.

In case of camera disconnections, the script automatically saves the progress in outputfilename_backed_up.csv



### Live fitting without saving data


Git:
```
python live_camera_fit.py --mode heatmap --roi-size 350 --downsample 2 --exposure 10000 --gain 0
```
pip:
```
python pygator.beam_profile.live_camera_fit --mode heatmap --roi-size 350 --downsample 2 --exposure 10000 --gain 0
```

This is a simple 2D fitting of the beam at single spot. It does not save or record any data. 


### Live Camera


Git:
```
python live_camera_fit --mode heatmap --roi-size 350 --downsample 2 --exposure 10000 --gain 0
```
pip:
```
python pygator.beam_profile.live_camera --mode heatmap --exposure 10000 --gain 0
```

Simple display of the beam in real time. This is basically what spinnaker software 


