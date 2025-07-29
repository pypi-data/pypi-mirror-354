import machine
from typing import Callable, Optional


def get_sys_info() -> tuple:
    """
    Get system information including core frequency and temperature.  
    
    :return: tuple of (frequency, temperature)
    """
    
def get_mem_info() -> tuple:
    """
    Get memory usage information.
    
    :return: tuple of (free, used, total) memory in bytes
    """

def get_fs_info(path='/') -> tuple:
    """
    Get filesystem information for the given path.
    
    :param path: Path to check filesystem info for.
    :return: tuple of (total, used, free, usage percentage)
    """


class WifiManager:
    """
    A class to manage WiFi connections on the TiCLE.
    This class provides methods to scan for available networks, connect to a network, disconnect, and get the IP address.
    It uses the `network` module to handle WiFi operations.
    """
    def __init__(self, *, iface=None):
        """
        Initialize the Wifi class.
        :param iface: Optional network interface to use. If not provided, it defaults to the STA_IF interface.
        """

    def scan(self) -> list[tuple[str,int,int,int]]:
        """
        Scan for available WiFi networks.
        
        :return: List of tuples containing (SSID, RSSI, channel, security).
        """

    def available_ssids(self) -> list[str]:
        """
        Get a list of available SSIDs from the scanned access points.
        
        :return: List of unique SSIDs found in the scanned access points.
        """

    def connect(self, ssid: str, password: str, timeout: float = 20.0) -> bool:
        """
        Connect to a WiFi network with the given SSID and password.
        
        :param ssid: SSID of the WiFi network to connect to.
        :param password: Password for the WiFi network.
        :param timeout: Timeout in seconds for the connection attempt (default is 20 seconds).
        :return: True if connected successfully, False otherwise.
        """

    def disconnect(self) -> None:
        """
        Disconnect from the currently connected WiFi network.
        This method will disconnect the WiFi interface if it is currently connected.
        """
    
    @property
    def is_connected(self) -> bool:
        """
        Check if the WiFi interface is currently connected to a network.
        
        :return: True if connected, False otherwise.
        """
    
    @property
    def ip(self) -> str | None:
        """
        Get the IP address of the connected WiFi network.
        
        :return: IP address as a string if connected, None otherwise.
        """
        
    def ifconfig(self) -> tuple | None:
        """
        Get the IP address of the connected WiFi network.
        
        :return: Tuple containing (ip, netmask, gateway, dns) if connected, None otherwise.
        """


class pLed():
    """
    Basic Led control class built into Pico2W.
    """

    def on(self):
        """
        Turn on the built-in LED.
        """
    
    def off(self):
        """
        Turn off the built-in LED.
        """
    
    def toggle(self):
        """
        Toggle the state of the built-in LED.
        """
    
    def value(self, val: int | bool):
        """
        Set the state of the built-in LED.
        
        :param val: True/1 to turn on, False/0 to turn off.
        """
    
    def value(self) -> int:
        """
        Get the current state of the built-in LED.
        
        :return: 1 if on, 0 if off.
        """


class Din:
    """
    A class to read digital input pins.
    This class allows reading the state of multiple GPIO pins as digital inputs.
    It provides a convenient way to read the state of multiple input pins simultaneously.
    The class supports pull-up and pull-down configurations, as well as callback triggers for pin state changes.
    """
    LOW         = 0
    HIGH        = 1
    
    PULL_DOWN   = 1
    PULL_UP     = 2
    CB_FALLING  = 4
    CB_RISING   = 8
    
    def __init__(self, pins:tuple[int, ...], pull:int|None=None, trigger:int|None=0, callback:function|None=None):
        """
        Initialize the digital input pins.
        
        if trigger and callback are provided, the callback function will be called when the pin state changes.
        callback function signature is `def on_user(pin:int)`:  
            pin is the GPIO pin number that triggered the callback.  
                    
        :param pins: Tuple of GPIO pin numbers to be used as digital inputs.
        :param pull: Pull-up or pull-down configuration (default is None).
        :param trigger: Callback trigger type (default is None).
        :param callback: Callback function for the trigger (default is None).
        """
    
    def __getitem__(self, index:int) -> int:
        """
        Get the value of a specific pin.
        
        :param index: Index of the pin (0 to len(pins)-1).
        :return: Pin value (0 or 1).
        """

    def __len__(self) -> int:
        """
        Get the number of digital input pins.
        
        :return: Number of pins.
        """


