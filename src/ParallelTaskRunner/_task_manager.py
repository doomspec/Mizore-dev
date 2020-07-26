from ._task_runner import TaskRunner
from ._task import Task
from multiprocessing import Queue
import time
import numpy


class TaskManager:
    """
    The class for parallelly evaluate quantum circuits.
    Holds the task queue and result queue for TaskRunner to read the inputs and put the outputs.
    """
    def __init__(self, n_processor):

        self.n_processor = n_processor
        self.processor_list = []
        self.task_queue = Queue()
        self.result_queue = Queue()
        self.n_task_processed = 0
        self.n_task_remain_by_series_id = dict()

        for i in range(n_processor):
            self.processor_list.append(TaskRunner(
                self.task_queue, self.result_queue))
        for i in range(n_processor):
            self.processor_list[i].start()
        return

    def add_task(self, task: Task, task_series_id=0):

        if task_series_id in self.n_task_remain_by_series_id.keys():
            self.n_task_remain_by_series_id[task_series_id] += 1
        else:
            self.n_task_remain_by_series_id[task_series_id] = 1

        task.id = self.n_task_processed
        self.task_queue.put(task)

        self.n_task_processed += 1

    RECEIVE_PERIOD = 0.02

    def receive_task_result(self, task_series_id=0):
        result_list = []
        id_list = []
        while (self.n_task_remain_by_series_id[task_series_id] != 0):
            task_result = self.result_queue.get(True)
            result_list.append(task_result.result)
            id_list.append(task_result.id)
            self.n_task_remain_by_series_id[task_series_id] -= 1
            time.sleep(TaskManager.RECEIVE_PERIOD)
        id_rank_list = numpy.argsort(numpy.array(id_list))
        ranked_result_list = []
        for i in range(len(id_list)):
            ranked_result_list.append(result_list[id_rank_list[i]])
        return ranked_result_list

    def close(self):
        for processor in self.processor_list:
            processor.terminate()
