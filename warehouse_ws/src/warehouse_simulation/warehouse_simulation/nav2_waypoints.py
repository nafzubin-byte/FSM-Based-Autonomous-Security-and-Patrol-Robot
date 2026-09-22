import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
import math

class WaypointNavigator(Node):
    def __init__(self):
        super().__init__('waypoint_navigator')
        # Create an Action Client for Nav2
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        
        # Define your warehouse waypoints [x, y, yaw_angle]
        self.waypoints = [
            [2.0, 0.0, 0.0],     # Point 1: 2 meters forward
            [2.0, 2.0, 1.57],    # Point 2: 2 meters left, facing 90 degrees
            [0.0, 0.0, 0.0]      # Point 3: Back to origin
        ]
        self.current_wp_index = 0
        
        # Start the navigation loop
        self.send_next_goal()

    def send_next_goal(self):
        if self.current_wp_index >= len(self.waypoints):
            self.get_logger().info("All waypoints completed! Patrol finished.")
            rclpy.shutdown()
            return

        wp = self.waypoints[self.current_wp_index]
        self.get_logger().info(f"Navigating to Waypoint {self.current_wp_index + 1}: x={wp[0]}, y={wp[1]}")
        
        # Wait for Nav2 server to be ready
        self.nav_client.wait_for_server()
        
        # Create Goal Message
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        
        goal_msg.pose.pose.position.x = float(wp[0])
        goal_msg.pose.pose.position.y = float(wp[1])
        
        # Convert Yaw (radians) to Quaternion for ROS2
        goal_msg.pose.pose.orientation.z = math.sin(wp[2] / 2.0)
        goal_msg.pose.pose.orientation.w = math.cos(wp[2] / 2.0)
        
        # Send goal and attach callbacks
        self.send_goal_future = self.nav_client.send_goal_async(goal_msg)
        self.send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error("Nav2 rejected the goal. Is it inside an obstacle?")
            return

        self.get_logger().info("Goal accepted by Nav2, calculating path...")
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        status = future.result().status
        if status == 4: # 4 = SUCCEEDED
            self.get_logger().info("Arrived successfully!")
            self.current_wp_index += 1
            self.send_next_goal()
        else:
            self.get_logger().warn(f"Navigation failed with status code: {status}")

def main(args=None):
    rclpy.init(args=args)
    node = WaypointNavigator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
