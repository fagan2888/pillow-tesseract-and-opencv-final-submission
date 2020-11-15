import zipfile
from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np


face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

images = {}
imgname_list = []


def unzip_images(zip_name):
    zip_file = zipfile.ZipFile(zip_name)
    for every in zip_file.infolist():
        images[every.filename] = [Image.open(zip_file.open(every.filename))]
        imgname_list.append(every.filename)
        
        
unzip_images('readonly/images.zip')

if __name__ == '__main__':
    for name in imgname_list:
        img = images[name][0]

        images[name].append(pytesseract.image_to_string(img).replace('-\n',''))

        if 'Mark' in images[name][1]:

            print('Results found in file',name)

            try:
                faces = face_cascade.detectMultiScale(np.array(img),1.35,4).tolist()

                images[name].append(faces)

                each_face = []

                for x,y,w,h in images[name][2]:
                    each_face.append(img.crop((x,y,x+w,y+h)))

                contact_sheet = Image.new(img.mode,(550,110*int(np.ceil(len(each_face)/5))))

                x = 0
                y = 0

                for face in each_face:
                    face.thumbnail((110,110))

                    contact_sheet.paste(face,(x,y))

                    if x + 110 == contact_sheet.width:
                        x = 0
                        y = y + 110
                    else:
                        x = x + 110

                display(contact_sheet)
            except:
                print('NO FACES IN FILE!!')
