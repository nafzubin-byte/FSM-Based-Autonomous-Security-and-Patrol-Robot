import os

world_content = """<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="warehouse_world">
    <include><uri>model://sun</uri></include>
    <include><uri>model://ground_plane</uri></include>

    <!-- Pentagon Perimeter Walls -->
    <model name="penta_wall_1"><static>true</static><pose>0 8.5 1 0 0 0</pose><link name="link"><collision name="col"><geometry><box><size>9.5 0.2 2</size></box></geometry></collision><visual name="vis"><geometry><box><size>9.5 0.2 2</size></box></geometry><material><ambient>0.8 0.8 0.8 1</ambient></material></visual></link></model>
    <model name="penta_wall_2"><static>true</static><pose>8.0 2.5 1 0 0 -1.2566</pose><link name="link"><collision name="col"><geometry><box><size>9.5 0.2 2</size></box></geometry></collision><visual name="vis"><geometry><box><size>9.5 0.2 2</size></box></geometry><material><ambient>0.8 0.8 0.8 1</ambient></material></visual></link></model>
    <model name="penta_wall_3"><static>true</static><pose>5.0 -6.5 1 0 0 -2.5133</pose><link name="link"><collision name="col"><geometry><box><size>9.5 0.2 2</size></box></geometry></collision><visual name="vis"><geometry><box><size>9.5 0.2 2</size></box></geometry><material><ambient>0.8 0.8 0.8 1</ambient></material></visual></link></model>
    <model name="penta_wall_4"><static>true</static><pose>-5.0 -6.5 1 0 0 2.5133</pose><link name="link"><collision name="col"><geometry><box><size>9.5 0.2 2</size></box></geometry></collision><visual name="vis"><geometry><box><size>9.5 0.2 2</size></box></geometry><material><ambient>0.8 0.8 0.8 1</ambient></material></visual></link></model>
    <model name="penta_wall_5"><static>true</static><pose>-8.0 2.5 1 0 0 1.2566</pose><link name="link"><collision name="col"><geometry><box><size>9.5 0.2 2</size></box></geometry></collision><visual name="vis"><geometry><box><size>9.5 0.2 2</size></box></geometry><material><ambient>0.8 0.8 0.8 1</ambient></material></visual></link></model>

    <!-- Security Room with Doorway and Table -->
    <model name="sec_wall_back"><static>true</static><pose>-4.5 5.5 1 0 0 0</pose><link name="link"><collision name="col"><geometry><box><size>3.0 0.2 2</size></box></geometry></collision><visual name="vis"><geometry><box><size>3.0 0.2 2</size></box></geometry><material><ambient>0.3 0.3 0.3 1</ambient></material></visual></link></model>
    <model name="sec_wall_side"><static>true</static><pose>-6.0 4.0 1 0 0 -1.5707</pose><link name="link"><collision name="col"><geometry><box><size>3.0 0.2 2</size></box></geometry></collision><visual name="vis"><geometry><box><size>3.0 0.2 2</size></box></geometry><material><ambient>0.3 0.3 0.3 1</ambient></material></visual></link></model>
    <model name="sec_wall_front_left"><static>true</static><pose>-5.2 2.6 1 0 0 0</pose><link name="link"><collision name="col"><geometry><box><size>1.4 0.2 2</size></box></geometry></collision><visual name="vis"><geometry><box><size>1.4 0.2 2</size></box></geometry><material><ambient>0.3 0.3 0.3 1</ambient></material></visual></link></model>
    <model name="security_table"><static>true</static><pose>-5.3 4.3 0.4 0 0 0</pose><link name="link"><collision name="col"><geometry><box><size>1.2 0.7 0.8</size></box></geometry></collision><visual name="vis"><geometry><box><size>1.2 0.7 0.8</size></box></geometry><material><ambient>0.6 0.3 0.1 1</ambient></material></visual></link></model>

    <!-- Storage Racks with Passable Aisles -->
    <model name="shelf_left"><static>true</static><pose>-2.5 0 0.75 0 0 0</pose><link name="link"><collision name="col"><geometry><box><size>1.2 4.0 1.5</size></box></geometry></collision><visual name="vis"><geometry><box><size>1.2 4.0 1.5</size></box></geometry><material><ambient>0.1 0.3 0.8 1</ambient></material></visual></link></model>
    <model name="shelf_right"><static>true</static><pose>2.5 0 0.75 0 0 0</pose><link name="link"><collision name="col"><geometry><box><size>1.2 4.0 1.5</size></box></geometry></collision><visual name="vis"><geometry><box><size>1.2 4.0 1.5</size></box></geometry><material><ambient>0.1 0.3 0.8 1</ambient></material></visual></link></model>
    <model name="shelf_bottom"><static>true</static><pose>0 -3.5 0.75 0 0 1.5707</pose><link name="link"><collision name="col"><geometry><box><size>1.2 4.0 1.5</size></box></geometry></collision><visual name="vis"><geometry><box><size>1.2 4.0 1.5</size></box></geometry><material><ambient>0.1 0.3 0.8 1</ambient></material></visual></link></model>

    <!-- Robot -->
    <model name="warehouse_robot">
      <pose>0 2 0.15 0 0 0</pose>
      <link name="base_link">
        <inertial><mass>10.0</mass><inertia><ixx>0.1</ixx><iyy>0.2</iyy><izz>0.2</izz></inertia></inertial>
        <collision name="collision"><geometry><box><size>0.5 0.3 0.15</size></box></geometry></collision>
        <visual name="visual"><geometry><box><size>0.5 0.3 0.15</size></box></geometry></visual>
      </link>
      <link name="left_wheel">
        <pose>0.0 0.18 -0.05 1.5707 0 0</pose>
        <inertial><mass>1.0</mass><inertia><ixx>0.005</ixx><iyy>0.005</iyy><izz>0.005</izz></inertia></inertial>
        <collision name="collision"><geometry><cylinder><radius>0.1</radius><length>0.05</length></cylinder></geometry></collision>
        <visual name="visual"><geometry><cylinder><radius>0.1</radius><length>0.05</length></cylinder></geometry></visual>
      </link>
      <link name="right_wheel">
        <pose>0.0 -0.18 -0.05 1.5707 0 0</pose>
        <inertial><mass>1.0</mass><inertia><ixx>0.005</ixx><iyy>0.005</iyy><izz>0.005</izz></inertia></inertial>
        <collision name="collision"><geometry><cylinder><radius>0.1</radius><length>0.05</length></cylinder></geometry></collision>
        <visual name="visual"><geometry><cylinder><radius>0.1</radius><length>0.05</length></cylinder></geometry></visual>
      </link>
      <link name="front_caster">
        <pose>0.2 0 -0.1 0 0 0</pose>
        <inertial><mass>0.2</mass><inertia><ixx>0.0001</ixx><iyy>0.0001</iyy><izz>0.0001</izz></inertia></inertial>
        <collision name="collision"><geometry><sphere><radius>0.05</radius></sphere></collision>
      </link>
      <link name="rear_caster">
        <pose>-0.2 0 -0.1 0 0 0</pose>
        <inertial><mass>0.2</mass><inertia><ixx>0.0001</ixx><iyy>0.0001</iyy><izz>0.0001</izz></inertia></inertial>
        <collision name="collision"><geometry><sphere><radius>0.05</radius></sphere></collision>
      </link>
      <link name="lidar_link">
        <pose>0.2 0 0.15 0 0 0</pose>
        <sensor name="lidar" type="ray">
          <always_on>true</always_on><visualize>true</visualize><update_rate>10</update_rate>
          <ray>
            <scan><horizontal><samples>360</samples><resolution>1</resolution><min_angle>-3.14159</min_angle><max_angle>3.14159</max_angle></horizontal></scan>
            <range><min>0.15</min><max>12.0</max><resolution>0.01</resolution></range>
          </ray>
          <plugin name="laser_controller" filename="libgazebo_ros_ray_sensor.so">
            <ros><remapping>~/out:=scan</remapping></ros>
            <output_type>sensor_msgs/LaserScan</output_type>
          </plugin>
        </sensor>
      </link>
      <joint name="left_wheel_joint" type="revolute"><parent>base_link</parent><child>left_wheel</child><axis><xyz>0 0 1</xyz></axis></joint>
      <joint name="right_wheel_joint" type="revolute"><parent>base_link</parent><child>right_wheel</child><axis><xyz>0 0 1</xyz></axis></joint>
      <joint name="front_caster_joint" type="fixed"><parent>base_link</parent><child>front_caster</child></joint>
      <joint name="rear_caster_joint" type="fixed"><parent>base_link</parent><child>rear_caster</child></joint>
      <joint name="lidar_joint" type="fixed"><parent>base_link</parent><child>lidar_link</child></joint>
      <plugin name="differential_drive_controller" filename="libgazebo_ros_diff_drive.so">
        <update_rate>50</update_rate>
        <left_joint>left_wheel_joint</left_joint>
        <right_joint>right_wheel_joint</right_joint>
        <wheel_separation>0.36</wheel_separation>
        <wheel_diameter>0.2</wheel_diameter>
        <command_topic>cmd_vel</command_topic>
        <odometry_topic>odom</odometry_topic>
        <odometry_frame>odom</odometry_frame>
        <robot_base_frame>base_link</robot_base_frame>
        <publish_odom>true</publish_odom>
        <publish_odom_tf>true</publish_odom_tf>
      </plugin>
    </model>
  </world>
</sdf>
"""

path = os.path.expanduser("~/warehouse_ws/src/warehouse_simulation/worlds/warehouse.world")
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w") as f:
    f.write(world_content)
print("SDF file successfully written via script.")
