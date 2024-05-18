# Rice Image Processing Project

## Introduction

In this project, we have compiled multiple images showcasing different types of rice. Our goal is to apply image processing techniques, such as morphology, to measure the length and width of various rice grains.

## Rice Types

1. Super Tota
2. 1.5 Saal Purana Kainat
3. Kacha Super Fan
4. Kainat Steam
5. Super Kernel Naya

## Picture Acquisition

- **Camera:** Vivo V21e camera
- **Reference Object:** Paper cut in shape of coin with a diameter of 19mm

## Working

### Basic Steps

1. **Opening:** Removing small isolated dots by applying an opening operation on the image.
2. **Thresholding:** Separating foreground and background using thresholding.
3. **Border Clearing:** Using clear border morphology to remove images touching the border.

### Labelled Image and Region Props

- Utilizing SK Images built-in functionality to obtain a labelled image.
- Extracting region properties such as orientation, major axis, minor axis, diameter, and bounding box.
- Storing region props table in a Pandas dataframe.

### Image Extraction and Measurement

- Converting the Pandas dataframe to a numpy array.
- Using region properties to extract rice from the image.
- Measuring the length of rice grains:
    1. Comparing the diameter of a reference object (paper cut in shape of a coin) with the pixel pitch to calculate the length of one pixel.
    2. Multiplying the major axis of rice by the length of one pixel to determine the length of the rice grain.
    3. Similarly, multiplying the minor axis of rice by the length of one pixel gives the width of the rice grain.

### Storing Results

- Creating a dictionary containing all rice information.
- Converting the dictionary into a dataframe.
- Using built-in functions to store results in a CSV file.

