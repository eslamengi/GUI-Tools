import React, { useState } from 'react';
import './App.css';

const operations = [
  { value: 'histogram', label: 'Image Histogram' },
  { value: 'equalize', label: 'Histogram Equalization' },
  { value: 'fft', label: 'Fourier Transform (FFT)' },
  { value: 'sobel', label: 'Edge Detection (Sobel)' },
  { value: 'laplace', label: 'Edge Detection (Laplace)' },
  { value: 'noise_sp', label: 'Add Salt & Pepper Noise' },
  { value: 'noise_gaussian', label: 'Add Gaussian Noise' },
  { value: 'noise_periodic', label: 'Add Periodic Noise' },
  { value: 'remove_sp', label: 'Remove S&P Noise' },
  { value: 'remove_gaussian', label: 'Remove Gaussian Noise' },
  { value: 'remove_periodic', label: 'Remove Periodic Noise' },
];

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [operation, setOperation] = useState('histogram');
  const [resultImg, setResultImg] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setResultImg(null);
    setError('');
  };

  const handleOperationChange = (e) => {
    setOperation(e.target.value);
    setResultImg(null);
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setError('Please select an image file.');
      return;
    }
    setLoading(true);
    setError('');
    setResultImg(null);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('operation', operation);
      // TODO: Replace with your backend API endpoint
      const response = await fetch('/api/process', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error('Processing failed');
      const blob = await response.blob();
      setResultImg(URL.createObjectURL(blob));
    } catch (err) {
      setError('Error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Digital Image Processing Toolbox (Web)</h1>
        <form className="upload-form" onSubmit={handleSubmit}>
          <input type="file" accept="image/*" onChange={handleFileChange} />
          <select value={operation} onChange={handleOperationChange}>
            {operations.map((op) => (
              <option key={op.value} value={op.value}>{op.label}</option>
            ))}
          </select>
          <button type="submit" disabled={loading}>
            {loading ? 'Processing...' : 'Process Image'}
          </button>
        </form>
        {error && <div className="error">{error}</div>}
        <div className="images-container">
          {selectedFile && (
            <div>
              <h3>Original Image</h3>
              <img
                src={URL.createObjectURL(selectedFile)}
                alt="Original"
                className="image-preview"
              />
            </div>
          )}
          {resultImg && (
            <div>
              <h3>Processed Result</h3>
              <img src={resultImg} alt="Result" className="image-preview" />
              <a href={resultImg} download="result.png">Download Result</a>
            </div>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;
