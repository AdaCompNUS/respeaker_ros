import rospy
from audio_common_msgs.msg import AudioData
import numpy as np

class Listener:

    def __init__(self):
        rospy.init_node('listener')
        rospy.Subscriber('/audio', AudioData, self.callback)
        rospy.spin()

    def callback(self, data):
        rt_value = np.frombuffer(data.data, dtype=np.int16)
        rt_value = np.reshape(rt_value, (2725, 4))
        a=1


if __name__ == '__main__':
    system = Listener()