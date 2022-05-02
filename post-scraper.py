from asyncio import get_running_loop
import cv2
import os

#clean up the scraped image directories
#lint up the folder by file size, amount of faces recognized

def GetNumFaces(imagePath):
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30,30),
        )

    return len(faces)

def main():
    directory = "Images/Zendaya"
    dirtyFileCount = 0
    allFileCount = 0
    cleanFileCount = 0

    for fileName in os.listdir(directory):
        f = os.path.join(directory, fileName)
        split = fileName.split('.')
        extension = split[1]
        allFileCount+=1
        if (GetNumFaces(f) == 0 or GetNumFaces(f) > 1):
            dirtyFileCount+=1 
            os.remove(f)
        else:
            os.rename(f, os.path.join(directory, str(cleanFileCount) + "." + extension))
            cleanFileCount+=1

    
    print(str(dirtyFileCount) + "/" + str(allFileCount) + " images were removed.")
        
    

            

main()

    


