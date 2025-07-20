# Digital Image Processing Toolbox (GUI)

A user-friendly Python application for interactive image processing, visualization, and analysis. Built with Tkinter, this toolbox enables users to upload images, apply a variety of processing techniques, visualize results, and save outputs—all through an intuitive graphical interface.

---

## Features

- **Image Upload:** Load images in common formats (JPG, PNG, etc.)
- **Histogram Visualization:** View the intensity histogram of the image
- **Histogram Equalization:** Enhance image contrast
- **Fourier Transform (FFT):** Visualize the frequency domain
- **Edge Detection:** Apply Sobel and Laplace filters
- **Noise Addition:** Add Salt & Pepper, Gaussian, or Periodic noise
- **Noise Removal:** Remove noise using median, Gaussian, or Butterworth filters
- **Save Results:** Save processed images locally

---

## Screenshots

### GUI Layout
![GUI Layout](https://user-images.githubusercontent.com/37985105/151868408-eb70199d-d2bb-4378-bce0-517650e3d60f.png)

### Example Operations
- **Open Image:**
  ![Open Image](https://user-images.githubusercontent.com/37985105/151868414-7b646fac-3c37-40c0-9246-3556b8d519de.png)
- **Histogram & Equalization:**
  ![Histogram Equalization](https://user-images.githubusercontent.com/37985105/151868431-0deeb7eb-c0fb-4d0c-adc6-01d961c9c18e.png)
- **FFT:**
  ![FFT](https://user-images.githubusercontent.com/37985105/151868421-67bcd36a-5804-4645-99ff-d08c7f943b0b.png)
- **Edge Detection (Sobel, Laplace):**
  ![Sobel](https://user-images.githubusercontent.com/37985105/151868451-0ccd013a-fdef-4597-abf9-77b858838416.png)
  ![Laplace](https://user-images.githubusercontent.com/37985105/151868437-d63a2755-7a90-4b1b-936d-bedb16f8ae4f.png)
- **Noise Addition & Removal:**
  ![S P](https://user-images.githubusercontent.com/37985105/151868447-19fb4cc0-ea0e-4b21-a9b8-afdd18d85820.png)
  ![Gauss](https://user-images.githubusercontent.com/37985105/151868424-e9e59fab-939d-411a-85dc-b0ceb4a37f19.png)
  ![periodic](https://user-images.githubusercontent.com/37985105/151868441-9388fc8d-843c-4836-b19e-c6a190a93795.png)

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd "Digital Image Processing Toolbox - GUI"
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Run the application:
   ```bash
   python "Image Processing Toolbox.py"
   ```
2. Use the GUI to:
   - Open an image
   - Select processing operations (histogram, FFT, filters, noise, etc.)
   - View results in real time
   - Save processed images

---

## Requirements

- Python 3.7+
- Tkinter
- Pillow (PIL)
- scikit-image
- matplotlib
- numpy
- scipy

Install all dependencies with:
```bash
pip install -r requirements.txt
```

---

## Project Structure

```
Digital Image Processing Toolbox - GUI/
├── Image Processing Toolbox.py   # Main application
├── Readme.md                    # Project documentation
├── GUI ToolBox Sample result.md # Sample results and screenshots
└── requirements.txt             # Python dependencies
```

---

## Credits

Developed by:
- [Eslam Ahmed Elsheikh](https://github.com/eslamengi)
- [Ahmed Abdelmoneim Elshazli](https://github.com/shazli1)
- [Ahmed Mostafa ElBaz](https://github.com/ahmed-elbaz)

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
