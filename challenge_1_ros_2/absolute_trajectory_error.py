#!/usr/bin/env python3

import hmac
import hashlib
import rclpy
from rclpy.node import Node
import sys
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped, PoseWithCovarianceStamped
import os
import time
from ament_index_python.packages import get_package_share_directory, get_package_prefix

f_est = []
f_gt = []
n_skip = 350
num_skipped_est = 0
num_skipped_gt = 0

SKEY = b"Lu<ujx{U1l{U3:s}"


class ATENode(Node):
    def __init__(self):
        super().__init__('ate_computer')
        
        self.sub_est = self.create_subscription(
            Odometry,
            '/odometry/filtered',
            self.est,
            10)
        
        self.sub_gt = self.create_subscription(
            Odometry,
            '/odom',
            self.gt,
            10)
    
    def est(self, data):
        global n_skip
        global num_skipped_est
        global num_skipped_gt
        if num_skipped_est >= n_skip:
            timestamp = data.header.stamp.sec + data.header.stamp.nanosec / 1e9
            f_est.writelines([str(timestamp), ' '])
            f_est.writelines([str(data.pose.pose.position.x),' ',
                    str(data.pose.pose.position.y),' ',
                    str(data.pose.pose.position.z),' '])
            f_est.writelines([str(data.pose.pose.orientation.x),' ',
                    str(data.pose.pose.orientation.y),' ',
                    str(data.pose.pose.orientation.z),' ',
                    str(data.pose.pose.orientation.w),'\n'])
            f_est.flush()
        else:
            num_skipped_est = num_skipped_est+1

    def gt(self, data):
        global n_skip
        global num_skipped_est
        global num_skipped_gt
        if num_skipped_gt >= n_skip:
            timestamp = data.header.stamp.sec + data.header.stamp.nanosec / 1e9
            f_gt.writelines([str(timestamp), ' '])
            f_gt.writelines([str(data.pose.pose.position.x),' ',
                    str(data.pose.pose.position.y),' ',
                    str(data.pose.pose.position.z),' '])
            f_gt.writelines([str(data.pose.pose.orientation.x),' ',
                    str(data.pose.pose.orientation.y),' ',
                    str(data.pose.pose.orientation.z),' ',
                    str(data.pose.pose.orientation.w),'\n'])
            f_gt.flush()
        else:
            num_skipped_gt = num_skipped_gt+1

def sign_score(group, route, score_text):
    message = f"{group}:{route}:{score_text}".encode()
    return hmac.new(
        SKEY,
        message,
        hashlib.sha256
    ).hexdigest()

def main(args=None):
    global f_est, f_gt
    
    group_no = sys.argv[1] if len(sys.argv) > 1 else "default"
    route_no = sys.argv[2] if len(sys.argv) > 2 else "1"
    
    fname = "/home/bot/challenge1/"+str(group_no)+"_"+str(route_no)+"_"  
    
    try:
        with open(fname +'est.txt','w') as f_est:
            with open(fname +'gt.txt','w') as f_gt:
                rclpy.init(args=args)
                node = ATENode()
                
                try:
                    rclpy.spin(node)
                except KeyboardInterrupt:
                    pass
                except Exception as e:
                    print(f"Exception during spin: {e}")
                finally:
                    node.destroy_node()
                    rclpy.shutdown()
    finally:
        print("ROSInterruptException detected. Computing ATE")
        
        try:
            pkg_prefix = get_package_prefix('challenge-1-ros-2')
            pkg_path = os.path.join(pkg_prefix, 'lib', 'challenge-1-ros-2')
        except Exception as e:
            print(f"Warning: Could not find package, using fallback path: {e}")
            pkg_path = os.path.dirname(os.path.abspath(__file__))
        
        cmd = 'python3 ' + os.path.join(pkg_path, 'evaluate_ate') + ' --plot '+fname+'plot.png '+fname +'gt.txt '+fname +'est.txt  > '+fname+'log.txt'
        print(cmd)
        os.system(cmd)
        print("ATE done")
        
        # Read, sign and print the ATE result
        try:
            log_path = fname + 'log.txt'

            with open(log_path, 'r') as log_file:
                ate_result = log_file.read().strip()

            # Ensure the result is a valid numeric score
            import math
            score = float(ate_result)
            if not math.isfinite(score) or score < 0:
                raise ValueError("Invalid ATE score")

            # Sign the exact score string
            signature = sign_score(
                group_no, route_no, ate_result
            )

            # Write signed result to a temporary file
            temp_path = fname + 'log.tmp'
            with open(temp_path, 'w') as f:
                f.write(f"{ate_result}\n")
                f.write(f"{signature}\n")

            # Replace the original log atomically
            os.replace(temp_path, log_path)

            print("********************")
            print(f"**** ATE Result: {ate_result}")
            print("********************")

        except Exception as e:
            print(f"Could not sign ATE result: {e}")


if __name__ == '__main__':
    main()
    
    
