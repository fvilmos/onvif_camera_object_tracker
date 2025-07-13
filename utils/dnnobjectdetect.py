#########################################################
# Track targets on ONVIF camera
#
# Author: fvilmos
# https://github.com/fvilmos
##########################################################

import cv2
import numpy as np

class DnnObjectDetect():
    """
    Using a Dnn model to detect face

    """
    def __init__(self, MODEL='./data/frozen_inference_graph.pb', PROTO='./data/ssd_mobilenet_v2_coco_2018_03_29.pbtxt', CONFIDENCE=0.8, DETECT={1: 'person'}):
        """
        init function 
        Args:
            MODEL (str, optional): caffemodel. Defaults to './data/frozen_inference_graph.pb'.
            PROTO (str, optional): prototxt. Defaults to './data/ssd_mobilenet_v2_coco_2018_03_29.pbtxt'.
            DETECT (str, optional): Type of object to be detected ['Face', 'Person']. Default is 'Face'.
        """     

        self.network = cv2.dnn.readNetFromTensorflow(MODEL,PROTO)    

        self.type = DETECT
        self.confidence = CONFIDENCE

    def detect(self,img, size=(300,300)):
        """
        Detect the face
        Args:
            img ([type]): image

        Returns:
            [type]: list of detected faces
        """

        detections = []
        tp =[]
        h,w = img.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(img,size))
        self.network.setInput(blob)

        det = self.network.forward()
        for d in det:
            conf = d[0,0,2]

            # process just high confidence detections
            if conf > self.confidence:
                classId = int(d[0, 0, 1])

                print ("classId:", classId)

                if classId in self.type:
                    for id in list(self.type.keys()):
                        if classId == int(id):
                            # calculate bounding box
                            bbox = (d[0,0,3:7]* np.array([w,h,w,h])).astype(int)
                            bbox = (bbox[0],bbox[1],bbox[2]-bbox[0],bbox[3]-bbox[1])

                            # calculate center point
                            tp = [bbox[0] + bbox[2]//2, bbox[1] + bbox[3]//2, bbox[3]]                       
                            detections.append({"bbox":bbox, 'classId': classId, "tp": tp, 'confidence': conf})

        return tp, detections

    def draw_detections(self,det,img,COLOR=[0,255,0]):
        """
        Draw detections

        Args:
            det ([type]): list of detected faces
            img ([type]): image
            COLOR (list, optional): box color. Defaults to [0,255,0].
        """

        for val in det:
            cv2.rectangle(img,(val[0],val[1]),(val[0]+val[2],val[1]+val[3]),COLOR,2)


    def detect_and_draw(self,img):
        """
        Draw detection on an image
        Args:
            img ([type]): image to draw the detections
        """
        det = self.detect(img)
        self.draw_detections(det,img)