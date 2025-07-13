# ONVIF camera object tracker

The project implements an object tracker using a ONVIF enabled survailance camera [1,2]. Can be used to deploy your own object detection system (like a lazy cat detector :), see below), while running this implementation on a low end device like a raspberry pi.

<p align="center">
  <a name="video" href=""><img src="assets/vid.gif" alt="" width="400"></a>
</p>

Fist the program discovers all ONVIF compatible cameras, then check if PTZ service (remote Pan / Tilt/Zoom) is available.
After the proper startup the camera resets its position and depending on the configurrion options (see ```utils.config.py```) starts in ```gurdrian``` mode or in ```manual``` mode.

In ```guardian``` mode the camera waits for a certain time then scans the location, moves one step in horizontal then repeat till max rotation value is reached. After this a new horizontal value is choses and the process repeats, till all the area available is scanned.
```NOTE: DEBUG mode needs to be enable to view the camera feed, othervise headless mode will start = no GUI.```

In ```manual``` mode, by clicking on the rendered image (DEBUG mode neds to be enables), the user can use the 'wsad' keys to position the camera on a proper region, if object is detected, then the camera takes the control and moves its center point to the detected object center point.

### Install

The following packages will be needed (I recommand to create a conda environment pythin 3.10 or bigger for this project):

```code
pip install wsdiscovery onvif-zeep opencv-python requests

```


### Configuration

Before to use the program, you need to fill out the right parameter of the camera on your network. Port can varray for diffrent ONVIF cameras like the user / password too. For SriHome cameras there is by default a default admin user defined. You need to find out the right password, or sette it up as usual. Usefull ONVIF camera tool on Linux is [4].

```python
IP=""               # Camera IP address, leave empty for auto-discovery
PORT=""           # Port, default is 80
USER="XXX"        # Username, fill it if no anonymous access is allowed
PASS="YYY"       # Password, fill it if no anonymous access is allowed

```

### Object detector

For the current implementation a mobilenet v2 with SSD head is used. More information on the model or variants, can be found here: [5]. To detect defferent objects, use the right COCO definitions from: [6] and add it to the config file like:
```code
COCO_90_LABEL_TO_DETECT = {1:"person"}
```
For custom detectors the ```DnnObjectDetect``` class can be extended.

/Enjoy.


### References
1. [onvif standard](https://www.onvif.org/)
2. [tello_bject_tracking - similar project](https://github.com/fvilmos/tello_object_tracking)
3. [SriHome SP028 / SP030 camera](https://www.sricam.com/product.html#11ee6f34446c4743bdf59eef23a517dd)
4. [onvif-view](https://github.com/mDNSService/onvif-viewer)
5. [how to load Tensorflow models with OpenCV](https://jeanvitor.com/tensorflow-object-detecion-opencv/)
6. [COCO labels](https://gist.github.com/aallan/fbdf008cffd1e08a619ad11a02b74fa8)


