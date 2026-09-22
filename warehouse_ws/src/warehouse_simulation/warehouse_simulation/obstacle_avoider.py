import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoider(Node):
    def __init__(self):
        super().__init__('obstacle_avoider')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)
        self.get_logger().info('Advanced Obstacle Avoider Node Initialized')

    def scan_callback(self, msg):
        twist = Twist()
        num_ranges = len(msg.ranges)
        if num_ranges == 0:
            return

        # Divide scan into left, front, and right sectors
        left_slice = msg.ranges[int(num_ranges * 0.15):int(num_ranges * 0.35)]
        front_slice = msg.ranges[int(num_ranges * 0.4):int(num_ranges * 0.6)]
        right_slice = msg.ranges[int(num_ranges * 0.65):int(num_ranges * 0.85)]

        def get_min(slice_data):
            valid = [r for r in slice_data if not (r == float('inf') or r == float('nan') or r == 0.0) and r > 0.2]
            return min(valid) if valid else float('inf')

        min_front = get_min(front_slice)
        min_left = get_min(left_slice)
        min_right = get_min(right_slice)

        self.get_logger().info(f'Front: {min_front:.2f}m | Left: {min_left:.2f}m | Right: {min_right:.2f}m', throttle_duration_sec=1.0)

        # If an obstacle is close in front, back up and steer toward the clearer side
        if min_front < 0.8:
            twist.linear.x = -0.25  # Move backward to un-stick
            if min_left > min_right:
                twist.angular.z = 0.75  # Turn left
            else:
                twist.angular.z = -0.75 # Turn right
        else:
            twist.linear.x = 0.3   # Move forward safely
            twist.angular.z = 0.0

        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoider()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
