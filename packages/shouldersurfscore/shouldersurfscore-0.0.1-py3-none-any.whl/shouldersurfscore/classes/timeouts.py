import datetime

class DeviceLockout(Exception):
    def __init__(self, number_of_guesses):
        message = f'Device is now locked, after {number_of_guesses} guesses.'
        super().__init__(message)

class TimeOut:
    def __init__(self, time_out_iterable, factory_reset_tries: int):
        '''
        
        '''
        self.time_out_iterable = time_out_iterable
        self.factory_reset_tries = factory_reset_tries

        self.elapsed_time = datetime.timedelta(seconds=0.0)
        self.guesses = 0
    

    def make_guess(self):
        self.guesses += 1

        if self.guesses == self.factory_reset_tries:
            raise DeviceLockout(self.guesses)
        
        if type(self.time_out_iterable) == list:
            self.elapsed_time += self.time_out_iterable.pop(0)
        
        else:
            self.elapsed_time += next(self.time_out_iterable)