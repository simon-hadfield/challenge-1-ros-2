import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler, Shutdown
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, TextSubstitution
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Declare launch arguments
    group_arg = DeclareLaunchArgument(
        'group',
        default_value='0',
        description='Group number'
    )
    
    route_arg = DeclareLaunchArgument(
        'route',
        default_value='0',
        description='Route number'
    )
    
    # Get launch configurations
    group = LaunchConfiguration('group')
    route = LaunchConfiguration('route')
    
    # ************** INCLUDE THE GROUPS LAUNCH FILE *********
    home_dir = os.environ.get('HOME', '')
    group_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            home_dir,
            '/group',
            group,
            '_KF.launch.py'
        ])
    )
    
    # ***************** bringup the real robot *****************
    robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('turtlebot3_bringup'),
                'launch',
                'robot.launch.py'
            ])
        ])
    )
    
    # **************** Route ****************
    challenge1_route_node = Node(
        package='challenge-1-ros-2',
        executable='challenge1_route',
        name='challenge1_route',
        output='screen',
        arguments=[route]
    )
    
    # Event handler to shutdown when challenge1_route exits
    shutdown_event = RegisterEventHandler(
        OnProcessExit(
            target_action=challenge1_route_node,
            on_exit=[Shutdown(reason='challenge1_route finished')]
        )
    )
    
    # **************** Error calculation node ****************
    ate_node = Node(
        package='challenge-1-ros-2',
        executable='absolute_trajectory_error',
        name='ATE',
        output='screen',
        arguments=[group, route]
    )
    
    # **************** Fix and add noise to odom/imu, create fake gps ****************
    odom_corrector_node = Node(
        package='challenge-1-ros-2',
        executable='challenge1_correct_odom',
        name='odom_corrector',
        output='screen'
    )
    
    imu_corrector_node = Node(
        package='challenge-1-ros-2',
        executable='challenge1_correct_imu',
        name='imu_corrector',
        output='screen'
    )
    
    gps_corrector_node = Node(
        package='challenge-1-ros-2',
        executable='challenge1_correct_gps',
        name='gps_corrector',
        output='screen'
    )
    
    return LaunchDescription([
        group_arg,
        route_arg,
        group_launch,
        robot_launch,
        challenge1_route_node,
        shutdown_event,
        ate_node,
        odom_corrector_node,
        imu_corrector_node,
        gps_corrector_node
    ])

	
	
	
