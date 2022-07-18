import rospy
import cv2
import numpy as np
from std_msgs.msg import Int16
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

rospy.init_node("image_processing")
human=rospy.Publisher("/human",Int16,queue_size=1)
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

vid=cv2.VideoCapture(2)

bridge=CvBridge()
pub=rospy.Publisher("/test_img",Image,queue_size=1)

while not rospy.is_shutdown():
    _,img=vid.read()
    temp_img=bridge.cv2_to_imgmsg(img,"bgr8")
    pub.publish(temp_img)
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
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
    cv2.imshow("Image", img)
    cv2.waitKey(30)

cv2.destroyAllWindows()