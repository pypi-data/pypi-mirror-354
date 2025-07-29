
import utime

class DistanceScanner:
    """
    A class to control a motor motor and an Distance sensor for distance scanning.
    It sweeps the Motor across a specified range and takes distance readings at each angle.
    The best angle with the minimum distance is returned.
    """
    
    def __init__(self, motor:object, sensor:object, step:int=2, settle_ms:int=20, samples:int=5):
        """
        :param motor: motorMotor object
        :param sensor: Ultrasensor object 
        :param step: int, angle step for motor motor
        :param settle_ms: int, time to wait for motor to settle in ms
        :param samples: int, number of samples to take for each angle
        """
        self.motor = motor
        self.sensor = sensor
        self.step = step
        self.settle_ms = settle_ms
        self.samples = samples

    def __median(self, lst:list) -> float:
        """
        calculate median value of a list of numbers.
        :param seq: list[float]
        :return: float
        """    
        lst = sorted(lst)
        n = len(lst)
        mid = n // 2
        return lst[mid] if n & 1 else 0.5 * (lst[mid-1] + lst[mid])

    def sweep(self, start:int=0, end:int=180) -> dict: 
        """
        Sweep the motor motor from start to end angle and return the best angle with minimum distance.
        :param start: int, starting angle
        :param end: int, ending angle
        :return: dict, best angle and distance
        """
        best = {'angle': None, 'dist': 1e9}
        direction = 1 if end >= start else -1

        for angle in range(start, end + direction, self.step * direction):
            self.motor.angle(angle)
            utime.sleep_ms(self.settle_ms)

            reads = []
            for _ in range(self.samples):
                d = self.sensor.read()
                if d is not None:
                    reads.append(d)
                utime.sleep_us(60)

            if reads:
                dist = self.__median(reads)
                if dist < best['dist']:
                    best = {'angle': angle, 'dist': dist}

        return best
