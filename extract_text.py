import cv2
import pytesseract
import pandas as pd
import argparse

# Function to preprocess the image
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return binary

# Function to detect and recognize text with coordinates
def detect_text_with_coordinates(image_path, confidence_threshold):
    image = preprocess_image(image_path)
    custom_config = r'--oem 3 --psm 6'  # Custom config for Tesseract
    data = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)
    
    texts = []
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > confidence_threshold:  # Confidence threshold to filter out low quality text
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            text = data['text'][i]
            texts.append({'Text': text, 'Coordinates': (x, y, w, h)})
    
    return texts

# Function to save text and coordinates to a DataFrame and file
def save_to_file(text_data, output_file):
    df = pd.DataFrame(text_data)
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

# Function to generate an HTML file with the image and table
def generate_html(image_path, text_data, html_file):
    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image Text Coordinates</title>
        <style>
            #image-container {{
                position: relative;
                display: inline-block;
            }}
            #highlight-box {{
                position: absolute;
                border: 2px solid red;
                pointer-events: none;
                display: none;
            }}
        </style>
    </head>
    <body>
        <div id="image-container">
            <img id="image" src="{image_path}" alt="Diagram Image">
            <div id="highlight-box"></div>
        </div>
        <table border="1">
            <tr><th>Text</th><th>Coordinates</th></tr>
    '''

    for item in text_data:
        text = item['Text']
        x, y, w, h = item['Coordinates']
        html_content += f'''
        <tr>
            <td>{text}</td>
            <td><a href="#" onclick="highlight({x}, {y}, {w}, {h})">({x}, {y})</a></td>
        </tr>
        '''

    html_content += '''
        </table>
        <script>
            function highlight(x, y, w, h) {
                var highlightBox = document.getElementById('highlight-box');
                highlightBox.style.left = x + 'px';
                highlightBox.style.top = y + 'px';
                highlightBox.style.width = w + 'px';
                highlightBox.style.height = h + 'px';
                highlightBox.style.display = 'block';
            }
        </script>
    </body>
    </html>
    '''

    with open(html_file, 'w') as file:
        file.write(html_content)
    print(f"HTML file saved to {html_file}")

# Main function
def main(tesseract_path, image_path, confidence_threshold, output_csv, output_html):
    # Set the Tesseract executable path
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    text_data = detect_text_with_coordinates(image_path, confidence_threshold)
    save_to_file(text_data, output_csv)
    generate_html(image_path, text_data, output_html)

# Command-line interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract text and coordinates from an image and generate a table and HTML page.')
    parser.add_argument('image_path', type=str, help='Path to the image file')
    parser.add_argument('--tesseract_path', type=str, default='/opt/homebrew/bin/tesseract', help='Path to the Tesseract binary')
    parser.add_argument('--confidence_threshold', type=int, default=60, help='Confidence threshold for text recognition')
    parser.add_argument('--output_csv', type=str, default='output.csv', help='Output CSV file name')
    parser.add_argument('--output_html', type=str, default='output.html', help='Output HTML file name')
    
    args = parser.parse_args()
    
    main(args.tesseract_path, args.image_path, args.confidence_threshold, args.output_csv, args.output_html)