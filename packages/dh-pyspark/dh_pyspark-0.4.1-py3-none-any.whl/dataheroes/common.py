import os
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor

import psutil
from threadpoolctl import threadpool_limits

from .configuration import Singleton
from .utils import telemetry


def can_use_threadpool_limits():
    try:
        with threadpool_limits(limits=os.cpu_count(), user_api="blas"):
            pass
        return True
    except Exception as e:
        return False

def get_consecutive_integer_series(integer_list):
    integer_list = sorted(integer_list)
    start_item = integer_list[0]
    end_item = integer_list[-1]

    a = set(integer_list)  # Set a
    b = range(start_item, end_item+1)

    # Pick items that are not in range.
    c = set(b) - a  # Set operation b-a

    li = []
    start = 0
    for i in sorted(c):
        end = b.index(i)  # Get end point of the list slicing
        li.append(b[start:end])  # Slice list using values
        start = end + 1  # Increment the start point for next slicing
    li.append(b[start:])  # Add the last series

    for sliced_list in li:
        if not sliced_list:
            # list is empty
            continue
        if len(sliced_list) == 1:
            # If only one item found in list
            yield str(sliced_list[0])
        else:
            yield "{0}-{1}".format(sliced_list[0], sliced_list[-1])

def parse_parent_finished_list_to_str(l : list) -> str:
    on_levels = {}
    for (level, idx) in l:
        if level in on_levels:
            on_levels[level].append(idx)
        else:
            on_levels[level] = [idx]
    on_level_str = []
    for (lvl, lst) in on_levels.items():
        lststr = " ".join([e for e in get_consecutive_integer_series(lst)])
        on_level_str.append(f"{str(lvl)}<{lststr:s}>")
    # on_level_str = [f"{lvl}<{[e for e in get_consecutive_integer_series(lst)]}>" for (lvl, lst) in on_levels.items()]
    return " ".join(on_level_str)

def print_task_states():
    pool_manager = ThreadPoolManager()

    state_counts = {
        'PENDING_LEAF': 0,
        'PENDING_NODE': 0,
        'RUNNING_LEAF': 0,
        'RUNNING_NODE': 0,
        'FINISHED_LEAF': 0,
        'FINISHED_NODE': 0,
        'CANCELLED_LEAF': 0,
        'CANCELLED_NODE': 0,
    }

    task_counts = {'_create_parent_node': 0, '_create_leaf_node': 0}
    pending_leaf_list = []
    pending_parent_list = []
    running_leaf_list = []
    running_parent_list = []
    finished_leaf_list = []
    finished_parent_list = []

	# count submitted tasks by state
    for name, future in pool_manager.task_futures:
        if future._state == 'PENDING':
            if name == "_create_leaf_node":
                state_counts['PENDING_LEAF'] += 1
                pending_leaf_list.append(pool_manager.task_futures_args[future][1])
            elif name == "_create_parent_node":
                state_counts['PENDING_NODE'] += 1
                pending_parent_list.append((pool_manager.task_futures_args[future][1], pool_manager.task_futures_args[future][2]))
            else:
                raise ValueError("Incorrect name of task in \"pool_manager.task_futures\"")
        elif future._state == 'RUNNING':
            if name == "_create_leaf_node":
                state_counts['RUNNING_LEAF'] += 1
                running_leaf_list.append(pool_manager.task_futures_args[future][1])
            elif name == "_create_parent_node":
                state_counts['RUNNING_NODE'] += 1
                running_parent_list.append((pool_manager.task_futures_args[future][1], pool_manager.task_futures_args[future][2]))
            else:
                raise ValueError("Incorrect name of task in \"pool_manager.task_futures\"")
        elif future._state == 'FINISHED':
            if name == "_create_leaf_node":
                state_counts['FINISHED_LEAF'] += 1
                finished_leaf_list.append(pool_manager.task_futures_args[future][1])
            elif name == "_create_parent_node":
                state_counts['FINISHED_NODE'] += 1
                finished_parent_list.append((pool_manager.task_futures_args[future][1], pool_manager.task_futures_args[future][2]))
            else:
                raise ValueError("Incorrect name of task in \"pool_manager.task_futures\"")
        elif future._state == 'CANCELLED':
            if name == "_create_leaf_node":
                state_counts['CANCELLED_LEAF'] += 1
            elif name == "_create_parent_node":
                state_counts['CANCELLED_NODE'] += 1
            else:
                raise ValueError("Incorrect name of task in \"pool_manager.task_futures\"")
	
	# count tasks in the task queue by task type (not submitted yet)
    for task in pool_manager.task_queue:
        task_counts[task[0].__name__] += 1

    total_pool_pending = (state_counts['PENDING_LEAF'] + state_counts['PENDING_NODE'])
    total_pool_running = (state_counts['RUNNING_LEAF'] + state_counts['RUNNING_NODE'])
    total_pool_finished = (state_counts['FINISHED_LEAF'] + state_counts['FINISHED_NODE'])
    print(f"No of tasks in POOL (PENDING): \t\t{state_counts['PENDING_LEAF']} + {state_counts['PENDING_NODE']} = \t{total_pool_pending}")
    print(f"No of tasks in POOL (RUNNING): \t\t{state_counts['RUNNING_LEAF']} + {state_counts['RUNNING_NODE']} = \t{total_pool_running}")
    print(f"No of tasks in POOL (FINISHED): \t{state_counts['FINISHED_LEAF']} + {state_counts['FINISHED_NODE']} = \t{total_pool_finished}")
    # print(f"No of tasks in POOL (CANCELLED): \t{state_counts['CANCELLED_LEAF']} + {state_counts['CANCELLED_NODE']} = \t{(state_counts['CANCELLED_LEAF'] + state_counts['CANCELLED_NODE'])}")
    pending_leaf_str = " ".join(f"{v}" for v in sorted(pending_leaf_list))
    pending_parent_str = " ".join(f"{level}<{idx}>" for (level, idx) in sorted(pending_parent_list))
    if len(pending_leaf_list) + len(pending_parent_list) > 0:
        print(f"[INFO_POOL][PENDING ]: {pending_leaf_str} || {pending_parent_str} || [TOTAL_PENDING]: {total_pool_pending}")
    running_leaf_str = " ".join(f"{v}" for v in sorted(running_leaf_list))
    running_parent_str = " ".join(f"{level}<{idx}>" for (level, idx) in sorted(running_parent_list))
    if len(running_leaf_list) + len(running_parent_list) > 0:
        print(f"[INFO_POOL][RUNNING ]: {running_leaf_str} || {running_parent_str} || [TOTAL_RUNNING]: {total_pool_running}")
    if len(finished_leaf_list) > 0:
        print(f"[INFO_POOL][FINISHED]:[LEAFS  ]: {' '.join([str(s) for s in get_consecutive_integer_series(finished_leaf_list)])}")
    if len(finished_parent_list) > 0:
        print(f"[INFO_POOL][FINISHED]:[PARENTS]: {parse_parent_finished_list_to_str(finished_parent_list)}")
    print(f"No of tasks in QUEUE: \t\t\t{task_counts['_create_leaf_node']} + {task_counts['_create_parent_node']} = \t{(task_counts['_create_leaf_node'] + task_counts['_create_parent_node'])}")
    print(f"Total number of tasks in POOL: {sum(state_counts.values())}")

    # print now the number of tasks in pool_manager.thread_pool_executor
    print(f"Number of tasks in ThreadPoolExecutor: {pool_manager.thread_pool_executor._work_queue.qsize()}")