class Dout:
    """
    A class to control digital output pins.
    This class allows setting the state of multiple GPIO pins to either LOW or HIGH.
    It provides a convenient way to control multiple output pins simultaneously.
    """
    LOW         = 0
    HIGH        = 1
    PULL_DOWN   = machine.Pin.PULL_DOWN
    PULL_UP     = machine.Pin.PULL_UP
        
    def __init__(self, pins:tuple[int, ...], pull:int|None=None):
        """
        Initialize the Dout class with a tuple of GPIO pin numbers.
        
        :param pins: Tuple of GPIO pin numbers to be used as digital outputs.
        :param pull: Pull-up or pull-down configuration (default is None).
        :raises ValueError: If the provided pins are not valid GPIO pin numbers.
        """
        
    def __getitem__(self, index:int):
        """
        Get the value of a specific pin.
        
        :param idx: Index of the pin (0 to len(pins)-1).
        :return: Pin value (0 or 1).
        """

    def __setitem__(self, index:int, value:int):
        """
        Set the value of a specific pin to LOW or HIGH.
        
        :param idx: Index of the pin (0 to len(pins)-1).
        :param value: Pin value to set (0 for LOW, 1 for HIGH).
        :raises ValueError: If the value is not 0 or 1.
        """

    def __len__(self) -> int:
        """
        Get the number of digital input pins.
        
        :return: Number of pins.
        """


class Adc():
    """
    A class to read analog values from ADC pins.
    """
    
    def __init__(self, pins:tuple, period:int=0, callback:function=None):
        """
        Initialize the ADC pin.
 
        If period and callback are provided, the callback function will be called repeatedly at the specified interval.
        The callback function signature is `def on_user(pin:int, value:float, level:int)`: 
            pin is the GPIO pin number,
            value is the analog value in volts,
            level is the raw ADC value (0-65535).            
    
        :param pins: Tuple of GPIO pin numbers (26, 27, or 28).
        :param period: Interval in milliseconds to call the callback function.
        :param callback: Callback function to be called at the specified interval.
        """        
                
    def __getitem__(self, index:int) -> tuple:
        """
        Read the analog value from the ADC pin.
        resolution = 3.3V/4096 = 0.0008056640625V/bit. (0.806mV/bit)
        Therefore, the voltage can be accurately represented up to three decimal places.
        
        :param index: Index of the pin (0 to len(pins)-1).
        :return: Tuple of (voltage, raw_value).
        """

    def __len__(self) -> int:
        """
        Get the number of ADC pins.
        
        :return: Number of pins.
        """


