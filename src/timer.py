import time
import calendar


class Timer:
    def __init__(self):
        self.starting_time = 0
        self.ending_Time = 0
        self.addition = 0

    def start_timer(self):
        self.starting_time = calendar.timegm(time.gmtime())
        return True

    def pause(self):
        self.addition = calendar.timegm(time.gmtime()) - self.starting_time
        self.starting_time = 0
        self.ending_Time = 0
        return True

    def reset(self):
        self.starting_time = 0
        self.ending_Time = 0
        self.addition = 0
        return True

    def stop(self):
        if not self.starting_time == 0:
            self.ending_Time = calendar.timegm(time.gmtime())
            return (self.starting_time - self.ending_Time) + self.addition
        else:
            return self.addition