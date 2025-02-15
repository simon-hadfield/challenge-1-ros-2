#!/usr/bin/env python

import rospy
import sensor_msgs
from sensor_msgs.msg import NavSatFix
from nav_msgs.msg import Odometry
import random
from gps_tools import GPStoUTM

pub = []
gps = GPStoUTM()


def callback(in_data):
    # Prep output header etc
    out_data = NavSatFix()
    out_data.header.frame_id = "odom"
    out_data.header.stamp = in_data.header.stamp
    out_data.status.status = 0  # sensor_msgs.NavSatStatus.STATUS_FIX
    out_data.status.service = 1  # sensor_msgs.NavSatStatus.SERVICE_GPS

    # uncertainty
    out_data.position_covariance = (1, 0, 0, 0, 1, 0, 0, 0, 1)
    out_data.position_covariance_type = 0  # out_data.COVARIANCE_TYPE_UNKNOWN

    # Copy and noise the pose (hacky as hell)
    noise_range = 0.1
    longi = in_data.pose.pose.position.y/100.0  + 1.0 + random.uniform(-noise_range, noise_range)
    lati = in_data.pose.pose.position.x/100.0 + 1.0 + random.uniform(-noise_range, noise_range)
    out_data.latitude, out_data.longitude = gps.UTMtoLL(longi, lati, 1, "U")

    pub.publish(out_data)


if __name__ == '__main__':
    rospy.init_node('odom_corrector')
    pub = rospy.Publisher('/gps/fix', NavSatFix, queue_size=10)

    rospy.Subscriber('/odom', Odometry, callback)
    rospy.spin()
