How to use pygator beam profiler with FLIR cameras

To run this, you need to install PySpin. PySpin can be found here https://www.teledynevisionsolutions.com/support/support-center/software-firmware-downloads/iis/spinnaker-sdk-download/spinnaker-sdk--download-files/

Do NOT install this package
```
pip install pyspin
```
This pyspin is different than PySpin, which is a wrapper, not a package. 


### Live Camera
You can look at the beam live using the live_camera.py script. 

The command line for this is 

```
python path_to_file/live_camera.py --mode heatmap --exposure 10000 --gain 0
```

There are 2 display modes: default="gray" and "heatmap"

This can serve as a basic test of correct installation of PySpin.


### Basic Beam Profiler
The fitting math can be found in fit_gaussian.py

python path_to_file/live_camera_fit.py --mode heatmap --roi-size 350 --downsample 2 --exposure 10000 --gain 0

ROI: is the region of interest. It's a square shape around the highest peak with a size equal to the number of pixels. In this example it's a square of 350 pixel side length. This square will be plotted on the image.

downsample:
When we downsample like this:
```
cropped = cv2.resize(cropped, (cropped.shape[1] // downsample, cropped.shape[0] // downsample), interpolation=cv2.INTER_AREA)
```

we’re using:

cv2.INTER_AREA interpolation

This does approximate area-based resampling, which is similar to averaging pixels together especially when downsampling by integer factors like 2 or 4.

So, for example:

If downsample=2, OpenCV effectively averages 2×2 pixel blocks into one pixel.

If downsample=4, it uses 4×4 blocks, and so on.

This isn’t a naive pixel-wise average but a resampling algorithm that gives similar results with more accurate interpolation.

