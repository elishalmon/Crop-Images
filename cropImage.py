import cv2
import os
import numpy as np
import matplotlib.pyplot as plt


imagesFolder = ''
croppedFolder = ''
height = 500
width = 500
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (0, 0, 255)
averageCrop = []


def renameImages():

    '''
    Changes all the names of images to '1.png', '2.png' etc.
    '''

    for imageNumber, image in enumerate(os.listdir(imagesFolder)):
        full_path = os.path.join(imagesFolder, image)
        try:
            os.rename(full_path, imagesFolder + str(imageNumber + 1) + '.png')
        except FileExistsError:
            pass

def resizeImages():

    '''
    Resized all images to a uniform size,
    You can change the size with the variables 'height' and 'width
    at the top of the file
    '''

    for image in os.listdir(imagesFolder):
        img = cv2.imread(imagesFolder + image, 1)
        img = cv2.resize(img, (height, width), interpolation=cv2.INTER_AREA)
        isWritten = cv2.imwrite(imagesFolder + image, img)
        if not isWritten:
            print(image, ' Resized failded')


def addText(img, text, size, textY):

    '''
    Add text to display on image
    '''

    font = cv2.FONT_HERSHEY_SIMPLEX
    textSize = cv2.getTextSize(text, font, size, 1)[0]
    textX = int((img.shape[1] - textSize[0]) / 2)
    cv2.putText(img, text, (textX, textY), font, size, RED_COLOR, 2)
    return img


def updateImagePixelAverage(img):
    averageCrop.append(img.mean())


def calculateFFT():

    s = np.array(averageCrop)
    fft = np.fft.fft(s)
    fft = np.absolute(fft)
    plt.ylabel("Amplitude")
    plt.xlabel("Frequency [Hz]")
    plt.plot(fft)
    plt.show()


def preProcessing(imgFolder):

    '''
    Arranges and organizes the images
    '''

    global imagesFolder, croppedFolder
    imagesFolder = imgFolder
    croppedFolder = os.path.dirname(imagesFolder[:-1]) + '/cropped/'
    #croppedFolder = os.path.dirname(imagesFolder + 'cropped/')
    Images.amountOfImages = len(os.listdir(imagesFolder))
    renameImages()
    resizeImages()


class Images:

    currentImage = 0
    amountOfImages = 0
    startPoint = None
    endPoint = None

    def changeImage(self, request):

        '''
        Change the image to display according to the user request
        '''

        if request == 'next':
            self.currentImage += 1
            if self.currentImage > self.amountOfImages:
                self.currentImage = 1
        else:
            self.currentImage -= 1
            if self.currentImage == 0:
                self.currentImage = self.amountOfImages
        pathImage = imagesFolder + str(self.currentImage) + ".png"
        img = cv2.imread(pathImage, 1)
        img = addText(img, '<<< press \'a\'    {}/{}    press \'d\' >>>'.format(self.currentImage, self.amountOfImages), 0.65, height - 50)
        return img


    def dispalyPixel(self, pixel):

        '''
        Displays the pixel where the user clicked with the mouse in a format: (x, y, (r,g,b))
        '''

        pathImage = imagesFolder + str(self.currentImage) + ".png"
        img = cv2.imread(pathImage, 1)
        position = (pixel[0], pixel[1])
        cv2.putText(img, str(pixel), position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (209, 80, 0, 255), 1)
        return img


    def displayRectangleToCrop(self, startPoint, endPoint):

        '''
        Displays the square that the user marked with two points
        (the place where the user pressed the button and the place where the user released the button)
        '''

        pathImage = imagesFolder + str(self.currentImage) + ".png"
        img = cv2.imread(pathImage, 1)
        img = cv2.rectangle(img, startPoint, endPoint, (255, 0, 0), 2)
        img = addText(img, 'To crop all images press \'X\',', 0.65, height - 50)
        img = addText(img, 'To stop cropping anytime press \'S\'', 0.65, height - 25)
        return img

    def cropAllImages(self, startPoint, endPoint):

        '''
        Manages the image window while cropping,
        displays each image with the rectangle that is going to be cropped
        You can change the time at which each cropped image is displayed in line 174
        '''

        try:
            os.mkdir(croppedFolder)
        except FileExistsError:
            pass

        global averageCrop

        averageCrop = []
        for i in range(1, self.amountOfImages + 1):
            pathImage = imagesFolder + str(i) + ".png"
            img = cv2.imread(pathImage, 1)
            img = cv2.rectangle(img, startPoint, endPoint, (255, 0, 0), 2)
            img = addText(img, '{} images have already been cropped'.format(i), 0.65, 50)
            cv2.imshow('image', img)
            startY = startPoint[1]
            startX = startPoint[0]
            endY = endPoint[1]
            endX = endPoint[0]
            imageToCrop = cv2.imread(pathImage, 1)
            croppedImg = imageToCrop[startY:startY + endY - startY, startX:startX + endX - startX]
            updateImagePixelAverage(croppedImg)
            isWritten = cv2.imwrite(croppedFolder + '/' + str(i) + '.png', croppedImg)
            if not isWritten:
                print('error')
            k = cv2.waitKey(100) #change the time in ms
            if k == ord('s'):
                img = addText(img, 'Cropped has been terminated!', 0.65, 75)
                img = addText(img, 'For FFT graph press \'F\'', 0.65, 100)
                return img
        pathImage = imagesFolder + str(self.amountOfImages) + ".png"
        img = cv2.imread(pathImage, 1)
        img = addText(img, '{} images have already been cropped'.format(self.amountOfImages), 0.65, 50)
        img = addText(img, 'All images cropped successfully!', 0.65, 75)
        img = addText(img, 'For FFT graph press \'F\'', 0.65, 100)
        return img



