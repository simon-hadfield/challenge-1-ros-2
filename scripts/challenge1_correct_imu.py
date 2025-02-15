#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu

pub = []

def callback(data):
    ocov = list(data.orientation_covariance)
    acov = list(data.angular_velocity_covariance)
    ocov[0]=1
    ocov[4]=1
    acov[0]=1
    acov[4]=1
    data.orientation_covariance=tuple(ocov)
    data.angular_velocity_covariance=tuple(acov)
    pub.publish(data)


if __name__ == '__main__':
    rospy.init_node('imu_corrector')
    pub = rospy.Publisher('/imu_corrected', Imu, queue_size=10)

    rospy.Subscriber('/imu', Imu, callback)
    rospy.spin()