class Pwm:
    """
    A class to control PWM (Pulse Width Modulation) on TiCLE.
    This class allows setting the frequency, period, and duty cycle of PWM signals.
    It can be used to control devices like motors, LEDs, and other peripherals that require PWM signals.
    The class supports multiple pins for PWM output, allowing simultaneous control of multiple devices.

    Example
    -------
    >>> with Pwm((8, 9, 10), 50) as pwm:
    ...     pwm[0].duty = 25
    ...     pwm.all.duty = 80
    ...     pwm.all.enable = False
    """

    class _PwmPin:
        """
        A class to control a single PWM pin.
        This class allows setting the frequency, period, and duty cycle of a PWM signal on a specific pin.
        It is used internally by the Pwm class to manage individual PWM pins.
        """
        def __init__(self, pin: int):
            """
            Initialize the PWM pin.
            :param pin: GPIO pin number for PWM output.
            """

        def __apply_freq(self):
            """
            Apply the frequency to the PWM pin.
            This method sets the frequency of the PWM signal on the pin.
            It calculates the period in microseconds based on the frequency and updates the PWM pin accordingly.
            """

        def __apply_duty(self):
            """
            Apply the duty cycle to the PWM pin.
            This method sets the duty cycle of the PWM signal on the pin.
            It calculates the raw duty cycle value based on the percentage and updates the PWM pin accordingly.
            """

        @property
        def freq(self) -> int:
            """
            Frequency [Hz].
            This property gets or sets the frequency of the PWM signal.

            :return: Frequency in Hz.
            """

        @freq.setter
        def freq(self, hz: int):
            """
            Set the frequency of the PWM signal.
            
            :param hz: Frequency in Hz.
            :raises ValueError: If the frequency is less than or equal to 0.
            """

        @property
        def period(self) -> int:
            """
            Period [us].
            This property gets or sets the period of the PWM signal in microseconds.
            
            :return: Period in microseconds.
            """

        @period.setter
        def period(self, us: int):
            """
            Set the period of the PWM signal in microseconds.
            :param us: Period in microseconds.
            :raises ValueError: If the period is less than or equal to 0.
            """

        @property
        def duty(self) -> int:
            """
            Duty cycle [%].
            This property gets or sets the duty cycle of the PWM signal as a percentage (0-100).
            
            :return: Duty cycle percentage.
            """

        @duty.setter
        def duty(self, pct: int):
            """
            Set the duty cycle of the PWM signal as a percentage (0-100).
            :param pct: Duty cycle percentage (0-100).
            :raises ValueError: If the percentage is less than 0 or greater than 100.
            """

        @property
        def duty_raw(self) -> int:
            """
            Duty cycle in raw value [0-65535].
            This property gets or sets the duty cycle of the PWM signal in raw value (0-65535).
            
            :return: Duty cycle in raw value.
            """

        @duty_raw.setter
        def duty_raw(self, raw: int):
            """
            Set the duty cycle of the PWM signal in raw value (0-65535).
            
            :param raw: Duty cycle in raw value (0-65535).
            :raises ValueError: If the raw value is less than 0 or greater than 65535.
            """

        @property
        def duty_us(self) -> int:
            """
            Duty cycle in microseconds [0-period_us].
            This property gets or sets the duty cycle of the PWM signal in microseconds (0 to period_us).
            
            :return: Duty cycle in microseconds.
            """

        @duty_us.setter
        def duty_us(self, us: int):
            """
            Set the duty cycle of the PWM signal in microseconds (0 to period_us).
            
            :param us: Duty cycle in microseconds (0 to period_us).
            :raises ValueError: If the microseconds value is less than 0 or greater than period_us.
            """

        @property
        def enable(self) -> bool:
            """
            Enable or disable the PWM signal.
            This property gets or sets whether the PWM signal is enabled or disabled.
            
            :return: True if enabled, False if disabled.
            """

        @enable.setter
        def enable(self, flag: bool):
            """
            Enable or disable the PWM signal.
            
            :param flag: True to enable the PWM signal, False to disable it.
            """

    class _PwmGroup:
        """
        A class to manage a group of PWM pins.
        This class allows setting the frequency, period, and duty cycle for multiple PWM pins simultaneously.
        It provides a convenient way to control multiple PWM outputs with the same settings.
        """

        def __init__(self, pins:tuple):
            """
            Initialize the PWM group with a tuple of PWM pins.
            
            :param pins: Tuple of PwmPin objects to be managed as a group.
            """

        @property
        def freq(self) -> int:
            """
            Frequency [Hz].
            This property gets or sets the frequency of the PWM signal for all pins in the group.
            
            :return: Frequency in Hz.
            """

        @freq.setter
        def freq(self, hz: int):
            """
            Set the frequency of the PWM signal for all pins in the group.
            
            :param hz: Frequency in Hz.
            :raises ValueError: If the frequency is less than or equal to 0.
            """

        @property
        def period(self) -> int:
            """
            Period [us].
            This property gets or sets the period of the PWM signal for all pins in the group.
            
            :return: Period in microseconds.
            """

        @period.setter
        def period(self, us: int):
            """
            Set the period of the PWM signal for all pins in the group.
            
            :param us: Period in microseconds.
            :raises ValueError: If the period is less than or equal to 0.
            """

        @property
        def duty(self) -> int:
            """
            Duty cycle [%].
            This property gets or sets the duty cycle of the PWM signal for all pins in the group.
            
            :return: Duty cycle percentage.
            """

        @duty.setter
        def duty(self, pct: int):
            """
            Set the duty cycle of the PWM signal for all pins in the group.
            
            :param pct: Duty cycle percentage (0-100).
            :raises ValueError: If the percentage is less than 0 or greater than 100.
            """

        @property
        def enable(self) -> bool:
            """
            Enable or disable the PWM signal for all pins in the group.
            This property gets or sets whether the PWM signal is enabled or disabled for all pins in the group.
            
            :return: True if enabled, False if disabled.
            """

        @enable.setter
        def enable(self, flag: bool):
            """
            Enable or disable the PWM signal for all pins in the group.
            
            :param flag: True to enable the PWM signal, False to disable it.
            """

        def map(self, fn:function) -> None:
            """
            Apply a function to all PWM pins in the group.
            This method allows you to apply a function to each PWM pin in the group.
            
            :param fn: Function to apply to each PWM pin.
            :raises TypeError: If the provided function is not callable.
            """

    def __init__(self, pins:tuple):
        """
        Initialize the Pwm class with a tuple of GPIO pin numbers and a frequency.
        
        :param pins: Tuple of GPIO pin numbers to be used for PWM output.
        :raises ValueError: If the frequency is less than or equal to 0.
        """
        self._pins = [Pwm._PwmPin(pin) for pin in pins]
        self.all = Pwm._PwmGroup(self._pins)
        
    def __getitem__(self, idx: int) -> _PwmPin:
        """
        Get a specific PWM pin by index.
        
        :param idx: Index of the pin (0 to len(pins)-1).
        :return: PwmPin object for the specified pin.
        """
        return self._pins[idx]
    
    def __len__(self):
        """
        Get the number of PWM pins.
        
        :return: Number of PWM pins.
        """

    def __iter__(self):
        """
        Iterate over the PWM pins.
        
        :return: An iterator over the PwmPin objects.
        """


