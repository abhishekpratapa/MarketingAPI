import time
import calendar


# class:        Timer
#
# Description:  This is a class acts as a stopwatch
#
# Methods:
#
#       start:     This function starts the stopwatch
#       pause:     This function pauses the stopwatch and doesn't start recording until start is pressed again
#       lap:       This function returns a lab time and keeps the stopwatch going
#       reset:     This function resets the stopwatch to zero
#       stop:      This function stops the stopwatch and return the total time it took to run the program

class Timer:
    def __init__(self):
        self.starting_time = 0
        self.ending_Time = 0
        self.addition = 0

    # Method: start
    #
    # Description: start the database
    #
    # return: True if the stopwatch has started [Boolean]

    def start(self):
        self.starting_time = calendar.timegm(time.gmtime())
        return True

    # Method: pause
    #
    # Description: pause the stopwatch
    #
    # return: the lap time [Float]

    def pause(self):
        self.addition = self.addition + calendar.timegm(time.gmtime()) - self.starting_time
        self.starting_time = 0
        self.ending_Time = 0
        return self.addition

    # Method: lap
    #
    # Description: call lap on the stopwatch
    #
    # return: the lap time [Float]

    def lap(self):
        self.addition = self.addition + calendar.timegm(time.gmtime()) - self.starting_time
        self.starting_time = calendar.timegm(time.gmtime())
        self.ending_Time = 0
        return self.addition

    # Method: reset
    #
    # Description: reset the stopwatch
    #
    # return:   True if the stopwatch

    def reset(self):
        self.starting_time = 0
        self.ending_Time = 0
        self.addition = 0
        return True

    # Method: stop
    #
    # Description: stop the stopwatch
    #
    # return:   The float value on the stopwatch [Float]

    def stop(self):
        if not self.starting_time == 0:
            self.ending_Time = calendar.timegm(time.gmtime())
            return (self.starting_time - self.ending_Time) + self.addition
        else:
            return self.addition