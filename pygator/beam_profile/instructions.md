How to use

### Beam Profile with Propagation
python beam_profile_fit.py --mode heatmap --roi-size 350 --downsample 2 --exposure 10000 --gain 0 --output beam_data.csv

Performs live 2D Gaussian fitting of the beam and displays the result with overlays. Unlike live_camera_fit.py, this script allows recording beam waist data (wx, wy) as a function of propagation distance z.
Press r to start/stop recording data.
Press f to save the recorded data to the specified CSV file (--output).
Press q to quit.


ROI: is the region of interest. It's a square shape around the highest peak with a size equal to the number of pixels. In this example it's a square of 350 pixel side length. 

downsample:
✅ What Happens with Downsampling in the Code

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
 
--pixel-size is the camera's pixel size. 
--output is the name of the CSV file to be saved, if chosen


Saved CSV includes:
z [m]: propagation distance (from stage or user input)
wx [m]: horizontal beam waist (meters)
wy [m]: vertical beam waist (meters)
wx_std [m], wy_std [m]: standard deviations over recent frames (stability estimate)
If the beam cannot be fit (too faint / absent), the frame is skipped with a warning.
If the camera disconnects unexpectedly, any recorded data up to that point is saved automatically to a backup CSV.



### Live fitting without saving data

python live_camera_fit.py --mode heatmap --roi-size 350 --downsample 2 --exposure 10000 --gain 0


Fitting a 2D gaussian to the beam live. This doesn't save the data. The parameters are in units of pixel numbers. 