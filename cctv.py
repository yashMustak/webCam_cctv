#import numpy as np
import cv2
import sys
import os
import time
import smtplib
import config
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

face_cascade = cv2.CascadeClassifier("haarCascadeFaceF.xml")
mailto = "srivastavayash1234@gmail.com"
msg = MIMEMultipart()
msg["Subject"] = "Laptop theft warning"
msg["From"] = config.emailaddress
msg["To"] = mailto
mailServer = smtplib.SMTP('smtp.gmail.com' , 587)
mailServer.starttls()
mailServer.login(config.emailaddress , config.emailpassword)

temp_folder = "faces"
count = 0

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.5, 5)
    for (x,y,w,h) in faces:
        count = count + 1
        roi_f = gray[y:y+h, x:x+w]
        cv2.imwrite(os.path.join("face"+str(count)+".png"), img)
        image_data = open("face"+str(count)+".png", 'rb').read()
        text = MIMEText("Someone is in your room!!")
        msg.attach(text)
        image = MIMEImage(image_data, name = os.path.basename("face"+str(count)+".png"))
        msg.attach(image)
        mailServer.sendmail(config.emailaddress, mailto, msg.as_string())
        print("mail sent!")

    cv2.imshow("img", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

mailServer.quit()
cv2.destroyAllWindows()
cap.release()
        
        
