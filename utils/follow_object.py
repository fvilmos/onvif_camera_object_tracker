#########################################################
# Track targets on ONVIF camera
#
# Author: fvilmos
# https://github.com/fvilmos
##########################################################
from utils.dnnobjectdetect import DnnObjectDetect
from utils.kalman import clKalman
from utils.safethread import SafeThread
import threading

class FollowObject():
    ''' 
    Object follower class
    This class uses DNN object detection to find the target object
    and uses Kalman filter to smooth the movement of the camera.'''
    def __init__(self,callback_od, callback_nd, dnn_model,DEBUG=True):

        # initialize the object detector
        self.obj_det = dnn_model

        if not isinstance(self.obj_det, DnnObjectDetect):
            raise TypeError("dnn_model must be an instance of DnnObjectDetect")
            exit(1)
        
        self.img = None
        self.detections = None
        
        # callback function to call when the object is detected
        self.callback_obj_detected = callback_od

        # callback function to call when the object is detected
        self.callback_no_detection = callback_nd
        
        # Kalman estimators
        self.kf = clKalman()
        self.kfarea= clKalman()
        self.cx = 0
        self.cy = 0

        # target point to follow
        self.target_point = None
        self.DEBUG = DEBUG

        # processing frequency (to spare CPU time)
        self.cycle_counter = 1
        self.cycle_activation = 10

        # Kalman estimator scale factors
        self.kvscale = 10  
        self.khscale = 10

        # ticker for timebase
        self.ticker = threading.Event()

        # check if initialization is needed
        self.init_needed = True

        # start the worker thread
        self.wt = SafeThread(target=self.__worker).start()

    def set_activation_periodicity(self,period:int=100):
        """
        Set the activation period for the worker thread.
        This is the frequency at which the worker thread will process the image.
        :param period: int, the number of cycles after which the worker thread will process the image.
        """
        self.cycle_activation = period


    def init_tracker(self,img_w,img_h):
        """
        Initialize the Kalman filter with the image width and height.
        This is called once when the image size is known.
        :param img_w: int, the width of the image.
        :param img_h: int, the height of the image.
        """
        if self.init_needed == True:
            self.cx = img_w//2
            self.cy = img_h//2
            self.kf.init(self.cx,self.cy)
        else:
            self.init_needed = False
    
    def set_image(self, img):
        """
        Set the image to be processed by the worker thread.
        :param img: numpy array, the image to be processed.
        """
        self.img = img.copy()

    def get_image(self):
        """
        Get the image that is being processed by the worker thread.
        :return: numpy array, the image being processed.
        """
        return self.img

    def __worker(self):
            """
            Worker thread to process command / detections
            """
            # time base
            self.ticker.wait(0.05)  # wait for 50ms

            # process image
            if self.img is not None and self.cycle_counter % self.cycle_activation == 0:

                _, detections = self.obj_det.detect(self.img,size=[300, 300])

                if len(detections)>0:
                    #self.target_point = [detections[0][0] + detections[0][2]//2, detections[0][1] + detections[0][3]//2]
                    
                    # format: {"bbox":bbox, 'classId': classId, "tp": tp, 'confidence': conf}
                    self.detections = detections

                    for det in detections:
                        # get the center point of the detection
                        self.target_point = det['tp']

                        # process corrections, compute delta between two objects
                        _,cp = self.kf.predictAndUpdate(self.cx,self.cy,True)

                        # calculate delta over 2 axis
                        mvx = -int((cp[0][0]-self.target_point[0])//self.kvscale)
                        mvy = int((cp[1][0]-self.target_point[1])//self.khscale)

                        if self.DEBUG:
                            print (str(self.cycle_counter), mvx,mvy)
                        
                        if self.callback_obj_detected is not None:
                            self.callback_obj_detected(mvx,mvy)
                else:
                    # no detections, wait till next cycle
                    self.detections = None
                    self.img = None
                    if self.callback_no_detection is not None:
                        self.callback_no_detection()

            self.cycle_counter +=1
