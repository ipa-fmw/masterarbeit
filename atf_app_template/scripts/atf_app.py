#!/usr/bin/python
import unittest
import yaml
from subprocess import call

import rospy
import rostest
import rostopic
from atf_recorder import RecordingManager


class AtfApp:
    def __init__(self):
        self.recorder = RecordingManager('testblock_name')

    def execute(self):
        # Example for recorder usage
        self.recorder.start()
        self.recorder.error()
        self.recorder.stop()


class Test(unittest.TestCase):
    def setUp(self):
        self.app = AtfApp()

        robot_config = self.load_data(rospy.get_param('/robot_config'))
        self.topics = robot_config['wait_for_topics']
        self.services = robot_config['wait_for_services']

    def tearDown(self):
        call("killall gzclient", shell=True)
        call("killall gzserver", shell=True)

    def test_Recording(self):
        # Wait for topics and services
        for topic in self.topics:
            rospy.wait_for_message(topic, rostopic.get_topic_class(topic, blocking=True)[0], timeout=None)

        for service in self.services:
            rospy.wait_for_service(service, timeout=None)

        self.app.execute()

    @staticmethod
    def load_data(filename):
        rospy.loginfo("Reading data from yaml file...")

        with open(filename, 'r') as stream:
            doc = yaml.load(stream)

        return doc


if __name__ == '__main__':
    rospy.init_node('test_name')
    rostest.rosrun('atf_app', 'test_name', Test, sysargs=None)
