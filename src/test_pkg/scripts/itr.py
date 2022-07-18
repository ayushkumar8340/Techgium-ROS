#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import Float32
from std_msgs.msg import Int16
from std_msgs.msg import String
import time
import json

data_segment=[-1,-1,-1,-1,-1,-1,-1,-1]
laser_data = LaserScan()
segment_data=Int16MultiArray()
distance=Float32()
building_height=-1
itr_var=Int16()
stop_data=dict()
count=0
def build_cb(msg):
    global building_height
    building_height=msg.data
    print(building_height)

def laser_cb(msg):
    global data_segment
    data_segment[2]=min(msg.ranges[850:904])

def stop_cb(msg):
    global stop_data
    stop_data=json.loads(msg.data)
def dist_cb(msg):
    global distance
    distance=msg
def lidar():
    global laser_data
    global data_segment
    global distance
    global itr_pub
    global itr_var
    global stop_data
    global count
    while not rospy.is_shutdown():
        if(building_height!=-1):
            if(distance.data>building_height and count==0):
                time.sleep(3)
                itr_var.data+=1
                itr_pub.publish(itr_var)
                count+=1
            if(data_segment[2]>0.1 and data_segment[2]<0.3 and distance.data<20):
                count=0

if __name__=="__main__":
    rospy.init_node("iteration_node",anonymous=True)
    rospy.Subscriber("/scan",LaserScan,laser_cb)
    rospy.Subscriber("/sonar_dist",Float32,dist_cb)
    rospy.Subscriber("/building_fixed",Float32,build_cb)
    rospy.Subscriber("/flag_stop",String,stop_cb)
    itr_pub=rospy.Publisher("/itr_pub",Int16,queue_size=1)
    lidar()