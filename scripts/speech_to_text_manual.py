#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuki Furuta <furushchev@jsk.imi.i.u-tokyo.ac.jp>

import actionlib
import rospy
import speech_recognition as SR

from actionlib_msgs.msg import GoalStatus, GoalStatusArray
from audio_common_msgs.msg import AudioData
from sound_play.msg import SoundRequest, SoundRequestAction, SoundRequestGoal
from speech_recognition_msgs.msg import SpeechRecognitionCandidates
from std_msgs.msg import String

class SpeechToText(object):
    def __init__(self):
        # format of input audio data
        self.sample_rate = rospy.get_param("~sample_rate", 16000)
        self.sample_width = rospy.get_param("~sample_width", 2L)
        # language of STT service
        self.language = rospy.get_param("~language", "en")
        # ignore voice input while the robot is speaking
        self.self_cancellation = rospy.get_param("~self_cancellation", True)
        # time to assume as SPEAKING after tts service is finished
        self.tts_tolerance = rospy.Duration.from_sec(
            rospy.get_param("~tts_tolerance", 0.5))

        self.recognizer = SR.Recognizer()

        self.pub_speech = rospy.Publisher(
            "/rls_perception_services/speech_recognition_respeaker/", String, queue_size=1)
        # self.sub_audio = rospy.Subscriber("audio", AudioData, self.audio_cb)

    def run(self):
        while not rospy.is_shutdown():
            user_input = raw_input("please enter anything to start recording, enter q to quit")
            if user_input == "q":
                return False

            try:
                msg = rospy.wait_for_message('speech_audio', AudioData, timeout=5.0)
            except Exception as e:
                rospy.logwarn('No Audio detected in 5 seconds')
                continue

            data = SR.AudioData(msg.data, self.sample_rate, self.sample_width)
            try:
                rospy.loginfo("Waiting for result %d" % len(data.get_raw_data()))
                result = self.recognizer.recognize_google(data, language=self.language)
                rospy.loginfo("Detected: %s" % result)
                # msg = SpeechRecognitionCandidates(result)
                self.pub_speech.publish(result)
            except SR.UnknownValueError as e:
                rospy.logerr("Failed to recognize: %s" % str(e))
            except SR.RequestError as e:
                rospy.logerr("Failed to recognize: %s" % str(e))

if __name__ == '__main__':
    rospy.init_node("speech_to_text_manual")
    stt = SpeechToText()
    stt.run()
