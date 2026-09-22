import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_dir = get_package_share_directory("warehouse_simulation")
    world_file = os.path.join(pkg_dir, "worlds", "warehouse.world")
    gazebo_ros_dir = get_package_share_directory("gazebo_ros")

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(gazebo_ros_dir, "launch", "gazebo.launch.py")
            ),
            launch_arguments={"world": world_file}.items()
        ),
    ])
