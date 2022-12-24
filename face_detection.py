import cv2
import numpy as np
import face_recognition as facerec

def resize(img, size) :
  width = int(img.shape[1]*size)
  height = int(img.shape[0]*size)
  dimension = (width, height)
  return cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)


image = facerec.load_image_file('sample images/IMG-1357.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = resize(image, 0.50)
image_test = facerec.load_image_file('sample images/parvse.JPG')
image_test = cv2.cvtColor(image_test, cv2.COLOR_BGR2RGB)
image_test = resize(image_test, 0.50)

facelocation_image = facerec.face_locations(image)[0]
encode_image = facerec.face_encodings(image)[0]
cv2.rectangle(image, (facelocation_image[3], facelocation_image[0]), (facelocation_image[1], facelocation_image[2]), (255, 0, 255), 3)

facelocation_imagetest = facerec.face_locations(image_test)[0]
encode_imagetest = facerec.face_encodings(image_test)[0]
cv2.rectangle(image_test, (facelocation_imagetest[3], facelocation_imagetest[0]), (facelocation_imagetest[1], facelocation_imagetest[2]), (255, 0, 255), 3)

cv2.imshow('train', image)
cv2.imshow('test', image_test)
cv2.waitKey(0)
cv2.destroyAllWindows()