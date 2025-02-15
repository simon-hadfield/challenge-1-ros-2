#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
import random

pub = []

def callback(data):
    cov = list(data.pose.covariance)
    cov[14] = 1
    cov[21] = 1
    cov[28] = 1
    data.pose.covariance = tuple(cov)
    data.pose.pose.position.x += random.uniform(-0.01, 0.01)
    data.pose.pose.position.y += random.uniform(-0.001, 0.001)
    data.pose.pose.orientation.z += random.uniform(-0.05, 0.05)
    data.twist.twist.linear.x += random.uniform(-0.01, 0.01)
    data.twist.twist.linear.y += random.uniform(-0.001, 0.001)
    data.twist.twist.angular.z += random.uniform(-0.05, 0.05)
    pub.publish(data)


if __name__ == '__main__':
    rospy.init_node('odom_corrector')
    pub = rospy.Publisher('/odom_corrected', Odometry, queue_size=10)

    rospy.Subscriber('/odom', Odometry, callback)
    rospy.spin()
