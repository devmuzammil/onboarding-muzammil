import time

def timer(func):
    def wrapper():
        start=time.time()
        func()
        end=time.time()
        elapsed=end-start
        print(f"Function took {elapsed:.2f} seconds")

    return wrapper


@timer
def slow_function():
    time.sleep(2)


slow_function()