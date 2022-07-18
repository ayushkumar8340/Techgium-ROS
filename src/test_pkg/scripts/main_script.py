#!/usr/bin/env python3
import math
import rospy
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import Int16
import time
import json
import xlsxwriter

data_send=String()
lidar_segments=[0,0,0,0,0,0,0,0]
profile_flag=-1
start_flag=-1
stop_flag=-1
start_time=0
stop_time=0
acc_x=0
acc_y=0
data_frame={
    "a1": 0,
    "b1": 0,
    "c1": 0,
    "d1": 0,
    "e1": 0,
    "f1": 0,
    "g1": 0,
    "h1": 0,
    "quad":0, 
    "building_height": 0, 
    "active_height": 0,   
    "speed": 0,
    "speed_x":0,              
    "speed_y":0,
    "speed_z":0,
    "distance":0,           
    "iteration":0,         
    "longitude": 0,        
    "latitude": 0,
    "acceleration_x": 2,     
    "acceleration_y": 0,
    "acceleration_z": 0,
    "jerk_warning": 0,
    "collision_warning": 0,
    "human_detection": 0,
    "rotate_warning": 0,
    "nodes": 0,
    "jerk_x": 0,
    "jerk_y": 0,
    "jerk_z": 0
}

def data_cb(msg):
    global lidar_segments
    for i in range(8):
        lidar_segments[i]=msg.data[i]
def dist_cb(msg):
    global data_frame
    data_frame["active_height"]=msg.data
def build_cb(msg):
    global data_frame
    data_frame["building_height"]=msg.data
def accX_cb(msg):
    global acc_x
    global data_frame
    data_frame["acceleration_x"]=msg.data
    acc_x=msg.data/100
def accY_cb(msg):
    global data_frame
    global acc_y
    data_frame["acceleration_y"]=msg.data
    acc_y=msg.data/100
def accZ_cb(msg):
    global data_frame
    data_frame["acceleration_z"]=msg.data
def jerkX_cb(msg):
    global data_frame
    data_frame["jerk_x"]=msg.data
    data_frame["jerk_warning"]=msg.data
    
def jerkY_cb(msg):
    global data_frame
    data_frame["jerk_y"]=msg.data
    data_frame["jerk_warning"]=msg.data 
      
def jerkZ_cb(msg):
    global data_frame
    data_frame["jerk_z"]=msg.data
    data_frame["jerk_warning"]=msg.data

def human_cb(msg):
    global data_frame
    data_frame["human_detection"]=msg.data

def rot_cb(msg):
    global data_frame
    data_frame["quad"]=msg.data

def itr_cb(msg):
    global data_frame
    data_frame["iteration"]=msg.data

def lidar_warn_cb(msg):
    global data_frame
    data_frame["collision_warning"]=msg.data  
def rot_warning_cb(msg):
    global data_frame
    data_frame["rotate_warning"]=msg.data
def profile_cb(msg):
    global profile_flag
    data=json.loads(msg.data)
    profile_flag=data["flag"]
def start_cb(msg):
    global start_flag
    global building_flag
    data=json.loads(msg.data)
    start_flag=data["flag"]
    building_flag.publish(1)
    building_flag.publish(1)
    print("here")
def data_saver():
    pass
def stop_cb(msg):
    global stop_flag
    data=json.loads(msg.data)
    stop_flag=data["flag"]
def rotX_cb(msg):
    global data_frame
    data_frame["speed_x"]=msg.data

def rotY_cb(msg):
    global data_frame
    data_frame["speed_y"]=msg.data

def rotZ_cb(msg):
    global data_frame
    data_frame["speed_z"]=msg.data

def control():
    global lidar_segments
    global profile_flag
    global start_flag
    global stop_flag

    global start_time
    global stop_time
    global acc_x
    global acc_y
    
    rospy.Subscriber("/lidar_segments",Int16MultiArray,data_cb)
    rospy.Subscriber("/sonar_dist",Float32,dist_cb)
    rospy.Subscriber("/building",Float32,build_cb)
    rospy.Subscriber("/accX",Int16,accX_cb)
    rospy.Subscriber("/accY",Int16,accY_cb)
    rospy.Subscriber("/accZ",Int16,accZ_cb)
    rospy.Subscriber("/jerkX",Int16,jerkX_cb)
    rospy.Subscriber("/jerkY",Int16,jerkY_cb)
    rospy.Subscriber("/jerkZ",Int16,jerkZ_cb)
    rospy.Subscriber("/human",Int16,human_cb)
    rospy.Subscriber("/rotation_arrow",Int16,rot_cb)
    rospy.Subscriber("/itr_pub",Int16,itr_cb)
    rospy.Subscriber("/lidar_warning",Int16,lidar_warn_cb)
    rospy.Subscriber("/rot_warning",Int16,rot_warning_cb)
    rospy.Subscriber("/profile_flag",String,profile_cb)
    rospy.Subscriber("/ros_start",String,start_cb)
    rospy.Subscriber("/flag_stop",String,stop_cb)
    rospy.Subscriber("/rotX",Int16,rotX_cb)
    rospy.Subscriber("/rotY",Int16,rotY_cb)
    rospy.Subscriber("/rotZ",Int16,rotZ_cb)
    data_pub=rospy.Publisher("/express",String,queue_size=10)
    rate=rospy.Rate(30)
    while not rospy.is_shutdown():
        data_frame["speed"]=math.sqrt(acc_x**2+acc_y**2)
        data_frame["a1"]=lidar_segments[7]
        data_frame["b1"]=lidar_segments[6]
        data_frame["c1"]=lidar_segments[5]
        data_frame["d1"]=lidar_segments[4]
        data_frame["e1"]=lidar_segments[3]
        data_frame["f1"]=lidar_segments[2]
        data_frame["g1"]=lidar_segments[1]
        data_frame["h1"]=lidar_segments[0]
        data_send.data=json.dumps(data_frame)
        data_pub.publish(data_send)
        data_saver()
        if(start_flag==1):
            #start_time_note
            pass
        if(stop_flag==1):
            #stop time note
            pass
        if(profile_flag==1):
        #show data
           pass 
        rate.sleep()

if __name__=="__main__":
    rospy.init_node("data_transfer_node",anonymous=True)
    building_flag=rospy.Publisher("/building_flag",Int16,queue_size=1)
    control()