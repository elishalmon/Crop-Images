import cv2
import cropImage
from cropImage import Images
from tkinter import *
from tkinter import filedialog


imagesObj = Images()
startPoint = endPoint = pixel = None
croppedClickFlag = imagesCropped = False
BLACK_COLOR = (255, 0, 0)
height = 500
width = 500


def startImagesDisplay():

    '''
    This function manages the image viewer window
    '''

    global croppedClickFlag, imagesCropped

    def mouse_callback(event, x, y, flags, params):

        '''
        Monitoring user clicks with the mouse on the image
        '''

        global pixel, startPoint, endPoint, croppedClickFlag

        if event == cv2.EVENT_LBUTTONDOWN:
            croppedClickFlag = False
            b, g, r = (img[x, y])
            pixel = (x, y, (r, g, b))
            imgT = imagesObj.dispalyPixel(pixel)
            cv2.imshow('image', imgT)
            startPoint = (x, y)

        if event == cv2.EVENT_LBUTTONUP:
            endPoint = (x, y)
            if startPoint[0] != endPoint[0] and startPoint[1] != endPoint[1]:
                imgT = imagesObj.displayRectangleToCrop(startPoint, endPoint)
                croppedClickFlag = True
                cv2.imshow('image', imgT)


    # Display the first image
    img = imagesObj.changeImage('next')
    cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback('image', mouse_callback)
    cv2.imshow('image', img)

    while True:

        '''
        Monitoring user presses on the keyboard
        '''

        k = cv2.waitKeyEx(0) & 0xFF
        if k == ord('a') or k == ord('d'):
            if k == ord('a'):
                request = 'prev'
            else:
                request = 'next'
            croppedClickFlag = False
            img = imagesObj.changeImage(request)
            if img is not None:
                cv2.imshow('image', img)
        elif k == ord('x') and croppedClickFlag:
            img = imagesObj.cropAllImages(startPoint, endPoint)
            cv2.imshow('image', img)
            imagesCropped = True
        elif k == ord('f') and imagesCropped:
            cropImage.calculateFFT()
        elif k == 27 or k == 255:
            break
    cv2.destroyAllWindows()


def start():

    root = Tk()

    def browseFunc():
        dirPath = filedialog.askdirectory()
        if len(dirPath) > 0:
            dirPath += '/'
            cropImage.preProcessing(dirPath)
            startImagesDisplay()

    root.geometry("500x400")
    browseLabel = Label(root, text="Hello! Please browse an images folder", padx=20, pady=100, font=("Helvetica", 16))
    browseLabel.pack()
    browseButton = Button(root, text="Browse", padx=75, font=("Helvetica", 16), command=browseFunc)
    browseButton.pack()

    root.mainloop()

if __name__ == '__main__':
    start()
