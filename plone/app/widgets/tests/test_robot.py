from plone.app.widgets.testing import PLONEAPPWIDGETS_DX_ROBOT_TESTING
from plone.app.widgets.testing import SELECT_WIDGET_ROBOT_TESTING
from plone.testing import layered
import os
import robotsuite
import unittest


from plone.app.testing.interfaces import ROBOT_TEST_LEVEL


def test_suite():
    suite = unittest.TestSuite()
    current_dir = os.path.abspath(os.path.dirname(__file__))
    robot_dir = os.path.join(current_dir, 'robot')
    robot_tests = [
        os.path.join('robot', doc) for doc in
        os.listdir(robot_dir) if doc.endswith('.robot') and
        doc.startswith('test_')
    ]
    for robot_test in robot_tests:
        robottestsuite = robotsuite.RobotTestSuite(robot_test)
        robottestsuite.level = ROBOT_TEST_LEVEL
        suite.addTests([
            layered(robottestsuite,
                    layer=PLONEAPPWIDGETS_DX_ROBOT_TESTING),
        ])

    robot_widgets_dir = os.path.join(current_dir, 'robot_widgets')
    robot_widgets_tests = [
        os.path.join('robot_widgets', doc) for doc in
        os.listdir(robot_widgets_dir) if doc.endswith('.robot') and
        doc.startswith('test_')
    ]
    for robot_test in robot_widgets_tests:
        robottestsuite = robotsuite.RobotTestSuite(robot_test)
        robottestsuite.level = ROBOT_TEST_LEVEL
        suite.addTests([
            layered(robottestsuite,
                    layer=SELECT_WIDGET_ROBOT_TESTING),
        ])

    return suite
