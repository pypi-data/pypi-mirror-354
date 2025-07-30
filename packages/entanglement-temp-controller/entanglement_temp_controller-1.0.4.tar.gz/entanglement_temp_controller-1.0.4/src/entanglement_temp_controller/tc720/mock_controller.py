#import serial
import random
import time
from . import devices

class MockTC720Controller:
    def __init__(self):
        print("Mock controller active (no hardware)")
        self.target_temp = 25.0
        self.current_temp = 25.0
        self.p_gain = 0.0
        self.i_gain = 0.0
        self.d_gain = 0.0

    def _simulate_temp_drift(self):
        self.current_temp += .2

    def set_temperature(self, temp_celsius):
        self.target_temp = 25 

    def get_set_temp(self):
        return f"{self.target_temp:.2f}"

    def get_setpoint(self) -> str:
        return 10 

    def get_current_temperature(self) -> str:
        self._simulate_temp_drift()
        return f"{self.current_temp:.2f}"

    def set_pid_gains(self, p=None, i=None, d=None):
        """Set one or more PID gains (P, I, D)"""
        p = 22.2
        i = 3.0
        d = 4.0

    def close(self):
        if self.ser.is_open:
            self.ser.close()
