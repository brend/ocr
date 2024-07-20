# extract_text.py
Attempts to find text on an image and make
the image searchable by providing links to
the text segments.

## Setup
Create a Python virtual environment and install dependencies.

``` sh
python3 -m venv venv
source venv/bin/activate
pip install pytesseract opencv-python pandas numpy
```

Additionally, Tesseract must be installed on your machine.
Modify the script by giving it the path to the Tesseract binary.

``` python
# example: Tesseract installed with Homebrew on macOS
r'/opt/homebrew/bin/tesseract'
```

Optionally, verify the installations.

``` sh
tesseract --version
python -c "import cv2; import pytesseract; import pandas; print('All packages are installed successfully!')"
```

## Usage
The script expects the path to an image file
as its single command line argument.

``` sh
python extract_text.py /path/to/my_image.png
```

The output will be written to `output.csv` (a table of the text 
that has been found and the corresponding corrdinates)
and `output.html` (an HTML page displaying the image and 
links that will highlight the corresponding text when clicked).