class Button:
    """
    A simple button class to handle single click, double click and long press events.
    """
    
    def __init__(self, double_click_ms:int=260, long_press_ms:int=800, debounce_ms:int=20):
        """
        Initializes the button with specified timings for double click, long press, and debounce.
        
        :param double_click_ms: Time in milliseconds to consider a double click.
        :param long_press_ms: Time in milliseconds to consider a long press.
        :param debounce_ms: Time in milliseconds to debounce the button press.
 
        on_clicked, on_double_clicked, on_long_pressed are callback functions that will be called when the respective events occur.
        They should be defined as:
            def on_clicked():
                # Handle single click event
                pass
            
            def on_double_clicked():
                # Handle double click event
                pass
            
            def on_long_pressed():
                # Handle long press event
                pass
        """

    on_clicked: Optional[Callable[[], None]]  #: Called once on a **single click**.
    on_double_clicked: Optional[Callable[[], None]] #: Called once on a **double click**.
    on_long_pressed: Optional[Callable[[], None]]  #: Called once on a **long press**.


def i2cdetect(bus:int, show:bool=False) -> list | None:
    """
    Detect I2C devices on the specified bus.

    :param bus: The I2C bus number. 0 or 1.
    :param show: If True, it prints the entire status, if False, it returns only the recognized device addresses in a list.
    :return: A list of detected I2C devices.
    """
 

class I2c:
    """
    I2C class for TiCLE.
    This class is a wrapper around the machine.I2C class to provide a more user-friendly interface.
    It automatically detects the I2C bus based on the provided SDA and SCL pins.
    """
    
    def __init__(self, scl:int, sda:int, addr:int, freq:int=400_000):
        """
        Initialize the I2C bus with the specified SDA and SCL pins.
        
        :param scl: The SCL pin number.
        :param sda: The SDA pin number.
        :param freq: The frequency of the I2C bus (default is 400kHz).
        """        
        
    def read_u8(self, reg: int) -> int:
        """
        Read an unsigned 8-bit value from the specified register.
        
        :param reg: The register address to read from.
        :return: The value read from the register.
        """

    def read_u16(self, reg: int, *, little_endian: bool = True) -> int:
        """
        Read an unsigned 16-bit value from the specified register.
        
        :param reg: The register address to read from.
        :param little_endian: If True, read the value in little-endian format, otherwise in big-endian format.
        :return: The value read from the register.
        """

    def write_u8(self, reg: int, val: int) -> None:
        """
        Write an unsigned 8-bit value to the specified register.
        
        :param reg: The register address to write to.
        :param val: The value to write to the register (0-255).
        """

    def write_u16(self, reg: int, val: int, *, little_endian: bool = True) -> None:
        """
        Write an unsigned 16-bit value to the specified register.
        
        :param reg: The register address to write to.
        :param val: The value to write to the register (0-65535).
        :param little_endian: If True, write the value in little-endian format, otherwise in big-endian format.
        """

    def readfrom(self, nbytes: int, *, stop: bool = True) -> bytes:
        """
        Read a specified number of bytes from the I2C device.
        
        :param nbytes: The number of bytes to read.
        :param stop: If True, send a stop condition after reading.
        :return: The bytes read from the I2C device.
        """

    def readinto(self, buf: bytearray, *, stop: bool = True) -> int:
        """
        Read bytes into a buffer from the I2C device.
        
        :param buf: The buffer to read the bytes into.
        :param stop: If True, send a stop condition after reading.
        :return: The number of bytes read into the buffer.
        """

    def readfrom_mem(self, reg: int, nbytes: int, *, addrsize: int = 8) -> bytes:
        """
        Read a specified number of bytes from a specific register in the I2C device.
        
        :param reg: The register address to read from.
        :param nbytes: The number of bytes to read.
        :param addrsize: The address size in bits (default is 8 bits).
        :return: The bytes read from the specified register.
        """

    def readfrom_mem_into(self, reg: int, buf: bytearray, *, addrsize: int = 8) -> int:
        """
        Read bytes from a specific register in the I2C device into a buffer.
        
        :param reg: The register address to read from.
        :param buf: The buffer to read the bytes into.
        :param addrsize: The address size in bits (default is 8 bits).
        :return: The number of bytes read into the buffer.
        """

    def writeto(self, buf: bytes, *, stop: bool = True) -> int:
        """
        Write bytes to the I2C device.
        
        :param buf: The bytes to write to the I2C device.
        :param stop: If True, send a stop condition after writing.
        :return: The number of bytes written to the I2C device.
        """

    def writeto_mem(self, reg: int, buf: bytes, *, addrsize: int = 8) -> int:
        """
        Write bytes to a specific register in the I2C device.
        
        :param reg: The register address to write to.
        :param buf: The bytes to write to the specified register.
        :param addrsize: The address size in bits (default is 8 bits).
        :return: The number of bytes written to the specified register.
        """


