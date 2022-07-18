#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int16
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import Float32
from std_msgs.msg import String
import json

data_segment=[-1,-1,-1,-1,-1,-1,-1,-1]
segments=[0,0,0,0,0,0,-1,0]
laser_data = LaserScan()
segment_data=Int16MultiArray()
distance=Float32()
building_height=-1
flag=Int16()
stop_data=dict()
stop_var=-1
def dist_cb(msg):
    global distance
    distance=msg
def build_cb(msg):
    global flag
    flag=msg
def laser_cb(msg):
    global data_segment
    # itr_var=int((len(msg.ranges))/8)
    # data_segment[0]=min(min(msg.ranges[1076:1147]),min(msg.ranges[0:71]))
    # prev=71
    # for i in range(1,8):
    #     temp=itr_var*(i)
    #     data_segment[i]=min(msg.ranges[prev+2:temp])
    #     prev=temp
    data_segment[2]=min(msg.ranges[850:904])
def stop_cb(msg):
    global stop_data
    global stop_var
    stop_data=json.loads(msg.data)
    stop_var=stop_data['flag']

threshold_max_avg=0
threshold_min=0

def lidar_control():
    global laser_data
    global data_segment
    global segments
    global segment_pub
    global flag
    global building_height
    global distance
    global building_pub
    global build_fixed
    global stop_var
    while not rospy.is_shutdown():
        print(data_segment[2])
        if(flag.data==1):
            while True:
                if(data_segment[2]>=threshold_min and data_segment[2]<=threshold_max_avg):
                    print("building_may_be_present")
                elif(data_segment[2]>(0.1*threshold_max_avg+threshold_max_avg)):
                    building_height=distance.data
                    print("building ended")
                    build_fixed.publish(building_height)
                    
                    break
                building_pub.publish(distance.data)
            flag.data=0

        if(stop_var==0):
            print("here")
            build_fixed.publish(-1)
            building_height=0
            building_pub.publish(building_height)
            stop_var=-1

if __name__=="__main__":
    rospy.init_node("building_height")
    rospy.Subscriber("/scan",LaserScan,laser_cb)
    rospy.Subscriber("/sonar_dist",Float32,dist_cb)
    rospy.Subscriber("/building_flag",Int16,build_cb)
    segment_pub=rospy.Publisher("/lidar_segments",Int16MultiArray,queue_size=1)
    building_pub=rospy.Publisher("/building",Float32,queue_size=1)
    build_fixed=rospy.Publisher("/building_fixed",Float32,queue_size=1)
    rospy.Subscriber("/flag_stop",String,stop_cb)
    lidar_control()