class ThreadPoolManager(metaclass=Singleton):
    def __init__(self, max_workers=None):
        self.thread_pool_executor = ThreadPoolExecutor(max_workers=max_workers)
        self.task_queue = []
        self.task_futures = []
        self.lock = threading.Lock()
        self.dm_lock = threading.Lock() 
        """The dm_lock (data manager lock) is used to make the data manager accesses be executed sequentially no matter
                in a multithreaded environment. Specifically, when the data manager is reading from the database, no writing 
                to disk should happen and vice versa, no reading from the database on disk should be done when writing to it.
                At the moment, the lock is used in:
                  - dataheroes/core/tree/manager.py, inside TreeManager.build().after_create_leaf_node(), where node related 
                    data is written to the database
                  - dataheroes/core/tree.tree.py, inside CoresetTree._create_father_node(), where tree node related data is 
                    read from database at the construction of parent nodes, in case that data is missing from the cache
        """

        self._QUEUE_AND_POOL_DEBUG = os.getenv("_QUEUE_AND_POOL_DEBUG", False)
        if self._QUEUE_AND_POOL_DEBUG:
            print(f"[INFO]: Running with ThreadPoolExecutor pool and ThreadPoolManager queue debugging ...")
            self.last_parents_queue_idxes = []
            self.last_leafs_queue_idxes = []
            self.task_futures_args = {}
        self.start()
        self.executor_exception = None
        self.main_thread = None
        self.max_workers = max_workers
    def has_running_tasks(self):
        # Both running and pending tasks consume memory since the args are already loaded at this stage (X, y, w etc..)
        return len([f for _, f in self.task_futures if f._state in ('RUNNING', 'PENDING')]) > 0

    @telemetry
    def restart_executor(self, max_workers=None):
        self.executor_exception = None
        self.thread_pool_executor.shutdown(wait=True)
        del self.thread_pool_executor
        self.thread_pool_executor = ThreadPoolExecutor(max_workers=max_workers)
        self.max_workers = max_workers

    def add_to_queue(self, task, condition, priority, *args):
        """
        Adds to queue only if the number of waiting (already processed) nodes is smaller than the number of
        workers. Otherwise, just sleeps.
        """
        while True:
            if task.__name__ == "_create_parent_node":
                with self.lock:
                    self.task_queue.append((task, condition, priority, args))
                    if self._QUEUE_AND_POOL_DEBUG:
                        print_task_states()
                break
            else:
                with self.lock:
                    pending_jobs = [f for name, f in self.task_futures if
                                    f._state in ('PENDING') and name == "_create_leaf_node"]
                    if not pending_jobs or len(pending_jobs) < self.max_workers:
                        self.task_queue.append((task, condition, priority, args))
                        if self._QUEUE_AND_POOL_DEBUG:
                            print_task_states()
                        break
                time.sleep(0.1)

    def _submit_tasks(self):
        with self.lock:
            try:
                if self._QUEUE_AND_POOL_DEBUG:
                    if len(self.task_queue) > 0:
                        the_leafs_str   = "[INFO_QUEUE][LEAFS  ]: priority\tchunk_id\n"
                        the_parents_str = "[INFO_QUEUE][PARENTS]: priority\tlevel\tidx\n"
                        new_leafs_queue_list = []
                        new_parents_queue_list = []
                        for the_task in self.task_queue:
                            if the_task[0].__name__ == "_create_parent_node":
                                new_parents_queue_list.append(the_task[3][1])
                                the_parents_str += f"[INFO_QUEUE][PARENTS]: {the_task[2]}\t{the_task[3][0]}\t{the_task[3][1]}\n"
                            elif the_task[0].__name__ == "_create_leaf_node":
                                new_leafs_queue_list.append(the_task[3][1])
                                the_leafs_str += f"[INFO_QUEUE][LEAFS  ]: {the_task[2]}\t{the_task[3][1]}\n"
                        new_parents_queue_list = sorted(new_parents_queue_list)
                        if (new_parents_queue_list != self.last_parents_queue_idxes) or (new_leafs_queue_list != self.last_leafs_queue_idxes):
                            self.last_parents_queue_idxes = new_parents_queue_list
                            print(the_parents_str)
                            self.last_leafs_queue_idxes = new_leafs_queue_list
                            print(the_leafs_str)
                tasks_to_remove = []
                # sort due to priorities
                self.task_queue.sort(key=lambda x: x[2], reverse=True)
                for task, condition, priority, args in self.task_queue:
                    if condition is None or condition(*args):
                        future = self.thread_pool_executor.submit(task, *args)
                        tasks_to_remove.append((task, condition, priority, args))
                        self.task_futures.append((task.__name__, future))  # Keep track of the future
                        if self._QUEUE_AND_POOL_DEBUG:
                            if task.__name__ == "_create_leaf_node":
                                self.task_futures_args[future] = ("_create_leaf_node", args[1])
                            elif task.__name__ == "_create_parent_node":
                                self.task_futures_args[future] = ("_create_parent_node", args[0], args[1])
                for task_to_remove in tasks_to_remove:
                    self.task_queue.remove(task_to_remove)
            except Exception as e:
                self.executor_exception = e
                # we raise it in another place
                raise e

    def check_exceptions(self):
        exceptions = [f._exception for _, f in self.task_futures if f._exception is not None]
        if len(exceptions) > 0:
            self.thread_pool_executor.shutdown(wait=False)
            raise exceptions[0]

    @telemetry
    def wait_until_empty(self):
        while self.executor_exception is None:
            self.check_exceptions()
            with self.lock:
                if not self.task_queue and all(future.done() for _, future in self.task_futures):
                    break
            time.sleep(0.01)
        if self.executor_exception is not None:
            raise self.executor_exception
        self.check_exceptions()
        self.thread_pool_executor.shutdown(wait=True)
        if self.main_thread is not None:
            self.main_thread.join(0.01)

    def run(self, interval=.01):
        while True:
            self._submit_tasks()
            time.sleep(interval)

    def start(self, interval=.01):
        self.main_thread = threading.Thread(target=self.run, args=(interval,), daemon=True)
        self.main_thread.start()

    def __del__(self):
        ThreadPoolManager().thread_pool_executor.shutdown(wait=True)


