#!/usr/bin/env python3
from configparser import Interpolation
import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
def control():
    rospy.init_node("test")
    bridge=CvBridge()
    pub=rospy.Publisher("/test_img",Image,queue_size=1)
    vid=cv2.VideoCapture(0)
    rate=rospy.Rate(100)
    while not rospy.is_shutdown():
        _,frame=vid.read()
        resized_frame=cv2.resize(frame,(650,500),interpolation=cv2.INTER_LINEAR)
        img=bridge.cv2_to_imgmsg(resized_frame,"bgr8")
        pub.publish(img)
        rate.sleep()

if __name__=="__main__":
    control()