import threading
import time
from copy import deepcopy


class Loop:
    def __init__(self, v, mainFunc=None, mainFuncArgs=(None)):
        self.v = v
        self.v.TICK = 0
        self.v.RUNNING = True

        self.mainFunc = mainFunc
        self.mainFuncArgs = mainFuncArgs

        self.processes = {}

    def run(self):
        self.v.RUNNING = True
        self.v.TICK = 0

        if self.mainFunc is not None:
            while self.v.RUNNING:
                start = time.perf_counter()

                self.v.TICK += 1

                self.mainFunc(self.mainFuncArgs)

                end = time.perf_counter()

                time.sleep(max(0, (1 / self.v.FPS / 2) - (end - start)))
        else:
            while self.v.RUNNING:
                start = time.perf_counter()

                self.v.TICK += 1

                end = time.perf_counter()

                time.sleep(max(0, (1 / self.v.FPS / 2) - (end - start)))

        for i in self.processes:
            self.removeProcess(i)

    def stop(self):
        self.v.RUNNING = False

    def process(self, func, args):
        last = deepcopy(self.v.TICK)

        while not self.v.RUNNING:
            pass
        if args is None:
            while self.v.RUNNING:
                while last == self.v.TICK:
                    pass

                t = threading.Thread(target=self.processFuncShellNoArgs, daemon=True, args=(func, ))
                t.start()
                t.join()

                last = deepcopy(self.v.TICK)
        else:
            while self.v.RUNNING:
                while last == self.v.TICK:
                    pass

                t = threading.Thread(target=self.processFuncShell, daemon=True, args=(func, args, ))
                t.start()
                t.join()

                last = deepcopy(self.v.TICK)

    def processFuncShell(self, func, args):
        func(args)

        # t = deepcopy(threading.current_thread())
        # self.terminate(t)

    def processFuncShellNoArgs(self, func):
        func()

        # t = deepcopy(threading.current_thread())
        # self.terminate(t)

    def terminate(self, t):
        t.join()

    def addProcess(self, name, func, args = None):

        if name not in self.processes:
            self.processes[name] = threading.Thread(target=self.process, daemon=True, args=(func, args))
            self.processes[name].start()

    def removeProcess(self, name):
        try:
            self.processes[name].join()
            self.processes.pop(name)
        except:
            print("ERROR: process either doesn't exist, or you already joined the thread you idiot")
