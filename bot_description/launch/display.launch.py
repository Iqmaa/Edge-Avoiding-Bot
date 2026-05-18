#  launch files helps to allow us run multiple nodes(chunks of code that performs specific 
# tasks that communicate via topics ) at the same time instead of launching them manually

import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    bot_description_dir = get_package_share_directory("bot_description")

    model_arg = DeclareLaunchArgument(name="model", default_value=os.path.join(
                                        bot_description_dir, "urdf", "bot.urdf.xacro"
                                        ),
                                      description="Absolute path to robot urdf file")

    # This uses the xacro tool to "cook" your XACRO file into a raw URDF string. 
    # It also passes a flag is_sim:=True, that tells the robot model it's running in a simulation.
    robot_description = ParameterValue(Command([
            "xacro ",
            LaunchConfiguration("model"),
            " is_sim:=True",
        ]),
        value_type=str
    )
    
    # This is the first node. It takes the robot description and joint positions to calculate the 3D pose of every link (TF tree).
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description,
                     "use_sim_time": True}]
    )

    # Second node. Pops up a window with sliders. Since we don't have a physical robot or Gazebo running yet, these sliders act as "fake encoders" to move the robot's joints.
    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )
    # Third node. loads the display.rviz config file so the robot and sensors show up correctly immediately.
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", os.path.join(bot_description_dir, "rviz", "display.rviz")],
    )

    return LaunchDescription([
        model_arg,
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        rviz_node
    ])