from multiprocessing.pool import Pool, ThreadPool
from typing import Callable


class TaskPool:
    def __init__(self, num_workers: int, use_threads: bool = False) -> None:
        self.num_workers = num_workers
        self.use_threads = use_threads

    def run(self, func: Callable, args: list[list]) -> any:
        """
        Run a function on a list of arguments using a multiprocessing pool.

        :param func: The function to run.
        :param args: The list of arguments to run the function on.
        :return: The results of the function calls.
        """

        try:
            if self.use_threads:
                pool = ThreadPool(self.num_workers)
            else:
                pool = Pool(self.num_workers)
            data = pool.starmap(func, args)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as e:
            raise e
        else:
            return data
        finally:
            pool.close()
            pool.join()
