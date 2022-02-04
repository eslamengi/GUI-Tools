"""
Developers: the Three Heroes
    1- Eslam Ahmed Elsheikh // https://github.com/eslamengi
    2- Ahmed Abdelmoneim Elshazli 
    3- Ahmed Mostafa ElBaz // https://github.com/ahmed-elbaz
"""
#### Load needed packages

from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog #it provides interfaces to the native file dialogues 
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
from skimage import img_as_ubyte,img_as_float
from skimage import io, filters
from skimage import color
from skimage.filters import median
from skimage.filters import gaussian
from skimage.morphology import disk
from scipy import ndimage
from scipy.fftpack import fft , fft2 ,fftshift , ifftshift , ifft2
from scipy.signal import sosfiltfilt, butter
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow, show, subplot, title, get_cmap, hist
from skimage.color import rgb2gray, gray2rgb, rgb2hsv, rgb2lab, lab2rgb

#######################################################


root=Tk()
root.title('Image Processing (GUI ToolBox)')

#make icon in the tool bar
root.iconbitmap("E:/Image Processing Toolbox - GUI/Nile University icon.ico") 


#adding font option to apply it in gui
buttonFont = ft.Font(family='Arial', size=14, weight='bold')#, underline = 1)
entryFont = ft.Font(family='Tahoma', size=10, weight='bold')#, underline = 1)
functionfont = ft.Font(family='Arial', size=10, weight='bold', underline = 1)
rbuttonfont = ft.Font(family='Arial', size=10)#, weight='bold')#, underline = 1)


############################
# using frames help to use grid & pack methods together
###########################

frame1 = LabelFrame(root, padx = 10, pady=10) #padx,pady add padding inside the frame
#frame1.pack(padx=8, pady=8) #padx, pady in pack add padding outside the frame (around the frame)
frame1.grid(row=0, column=0)#, columnspan=3)
#frame1.configure(bg="#FAEBD7")
frame2 = LabelFrame(root, padx = 10, pady=10) #padx,pady add padding inside the frame
#frame2.pack(padx=8, pady=8) #padx, pady in pack add padding outside the frame (around the frame)
#frame2.configure(bg="green")
frame3 = LabelFrame(root, text = "Original Image",  padx = 10, pady=10) #padx,pady add padding inside the frame
#frame3.pack(padx=8, pady=8) #padx, pady in pack add padding outside the frame (around the frame)
#frame3.configure(bg="red")
frame4 = LabelFrame(root, text = "Image Processing Area 1",  padx = 10, pady=10) #padx,pady add padding inside the frame
#frame4.pack(padx=8, pady=8) #padx, pady in pack add padding outside the frame (around the frame)
#frame4.configure(bg="yellow")
frame5 = LabelFrame(root, text = "Image Processing Area 2",  padx = 10, pady=10) #padx,pady add padding inside the frame
#frame5.pack(padx=8, pady=8) #padx, pady in pack add padding outside the frame (around the frame)
#frame5.configure(bg="orange")
frame1.grid(row=0, column=0, columnspan=5)
frame2.grid(row=1, column=0, columnspan=5)
frame3.grid(row=2, column=0)#, columnspan=3)
frame4.grid(row=2, column=1)#, columnspan=3)
frame5.grid(row=2, column=2)#, columnspan=3)


cr = Label(root, text="Developed by:\n The Three Heroes\
           [Ahmed Abdelmoneim Elshazli, Ahmed Mostafa ElBaz, Eslam Ahmed Elsheikh]", bg="black", fg="white", padx=10, pady=10)#, font = entryFont)
cr.grid(row=3, column=0, columnspan=3)


###### Open Image file Function
def open_file():
    #make variable global to use it outside function
    global my_image
    global image_file
    global np_image
    global path
    global my_histogram_label
    global label1
    global image_size
    
    #clear widget space
    for widget in frame3.winfo_children():
        widget.destroy()
    #below only get the dile directory location it return  [filename, location]
    path = filedialog.askopenfilename(initialdir = "E:/", title = "select a file",\
                                              filetypes = (("jpg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*")) )
    #below will print file location path on GUI
    #label1 = Label(frame3, text=path).pack()
    
    #load the image
    img = Image.open(path)
    img = img.resize((250, 220))
    
    #below will open image in GUI
    my_image = ImageTk.PhotoImage(img)#Image.open(path))
    
    my_image_label = Label(frame3, image = my_image).pack()
    
    np_image = plt.imread(path)
    image_size = np_image.shape
    if len(image_size) == 3:
        np_image = rgb2gray(np_image)
    
