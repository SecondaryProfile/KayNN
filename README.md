# KayNN

This is a simple Python application built using Kivy that allows users to select an image file and determine its dominant color using the K-Means clustering algorithm.

## Features

- Select an image file (PNG, JPG, JPEG, GIF) using a file chooser.
- Preview the selected image.
- Detect the dominant color in the image using K-Means clustering.
- Display the RGB and hex values of the dominant color.
- Display a preview of the dominant color.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/SecondaryProfile/KayNN.git
    ```

2. Install the required dependencies:

    ```bash
    pip install kivy opencv-python skikit-learn
    ```
3. Note in older versions of MacOS, you must run the following for opencv instead:

   ```bash
   pip3 install opencv-python==4.6.0.66
   ```
## Usage

1. Navigate to the directory where you cloned the repository:

    ```bash
    cd KayNN-main
    ```

2. Run the application:

    ```bash
    python main.py
    ```

3. Use the file chooser to select an image file.
4. Click the "Detect Color" button to analyze the image and display the dominant color.

## Screenshots

![App Screenshot](screenshots/screenshot.png)

## Dependencies

- [Kivy](https://kivy.org/)
- [OpenCV](https://opencv.org/)
- [SciKit Learn](https://scikit-learn.org)

## TODO

- Make output image an export
- Make the background color match the KNN output color (stupid but fun)
- Add support for other image types
