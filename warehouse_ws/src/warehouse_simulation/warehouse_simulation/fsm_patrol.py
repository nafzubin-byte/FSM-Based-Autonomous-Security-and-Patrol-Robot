import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Imu
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import math

class PatrolFSM(Node):
    def __init__(self):
        super().__init__('patrol_fsm')
        
        # Initial FSM State
        self.state = 'IDLE'
        
        # Publishers & Subscribers
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.alert_pub = self.create_publisher(String, '/robot_alert', 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)
        self.imu_sub = self.create_subscription(Imu, '/imu', self.imu_cb, 10)
        
        # Main State Machine Loop Timer (Runs at 10Hz)
        self.timer = self.create_timer(0.1, self.fsm_loop)
        
        # Sensor Variables
        self.min_front_dist = float('inf')
        self.impact_detected = False
        self.idle_counter = 0

        # Debounce Filter Variables
        self.obstacle_hit_count = 0
        self.obstacle_confirmed = False

        self.get_logger().info("FSM Node initialized. Starting in IDLE state.")

    def scan_cb(self, msg):
        """ Processes LiDAR data with spatial and temporal noise filtering. """
        num_ranges = len(msg.ranges)
        if num_ranges == 0: return
        
        front_slice = msg.ranges[int(num_ranges * 0.45):int(num_ranges * 0.55)]
        valid = [r for r in front_slice if r > 0.15 and not math.isinf(r) and not math.isnan(r)]
        
        # Spatial Median Filter
        if not valid:
            raw_dist = float('inf')
        else:
            valid.sort()
            raw_dist = valid[len(valid) // 2]
            
        self.min_front_dist = raw_dist

        # Temporal Debounce Filter
        if self.min_front_dist < 0.5:
            self.obstacle_hit_count += 1
        else:
            self.obstacle_hit_count = 0

        if self.obstacle_hit_count >= 3:
            self.obstacle_confirmed = True
        else:
            self.obstacle_confirmed = False

    def imu_cb(self, msg):
        """ Processes IMU data to detect sudden acceleration spikes (collisions). """
        ax = msg.linear_acceleration.x
        ay = msg.linear_acceleration.y
        az = msg.linear_acceleration.z
        accel_mag = math.sqrt(ax**2 + ay**2 + az**2)
        
        if accel_mag > 15.0:
            self.impact_detected = True

    def fsm_loop(self):
        if self.state == 'IDLE':
            self.state_idle()
        elif self.state == 'PATROLLING':
            self.state_patrolling()
        elif self.state == 'OBSTACLE_AVOIDANCE':
            self.state_obstacle_avoidance()
        elif self.state == 'ALERT':
            self.state_alert()

    def state_idle(self):
        cmd = Twist()
        self.cmd_pub.publish(cmd)
        self.idle_counter += 1
        if self.idle_counter > 30:
            self.get_logger().info(f"[TRANSITION] IDLE -> PATROLLING | Trigger: Auto-start timer completed.")
            self.state = 'PATROLLING'

    def state_patrolling(self):
        if self.impact_detected:
            self.get_logger().error(f"[TRANSITION] PATROLLING -> ALERT | Trigger: IMU Acceleration Spike")
            self.state = 'ALERT'
            return

        if self.obstacle_confirmed:
            self.get_logger().info(f"[TRANSITION] PATROLLING -> OBSTACLE_AVOIDANCE | Trigger: Obstacle confirmed for 3 frames.")
            self.state = 'OBSTACLE_AVOIDANCE'
            return

        cmd = Twist()
        cmd.linear.x = 0.3
        cmd.angular.z = 0.0
        self.cmd_pub.publish(cmd)

    def state_obstacle_avoidance(self):
        if self.impact_detected:
            self.get_logger().error(f"[TRANSITION] OBSTACLE_AVOIDANCE -> ALERT | Trigger: IMU Acceleration Spike")
            self.state = 'ALERT'
            return

        # Path is clear
        if self.min_front_dist >= 0.55:
            self.get_logger().info(f"[TRANSITION] OBSTACLE_AVOIDANCE -> PATROLLING | Trigger: Path clear.")
            self.obstacle_hit_count = 0
            self.obstacle_confirmed = False
            self.state = 'PATROLLING'
            return

        # IMPROVED AVOIDANCE: Back up slightly while turning to un-pin from obstacles
        cmd = Twist()
        cmd.linear.x = -0.15  # Backing up creates instant clearance
        cmd.angular.z = 0.8   # Sharp rotation to navigate away
        self.cmd_pub.publish(cmd)

    def state_alert(self):
        cmd = Twist()
        self.cmd_pub.publish(cmd)
        alert_msg = String()
        alert_msg.data = "CRITICAL ALERT: Physical collision or tipping event detected! Robot motion disabled."
        self.alert_pub.publish(alert_msg)
        self.get_logger().error("ROBOT IN ALERT STATE. MANUAL INTERVENTION REQUIRED.", throttle_duration_sec=2.0)

def main(args=None):
    rclpy.init(args=args)
    node = PatrolFSM()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
