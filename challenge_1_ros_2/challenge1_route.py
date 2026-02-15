#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import sys
import numpy as np
from geometry_msgs.msg import TwistStamped
import time


class Challenge1Route(Node):
    def __init__(self, route_no):
        super().__init__('challenge1_route')
        self.route_no = route_no
        self.pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        
    def run_route(self):
        move = TwistStamped()
        counter = 1
        speedup = 1.0
        fwd = 0.1
        tcurve = 0.5  # tight
        wcurve = 0.3  # wide
        time.sleep(5)    # wait for gazebo etc to start

        while True:
            #print(counter)
            move.header.stamp = self.get_clock().now().to_msg()
            
            # pirouette (just for testing)
            if self.route_no == "7":
                move.twist.angular.z = 1 * speedup
                end_step = 125
            # big circle
            elif self.route_no == "1":
                move.twist.linear.x = fwd * speedup
                move.twist.angular.z = wcurve * speedup
                end_step = 220
            # small circle
            elif self.route_no == "2":
                move.twist.linear.x = fwd * speedup
                move.twist.angular.z = tcurve * speedup
                end_step = 125
            # figure 8
            elif self.route_no == "3":
                move.twist.linear.x = fwd * speedup
                move.twist.angular.z = tcurve * speedup
                if counter>125  / speedup:
                    move.twist.angular.z = -tcurve * speedup
                end_step = 250
            # 3 loop figure 8
            elif self.route_no == "4":
                move.twist.linear.x = fwd * speedup
                move.twist.angular.z = tcurve * speedup
                if counter>125 / speedup:
                    move.twist.angular.z = -tcurve * speedup
                if counter>188 / speedup:
                    move.twist.angular.z = tcurve * speedup
                if counter>313 / speedup:
                    move.twist.angular.z = -tcurve * speedup
                end_step = 375
            # curvey edge triangle
            elif self.route_no == "5":
                edge_steps = 30
                corner_steps = 15
                move.twist.linear.x = fwd * speedup
                move.twist.angular.z = tcurve * speedup
                if counter>edge_steps / speedup:
                    move.twist.linear.x = 0 * speedup
                if counter> (edge_steps + corner_steps) / speedup:
                    move.twist.linear.x = fwd * speedup
                if counter> (edge_steps*2 + corner_steps) / speedup:
                    move.twist.linear.x = 0 * speedup
                if counter> (edge_steps*2 + corner_steps*2) / speedup:
                    move.twist.linear.x = fwd * speedup
                end_step = (edge_steps*3 + corner_steps*2)
            # outward spiral
            elif self.route_no == "6":
                move.twist.linear.x = fwd * speedup
                move.twist.angular.z = tcurve/(counter/100.0) * speedup
                end_step = 180
            else:
                raise Exception("Unknown route number ", self.route_no)
            if counter > end_step / speedup:
                break
            
            self.pub.publish(move)
            counter+=1
            time.sleep(0.1)
        move = TwistStamped()
        move.header.stamp = self.get_clock().now().to_msg()
        self.pub.publish(move)
        time.sleep(10)   # wait for rosbag to finish writing (enough)


def main(args=None):
    route_no = sys.argv[1] if len(sys.argv) > 1 else "0"
    print("Executing route: ", route_no)
    
    if route_no == "0":
        raise Exception("Please pass a route:= argument to the launch file specifying which route to take")
    
    rclpy.init(args=args)
    node = Challenge1Route(route_no)
    node.run_route()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main() 
        
        
        
