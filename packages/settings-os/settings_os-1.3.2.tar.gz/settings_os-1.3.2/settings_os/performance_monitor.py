import time
import functools
import logging
import tracemalloc
from typing import Optional, Callable


class PerformanceMonitor:
    @staticmethod
    def timer(logger: Optional[logging.Logger] = None):
        """
        Decorator to measure function execution time with optional logging
        
        :param logger: Optional logger to use instead of print
        :type logger: logging.Logger, optional
        """
        def decorator(func: Callable):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()

                execution_time = end_time - start_time
                hours = int(execution_time // 3600)
                minutes = int((execution_time % 3600) // 60)
                seconds = int(execution_time % 60)
                milliseconds = int((execution_time % 1) * 1000)

                formatted_time = f"{hours}h {minutes}m {seconds}s {milliseconds:03d}ms"

                log_message = f"{func.__name__} levou {formatted_time}"

                if logger:
                    logger.info(log_message)
                else:
                    print(log_message)

                return result
            return wrapper
        return decorator

    @staticmethod
    def memory_tracker(logger: Optional[logging.Logger] = None):
        """
        Decorator to track memory usage with optional logging
        
        :param logger: Optional logger to use instead of print
        :type logger: logging.Logger, optional
        """
        def decorator(func: Callable):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                tracemalloc.start()

                result = func(*args, **kwargs)

                current, peak = tracemalloc.get_traced_memory()
                memory_message = (
                    f"\nFunção: {func.__name__}.\n"
                    f"Uso de memória:\n"
                    f"- Memoria corrente pós processamento {current / 1024 / 1024:.4f} MB\n"
                    f"- Pico {peak / 1024 / 1024:.4f} MB"
                )
                if logger:
                    logger.info(memory_message)
                else:
                    print(memory_message)

                tracemalloc.stop()
                return result
            return wrapper
        return decorator


if __name__ == '__main__':
    performance = PerformanceMonitor()

    @performance.memory_tracker()
    @performance.timer()
    def slow_function():
        time.sleep(2)
        return "Done"

    result = slow_function()

    @performance.memory_tracker()
    @performance.timer()
    def memory_intensive_function():
        data = [i for i in range(1000000)]

        temp = [i**2 for i in data]

        processed_data = [x for x in temp if x % 2 == 0]

        return data, processed_data

    result = memory_intensive_function()
