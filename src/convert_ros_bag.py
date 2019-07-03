#!/usr/bin/env python
import rospy
import cv2
import sys
import rosbag
import os
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("usage rosrun my_ros_tools convert_ros_bag.py filename")
        sys.exit(1)
    filename = '.'.join(sys.argv[1].split('/')[-1].split('.')[:-1])
    path = '/'.join(sys.argv[1].split('/')[:-1]) + '/' + filename
    if(not os.path.exists(path)):
        os.mkdir(path)
    depthdir = path + '/' + 'depth'
    rgbdir = path + '/' + 'rgb'
    if(not os.path.exists(depthdir)):
        os.mkdir(depthdir)
    if(not os.path.exists(rgbdir)):
        os.mkdir(rgbdir)
    bag = rosbag.Bag(sys.argv[1])
    rgb_topic = '/camera/rgb/image_color'
    depth_topic = '/camera/depth_registered/sw_registered/image_rect_raw'
    rgb_txt = open(path + '/rgb.txt', 'w')
    depth_txt = open(path + '/depth.txt', 'w')

    rgb_txt.write('# color images\n')
    rgb_txt.write('# file: ' + filename + '.bag\n')
    rgb_txt.write('# timestamp filename\n')

    depth_txt.write('# depth images\n')
    depth_txt.write('# file: ' + filename + '.bag\n')
    depth_txt.write('# timestamp filename\n')
    bridge = CvBridge()
    rgb_count = bag.get_message_count(rgb_topic)
    depth_count = bag.get_message_count(depth_topic)
    print("bag file contains " + str(rgb_count) + " rgb images and " + str(depth_count) + " depth images")
    processed = 0
    percent = 0
    for topic, msg, t in bag.read_messages(topics=[rgb_topic, depth_topic]):
        if (topic == rgb_topic):
            time_str = str(t.secs) + '.' + str(t.nsecs / 1000).zfill(6)
            rgb_txt.write(time_str + ' rgb/' + time_str + '.png\n')
            rgb_img = bridge.imgmsg_to_cv2(msg)
            cv2.imwrite(path + '/rgb/' + time_str + '.png', rgb_img)
        if (topic == depth_topic):
            time_str = str(t.secs) + '.' + str(t.nsecs / 1000).zfill(6)
            depth_txt.write(time_str + ' depth/' + time_str + '.png\n')
            depth_img = bridge.imgmsg_to_cv2(msg)
            cv2.imwrite(path + '/depth/' + time_str + '.png', depth_img)
        processed = processed + 1
        if (processed * 100 / (rgb_count + depth_count) != percent):
            percent = processed * 100 / (rgb_count + depth_count)
            print(str(percent)+"% processed")
    print("complete")
