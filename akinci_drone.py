import cv2
import time
import RPi.GPIO as GPIO        

kamera = cv2.VideoCapture(0)
ret, frame = kamera.read()
cisimAlgilama = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_mcs_upperbody.xml')

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT) #lazer pin
GPIO.setup(18, GPIO.OUT) #sag sol servo pin
GPIO.setup(17, GPIO.OUT) #asagi yukari servo pin
pwm1 = GPIO.PWM(18, 50) #sagsol servo nesnesi olusturuldu
pwm1.start(6)           #sag-sol servo 90 dereceden basliyor
pwm2 = GPIO.PWM(17, 50) #asagi yukari servo nesnesi
pwm2.start(8)          #asagi yukari servo baslangic pozisyonu 
genis = 160 #goruntu genisligi tanimlamasi    
yuk = 120  #goruntu yuksekligi tanimlamasi

#lazeri acma ve kapama fonksiyonlari

def lazerAc():
    
    GPIO.setup(23, GPIO.OUT) #lazer acildi

def lazerKap():

    GPIO.setup(23, GPIO.IN) #lazer kapatildi


lazerKap() #lazer baslangic olarak kapali durumda

#servoyu gerekli aciya gondermek icin x ve y matrisleri olusturuldu

xmatris = []
i = 0
for i in range(genis):
        
        if i>=0 and i<genis/10:
            xmatris.append(55)
        elif i>=genis/10 and i<2*(genis/10):
            xmatris.append(60)
        elif i>=2*(genis/10) and i<3*(genis/10):
            xmatris.append(65)
        elif i>=3*(genis/10) and i<4*(genis/10):
            xmatris.append(70)
        elif i>=4*(genis/10) and i<5*(genis/10):
            xmatris.append(75)
        elif i>=5*(genis/10) and i<6*(genis/10):
            xmatris.append(80)
        elif i>=6*(genis/10) and i<7*(genis/10):
            xmatris.append(85)
        elif i>=7*(genis/10) and i<8*(genis/10):
            xmatris.append(90)
        elif i>=8*(genis/10) and i<9*(genis/10):
            xmatris.append(95)
        elif i>=9*(genis/10) and i<10*(genis/10):
            xmatris.append(100)
            
ymatris = []
j= 0
for j in range(yuk):
        
        if j>=0 and j<yuk/10:
            ymatris.append(144)
        elif j>=yuk/10 and j<2*(yuk/10):
            ymatris.append(140)
        elif j>=2*(yuk/10) and j<3*(yuk/10):
            ymatris.append(136)
        elif j>=3*(yuk/10) and j<4*(yuk/10):
            ymatris.append(132)
        elif j>=4*(yuk/10) and j<5*(yuk/10):
            ymatris.append(128)
        elif j>=5*(yuk/10) and j<6*(yuk/10):
            ymatris.append(124)
        elif j>=6*(yuk/10) and j<7*(yuk/10):
            ymatris.append(120)
        elif j>=7*(yuk/10) and j<8*(yuk/10):
            ymatris.append(116)
        elif j>=8*(yuk/10) and j<9*(yuk/10):
            ymatris.append(112)
        elif j>=9*(yuk/10) and j<10*(yuk/10):
            ymatris.append(108)

#lazeri goruntude algilanan alanin orta noktasina gonderen fonksiyon

def lazer(x,y):
    
    degis=1./18.*(xmatris[x]) + 1
    pwm1.ChangeDutyCycle(degis)    
    degis2=1./18.*(ymatris[y]) + 1
    pwm2.ChangeDutyCycle(degis2)
    lazerAc()
    time.sleep(0.5)
    lazerKap()

#goruntu isleme ve algilama baslangici
#sonsuz dongu
while True:
    #kare kare inceleme
    ret, frame = kamera.read()
    frame = cv2.resize(frame, (genis,yuk), fx=0.5, fy=0.5)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cisim = cisimAlgilama.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    
    

#algilanan cisim etrafinda dikdortgen ciziliyor
    for (x, y, w, h) in cisim:
    
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        ox = x+w/2
        oy = y+h/2
        print(ox,oy)
        lazer(ox,oy)
        
    #sonucun kullaniciya gosterilmesi
    cv2.imshow('Video', frame ) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#her sey bittiginde (q) ya basildiginda programi sonlandiriyoruz
GPIO.setup(23, GPIO.IN) 
GPIO.cleanup()
kamera.release()
cv2.destroyAllWindows()
