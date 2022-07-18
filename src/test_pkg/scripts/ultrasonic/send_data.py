from dis import dis
from ultrasonic import distance
import rospy
from std_msgs import Int16
import time

def control():
    dist=Int16()
    dist_pub=rospy.Publisher("/distance",Int16,queue_size=1)
    while not rospy.is_shutdown():
        dist.data=distance()
        dist_pub.publish(dist)
        time.sleep(0.1)
if __name__=="__main__":
    rospy.init_node("distance")
    control()