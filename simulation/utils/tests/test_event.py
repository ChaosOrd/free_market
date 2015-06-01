import unittest
from unittest.mock import Mock
from utils.event import Event
from types import MethodType


class EventTest(unittest.TestCase):

    def test_invokes_subscribed_function(self):
        event = Event()
        handler = Mock()

        event += handler
        event()

        handler.assert_called_once_with()

    def test_invokes_multiple_subscribed_functions(self):
        event = Event()
        first_handler = Mock()
        second_handler = Mock()

        event += first_handler
        event += second_handler
        event()

        first_handler.assert_called_once_with()
        second_handler.assert_called_once_with()

    def test_invokes_callbacks_with_arguments(self):
        event = Event()
        handler = Mock()
        argument = Mock()

        event += handler
        event(argument)

        handler.assert_called_once_with(argument)

    def test_does_not_invoke_removed_callbacks(self):
        event = Event()
        first_handler = Mock()
        second_handler = Mock()

        event += first_handler
        event += second_handler
        event -= first_handler
        event()

        self.assertFalse(first_handler.called)
        second_handler.assert_called_once_with()

    def test_invokes_methods_with_proper_self(self):
        event = Event()
        method_handler = Mock(spec=MethodType)

        event += method_handler
        event()

        method_handler.assert_called_once_with(method_handler.__self__)


if __name__ == '__main__':
    unittest.main()
