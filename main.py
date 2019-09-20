import cv2
import pyodbc

cam = cv2.VideoCapture(0);
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#insert/update data to sqlServer
def insertUpdate(Id, Name) :
    conn = pyodbc.connect(r'Driver={SQL Server};'
                          r'Server=DESKTOP-LVTN495\SQLEXPRESS;'
                          r'Database=FaceData;'
                          r'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cmd = "SELECT * FROM FaceData.dbo.People WHERE ID = '" +str(Id) + "'";
    cursor.execute(cmd)
    table = "FaceData.dbo.People"
    isRecordExist = 0;
    for row in cursor:
        isRecordExist = 1
    if (isRecordExist == 1):
        cmd = "UPDATE " + table + " SET Name = '" + str(Name) + "' Where ID = '" + str(Id) + "'"
    else:
        cmd = "INSERT INTO " + table + "(Id, Name) values ( '" + str(Id) + "', '" + str(Name) +"')"
    print(cmd)
    conn.execute(cmd)
    conn.commit()
    conn.close()

id = input('Enter your ID: ')
name = input('Enter your Name: ')
insertUpdate(id, name)
sampleNum = 0
while (True):
    #camera read
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    cv2.imshow('frame', img)
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
        cv2.imshow('frame', img)
        #incrementing sample number
        sampleNum = sampleNum + 1
        #saving the captured face in dataset folder
        cv2.imwrite("dataSet/User" + id + '.' + str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])


    #wait for 100 ms
    if (cv2.waitKey(100) & 0xFF == ord('q')):
        break
    #break if the samlple number is more than 20
    elif sampleNum > 100:
        print("saved 20 sample")
        break
cam.release()
cv2.destroyAllWindows()

