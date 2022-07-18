#!/usr/bin/env python3
from configparser import Interpolation
from tokenize import String
import rospy
import cv2
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import base64

rospy.init_node("video")
img_pub=rospy.Publisher("/express_video",String,queue_size=1)
def img_cb(msg):
    global img_pub
    global img_pub
    bridge=CvBridge()
    img=bridge.imgmsg_to_cv2(msg,"bgr8")
    img=cv2.resize(img,(420,326),interpolation=cv2.INTER_LINEAR)
    _,encoded=cv2.imencode(".jpeg",img)
    string_enc=base64.b64encode(encoded).decode('utf-8')
    img_pub.publish(string_enc)
    cv2.waitKey(1)


    
def control():
    
    rospy.Subscriber("/test_img",Image,img_cb)
    
    rospy.spin()



if __name__=="__main__":
    control()