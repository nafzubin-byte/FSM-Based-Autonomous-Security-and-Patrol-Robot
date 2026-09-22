from launch import LaunchDescription
from launch_ros.actions import SetRemap
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    return LaunchDescription([
        # Force Nav2 to publish directly to Gazebo's topic
        SetRemap(src='/cmd_vel_nav', dst='/cmd_vel'),
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource('/opt/ros/humble/share/nav2_bringup/launch/bringup_launch.py'),
            launch_arguments={
                'use_sim_time': 'true',
                'map': '/home/nafzuubuntu22/warehouse_ws/src/warehouse_simulation/worlds/warehouse_map.yaml',
                'params_file': '/opt/ros/humble/share/nav2_bringup/params/nav2_params.yaml'
            }.items(),
        )
    ])