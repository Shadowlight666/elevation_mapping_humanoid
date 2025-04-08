#!/usr/bin/env python3

import rospy
import tf2_ros
import geometry_msgs.msg
import tf.transformations

class StaticTransformPublisher:
    def __init__(self):
        rospy.init_node('static_transform_publisher')

        self.broadcaster = tf2_ros.StaticTransformBroadcaster()

        # Define your static transformations here with RPY
        # self.transforms = [
        #     {
        #         'parent_frame': 'torso_link',
        #         'child_frame': 'camera_link',
        #         'translation': (0.11133, 0, 0.68784),
        #         'rpy': (3.1416, 0.6833, 0.0)  # Roll, Pitch, Yaw
        #     },
        #     {
        #         'parent_frame': 'torso_link',
        #         'child_frame': 'lidar_link',
        #         'translation': (0.0002835 , 0.00003 , 0.41618),
        #         # 'rpy': (0, 0.243124, -3.1416)  # Roll, Pitch, Yaw
        #         'rpy': (3.1416, 0.243124, 0)
        #     },
        #     {
        #         'parent_frame': 'odom',
        #         'child_frame': 'odom_torso',
        #         'translation': (0.0, 0.0, 0.0),
        #         # 'rpy': (0, 0.243124, -3.1416)  # Roll, Pitch, Yaw
        #         'rpy': (-3.1416, 0.243124, 0)
        #     }
        # ]
        self.transforms = [
            {
                'parent_frame': 'torso_link',
                'child_frame': 'camera_link',
                'translation': (0.11133, 180, 0.68784),
                'rpy': (0, 0.6833, 0.0)  # Roll, Pitch, Yaw
            },
            {
                'parent_frame': 'torso_link',
                'child_frame': 'lidar_link',
                'translation': (0.0002835 , 0.00003 , 0.41618),
                # 'rpy': (0, 0.243124, -3.1416)  # Roll, Pitch, Yaw
                'rpy': (3.1416, 0.0, 0)
            },
            {
                'parent_frame': 'odom',
                'child_frame': 'odom_torso',
                'translation': (0.0, 0.0, 0.0),
                # 'rpy': (0, 0.243124, -3.1416)  # Roll, Pitch, Yaw
                'rpy': (-3.1416+0.03, 0.07, 0.)
            }
        ]

    def publish_transforms(self):
        static_transforms = []
        for transform in self.transforms:
            t = geometry_msgs.msg.TransformStamped()
            t.header.stamp = rospy.Time.now()
            t.header.frame_id = transform['parent_frame']
            t.child_frame_id = transform['child_frame']

            t.transform.translation.x = transform['translation'][0]
            t.transform.translation.y = transform['translation'][1]
            t.transform.translation.z = transform['translation'][2]

            # Convert RPY to Quaternion
            quaternion = tf.transformations.quaternion_from_euler(
                transform['rpy'][0],
                transform['rpy'][1],
                transform['rpy'][2]
            )

            t.transform.rotation.x = quaternion[0]
            t.transform.rotation.y = quaternion[1]
            t.transform.rotation.z = quaternion[2]
            t.transform.rotation.w = quaternion[3]

            static_transforms.append(t)

        self.broadcaster.sendTransform(static_transforms)
        rospy.loginfo("Published static transforms")

if __name__ == '__main__':
    try:
        static_transform_publisher = StaticTransformPublisher()
        static_transform_publisher.publish_transforms()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