class ReplSerial:
    """
    This class provides a way to read from and write to the REPL (Read-Eval-Print Loop) using a ring buffer.
    It allows for non-blocking reads, reading until a specific pattern, and writing data to the REPL.   
    """
    
    def __init__(self, timeout: float | None = None, *, bufsize=512, poll_ms=10):
        """
        Initialize the ReplSerial class.
    
        :param timeout: The timeout in seconds for read operations. If None, it will block until data is available.
        - timeout=None : blocking read
        - timeout=0    : non-blocking read
        - timeout>0    : wait up to timeout seconds
        :param bufsize: The size of the ring buffer (default is 512 bytes).
        :param poll_ms: The polling interval in milliseconds for reading data from the REPL (default is 10 ms).
        """

    @property
    def timeout(self):
        """
        Get the timeout for read operations.
        - timeout=None : blocking read
        - timeout=0    : non-blocking read
        - timeout>0    : wait up to timeout seconds
        """
    
    @timeout.setter
    def timeout(self, value:float|None):
        """
        Set the timeout for read operations.
        - timeout=None : blocking read
        - timeout=0    : non-blocking read
        - timeout>0    : wait up to timeout seconds
        
        :param value: The timeout value in seconds. If None, it will block indefinitely.
        """

    def read(self, size:int=1) -> bytes:
        """
        Read `size` bytes from the REPL buffer.
        If `size` is less than or equal to 0, it returns an empty byte string.
        If `size` is greater than the available data, it waits for data to become available based on the timeout.
        
        :param size: The number of bytes to read (default is 1).
        :return: The read bytes as a byte string.
        """   

    def read_until(self, expected: bytes = b'\n', max_size: int | None = None) -> bytes:
        """
        Read from the REPL buffer until the expected byte sequence is found, the maximum size is reached, or a timeout occurs.
        If `max_size` is specified, it limits the amount of data read.
        If `expected` is not found within the timeout, it returns an empty byte string.
        
        - timeout=0     : non-blocking -> return only when pattern or max_size is satisfied, else b''
        - timeout>0     : wait up to timeout, then same as above or b'' on timeout
        - timeout=None  : blocking until pattern or max_size
        
        :param expected: The expected byte sequence to look for (default is b'\n').
        :param max_size: The maximum size of data to read (default is None, no limit).
        :return: The data read from the REPL buffer, including the expected sequence if found.
        """

    def write(self, data: bytes) -> int:
        """
        Write `data` to the REPL UART.
        If `data` is not bytes or bytearray, it raises a TypeError.
        
        :param data: The data to write (must be bytes or bytearray).
        :return: The number of bytes written.
        """

    def close(self):
        """
        Close the REPL serial connection and deinitialize the timer.
        This method stops the periodic timer and releases resources.
        """


def input(prompt: str = "") -> str:
    """
    Blocking input() replacement with:
      - UTF-8 decoding (1–4 bytes per char)
      - ←/→ arrow cursor movement
      - Backspace deletes before cursor
      - Deletes at cursor
      - Proper insertion anywhere in the line
    """


#-----------------------------------------------------------------------------------------------
# Extensions
#------------------------------------------------------------------------------------------------


