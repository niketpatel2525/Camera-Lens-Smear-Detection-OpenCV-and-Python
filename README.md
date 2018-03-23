# Camera Lens Smear Detection- OpenCV and Python

This application helps to detect any kind of small smears on camera lens.
This application is useful in Street Map designing.

Flowchart for Algorithm procedure. 
setting:

    {
        flowChart : true
    }


```flow
st=>start: Input Images
op=>operation: Convert all images to same size (width & height)
op=>operation: Calculate mean of all images
op=>operation: Convert to grayscale and use Threshold image using openCV
e=>end: Final Result
```