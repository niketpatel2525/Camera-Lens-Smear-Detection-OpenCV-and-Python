import cv2
import numpy as np
import os
import glob
from random import randint
import sys

minRadius = 10
maxRadius = 12
minArea = 3.14 * minRadius**2
maxArea = 3.14 * maxRadius**2


def isSmearDetected(src):
    # store all image list in the list
    data= glob.glob(src+"/*.jpg")
    total_data_len = len(data)

    # find mean of all pixel values of all images
    meanByPixel = np.zeros((500,500,3),np.float)
    progressBar = 0
    lastProg = 0
    for img in data:
        curr_image = cv2.imread(img)
        # resize all images to the same size i.e. 500x500
        resize_curr_image = cv2.resize(curr_image,(500,500))
        resize_curr_image = cv2.medianBlur(resize_curr_image,5)
        i = np.array(resize_curr_image,dtype=np.float)
        meanByPixel += i

        # progress bar that updates at every 10%
        progress = ((progressBar) * 100) / total_data_len
        if progress >= lastProg:
            print ("Progress: "+str(progress) + "%")
            lastProg +=10
        progressBar += 1


    meanByPixel = meanByPixel /total_data_len
    # write mean image to the disk.
    cv2.imwrite("Mean_"+src.split('/')[1]+".jpg", meanByPixel)


    meanByPixel = np.array(np.round(meanByPixel),dtype=np.uint8)

    # convert mean image to grayscale means BGR -- > GRAY ( 3 pixel value to 1D pixel value )
    grayMeanImage = cv2.cvtColor(meanByPixel, cv2.COLOR_BGR2GRAY)

    # find ThresholdImage by using adaptiveThreshold method
    thresholdImage = cv2.adaptiveThreshold(grayMeanImage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 105, 11)

    # find invert image which will act as mask
    mask = cv2.bitwise_not(thresholdImage)

    # save mask to the disk
    cv2.imwrite("Mask_"+src.split('/')[1]+".jpg",mask)


    # read random image from the directory to detect the smear
    read = data[randint(0,total_data_len)]
    readImage = cv2.imread(read)
    resizedRead = cv2.resize(readImage,(500,500))
    cv2.imshow('Apply Mask', resizedRead)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    # find contours on mask image
    _,contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # if contours is size of smear then locate it on our randomly piced image
        if(cv2.contourArea(contours[0])>minArea and cv2.contourArea(contours[0])<maxArea):
            # draw contours around smear on original image
            result = cv2.drawContours(resizedRead,contours,-1,(0,255,255),2)

            # save the image to the disk.
            cv2.imwrite("final_"+src.split('/')[1]+".jpg",resizedRead)
            cv2.imshow("Final Result",result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return True


    return False


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args[0]:
        print ("Directory is invalid")
        sys.exit()

    print("Directory Found. \n Smear Dectection in Progress...")
    if(isSmearDetected(args[0])):
        print ("Smear is detected for "+args[0]+" source.")
    else:
        print("No Smear in "+ args[0])
