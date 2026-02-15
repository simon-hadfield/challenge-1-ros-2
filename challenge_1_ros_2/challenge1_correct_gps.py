#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
from nav_msgs.msg import Odometry
import random
from .gps_tools import GPStoUTM


class GpsCorrector(Node):
    def __init__(self):
        super().__init__('gps_corrector')
        self.gps = GPStoUTM()
        self.pub = self.create_publisher(NavSatFix, '/gps/fix', 10)
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.callback,
            10)
    
    def callback(self, in_data):
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
        out_data.latitude, out_data.longitude = self.gps.UTMtoLL(longi, lati, 1, "U")

        self.pub.publish(out_data)


def main(args=None):
    rclpy.init(args=args)
    node = GpsCorrector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
