import time

DEFAULT_ROUND_TO = 4


class Timer:
    """
    Helper class for measuring time.
    """
    def __init__(self):
        self._start = None
        self._end = None
        self._elapsed_time = None

    def start_timer(self):
        """
        Starts the timer, raising an expection if the timer is already running
        @return: None
        """
        if self._start is not None:
            raise Exception("Timer already running")

        self._start = time.perf_counter_ns()
        self._end = None
        self._elapsed_time = None

    def stop_timer(self):
        """
        Ends the timer, raising an exception if the timer is not running
        @return: int - the elapsed time
        """
        if self._start is None:
            raise Exception("Timer not running")

        self._end = time.perf_counter_ns()
        self._elapsed_time = self._end - self._start
        self._start = None
        return self._elapsed_time

    def reset(self):
        """
        Resets the timer and starts it again
        :return: None
        """
        self._start = time.perf_counter_ns()
        self._elapsed_time = None
        self._end = None

    def elapsed_time_ns(self,
                        round_to: int = DEFAULT_ROUND_TO) -> int:
        """
        Returns the elapsed time in nanoseconds formatted to the given decimal places
        @param round_to: int - the number of decimal places to round the output to
        @return: int - the elapsed time formatted for ns and rounded to a decimal place
        """
        return round(self._elapsed_time, round_to)

    def elapsed_time_ms(self,
                        round_to: int = DEFAULT_ROUND_TO) -> int:
        """
        Returns the elapsed time in milliseconds formatted to the given decimal places
        @param round_to: int - the number of decimal places to round the output to
        @return: int - the elapsed time formatted for ms and rounded to a decimal place
        """
        return round(self._elapsed_time / 1000000, round_to)

    def elapsed_time_s(self,
                       round_to: int = DEFAULT_ROUND_TO) -> int:
        """
        Returns the elapsed time in seconds formatted to the given decimal places
        @param round_to: int - the number of decimal places to round the output to
        @return: int - the elapsed time formatted for secs and rounded to a decimal place
        """
        return round(self._elapsed_time / 1000000000, round_to)