##### new function to use graphs on tkinter
''' need our image to be in numpy format to be able to use it in matplotlib'''

def histogram():

    #clear widget space
    for widget in frame4.winfo_children():
        widget.destroy()
    # the figure that will contain the plot
    fig = Figure(figsize = (4,4))#, dpi = 100)   
    # adding the subplot
    plot1 = fig.add_subplot(111)
      
    #plotting the graph
    plot1.hist(np_image.ravel(), 512)
    plt.tight_layout()
    
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master = frame4)  
    canvas.draw()
    
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
    
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, frame4)
    toolbar.update()
    
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

##### histogram equalization function
def histogram_equal():

#clear widget space
    for widget in frame5.winfo_children():
        widget.destroy()
    
    # the figure that will contain the plot
    fig1 = Figure(figsize = (4,4))#, dpi = 100)   
    # adding the subplot
    plot2 = fig1.add_subplot(111)
    
    #histogram equalized image
    eq = np.asarray(equalize_hist(np_image))
    #plotting the graph
    plot2.hist(eq.ravel(), 512)
    plt.tight_layout()
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig1, master = frame5)  
    canvas.draw()
    
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
    
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, frame5)
    toolbar.update()
    
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

##### FFT Transform function
def fft_transform():
#clear widget space
    for widget in frame4.winfo_children():
        widget.destroy()

    y=fft2(np_image, (255,255))
    x1=fftshift(y)
    x2=np.abs(x1)
    x3 = 20*np.log(x2)
    #fft_label = Label(frame4, image = x3).pack()
   
    # the figure that will contain the plot
    fig2 = Figure(figsize = (4,4))#, dpi = 100)   
    # adding the subplot
    plot3 = fig2.add_subplot(111)
   
    #plotting the graph
    plot3.imshow(x3,'gray',vmin=0, vmax=255)
    
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig2, master = frame4)  
    canvas.draw()
    
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
    
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, frame4)
    toolbar.update()
    
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

###### Filter Function
def filter_selection():
    #clear widget space
    for widget in frame5.winfo_children():
        widget.destroy()
        
    if filter_var.get() == 1:
        filtered_image = filters.sobel(np_image)
    
    elif filter_var.get() == 2:
        filtered_image = filters.laplace(np_image)
    
    fig3 = Figure(figsize = (4,4))#, dpi = 100)   
    # adding the subplot
    plot4 = fig3.add_subplot(111)
    
    #plotting the graph
    plot4.imshow(filtered_image, cmap=plt.cm.gray)
    
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig3, master = frame5)  
    canvas.draw()
    
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
    
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, frame5)
    toolbar.update()
    
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()
    
##noise addition function    
def noise_selection():
    
    global sp_noisy_image
    global gaussian_noisy_image
    global periodic_noisy_image
    #clear widget space
    for widget in frame4.winfo_children():
        widget.destroy()
        
    if noise_var.get() == 1:
        noisy_image = random_noise(np_image, mode='s&p')
        sp_noisy_image = noisy_image
    
    elif noise_var.get() == 2:
        noisy_image = random_noise(np_image, mode='gaussian', seed=None, clip=True)
        gaussian_noisy_image = noisy_image
        
    elif noise_var.get() == 3:
        #Generate a 2D sine wave image with the same dimensions of the original image
        x = np.arange(len(np_image[0]))  # generate 1-D sine wave  
        y = np.sin(2 * np.pi * x / 5)  #Control the frequency
        y += max(y) # offset sine wave by the max value to go out of negative range of sine 

        PeriodicNoise = np.array([[y[j]*127 for j in range(len(np_image[0]))] for i in range(len(np_image[:,0]))], dtype=np.uint8) # create 2-D array of sine-wave
        
        noisy_image = np_image * PeriodicNoise
        periodic_noisy_image = noisy_image
        
    fig4 = Figure(figsize = (4,4))#, dpi = 100)   
    # adding the subplot
    plot5 = fig4.add_subplot(111)
 
    #plotting the graph
    plot5.imshow(noisy_image, cmap=plt.cm.gray)
    
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig4, master = frame4)  
    canvas.draw()
    
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
    
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, frame4)
    toolbar.update()
    
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()    
    
