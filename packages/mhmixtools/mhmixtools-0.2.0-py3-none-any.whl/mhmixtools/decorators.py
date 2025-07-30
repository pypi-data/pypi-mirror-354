import time
from functools import wraps

def execution_time(func):
    @wraps(func)  # Preserves metadata like __name__ and __doc__
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            end = time.perf_counter()
            execution = end - start
            print(f"{func.__name__} failed after {execution:.10f} seconds")
            raise e  # Re-raise the exception after logging time
        end = time.perf_counter()
        execution = end - start
        print(f"{func.__name__} executed in {execution:.10f} seconds")
        return result
    return wrapper
