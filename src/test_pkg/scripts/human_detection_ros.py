#!/usr/bin/env python3
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import Int16
import numpy as np

net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
human=rospy.Publisher("/human",Int16,queue_size=1)

def img_cb(msg):
    global human
    global net
    global classes
    global output_layers
    bridge=CvBridge()
    img=bridge.imgmsg_to_cv2(msg,"bgr8")
    height, width, channels = img.shape
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    if(len(indexes)==0):
        human.publish(0)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            if(label=="person"):
                human.publish(1)

    cv2.imshow("frame",img)
    cv2.waitKey(1)
    
def control():
    rospy.init_node("test2")
    rospy.Subscriber("/test_img",Image,img_cb,queue_size=1,buff_size=2**24,tcp_nodelay=True)
    rospy.spin()



if __name__=="__main__":
    control()