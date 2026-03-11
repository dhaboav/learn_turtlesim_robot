from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()

    turltesim_node = Node(
        package="turtlesim",
        executable="turtlesim_node",
        name="turtle_node",
    )

    math_turtle_control_node = Node(
        package="turtlesim_controller",
        executable="test_drive",
        name="controller_node",
    )

    ld.add_action(turltesim_node)
    ld.add_action(math_turtle_control_node)

    return ld

    # listener_node = Node(
    #     package="demo_nodes_py",
    #     executable="listener",
    #     name="my_listener",
    #     remappings=[
    #         ("chatter", "my_chatter") # Topics remappings
    #     ]
    # )
