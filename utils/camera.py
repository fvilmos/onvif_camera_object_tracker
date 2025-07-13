####################################################
# Onvif camera calss, hadles snapshots and snapshots
#
# Author: fvilmos
# https://github.com/fvilmos
####################################################

from onvif import ONVIFCamera

import requests
import cv2
import numpy as np
import time


##################################################
# create the onvif camera object with ptz service
##################################################
class Camera:
    class Directions:
        UP = [0,0.01]
        DOWN = [0,-0.01]
        LEFT = [0.01,0]
        RIGHT = [-0.01,0]
        DEFAULT = [0,0]

    def __init__(self,ip,port,user,password):
        try:
            self.cam = ONVIFCamera(ip, port, user, password)
            self.media = self.cam.create_media_service()
            self.ptz = self.cam.create_ptz_service()
            self.move_request = self.__get_ptz_moverequest()
            self.sapshot_url = self.__get_snapshot_url()
        except Exception as e:
            print(f"Error initializing camera: {e}")
            exit(1)
        
    def __get_ptz_moverequest(self):
        # create service
        move_request = self.ptz.create_type('ContinuousMove')
        move_request.ProfileToken = self.media.GetProfiles()[0].token
        if move_request.Velocity is None:
            move_request.Velocity = self.ptz.GetStatus({'ProfileToken': move_request.ProfileToken}).Position
        
        return move_request

    def __get_snapshot_url(self):
        # return the url for snapshots
        return self.media.GetSnapshotUri(self.move_request.ProfileToken)['Uri']
    
    def get_snapshot_image(self):
        try:
            # get image from snapshot url
            data = requests.get(self.sapshot_url).content

            b_img = bytearray(data)
            np_array = np.asarray(b_img, dtype=np.uint8)
            img = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
        except:
            print("Error getting snapshot image")
            img = None

        return img
    
    def move_ptz_camera(self,direction:Directions=Directions.DEFAULT,step_multiplier=1.0,wait_time=0.0):
        self.move_request.Velocity.PanTilt.x = direction[0] * step_multiplier
        self.move_request.Velocity.PanTilt.y = direction[1] * step_multiplier

        self.ptz.ContinuousMove(self.move_request)
        if wait_time > 0:
            time.sleep(wait_time)
        self.ptz.Stop({'ProfileToken': self.move_request.ProfileToken,'PanTilt':True})

    def move_ptz_camera_xy(self,x,y,step_multiplier=1.0, wait_time=0.0):
        self.move_request.Velocity.PanTilt.x = x * step_multiplier
        self.move_request.Velocity.PanTilt.y = y * step_multiplier

        self.ptz.ContinuousMove(self.move_request)
        if wait_time > 0:
            time.sleep(wait_time)
        self.ptz.Stop({'ProfileToken': self.move_request.ProfileToken,'PanTilt':True})

    def get_min_max_pan_tilt(self):
        request = self.ptz.create_type('GetConfigurationOptions')
        request.ConfigurationToken = self.media.GetProfiles()[0].PTZConfiguration.token

        # get the min and max pan and tilt values
        ptz_configuration_options = self.ptz.GetConfigurationOptions(request)
        
        x_range = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange
        y_range = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange
        
        return (x_range.Min, x_range.Max, y_range.Min, y_range.Max)