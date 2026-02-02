#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import tty
import termios


def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key


class TeleopNode(Node):
    def __init__(self):
        super().__init__('teleop_wasd')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info(
            "Teleop started: W/A/S/D move, X stop, CTRL+C exit"
        )

    def run(self):
        twist = Twist()
        while rclpy.ok():
            key = get_key()
            twist.linear.x = 0.0
            twist.angular.z = 0.0

            if key.lower() == 'w':
                twist.linear.x = 0.1
            elif key.lower() == 's':
                twist.linear.x = -0.1
            elif key.lower() == 'a':
                twist.angular.z = 0.5
            elif key.lower() == 'd':
                twist.angular.z = -0.5
            elif key.lower() == 'x':
                pass
            else:
                continue

            self.publisher_.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = TeleopNode()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
