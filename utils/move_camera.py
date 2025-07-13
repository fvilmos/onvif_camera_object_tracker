
####################################################
# Onvif camera calss, hadles snapshots and snapshots
#
# Author: fvilmos
# https://github.com/fvilmos
####################################################
from utils.camera import Camera    
import time

class MoveCamera():
    """
    Implements the guard functionality if no detection is made.
    This class will move the camera in a predefined pattern to search for the target object.
    """
    def __init__(self, camera:Camera, pacience_limit:int=5):
        self.camera = camera

        # pacience limit is the number of cycles to wait before moving the camera
        # if no detection is made
        # this is to avoid moving the camera too often
        # and to give the object detection time to find the target object
        self.pacience_limit = pacience_limit
        
        self.camera_step = 0.1  # step size for camera movement
        self.camera_max_step = 1.0  # maximum step size for camera movement

        self.camera_height_step = -0.1  # step size for camera movement
        self.camera_min_step = -1.0  # maximum step size for camera movement
        
        self.camera_position_counter = 0
        self.pacience_counter = 0
        self.reset_counter = 0
        self.camera_height_counter = 0

        # reset the camera position and pacience counter
        self.reset_camera()
        
    def reset_camera(self):
        """
        Reset the camera position and pacience counter.
        This is called when the camera is moved back to the initial position.
        """
        self.camera_position_counter = 0
        self.pacience_counter = 0
        self.reset_counter = 0

        # reset camera position
        self.camera.move_ptz_camera_xy(1.0,1.0,step_multiplier=1.0)
        self.camera.ptz.ContinuousMove(self.camera.move_request)
        time.sleep(8)  # wait for the camera to move
        self.camera.ptz.Stop({'ProfileToken': self.camera.move_request.ProfileToken,'PanTilt':True})

    def reset_all_counters(self):
        """
        Reset the pacience counter and camera position counter.
        This is called when the camera is moved back to the initial position.
        """
        self.pacience_counter = 0
        self.camera_position_counter = 0
        self.reset_counter = 0
        self.camera_height_counter = 0

    def update(self):
        """
        Update the camera position based on the pacience counter.
        :param cam: Camera object to move.
        """
        if self.pacience_counter < self.pacience_limit:
            self.pacience_counter += 1
        else:
            # reset the counter
            self.pacience_counter = 0

            # move camera 1 step to the right
            self.camera.move_ptz_camera(direction=self.camera.Directions.RIGHT, step_multiplier=1.0, wait_time=1.0)
            self.camera_position_counter += self.camera_step

            if self.camera_position_counter >= self.camera_max_step:
                self.reset_camera()  # reset the camera position if maximum step is reached
                time.sleep(2)  # wait for the camera to move

                # move camera to a new height
                if self.camera_height_counter > self.camera_min_step:
                    #self.camera.move_ptz_camera(direction=self.camera.Directions.DOWN, step_multiplier=1.0, wait_time=1.0)
                    self.camera_height_counter += self.camera_height_step
                    

                    if self.camera_height_counter < self.camera_min_step:
                        self.camera_height_counter = self.camera_min_step

                    # move camera with n steps down
                    self.camera.move_ptz_camera_xy(0.0,self.camera_height_counter, step_multiplier=1.0, wait_time=1.0 + abs(self.camera_height_counter)* 10.0)
                else:
                    # reset the camera height counter
                    self.camera_height_counter = 0.0
