"""
Developers: the Three Heroes
    1- Eslam Ahmed Elsheikh // https://github.com/eslamengi
    2- Ahmed Abdelmoneim Elshazli 
    3- Ahmed Mostafa ElBaz // https://github.com/ahmed-elbaz
"""

import os
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import tkinter.font as ft
import matplotlib.pyplot as plt
import numpy as np
from numpy import asarray
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from skimage.transform import rescale, resize
from scipy import ndimage
from skimage import io
from skimage.io import imread
from skimage.exposure import equalize_hist
from skimage.util import random_noise
from skimage import img_as_ubyte, img_as_float
from skimage import io, filters
from skimage import color
from skimage.filters import median
from skimage.filters import gaussian
from skimage.morphology import disk
from scipy.fftpack import fft2, fftshift
from scipy.signal import sosfiltfilt, butter
from skimage.color import rgb2gray

class ImageProcessingToolboxApp:
    """
    Main application class for the Digital Image Processing Toolbox GUI.
    Encapsulates all GUI elements, state, and image processing logic.
    """
    def __init__(self, root: Tk):
        self.root = root
        self.root.title('Image Processing (GUI ToolBox)')
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "Nile University icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass  # Ignore icon errors for portability

        # Fonts
        self.buttonFont = ft.Font(family='Arial', size=14, weight='bold')
        self.entryFont = ft.Font(family='Tahoma', size=10, weight='bold')
        self.functionfont = ft.Font(family='Arial', size=10, weight='bold', underline=1)
        self.rbuttonfont = ft.Font(family='Arial', size=10)

        # Frames
        self.frame1 = LabelFrame(self.root, padx=10, pady=10)
        self.frame2 = LabelFrame(self.root, padx=10, pady=10)
        self.frame3 = LabelFrame(self.root, text="Original Image", padx=10, pady=10)
        self.frame4 = LabelFrame(self.root, text="Image Processing Area 1", padx=10, pady=10)
        self.frame5 = LabelFrame(self.root, text="Image Processing Area 2", padx=10, pady=10)
        self.frame1.grid(row=0, column=0, columnspan=5)
        self.frame2.grid(row=1, column=0, columnspan=5)
        self.frame3.grid(row=2, column=0)
        self.frame4.grid(row=2, column=1)
        self.frame5.grid(row=2, column=2)

        Label(self.root, text="Developed by:\n The Three Heroes\
           [Ahmed Abdelmoneim Elshazli, Ahmed Mostafa ElBaz, Eslam Ahmed Elsheikh]", bg="black", fg="white", padx=10, pady=10).grid(row=3, column=0, columnspan=3)

        # State
        self.image_path = None
        self.np_image = None
        self.image_size = None
        self.sp_noisy_image = None
        self.gaussian_noisy_image = None
        self.periodic_noisy_image = None

        # Tkinter variables
        self.filter_var = IntVar()
        self.noise_var = IntVar()
        self.removal_var = IntVar()

        # Buttons
        Button(self.frame1, text="Open Image", bg="black", fg="grey", command=self.open_file, font=self.buttonFont, borderwidth=5, width=36).grid(row=1, column=0, columnspan=3)
        Button(self.frame1, text="Image Histogram", bg="#3D59AB", fg="white", command=self.histogram, font=self.entryFont, borderwidth=5, width=20).grid(row=2, column=0)
        Button(self.frame1, text="FFT", bg="#3D59AB", fg="white", width=10, command=self.fft_transform, font=self.entryFont, borderwidth=5).grid(row=2, column=1)
        Button(self.frame1, text="Histogram Equalization", bg="#3D59AB", fg="white", command=self.histogram_equal, font=self.entryFont, borderwidth=5, width=20).grid(row=2, column=2)

        # Radio buttons and labels
        Label(self.frame2, text="Please select Filter", width=20, borderwidth=5, font=self.functionfont).grid(row=0, column=0)
        Label(self.frame2, text="Please select Noise Type", width=25, borderwidth=5, font=self.functionfont).grid(row=0, column=1)
        Label(self.frame2, text="Please select Noise removal filter", width=30, borderwidth=5, font=self.functionfont).grid(row=0, column=2)
        Radiobutton(self.frame2, text="Sobel", font=self.rbuttonfont, variable=self.filter_var, value=1, command=self.filter_selection).grid(row=1, column=0)
        Radiobutton(self.frame2, text="Laplace", font=self.rbuttonfont, variable=self.filter_var, value=2, command=self.filter_selection).grid(row=2, column=0)
        Radiobutton(self.frame2, text="S & P", font=self.rbuttonfont, variable=self.noise_var, value=1, command=self.noise_selection).grid(row=1, column=1)
        Radiobutton(self.frame2, text="Gaussian", font=self.rbuttonfont, variable=self.noise_var, value=2, command=self.noise_selection).grid(row=2, column=1)
        Radiobutton(self.frame2, text="Periodic", font=self.rbuttonfont, variable=self.noise_var, value=3, command=self.noise_selection).grid(row=3, column=1)
        Radiobutton(self.frame2, text="Remove S&P", font=self.rbuttonfont, variable=self.removal_var, value=1, command=self.noise_removal).grid(row=1, column=2)
        Radiobutton(self.frame2, text="Remove Gaussian", font=self.rbuttonfont, variable=self.removal_var, value=2, command=self.noise_removal).grid(row=2, column=2)
        Radiobutton(self.frame2, text="Remove Periodic", font=self.rbuttonfont, variable=self.removal_var, value=3, command=self.noise_removal).grid(row=3, column=2)

    def open_file(self) -> None:
        """Open an image file and display it in the GUI."""
        for widget in self.frame3.winfo_children():
            widget.destroy()
        path = filedialog.askopenfilename(title="Select a file", filetypes=(("jpg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*")))
        if not path:
            return
        try:
            img = Image.open(path)
            img = img.resize((250, 220))
            my_image = ImageTk.PhotoImage(img)
            Label(self.frame3, image=my_image).pack()
            self.frame3.image = my_image  # Prevent garbage collection
            self.np_image = plt.imread(path)
            self.image_size = self.np_image.shape
            if len(self.image_size) == 3:
                self.np_image = rgb2gray(self.np_image)
            self.image_path = path
        except Exception as e:
            Label(self.frame3, text=f"Error loading image: {e}", fg="red").pack()

    def histogram(self) -> None:
        """Display the histogram of the current image."""
        if self.np_image is None:
            return
        for widget in self.frame4.winfo_children():
            widget.destroy()
        fig = Figure(figsize=(4, 4))
        plot1 = fig.add_subplot(111)
        plot1.hist(self.np_image.ravel(), 512)
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.frame4)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, self.frame4)
        toolbar.update()
        canvas.get_tk_widget().pack()

    def histogram_equal(self) -> None:
        """Display the histogram of the equalized image."""
        if self.np_image is None:
            return
        for widget in self.frame5.winfo_children():
            widget.destroy()
        fig1 = Figure(figsize=(4, 4))
        plot2 = fig1.add_subplot(111)
        eq = asarray(equalize_hist(self.np_image))
        plot2.hist(eq.ravel(), 512)
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig1, master=self.frame5)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, self.frame5)
        toolbar.update()
        canvas.get_tk_widget().pack()

    def fft_transform(self) -> None:
        """Display the FFT of the current image."""
        if self.np_image is None:
            return
        for widget in self.frame4.winfo_children():
            widget.destroy()
        y = fft2(self.np_image, (255, 255))
        x1 = fftshift(y)
        x2 = np.abs(x1)
        x3 = 20 * np.log(x2 + 1e-8)  # Avoid log(0)
        fig2 = Figure(figsize=(4, 4))
        plot3 = fig2.add_subplot(111)
        plot3.imshow(x3, 'gray', vmin=0, vmax=255)
        canvas = FigureCanvasTkAgg(fig2, master=self.frame4)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, self.frame4)
        toolbar.update()
        canvas.get_tk_widget().pack()

    def filter_selection(self) -> None:
        """Apply selected edge detection filter and display result."""
        if self.np_image is None:
            return
        for widget in self.frame5.winfo_children():
            widget.destroy()
        filtered_image = None
        if self.filter_var.get() == 1:
            filtered_image = filters.sobel(self.np_image)
        elif self.filter_var.get() == 2:
            filtered_image = filters.laplace(self.np_image)
        if filtered_image is not None:
            fig3 = Figure(figsize=(4, 4))
            plot4 = fig3.add_subplot(111)
            plot4.imshow(filtered_image, cmap=plt.cm.gray)
            canvas = FigureCanvasTkAgg(fig3, master=self.frame5)
            canvas.draw()
            canvas.get_tk_widget().pack()
            toolbar = NavigationToolbar2Tk(canvas, self.frame5)
            toolbar.update()
            canvas.get_tk_widget().pack()

    def noise_selection(self) -> None:
        """Add selected noise type to the image and display result."""
        if self.np_image is None:
            return
        for widget in self.frame4.winfo_children():
            widget.destroy()
        noisy_image = None
        if self.noise_var.get() == 1:
            noisy_image = random_noise(self.np_image, mode='s&p')
            self.sp_noisy_image = noisy_image
        elif self.noise_var.get() == 2:
            noisy_image = random_noise(self.np_image, mode='gaussian', seed=None, clip=True)
            self.gaussian_noisy_image = noisy_image
        elif self.noise_var.get() == 3:
            x = np.arange(len(self.np_image[0]))
            y = np.sin(2 * np.pi * x / 5)
            y += max(y)
            PeriodicNoise = np.array([[y[j] * 127 for j in range(len(self.np_image[0]))] for i in range(len(self.np_image[:, 0]))], dtype=np.uint8)
            noisy_image = self.np_image * PeriodicNoise
            self.periodic_noisy_image = noisy_image
        if noisy_image is not None:
            fig4 = Figure(figsize=(4, 4))
            plot5 = fig4.add_subplot(111)
            plot5.imshow(noisy_image, cmap=plt.cm.gray)
            canvas = FigureCanvasTkAgg(fig4, master=self.frame4)
            canvas.draw()
            canvas.get_tk_widget().pack()
            toolbar = NavigationToolbar2Tk(canvas, self.frame4)
            toolbar.update()
            canvas.get_tk_widget().pack()

    def noise_removal(self) -> None:
        """Remove noise from the image using the selected method and display result."""
        for widget in self.frame5.winfo_children():
            widget.destroy()
        restored_image = None
        if self.removal_var.get() == 1 and self.sp_noisy_image is not None:
            restored_image = median(self.sp_noisy_image, disk(3))
        elif self.removal_var.get() == 2 and self.gaussian_noisy_image is not None:
            restored_image = gaussian(self.gaussian_noisy_image, sigma=1)
        elif self.removal_var.get() == 3 and self.periodic_noisy_image is not None:
            sos = butter(4, 0.125, output='sos')
            restored_image = sosfiltfilt(sos, self.periodic_noisy_image)
        if restored_image is not None:
            fig5 = Figure(figsize=(4, 4))
            plot6 = fig5.add_subplot(111)
            plot6.imshow(restored_image, cmap=plt.cm.gray)
            canvas = FigureCanvasTkAgg(fig5, master=self.frame5)
            canvas.draw()
            canvas.get_tk_widget().pack()
            toolbar = NavigationToolbar2Tk(canvas, self.frame5)
            toolbar.update()
            canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = Tk()
    app = ImageProcessingToolboxApp(root)
    root.mainloop()
