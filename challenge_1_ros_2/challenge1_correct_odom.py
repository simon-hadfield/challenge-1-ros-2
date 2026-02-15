#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import random


class OdomCorrector(Node):
    def __init__(self):
        super().__init__('odom_corrector')
        self.pub = self.create_publisher(Odometry, '/odom_corrected', 10)
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.callback,
            10)
    
    def callback(self, data):
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
        self.pub.publish(data)


def main(args=None):
    rclpy.init(args=args)
    node = OdomCorrector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

    
if __name__ == '__main__':
    main()