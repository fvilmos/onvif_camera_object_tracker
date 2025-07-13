#########################################################
# Track targets on ONVIF camera
#
# Author: fvilmos
# https://github.com/fvilmos
##########################################################
from utils import config
from utils.config import Config
from utils.camera import Camera
from utils.discovery import *
from utils.move_camera import MoveCamera
from utils.follow_object import FollowObject
from utils.dnnobjectdetect import DnnObjectDetect

import cv2

######################
# main loop
######################
def loop(cam:Camera):

    def cb_follow(vx,vy):
        global target_color
        """ Callback function when the object is detected. """
        if Config.DEBUG:
            print ("vx,vy:", vx,vy)

        # move axes by axes to get more precision
        # x axes
        if vx < Config.MIN_POS_THRESHOLD:
            cam.move_ptz_camera(direction=cam.Directions.RIGHT,step_multiplier=1.0)
        elif vx > Config.MAX_POS_THRESHOLD:
            cam.move_ptz_camera(direction=cam.Directions.LEFT,step_multiplier=1.0)
        else:
            cam.move_ptz_camera(direction=cam.Directions.DEFAULT,step_multiplier=1.0)
        
        # y axes
        if vy < Config.MIN_POS_THRESHOLD:
            cam.move_ptz_camera(direction=cam.Directions.DOWN,step_multiplier=1.0)
        elif vy > Config.MAX_POS_THRESHOLD:
            cam.move_ptz_camera(direction=cam.Directions.UP,step_multiplier=1.0)
        else:
            cam.move_ptz_camera(direction=cam.Directions.DEFAULT,step_multiplier=1.0)
        
        if vx <=Config.MAX_POS_THRESHOLD and vx >= Config.MIN_POS_THRESHOLD and \
           vy <=Config.MAX_POS_THRESHOLD and vy >= Config.MIN_POS_THRESHOLD:
            target_color = [0,0,255]  # red
        else:
            target_color = [0,255,0]  # green
        
        #move_camera.reset_all_counters()  # reset the pacience counter and camera position counter
    
    def cb_no_detection():
        """ Callback function when no detection is made."""
        global target_color
        target_color = [0,255,0]  # green
        if Config.GUARDIAN == True:
            move_camera.update()  # update the camera position to search for the target object

    obj_dnn = DnnObjectDetect(
        MODEL=Config.MODEL,
        PROTO=Config.PROTO,
        CONFIDENCE=Config.CONFIDENCE,
        DETECT=Config.COCO_90_LABEL_TO_DETECT
    )
    
    # instantiate the follower object
    obj_follower = FollowObject(callback_od=cb_follow, callback_nd=cb_no_detection,dnn_model=obj_dnn, DEBUG=Config.DEBUG)

    # set startup mode
    if Config.GUARDIAN:
        # create the move camera object
        # pacience_limit is the number of frames to wait before moving the camera
        # if the target object is not detected for this many frames, the camera will be moved
        # to search for the target object
        # if the target object is detected, the camera will be moved to the target object
        move_camera = MoveCamera(camera=cam, pacience_limit=5)

    # initiate tracker, and object detector
    while True:

        if Config.USE_RTSP:
            ret, img = cap.read()
            if not ret:
                print("Failed to read from RTSP stream")
                break
            img = cv2.resize(img, Config.STREAM_RESIZE_TO)

        else:
            img = cam.get_snapshot_image()

        kk = cv2.waitKey(1)
        h,w = img.shape[0:2]
        
        # initialize the trackerand update image to process
        obj_follower.init_tracker(w,h)
        obj_follower.set_image(img)

        if Config.DEBUG:
            if kk == 27:
                break
            
            draw_target(img, color=target_color)

            if kk == ord('w'):
                cam.move_ptz_camera(cam.Directions.UP)
            
            if kk == ord('s'):
                cam.move_ptz_camera(cam.Directions.DOWN)
            
            if kk == ord('a'):
                cam.move_ptz_camera(cam.Directions.LEFT)
            
            if kk == ord('d'):
                cam.move_ptz_camera(cam.Directions.RIGHT)

        if Config.DEBUG:
            if obj_follower.detections is not None:
                draw_detections(img, obj_follower.detections, color=target_color)

            cv2.imshow('DEBUG', img)

    # on terminate, reset the camera position
    cam.move_ptz_camera_xy(0,0,step_multiplier=1.0)  # reset position
    if Config.DEBUG:
        cv2.destroyAllWindows()

def draw_target(img, offset:list=[0,0],color:list=[0,255,0]):
    h,w = img.shape[0:2]
    cv2.circle(img,(w//2+offset[0],h//2+offset[1]),10,color,2)

def draw_detections(img, detections:list, color:list=[0,255,0]):
    """
    Draw detections on the image.
    :param img: image to draw on
    :param detections: list of detections
    :param color: color of the bounding box
    """
    # format of detections: [{'bbox': (x,y,w,h), 'classId': classId, 'tp': [cx,cy,size], 'confidence': conf}, ...]
    for val in detections:
        bbox = val['bbox']
        name = Config.COCO_90_LABEL_TO_DETECT[val['classId']]  # get the class ID
        cv2.rectangle(img,(bbox[0],bbox[1]),(bbox[0]+bbox[2],bbox[1]+bbox[3]),color,2)
        cv2.putText(img, name, (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)



if __name__ == '__main__':
    img = None
    # target color
    target_color = [0,255,0] # green

    ips_ports = get_onvif_devices()
    ips, ports = get_ips_ports(ips_ports)

    print (ips,ports)

    # filter the one with a specific port (i.e. SR030 uses 6688)
    # for other cases use IP or index to select the right onvif camera
    try:
        indx = ports.index(Config.PORT)
        ip,port = ips[indx], ports[indx]
    except:
        # fallbacks to the 1st device
        ip,port = ips[0], ports[0]

    # we have now the port and IP address of the onvif camera let's use it
    print ("ip and port to use:",ip,port)

    if Config.IP == "":
        # if IP is empty, use auto-discovery
        cam_obj = Camera(ip,port=port, user=Config.USER, password=Config.PASS)
        if Config.USE_RTSP:
            # use RTSP stream
            Config.IP = ip
            cap = cv2.VideoCapture("rtsp://{USER}:{PASS}@{IP}:8554/profile0".format(USER=Config.USER, PASS=Config.PASS, IP=ip))
    else:
        cam_obj = Camera(config.IP,port=config.PORT,USER=Config.USER,PASS=Config.PASS)
        if Config.USE_RTSP:
            # use RTSP stream
            cap = cv2.VideoCapture(Config.rtsp_url)

    # start the camera loop
    loop(cam_obj)

    