class TimeLogger(metaclass=Singleton):
    """
    for debug purposes
    """

    def __init__(self):
        self.times = {}

    def add(self, label, time_in_seconds):
        if label not in self.times:
            self.times[label] = []
        self.times[label].append(time_in_seconds)

    def get_total(self, label=None):
        total = 0
        for curr_label in self.times:
            if label is None or label == curr_label:
                total += sum(self.times[label])
        return total


class MetricsLogger(metaclass=Singleton):
    """
    for debug purposes
    """

    def __init__(self, interval=10):
        self.metrics = []
        self.time_start = time.time()
        self.start(interval)

    def run(self, interval):
        while True:
            self.metrics.append({'time': time.time() - self.time_start,
                                 'CPU % used': psutil.cpu_percent(interval=None),
                                 'memory % used': psutil.virtual_memory()[2]
                                 })
            time.sleep(interval)

    def start(self, interval):
        threading.Thread(target=self.run, args=(interval,), daemon=True).start()


def get_parallel_executor(n_jobs):
    """
    Return array for futures and the threadpool executor based on n_jobs
    The n_jobs is capped by the number of cpus on the machine
    If we cannot limit blas we cannot run in parallel and executor is None
    Args:
        n_jobs: expected concurrency by the user
    Returns: list, threadpool executor
    """
    if can_use_threadpool_limits():
        if n_jobs is None or n_jobs > 1:
            n_jobs = min(os.cpu_count(), n_jobs) if n_jobs is not None else os.cpu_count()
            return [], ThreadPoolExecutor(max_workers=n_jobs)
    return None, None
