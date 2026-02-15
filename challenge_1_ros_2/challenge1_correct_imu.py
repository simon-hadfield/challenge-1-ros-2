#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu


class ImuCorrector(Node):
    def __init__(self):
        super().__init__('imu_corrector')
        self.pub = self.create_publisher(Imu, '/imu_corrected', 10)
        self.subscription = self.create_subscription(
            Imu,
            '/imu',
            self.callback,
            10)
    
    def callback(self, data):
        ocov = list(data.orientation_covariance)
        acov = list(data.angular_velocity_covariance)
        ocov[0] = 1
        ocov[4] = 1
        acov[0] = 1
        acov[4] = 1
        data.orientation_covariance = tuple(ocov)
        data.angular_velocity_covariance = tuple(acov)
        self.pub.publish(data)


def main(args=None):
    rclpy.init(args=args)
    node = ImuCorrector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
