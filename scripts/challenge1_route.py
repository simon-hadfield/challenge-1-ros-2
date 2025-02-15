#!/usr/bin/env python

import rospy
import sys
import numpy as np
from geometry_msgs.msg import Twist
import time

if __name__ == '__main__':
    route_no = sys.argv[1]
    print("Executing route: ", route_no)
    
    if route_no == "0":
        raise Exception("Please pass a route:= argument to the launch file specifying which route to take")
    
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.init_node('challenge1_route')
    
    move = Twist()
    counter = 1
    speedup = 1.0
    fwd = 0.1
    tcurve = 0.5  # tight
    wcurve = 0.3  # wide
    time.sleep(10)    # wait for gazebo etc to start

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        print(counter)
        
        # pirouette (just for testing)
        if route_no == "7":
            move.angular.z = 1 * speedup
            end_step = 125
        # big circle
        elif route_no == "1":
            move.linear.x = fwd * speedup
            move.angular.z = wcurve * speedup
            end_step = 220
        # small circle
        elif route_no == "2":
            move.linear.x = fwd * speedup
            move.angular.z = tcurve * speedup
            end_step = 125
        # figure 8
        elif route_no == "3":
            move.linear.x = fwd * speedup
            move.angular.z = tcurve * speedup
            if counter>125  / speedup:
                move.angular.z = -tcurve * speedup
            end_step = 250
        # 3 loop figure 8
        elif route_no == "4":
            move.linear.x = fwd * speedup
            move.angular.z = tcurve * speedup
            if counter>125 / speedup:
                move.angular.z = -tcurve * speedup
            if counter>188 / speedup:
                move.angular.z = tcurve * speedup
            if counter>313 / speedup:
                move.angular.z = -tcurve * speedup
            end_step = 375
        # curvey edge triangle
        elif route_no == "5":
            edge_steps = 30
            corner_steps = 15
            move.linear.x = fwd * speedup
            move.angular.z = tcurve * speedup
            if counter>edge_steps / speedup:
                move.linear.x = 0 * speedup
            if counter> (edge_steps + corner_steps) / speedup:
                move.linear.x = fwd * speedup
            if counter> (edge_steps*2 + corner_steps) / speedup:
                move.linear.x = 0 * speedup
            if counter> (edge_steps*2 + corner_steps*2) / speedup:
                move.linear.x = fwd * speedup
            end_step = (edge_steps*3 + corner_steps*2)
        # outward spiral
        elif route_no == "6":
            move.linear.x = fwd * speedup
            move.angular.z = tcurve/(counter/100.0) * speedup
            end_step = 180
        else:
            raise Exception("Unknown route number ", route_no)
        if counter > end_step / speedup:
            break
        
        pub.publish(move)
        counter+=1
        rate.sleep()
    move = Twist()
    pub.publish(move)
    time.sleep(10)   # wait for rosbag to finish writing (enough) 
        
        
        
