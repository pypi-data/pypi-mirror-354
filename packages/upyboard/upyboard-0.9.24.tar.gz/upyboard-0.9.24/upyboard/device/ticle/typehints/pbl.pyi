
import utime

class UltrasoicServoScanner:
    """
    A class to control a servo motor and an ultrasonic sensor for distance scanning.
    It sweeps the servo motor across a specified range and takes distance readings at each angle.
    The best angle with the minimum distance is returned.
    """
    
    def __init__(self, servo:object, sonic:object, step:int=2, settle_ms:int=20, samples:int=5):
        """
        :param servo: ServoMotor object
        :param sonic: Ultrasonic object 
        :param step: int, angle step for servo motor
        :param settle_ms: int, time to wait for servo to settle in ms
        :param samples: int, number of samples to take for each angle
        """


    def sweep(self, start:int=0, end:int=180) -> dict: 
        """
        Sweep the servo motor from start to end angle and return the best angle with minimum distance.
        :param start: int, starting angle
        :param end: int, ending angle
        :return: dict, best angle and distance
        """

