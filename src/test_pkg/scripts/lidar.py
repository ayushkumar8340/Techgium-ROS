#!/usr/bin/env python3

from distutils.log import warn
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import Int16
import time
data_segment=[-1,-1,-1,-1,-1,-1,-1,-1]
segments=[0,0,0,0,0,0,-1,0]
laser_data = LaserScan()
segment_data=Int16MultiArray()


def laser_cb(msg):
    global data_segment
    itr_var=int((len(msg.ranges))/8)
    data_segment[0]=min(min(msg.ranges[1076:1147]),min(msg.ranges[0:71]))
    prev=71
    for i in range(1,8):
        temp=itr_var*(i)
        data_segment[i]=min(msg.ranges[prev+2:temp])
        prev=temp

def lidar_control():
    global laser_data
    global data_segment
    global segments
    global segment_pub
    global warning_pub
    while not rospy.is_shutdown():
        for i in range(8):
            if(data_segment[i]<0.15 and data_segment[i]>-1):
                segments[i]=2
            elif(data_segment[i]>0.16 and data_segment[i]<0.2):
                segments[i]=1 
            else:
                segments[i]=0
        if(data_segment[0]<0.13 or data_segment[1]<0.13 or data_segment[2]<0.13 or data_segment[3]<0.13 or data_segment[4]<0.13 or data_segment[5]<0.13 or data_segment[6]<0.13 or data_segment[7]<0.13):
            warning_pub.publish(1)
        else:
            warning_pub.publish(0)
            
        segment_data.data=segments
        segment_pub.publish(segment_data)
if __name__=="__main__":
    rospy.init_node("laser_scan_crane")
    rospy.Subscriber("/scan",LaserScan,laser_cb)
    segment_pub=rospy.Publisher("/lidar_segments",Int16MultiArray,queue_size=10)
    warning_pub=rospy.Publisher("/lidar_warning",Int16,queue_size=1)
    lidar_control()