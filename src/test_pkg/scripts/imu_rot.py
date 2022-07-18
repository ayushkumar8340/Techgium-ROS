#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int16

count=0
temp=0
real_val=0
sector=-1
rospy.init_node("rotation",anonymous=True)
rot_pub=rospy.Publisher("/rotation_arrow",Int16,queue_size=1)
rot_warning=rospy.Publisher("/rot_warning",Int16,queue_size=1)
def rotZ_cb(msg):
    global count
    global temp
    global real_val
    global sector
    global rot_pub

    count+=1
    if(count==1):
        temp=msg.data
    real_val=msg.data-temp
    if(real_val>=0 and real_val<=24 or real_val<0 and real_val>=-24):
        sector=0
    
    elif(real_val>24 and real_val<=69 or real_val<-24 and real_val>-69):
        sector=1
    elif(real_val>69 and real_val<=104 or real_val<-69 and real_val>-104):
        sector=2
    elif(real_val>104 and real_val<=149 or real_val<-104 and real_val>-149):
        sector=3

    elif(real_val>149 and real_val<=194 or real_val<-149 and real_val>-194):
        sector=4   
    elif(real_val>194 and real_val<=239 or real_val<-194 and real_val>-239):
        sector=5 
    elif(real_val>239 and real_val<=284 or real_val<-239 and real_val>-284):
        sector=6 
    elif(real_val>284 and real_val<=329 or real_val<-284 and real_val>-329):
        sector=7 
    
    if(real_val>360 or real_val<-360):
        rot_warning.publish(1)
    else:
        rot_warning.publish(0)
    print(sector)
    rot_pub.publish(sector)


    
def rot():

    rospy.Subscriber("/rotZ",Int16,rotZ_cb)
    rospy.spin()







if __name__=="__main__":
    rot()