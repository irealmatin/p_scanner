# Document Scanner

![row image][https://github.com/irealmatin/p_scanner/blob/main/input_image/img_for_scan5.jpg]
![cooking!!][https://github.com/irealmatin/p_scanner/blob/main/output_image/outlined_image.jpg]
![scanned image][https://github.com/irealmatin/p_scanner/blob/main/output_image/scanned_image.jpg]

## Processing pipeline:

- Load original image
- Resize for faster processing

- Convert to grayscale and apply Gaussian blur

- Edge detection (Canny)

- Find and filter contours

- Detect the document (4-point contour)

- Order corner points and apply perspective warp

- Generate a top-down “scanned” view of the document

### How to Run
1 . install dependencies
```python
pip install opencv-python numpy
```

2 . Run via : 
```python
python main.py
```

**put your path instead of this :** 
```python
img_path = "hand_on/document_scanner/input_image/img_for_scan5.jpg"
```

### Notes : 
- Make sure your image clearly shows the document edges
- The script currently displays the result using OpenCV windows
  
