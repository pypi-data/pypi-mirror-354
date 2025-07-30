import unittest
from unittest.mock import MagicMock, patch
from tc720.controller import TC720Controller

class TestTC720Controller(unittest.TestCase):

    @patch("tc720.controller.serial.Serial")
    def test_set_temperature(self, mock_serial):
        mock_instance = mock_serial.return_value
        controller = TC720Controller("/dev/fake")
        controller.set_temperature(25.0)
        mock_instance.write.assert_called_with(b"T=25.00\r")

    @patch("tc720.controller.serial.Serial")
    def test_get_setpoint(self, mock_serial):
        mock_instance = mock_serial.return_value
        mock_instance.readline.return_value = b"25.00\r\n"
        controller = TC720Controller("/dev/fake")
        result = controller.get_setpoint()
        self.assertEqual(result, "25.00")
        controller.close()

    @patch("tc720.controller.serial.Serial")
    def test_get_current_temperature(self, mock_serial):
        mock_instance = mock_serial.return_value

        mock_line = MagicMock()
        mock_line.decode.return_value.strip.return_value = "24.87"
        mock_instance.readline.return_value = mock_line

        controller = TC720Controller("/dev/fake")
        result = controller.get_current_temperature()
        self.assertEqual(result, "24.87")
        controller.close()

if __name__ == "__main__":
    unittest.main()
