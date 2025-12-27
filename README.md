# Document Scanner

## Processing pipeline:

- Load original image
- Resize for faster processing

- Convert to grayscale and apply Gaussian blur

- Edge detection (Canny)

- Find and filter contours

- Detect the document (4-point contour)

- Order corner points and apply perspective warp

- Generate a top-down “scanned” view of the document

  