class Relay:
    ON = Dout.HIGH
    OFF = Dout.LOW

    class _Channel:
        """
        A class representing a single relay channel.
        This class provides properties to get and set the state of the relay,
        turn the relay on or off, and set the delay in milliseconds.
        """
        def __init__(self, parent, idx):
            """
            Initialize the relay channel with a reference to the parent Relay instance and its index.
            
            :param parent: Reference to the parent Relay instance
            :param idx: Index of the relay channel (0-based)
            """

        @property
        def state(self) -> int:
            """
            Get the current state of the relay channel.
            This property returns the state of the relay channel, which can be either Relay.ON or Relay.OFF.
            
            :return: Current state of the relay channel (Dout.HIGH or Dout.LOW)
            """

        @state.setter
        def state(self, val: int) -> None:
            """
            Set the state of the relay channel.
            This property sets the state of the relay channel to either Relay.ON or Relay.OFF.
            
            :param val: State to set (Dout.HIGH or Dout.LOW)
            """

        def on(self) -> None:
            """
            Turn the relay channel on.
            This method sets the state of the relay channel to Relay.ON.
            """

        def off(self) -> None:
            """
            Turn the relay channel off.
            This method sets the state of the relay channel to Relay.OFF.
            """

        @property
        def delay_ms(self) -> int:
            """
            Get the minimum delay in milliseconds for the relay channel.
            This property returns the minimum delay in milliseconds that is applied after changing the state of the relay channel.
            
            :return: Minimum delay in milliseconds
            """

        @delay_ms.setter
        def delay_ms(self, ms: int) -> None:
            """
            Set the minimum delay in milliseconds for the relay channel.
            This property sets the minimum delay in milliseconds that is applied after changing the state of the relay channel.
            :param ms: Minimum delay in milliseconds
            """

    class _Group:
        """
        A class representing a group of relay channels.
        This class allows setting attributes for all channels in the group at once.
        """
        def __init__(self, channels):
            """
            Initialize the group of relay channels.
            
            :param channels: List of Relay._Channel objects
            """

        def __setattr__(self, name, value):
            """
            Set an attribute for all channels in the group.
            If the attribute name starts with an underscore, it is set on the group itself.
            
            :param name: Attribute name
            :param value: Value to set for the attribute
            """

        def __getattr__(self, name):
            """
            Get an attribute from the first channel in the group.
            """

    def __init__(self, pins:tuple[int, ...], min_delay_ms:int=5):
        """
        Initialize the Relay with specified GPIO pins and minimum delay.
        
        :param pins: Tuple of GPIO pin numbers for the relay channels (e.g., (2, 3, 4))
        :param min_delay_ms: Minimum delay in milliseconds after changing the state of a relay channel (default 5 ms)
        """

    def __getitem__(self, idx:int) -> _Channel:
        """
        Get the relay channel at the specified index.
        
        :param idx: Index of the relay channel (0-based)
        :return: Relay._Channel object for the specified index
        """

    def __len__(self) -> int:
        """
        Get the number of relay channels.
        
        :return: Number of relay channels
        """


class ServoMotor:
    """
    A class to control servo motors using PWM.
    This class allows setting the angle of individual servo motors and provides
    methods to set the angle for all servos at once.
    """
    class _Channel:
        """
        A class representing a single servo channel.
        This class provides properties to get and set the angle, speed, and non-blocking behavior of the servo.
        """
        def __init__(self, parent, idx):
            """
            Initialize the servo channel with a reference to the parent ServoMotor instance and its index.
            
            :param parent: Reference to the parent ServoMotor instance
            :param idx: Index of the servo channel (0-based)"""

        @property
        def angle(self) -> float:
            """
            Get the current angle of the servo channel.
            This property returns the current angle in degrees (0 to 180).
            
            :return: Current angle in degrees
            """

        @angle.setter
        def angle(self, deg: float) -> None:
            """
            Set the target angle for the servo channel.
            This property clamps the angle to the range [0, 180] degrees and updates the target angle.
            
            :param deg: Target angle in degrees (0 to 180)
            """

        @property
        def speed_ms(self) -> int:
            """
            Get the speed in milliseconds for the servo channel.
            This property returns the speed in milliseconds for moving to the target angle.
            
            :return: Speed in milliseconds
            """

        @speed_ms.setter
        def speed_ms(self, ms: int) -> None:
            """
            Set the speed in milliseconds for the servo channel.
            This property sets the speed for moving to the target angle.
            """

        @property
        def nonblocking(self) -> bool:
            """
            Get the non-blocking flag for the servo channel.
            This property indicates whether the servo channel operates in non-blocking mode.
            
            :return: True if non-blocking mode is enabled, False otherwise
            """

        @nonblocking.setter
        def nonblocking(self, flag: bool) -> None:
            """
            Set the non-blocking flag for the servo channel.
            This property enables or disables non-blocking mode for the servo channel.
            
            :param flag: True to enable non-blocking mode, False to disable
            """

    class _Group:
        def __init__(self, channels):
            """
            Initialize the group of servo channels.
            
            :param channels: List of ServoMotor._Channel objects
            """

        def __setattr__(self, name, value):
            """
            Set an attribute for all channels in the group.
            If the attribute name starts with an underscore, it is set on the group itself.
            :param name: Attribute name
            :param value: Value to set for the attribute
            """

        def __getattr__(self, name):
            """
            Get an attribute from the first channel in the group.
            If the attribute does not exist, it raises an AttributeError.
            
            :param name: Attribute name
            :return: Value of the attribute from the first channel
            """

    def __init__(self, pins:tuple[int, ...], freq:int=50, default_min_us:int=500, default_max_us: int=2500, initial_angle: float=0.0):
        """
        Initialize the ServoMotor with specified GPIO pins and parameters.
        
        :param pins: Tuple of GPIO pin numbers for the servo motors (e.g., (2, 3, 4))
        :param freq: PWM frequency in Hz (default 50 Hz)
        :param default_min_us: Default minimum pulse width in microseconds (default 500 us)
        :param default_max_us: Default maximum pulse width in microseconds (default 2500 us)
        :param initial_angle: Initial angle for all servos in degrees (default 0.0)
        """

    def __getitem__(self, idx: int) -> _Channel:
        """
        Get the servo channel at the specified index.
        
        :param idx: Index of the servo channel (0-based)
        :return: ServoMotor._Channel object for the specified index
        """
        return self._channels[idx]

    def deinit(self) -> None:
        """
        Deinitialize the ServoMotor instance.
        This method stops the timer and disables all PWM channels.
        """


