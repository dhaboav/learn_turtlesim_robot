#!/usr/bin/env python3

import math

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan


class LidarControl(Node):
    def __init__(self):
        super().__init__("lidar_control")
        self._lidar_subs = self.create_subscription(
            LaserScan, "/lidar", self.lidar_callback, qos_profile_sensor_data
        )
        self._cmd_vel_pubs = self.create_publisher(Twist, "/cmd_vel", 10)
        self.get_logger().info("Lidar Control has been started")

    def lidar_callback(self, sensor_data: LaserScan):

        SAFE_DIST = 1.5
        CRITICAL_DIST = 0.8

        zones = [12.0] * 8

        for i in range(360):
            val = sensor_data.ranges[i]

            # 1. Filtering the data
            if math.isinf(val) or math.isnan(val) or val < 0.4:
                val = 12.0

            # 2. mapping by 45 degrees
            zone_idx = i // 45

            # 3. Minimum for each zone
            if val < zones[zone_idx]:
                zones[zone_idx] = val

        # Navigation logic
        front_dist = min(zones[3], zones[4])
        left_dist = zones[5]
        right_dist = zones[2]

        self.get_logger().info(
            f"L: {left_dist:.2f} | F: {front_dist:.2f} | R: {right_dist:.2f}"
        )

        if front_dist < CRITICAL_DIST:
            self.get_logger().info("Danger: There object in front!")
            self.move_robot(0.0, 0.0)

            if left_dist > right_dist:
                self.get_logger().info("Turn left")
                self.move_robot(0.0, 0.5)
            else:
                self.get_logger().info("Turn right")
                self.move_robot(0.0, -0.5)

        elif front_dist < SAFE_DIST:
            self.get_logger().info("Beware: There an object...")
            if left_dist > right_dist:
                self.move_robot(0.5, 0.3)
            else:
                self.move_robot(0.5, -0.3)

        else:
            self.get_logger().info("Nothing in our way! Full Drive!")
            self.move_robot(1.0, 0.0)

    def move_robot(self, linear_x: float, angular_z: float) -> None:
        """Moves the robot based on linear and angular velocities.

        Args:
            linear_x (float): Linear speed along the x-axis in m/s.
            angular_z (float): Angular speed around the z-axis in rad/s.
        """
        drive = Twist()
        drive.linear.x = linear_x
        drive.angular.z = angular_z
        self._cmd_vel_pubs.publish(drive)


def main(args=None):
    rclpy.init(args=args)
    node = LidarControl()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
