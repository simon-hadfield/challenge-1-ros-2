#!/usr/bin/env python

import rospy
import sys
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped, PoseWithCovarianceStamped
import os
import time
import rospkg 
rospack = rospkg.RosPack()

f_est = []
f_gt = []
n_skip = 350
num_skipped_est = 0
num_skipped_gt = 0

def est(data):
    global n_skip
    global num_skipped_est
    global num_skipped_gt
    if num_skipped_est >= n_skip:
        f_est.writelines([str(data.header.stamp.secs),'.',
                str(data.header.stamp.nsecs),' '])
        f_est.writelines([str(data.pose.pose.position.x),' ',
                str(data.pose.pose.position.y),' ',
                str(data.pose.pose.position.z),' '])
        f_est.writelines([str(data.pose.pose.orientation.x),' ',
                str(data.pose.pose.orientation.y),' ',
                str(data.pose.pose.orientation.z),' ',
                str(data.pose.pose.orientation.w),'\n'])
    else:
        num_skipped_est = num_skipped_est+1

def gt(data):
    global n_skip
    global num_skipped_est
    global num_skipped_gt
    if num_skipped_gt >= n_skip:
        f_gt.writelines([str(data.header.stamp.secs),'.',
                str(data.header.stamp.nsecs),' '])
        f_gt.writelines([str(data.pose.pose.position.x),' ',
                str(data.pose.pose.position.y),' ',
                str(data.pose.pose.position.z),' '])
        f_gt.writelines([str(data.pose.pose.orientation.x),' ',
                str(data.pose.pose.orientation.y),' ',
                str(data.pose.pose.orientation.z),' ',
                str(data.pose.pose.orientation.w),'\n'])
    else:
        num_skipped_gt = num_skipped_gt+1

if __name__ == '__main__':
    #try:
    group_no = sys.argv[1]
    route_no = sys.argv[2]
	#raise Exception("Correct the output filepath")
    fname = "/vol/vssp/signsrc/challenge1/"+str(group_no)+"_"+str(route_no)+"_"  
    with open(fname +'est.txt','w') as f_est:
        with open(fname +'gt.txt','w') as f_gt:

            rospy.init_node('ate_computer')

            rospy.Subscriber('/odometry/filtered', Odometry, est)
            #rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, gt)
            rospy.Subscriber('/odom', Odometry, gt)
            #rospy.Subscriber('/vicon/ClusterA/ClusterA', TransformStamped, gt)
            rospy.spin()
    #except rospy.ROSInterruptException:
    #time.sleep(5)
    print("ROSInterruptException detected. Computing ATE")
    pkg_path = rospack.get_path('eee3043')
    cmd = pkg_path+'/scripts/evaluate_ate.py --plot '+fname+'plot.png '+fname +'gt.txt '+fname +'est.txt  > '+fname+'log.txt'
    print(cmd)
    os.system(cmd)
    print("ATE done")
    
    
