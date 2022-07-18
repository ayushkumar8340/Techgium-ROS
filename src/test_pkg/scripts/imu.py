#!/usr/bin/env python3
from locale import currency
import rospy 
from std_msgs.msg import Int16
import time
acc_state=0
acc_output=0

rospy.init_node("imu_data",anonymous=True)
jerkX=rospy.Publisher("/jerkX",Int16,queue_size=1)
jerkY=rospy.Publisher("/jerkY",Int16,queue_size=1)
jerkZ=rospy.Publisher("/jerkZ",Int16,queue_size=1)

varX=Int16()
varY=Int16()
varZ=Int16()

def accX_cb(msg):
    global acc_state
    global acc_output
    global jerkX
    global varX
    acc_output=acc_state
    acc_state=(msg.data/100)
        
def accY_cb(msg):
    global acc_state
    global acc_output
    global jerkY
    global varY
    varY=msg
    acc_output=acc_state
    acc_state=(msg.data/100)
           

def accZ_cb(msg):
    global acc_state
    global acc_output
    global jerkZ
    global varZ
    acc_output=acc_state
    varZ=msg
    acc_state=(msg.data/100)       
def imu():
    rospy.Subscriber("/accX",Int16,accX_cb)
    rospy.Subscriber("/accY",Int16,accY_cb)
    rospy.Subscriber("/accZ",Int16,accZ_cb)
    global varX
    global varY
    global varZ
    global jerkX
    global jerkY
    global jerkZ
    while not rospy.is_shutdown():
        if(varX.data>80):
            curr_time1=time.time()
            while True:
                prev_time1=time.time()
                jerkX.publish(1)
                if(prev_time1-curr_time1>0.5):
                    prev_time1=0
                    curr_time1=0
                    jerkX.publish(0)
                    break

        if(varY.data>70):
            curr_time2=time.time()
            while True:
                prev_time2=time.time()

                jerkY.publish(1)
                if(prev_time2-curr_time2>0.5):
                    prev_time2=0
                    curr_time2=0
                    jerkY.publish(0)
                    break

        if(varZ.data>150):
            curr_time3=time.time()
            while True:
                prev_time3=time.time()

                jerkZ.publish(1)
                if(prev_time3-curr_time3>0.5):
                    prev_time2=0
                    curr_time2=0
                    jerkZ.publish(0)
                    break
            

if __name__=="__main__":
    imu()