import datetime
import time


def logtime(func):
    """Measure how long doeas it take for a function to run """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)

        total_time = time.time() - start_time
        print(f'Time Elapsed {str(datetime.timedelta(seconds=total_time)).split(".")[0]}')
        return result

    return wrapper
