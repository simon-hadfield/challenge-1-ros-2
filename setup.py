from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'challenge-1-ros-2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Launch files
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bot',
    maintainer_email='bot@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'absolute_trajectory_error = challenge_1_ros_2.absolute_trajectory_error:main',
            'challenge1_correct_gps = challenge_1_ros_2.challenge1_correct_gps:main',
            'challenge1_correct_imu = challenge_1_ros_2.challenge1_correct_imu:main',
            'challenge1_correct_odom = challenge_1_ros_2.challenge1_correct_odom:main',
            'challenge1_route = challenge_1_ros_2.challenge1_route:main',
            'evaluate_ate = challenge_1_ros_2.evaluate_ate:main',
        ],
    },
)
