# Camera Lens Smear Detection- OpenCV and Python

This application helps to detect any kind of small smears on camera lens.
This application is useful in Street Map designing.

### Algorithm
* Convert all images to the same size (width & height)
* Find mean value for all images by pixel
* Convert mean image into grayscale image
* Apply threshold function using openCV.
* Calculate boundaries of all the polygoan possible after the previous step.
* if the polygoan area minimum or equal to the possible smear area, add it to the smear array.
* Apply mask to the all images using list of smear position we have.