class PiezoBuzzer:
    """
    A class to control a piezo buzzer using PWM.
    It can play tones, melodies, and supports effects like staccato, vibrato, and tremolo.
    """

    def __init__(self, pin:int, tempo:int=120):
        """
        Initialize the PiezoBuzzer with the specified pin and tempo.
        
        :param pin: GPIO pin number for the buzzer (default 1).
        :param tempo: Tempo in beats per minute (default 120).
        """

    def tone(self, note_oct:str, length:int=4, effect:str=None):
        """
        Play a single tone with the specified note, length, and effect.
        
        :param note_oct: Musical note with octave (e.g., 'C4', 'A#5').
        :param length: Length of the note in beats (default 4).
        :param effect: Effect to apply to the note (e.g., 'staccato', 'vibrato', 'tremolo', 'gliss:C#5').
        """

    def play(self, melody, effect:str=None, background:bool=False):
        """
        Play a melody consisting of notes and lengths.
        
        :param melody: List of notes and lengths (e.g., ['C4', 4, 'D4', 2, 'E4', 1]).
        :param effect: Effect to apply to the melody (e.g., 'staccato', 'vibrato', 'tremolo').
        :param background: If True, play the melody in the background (default False).
        """

    def stop(self):
        """
        Stop playing the current melody and reset the buzzer state.
        """

    def set_tempo(self, bpm:int):
        """
        Set the tempo for the buzzer in beats per minute.
        
        :param bpm: Tempo in beats per minute
        """


class SR04:
    """
    This class drives an HC-SR04 ultrasonic sensor by emitting a 40 kHz pulse 
    and measuring its time-of-flight (using the speed of sound ≈343 m/s at 20 °C) 
    to compute distances from 2 cm to 400 cm, then applies a Kalman filter 
    to smooth out measurement noise.
    """    
    
    def __init__(self, trig:int, echo:int, *, temp_c:float=20.0, R:int=25, Q:int=4):
        """
        Initialize the ultrasonic sensor with the specified trigger and echo pins.
        
        :param trig: GPIO pin number for the trigger pin.
        :param echo: GPIO pin number for the echo pin.
        :param temp_c: Temperature in degrees Celsius (default is 20.0).
        :param R: Measurement noise covariance (default is 25).
        :param Q: Process noise covariance (default is 4).
        """
    
    def read(self, timeout_us:int=30_000, temp_c:float|None=None) -> float|None:
        """
        Read the distance from the ultrasonic sensor.
        
        :param timeout_us: Timeout in microseconds for the echo signal.
        :return: Distance in centimeters or None if timeout occurs.
        """


class WS2812:
    """
    A class to control WS2812 NeoPixel LEDs in a grid layout.
    Supports 2D addressing with zigzag option, brightness control, and various effects.
    """
    RED     = (255, 0,   0)
    GREEN   = (0,   255, 0)
    BLUE    = (0,   0, 255)
    YELLOW  = (255, 255, 0)
    CYAN    = (0,   255, 255)
    MAGENTA = (255, 0,   255)
    WHITE   = (255, 255, 255)

    def __init__(self, pin:int, *, width:int, height:int, bright:float = 0.5, zigzag:bool = False):
        """
        Initialize the WS2812 LED grid.

        :param pin: GPIO pin number for the NeoPixel data line.
        :param width: Number of LEDs in the horizontal direction.
        :param height: Number of LEDs in the vertical direction.
        :param bright: Brightness level (0.0 to 1.0).
        :param zigzag: If True, the addressing will be zigzagged (i.e., alternate rows reversed).
        """
        
    def __len__(self) -> int: 
        """
        Get the total number of LEDs in the grid.

        :return: Total number of LEDs (width * height).
        """
    
    def __getitem__(self, idx:int | tuple[int, int]) -> tuple[int, int, int]:
        """
        Get the color of a specific LED by index or 2D coordinates.

        :param idx: An integer index or a tuple (x, y) for 2D coordinates.
        :return: A tuple (r, g, b) representing the color of the LED.
        :raises IndexError: If idx is out of bounds.
        """

    def __setitem__(self, idx:int|tuple[int, int], color):
        """
        Set the color of a specific LED by index or 2D coordinates.

        :param idx: An integer index or a tuple (x, y) for 2D coordinates.
        :param color: A tuple (r, g, b) representing the color to set.
        :raises TypeError: If color is not a tuple of three integers.
        """
    
    @property
    def width(self) -> int: 
        """
        Get the width of the NeoPixel grid.

        :return: Width of the grid.
        """

    @property
    def height(self) -> int:
        """
        Get the height of the NeoPixel grid.

        :return: Height of the grid.
        """ 
                
    @property
    def bright(self) -> float: 
        """
        Get the current brightness level.

        :return: Brightness level (0.0 to 1.0).
        """
    
    @bright.setter
    def bright(self, val:float):
        """
        Set the brightness level.
        :param val: Brightness level (0.0 to 1.0).
        :raises ValueError: If val is not in the range 0.0 to 1.0.
        """
        
    def update(self):
        """
        Update the NeoPixel strip with the current colors.
        This method writes the current color data to the NeoPixel strip.
        """
        
    def on(self, color=RED):
        """
        Turn on the NeoPixel grid with a specified color.
        :param color: A tuple (r, g, b) representing the color to turn on.
        :raises TypeError: If color is not a tuple of three integers.
        :raises ValueError: If any color value is not in the range 0-255.
        """

    def off(self):
        """
        Turn off the NeoPixel grid by filling it with black (0, 0, 0).
        """

    def deinit(self):
        """
        Deinitialize the NeoPixel strip.
        This method turns off the strip, deletes the NeoPixel object,
        and sets the pin to input mode.
        """

