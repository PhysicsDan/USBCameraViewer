# USB Camera Viewer


## Dependencies
```shell
conda install -c conda-forge opencv pyqt
```

## Usage
See what cameras are picked up:
```shell
python list_connected.py
```
This will print out any detected usb cameras (including e.g. laptop webcam) as well as the camera index.

Display camera feed.
```shell
python display_cameras.py
```
You can specify the directory to save images (when you click gui button) as well as the camera index so that the correct cameras are streamed.


### TODO
-[ ] Add in argparse so don't need to edit display cameras file
