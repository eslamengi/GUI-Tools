# Digital Image Processing Toolbox - Web Frontend

This is the React frontend for the Digital Image Processing Toolbox. It allows users to upload images, select processing operations, and view/download results in a modern, responsive web interface.

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the development server:
   ```bash
   npm start
   ```
   The app will run at http://localhost:3000 and proxy API requests to the backend at http://localhost:8000.

## Features
- Upload images from your local PC
- Select image processing operations (histogram, equalization, FFT, edge detection, noise, etc.)
- View original and processed images
- Download processed results
- Responsive design for desktop and mobile

## Backend API
This frontend expects a backend FastAPI server running at http://localhost:8000 with an endpoint at `/api/process` that accepts image uploads and operation selection.

---

For more details, see the main project documentation.