class tLed:
    """
    Basic NeoPixel control class built into TiCLE.
    This class provides methods to turn on the LED with a specified color,
    turn it off, and define some common colors.
    """
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    WHITE = (255, 255, 255)

    def __init__(self, bright:float=1.0):
        """
        Initialize the RgbLed object.
        """
                
    def on(self, color:tuple[int,int,int]=RED):
        """
        Turn on all NeoPixels with the specified color.
        
        :param color: RGB tuple (r, g, b) where 0 <= r, g, b <= 255
        """

    def off(self):
        """
        Turn off all NeoPixels (set to black).
        """

    @property
    def bright(self) -> float: 
        """
        Get the current brightness level.

        :return: Brightness level (0.0 to 1.0).
        """

    @bright.setter
    def bright(self, val:float):
        """
        Set the brightness level.
        :param val: Brightness level (0.0 to 1.0).
        :raises ValueError: If val is not in the range 0.0 to 1.0.
        """

class VL53L0X:
    """
    A class to interface with the VL53L0X time-of-flight distance sensor.
    This class provides methods to read distances, configure the sensor, and manage continuous measurements.
    It uses I2C communication to interact with the sensor.
    The sensor can measure distances from 30 mm to 1200 mm with a resolution of 1 mm.
    It supports both single-shot and continuous measurement modes.
    """

    def __init__(self, scl: int, sda: int, addr: int = 0x29):
        """
        Initialize the VL53L0X sensor with the specified I2C pins and address.
        
        :param scl: GPIO pin number for the SCL line.
        :param sda: GPIO pin number for the SDA line.
        :param addr: I2C address of the sensor (default is 0x29).
        """

    def read_distance(self) -> int:
        """
        Read the distance measurement from the sensor.
        This method triggers a measurement if one is not already active,
        waits for the measurement to complete, and then fetches the distance.
        
        :return: Distance in millimeters, or None if the measurement is not ready.
        """

    def start_continuous(self, period_ms: int = 0) -> None:
        """
        Start continuous measurements with the specified period in milliseconds.
        If period_ms is 0, continuous measurements will run at the default timing budget.
        
        :param period_ms: Measurement period in milliseconds (default is 0, which uses the timing budget).
        :raises ValueError: If period_ms is less than the minimum required period.
        """

    def stop_continuous(self) -> None:
        """
        Stop continuous measurements and reset the sensor to single-shot mode.
        This method clears the interrupt and stops the measurement.
        """

    def read_continuous(self) -> int | None:
        """
        Read the distance measurement in continuous mode.
        This method checks if a measurement is ready, and if so, fetches the distance.
        
        :return: Distance in millimeters, or None if no measurement is ready.
        """

    def configure_long_range(self) -> None:
        """
        Configure the sensor for long-range measurements.
        This method sets the minimum signal rate and adjusts the final range VCSEL period.
        """

    def configure_high_speed(self) -> None:
        """
        Configure the sensor for high-speed measurements.
        This method sets the minimum signal rate and adjusts the final range VCSEL period.
        """

    def set_timing_budget(self, budget_us: int) -> None:
        """
        Set the measurement timing budget in microseconds.
        This method updates the timing budget and configures the sensor registers accordingly.
        
        :param budget_us: Timing budget in microseconds (must be between 20000 and 330000).
        :raises ValueError: If budget_us is outside the valid range.       
        """


#-----------------------------------------------------------------------------------------------
# PBL
#------------------------------------------------------------------------------------------------
