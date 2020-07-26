from multiprocessing import Process, Queue
import time, pickle
from ._task_result import TaskResult


class TaskRunner(Process):
    def __init__(self, task_queue, result_queue):
        Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        return

    def run(self):
        while True:
            time.sleep(0.1)
            pickled_task = self.task_queue.get(True)
            # print(self.name,"get task")
            task = pickled_task
            self.process_task(task)
        return

    def process_task(self, task):
        result = task.run()
        self.result_queue.put(TaskResult(task.id, result))
        return
