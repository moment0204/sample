import cv
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(13,GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(15,GPIO.OUT, initial=GPIO.HIGH)

color_tracker_window = "Color Tracker"

class ColorTracker:
    
    def __init__(self):
        cv.NamedWindow( color_tracker_window,1)
        self.capture = cv.CaptureFromCAM(0)

    def run(self):
        while True:
            img = cv.QueryFrame( self.capture)

            cv.Smooth(img,img,cv.CV_BLUR,3);

            hsv_img = cv.CreateImage(cv.GetSize(img),8,3)
            cv.CvtColor(img,hsv_img,cv.CV_BGR2HSV)

            thresholded_img = cv.CreateImage(cv.GetSize(hsv_img),8,1)
            cv.InRangeS(hsv_img,(0,150,150),(25,255,255),thresholded_img)

            moments = cv.Moments(cv.GetMat(thresholded_img,1),0)
            area = cv.GetCentralMoment(moments,0,0)

            if(area > 100000):
                x = cv.GetSpatialMoment(moments,1,0)/area
                y = cv.GetSpatialMoment(moments,0,1)/area

                overlay = cv.CreateImage(cv.GetSize(img),8,3)

                cv.Circle(img,(int(x),int(y)),2,(255,255,255),20)
                cv.Add(img,overlay,img)

                cv.Merge(thresholded_img,None,None,None,img)
                
                GPIO.output(11,GPIO.LOW)
            else:
                GPIO.output(11,GPIO.HIGH)

            if(area > 1000):
                x = cv.GetSpatialMoment(moments,1,0)/area
                y = cv.GetSpatialMoment(moments,0,1)/area

                overlay = cv.CreateImage(cv.GetSize(img),8,3)

                cv.Circle(img,(int(x),int(y)),2,(255,255,255),20)
                cv.Add(img,overlay,img)

                cv.Merge(thresholded_img,None,None,None,img)
                
                GPIO.output(13,GPIO.LOW)
            else:
                GPIO.output(13,GPIO.HIGH)

            if(area > 10000):
                x = cv.GetSpatialMoment(moments,1,0)/area
                y = cv.GetSpatialMoment(moments,0,1)/area

                overlay = cv.CreateImage(cv.GetSize(img),8,3)

                cv.Circle(img,(int(x),int(y)),2,(255,255,255),20)
                cv.Add(img,overlay,img)

                cv.Merge(thresholded_img,None,None,None,img)
                
                GPIO.output(15,GPIO.LOW)
            else:
                GPIO.output(15,GPIO.HIGH)

            cv.ShowImage(color_tracker_window,img)

            if cv.WaitKey(10) ==27:
                break

if __name__=="__main__":
    color_tracker = ColorTracker()
    color_tracker.run()
