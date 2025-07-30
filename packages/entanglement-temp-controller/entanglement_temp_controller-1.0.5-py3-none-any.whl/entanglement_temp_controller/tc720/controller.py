import serial
import time
from . import devices

class TC720Controller:
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(
            port=port,
            baudrate=230400,
            timeout=1
        )

    def set_temperature(self, target_celsius: float):
        temp = int(round(target_celsius * 100))
        if temp < 0:
            temp = 65536 + temp
        hex_str = f"{temp:04x}"
        payload = ['1','c'] + list(hex_str)
        checksum = sum(ord(c) for c in payload) % 256
        checksum_hex = f"{checksum:02x}"
        full_cmd = ['*'] + payload + list(checksum_hex) + ['\r']
        self._send(full_cmd)

    def get_setpoint(self) -> str:
        #return self.parse_temp(resp)
        self.ser.reset_input_buffer()
        cmd = ['*','0','2','0','0','0','0','2','3','\r']
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        for ch in cmd:
            self.ser.write(ch.encode('ascii'))
            time.sleep(0.004)

        time.sleep(0.05)

        buf = []
        for _ in range(8):
            byte = self.ser.read(1)
            print(f"Raw get_setpoint response: {byte}")
            if not byte:
                raise TimeoutError("No response from TC-720 during setpoing read")
            buf.append(byte.decode('ascii'))
        return self.parse_temp(buf)

    def get_current_temperature(self) -> str:
        cmd = ['*', '0', '1', '0', '0', '0', '0', '2', '1', '\r']
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        for ch in cmd:
            self.ser.write(ch.encode('ascii'))
            time.sleep(0.004)

        time.sleep(0.05)

        buf = []
        for _ in range(8):
            b = self.ser.read(1)
            if not b:
                raise TimeoutError("No response from TC-720 for temperature read")
            buf.append(b.decode('ascii'))

        print("Raw temperature response:", ''.join(buf))
        return self.parse_temp(buf)

    def _send(self, cmd: str):
        self.ser.reset_input_buffer()
        for ch in cmd:
            self.ser.write(ch.encode('ascii'))
            time.sleep(0.1)

    def read_response(self, num_bytes=8):
        buf = []
        for _ in range(num_bytes):
            b = self.ser.read(1)
            if not b:
                break
            buf.append(b.decode('ascii'))
        return buf

    def _query(self, num_bytes=8, retries=3):
        result = []
        for attempt in range(retries):
            for _ in range(num_bytes):
                byte = self.ser.read(1)
                if byte:
                    result.append(chr(byte[0]))
                else:
                    break
            if len(result) == num_bytes:
                return result
            time.sleep(0.1)
        raise TimeoutError(f"Incomple response after {retries} attempts: got {len(result)} bytes")

    def parse_temp(self, chars):
        if len(chars) < 5:
            return None
        newval = 0
        divvy = 4096
        for pn in range(1,5):
            vally = ord(chars[pn])
            subby = 48 if vally < 97 else 87
            newval += ((vally - subby) * divvy)
            divvy /= 16
        if newval > 32767:
            newval -= 65536
        temp_c = newval / 100.0

        if not (-100 <= temp_c <= 300):
            return None
        return temp_c

    def set_pid_gains(self, p=None, i=None, d=None):
        """Set one or more PID gains (P, I, D)"""
        if p is not None:
            self._send(f"PG {p:.2f}")
        if i is not None:
            self._send(f"IG {i:.2f}")
        if d is not None:
            self._send(f"DG {d:.2f}")

    def close(self):
        if self.ser.is_open:
            self.ser.close()
