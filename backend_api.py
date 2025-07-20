from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from io import BytesIO
from PIL import Image
import numpy as np
from skimage.exposure import equalize_hist
from skimage.util import random_noise
from skimage.filters import sobel, laplace, median, gaussian
from skimage.morphology import disk
from scipy.fftpack import fft2, fftshift
from scipy.signal import sosfiltfilt, butter
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def pil_to_bytes(img: Image.Image, format='PNG'):
    buf = BytesIO()
    img.save(buf, format=format)
    buf.seek(0)
    return buf

def np_to_pil(np_img):
    if np_img.ndim == 2:
        np_img = (np_img * 255).clip(0, 255).astype(np.uint8)
        return Image.fromarray(np_img, mode='L')
    elif np_img.ndim == 3:
        np_img = (np_img * 255).clip(0, 255).astype(np.uint8)
        return Image.fromarray(np_img)
    else:
        raise ValueError('Unsupported image shape')

def plot_histogram(np_img):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.hist(np_img.ravel(), 512)
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf

def plot_fft(np_img):
    y = fft2(np_img, (255, 255))
    x1 = fftshift(y)
    x2 = np.abs(x1)
    x3 = 20 * np.log(x2 + 1e-8)
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(x3, cmap='gray', vmin=0, vmax=255)
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf

@app.post('/api/process')
async def process_image(file: UploadFile = File(...), operation: str = Form(...)):
    try:
        img = Image.open(BytesIO(await file.read())).convert('RGB')
        np_img = np.array(img) / 255.0
        if np_img.ndim == 3:
            np_img_gray = rgb2gray(np_img)
        else:
            np_img_gray = np_img
        # Operations
        if operation == 'histogram':
            buf = plot_histogram(np_img_gray)
            return StreamingResponse(buf, media_type='image/png')
        elif operation == 'equalize':
            eq = equalize_hist(np_img_gray)
            pil_img = np_to_pil(eq)
            return StreamingResponse(pil_to_bytes(pil_img), media_type='image/png')
        elif operation == 'fft':
            buf = plot_fft(np_img_gray)
            return StreamingResponse(buf, media_type='image/png')
        elif operation == 'sobel':
            filtered = sobel(np_img_gray)
            pil_img = np_to_pil(filtered)
            return StreamingResponse(pil_to_bytes(pil_img), media_type='image/png')
        elif operation == 'laplace':
            filtered = laplace(np_img_gray)
            pil_img = np_to_pil(filtered)
            return StreamingResponse(pil_to_bytes(pil_img), media_type='image/png')
        elif operation == 'noise_sp':
            noisy = random_noise(np_img_gray, mode='s&p')
            pil_img = np_to_pil(noisy)
            return StreamingResponse(pil_to_bytes(pil_img), media_type='image/png')
        elif operation == 'noise_gaussian':
            noisy = random_noise(np_img_gray, mode='gaussian', seed=None, clip=True)
            pil_img = np_to_pil(noisy)
            return StreamingResponse(pil_to_bytes(pil_img), media_type='image/png')
        elif operation == 'noise_periodic':
            x = np.arange(len(np_img_gray[0]))
            y = np.sin(2 * np.pi * x / 5)
            y += max(y)
            PeriodicNoise = np.array([[y[j] * 127 for j in range(len(np_img_gray[0]))] for i in range(len(np_img_gray[:, 0]))], dtype=np.uint8)
            noisy = np_img_gray * PeriodicNoise
            pil_img = np_to_pil(noisy)
            return StreamingResponse(pil_to_bytes(pil_img), media_type='image/png')
        elif operation == 'remove_sp':
            noisy = random_noise(np_img_gray, mode='s&p')
            restored = median(noisy, disk(3))
            pil_img = np_to_pil(restored)
            return StreamingResponse(pil_to_bytes(pil_img), media_type='image/png')
        elif operation == 'remove_gaussian':
            noisy = random_noise(np_img_gray, mode='gaussian', seed=None, clip=True)
            restored = gaussian(noisy, sigma=1)
            pil_img = np_to_pil(restored)
            return StreamingResponse(pil_to_bytes(pil_img), media_type='image/png')
        elif operation == 'remove_periodic':
            x = np.arange(len(np_img_gray[0]))
            y = np.sin(2 * np.pi * x / 5)
            y += max(y)
            PeriodicNoise = np.array([[y[j] * 127 for j in range(len(np_img_gray[0]))] for i in range(len(np_img_gray[:, 0]))], dtype=np.uint8)
            noisy = np_img_gray * PeriodicNoise
            sos = butter(4, 0.125, output='sos')
            restored = sosfiltfilt(sos, noisy)
            pil_img = np_to_pil(restored)
            return StreamingResponse(pil_to_bytes(pil_img), media_type='image/png')
        else:
            return JSONResponse({'error': 'Unknown operation'}, status_code=400)
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)