## noise removal function
def noise_removal():
    
    for widget in frame5.winfo_children():
        widget.destroy()
        
    if removal_var.get() == 1:
        # Apply median filter to the image with S & P noise
        restored_image = median(sp_noisy_image, disk(3))#, mode='constant', cval=0.0)
    
    elif removal_var.get() == 2:
        # Apply Gaussian filter to the image with Gaussian noise:
        restored_image = gaussian(gaussian_noisy_image, sigma=1)

    elif removal_var.get() == 3:
        # Create a lowpass Butterworth filter, and use it to filter the image with Periodic Noise
        sos = butter(4, 0.125, output='sos')
        restored_image = sosfiltfilt(sos, periodic_noisy_image)
    
    fig5 = Figure(figsize = (4,4))#, dpi = 100)   
    # adding the subplot
    plot6 = fig5.add_subplot(111)
     
    #plotting the graph
    plot6.imshow(restored_image, cmap=plt.cm.gray)
    
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig5, master = frame5)  
    canvas.draw()
    
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
    
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, frame5)
    toolbar.update()
    
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()  


###### creating variables for radio buttons

filter_var = IntVar()
noise_var = IntVar()
removal_var = IntVar()

###### Add Buttons in Frame 1
button_open = Button(frame1, text = "Open Image", bg="black", fg="grey", command=open_file, font=buttonFont, borderwidth=5, width=36)
button_hist = Button(frame1, text = "Image Histogram", bg ="#3D59AB", fg="white", command=histogram, font=entryFont, borderwidth=5, width=20)
button_FFT = Button(frame1, text = "FFT", bg = "#3D59AB", fg="white", width=10,command = fft_transform, font=entryFont, borderwidth=5)
button_hist_equal = Button(frame1, text = "Histogram Equalization", bg="#3D59AB" , fg="white", command=histogram_equal, font=entryFont, borderwidth=5, width=20)
#fg="#3D59AB"
button_open.grid(row=1, column=0, columnspan=3)
button_hist.grid(row=2, column=0)
button_FFT.grid(row=2, column=1)
button_hist_equal.grid(row=2, column=2) 

####### Add Labels & radio Buttons to frame2
Label(frame2, text = "Please select Filter", width=20, borderwidth=5, font= functionfont).grid(row=0, column=0)
Label(frame2, text = "Please select Noise Type", width=25, borderwidth=5, font= functionfont).grid(row=0, column=1)
Label(frame2, text= "Please select Noise removal filter",width=30,  borderwidth=5, font= functionfont).grid(row=0, column=2)

#filter buttons
rbutton_sobel = Radiobutton(frame2, text="Sobel", font=rbuttonfont,variable=filter_var,value=1,command=filter_selection)
rbutton_sobel.grid(row=1, column=0)
rbutton_laplace = Radiobutton(frame2, text="Laplace", font=rbuttonfont,variable=filter_var,value=2,command=filter_selection)
rbutton_laplace.grid(row=2, column=0)

#Noise Buttons
rbutton_sp = Radiobutton(frame2, text="S & P", font=rbuttonfont,variable=noise_var,value=1,command=noise_selection)
rbutton_sp.grid(row=1, column=1)
rbutton_Gauss = Radiobutton(frame2, text="Gaussian", font=rbuttonfont,variable=noise_var,value=2,command=noise_selection)
rbutton_Gauss.grid(row=2, column=1)
rbutton_periodic = Radiobutton(frame2, text="Periodic", font=rbuttonfont,variable=noise_var,value=3,command=noise_selection)
rbutton_periodic.grid(row=3, column=1)

#Noise removal Buttons
rbutton_notch = Radiobutton(frame2, text="Remove S&P", font=rbuttonfont,variable=removal_var,value=1,command=noise_removal)
rbutton_notch.grid(row=1, column=2)
rbutton_notch = Radiobutton(frame2, text="Remove Gaussian", font=rbuttonfont,variable=removal_var,value=2,command=noise_removal)
rbutton_notch.grid(row=2, column=2)
rbutton_notch = Radiobutton(frame2, text="Remove Periodic", font=rbuttonfont,variable=removal_var,value=3,command=noise_removal)
rbutton_notch.grid(row=3, column=2)


root.mainloop()
