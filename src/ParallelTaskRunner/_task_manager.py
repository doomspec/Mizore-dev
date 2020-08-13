from multiprocessing import Process,Queue
import time
import pickle
import numpy
from ._task import Task

class TaskResult:

    def __init__(self, id, result):
        self.id = id
        self.result = result

class TaskRunner(Process):

    def __init__(self, task_queue, result_queue):
        Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        while True:
            time.sleep(0.1)
            task_package = self.task_queue.get(True)
            result_package=[]
            for task in task_package:
                result = task.run()
                result_package.append(TaskResult(task.id, result))
            self.result_queue.put(result_package)

class TaskManager:
    """
    The class for parallelly evaluate quantum circuits.
    Holds the task queue and result queue for TaskRunner to read the inputs and put the outputs.
    """
    def __init__(self, n_processor=4,task_package_size=5):

        self.n_processor = n_processor
        self.processor_list = []
        self.task_queue = Queue()
        self.result_queue = Queue()
        self.n_task_processed = 0
        self.n_task_remain_by_series_id = dict()
        self.buffer_by_series_id = dict()
        self.task_package_size=task_package_size

        for i in range(n_processor):
            self.processor_list.append(TaskRunner(
                self.task_queue, self.result_queue))
        for i in range(n_processor):
            self.processor_list[i].start()

    def add_task_to_buffer(self, task: Task, task_series_id=0):

        task.id = self.n_task_processed
        self.n_task_processed += 1

        if task_series_id in self.n_task_remain_by_series_id.keys():
            self.n_task_remain_by_series_id[task_series_id] += 1
            self.buffer_by_series_id[task_series_id].append(task)
        else:
            self.n_task_remain_by_series_id[task_series_id] = 1
            self.buffer_by_series_id[task_series_id]=[task]

    def flush(self,task_series_id=0):
        task_package=[]
        for task in self.buffer_by_series_id[task_series_id]:
            task_package.append(task)
            if len(task_package)>=self.task_package_size:
                self.task_queue.put(task_package)
                task_package=[]
        if len(task_package)!=0:
            self.task_queue.put(task_package)
        self.buffer_by_series_id[task_series_id]=[]

    RECEIVE_PERIOD = 0.1

    def receive_task_result(self, task_series_id=0):
        result_list = []
        id_list = []
        while (self.n_task_remain_by_series_id[task_series_id] != 0):
            result_package = self.result_queue.get(True)
            for task_result in result_package:
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


