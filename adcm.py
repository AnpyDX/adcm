"""
A Designed CMake project Manager (aka. adcm)
>> (https://github.com/AnpyDX/adcm)

about:
    adcm is a python library that allow you to work on CMake project 
    in Visual Studio Code easily.
    
    This project was created for letting me easy to work on 
    C++ project with Visual Stuido Code (clangd + ninja), which
    only needs a simple configure file to setup.

Copyright (c) 2024 anpyd, All Rights Reserved.
"""

import os
import time
import hashlib
import threading

""" ADCM TYPES DEFINE """
class ADCM_Task(object):
    def __init__(self, cmds: list):
        self.cmds = cmds
    
    def exec(self):
        for cmd in self.cmds:
            # if command is str, considered as system command
            if isinstance(cmd, str):
                os.system(cmd)
            
            # otherwise function call
            else:
                cmd()

class ADCM_Trigger(object):
    def __init__(self, deps: list, tasks: list):
        self.deps: list = []
        self.deps_md5: list = []
        self.tasks = tasks
        self.md5_generator = hashlib.md5()

        for depf in deps:
            dep_file = open(depf, "r")
            self.deps.append(dep_file)
            self.deps_md5.append(self.get_md5(dep_file))

    def run(self, stop_sign):
        global adcm_project_tasks

        while True:
            # if stop_sign is set, stop loop to release thread
            if (stop_sign.is_set()):
                break

            index = 0
            for dep_file in self.deps:
                md5_value = self.get_md5(dep_file)

                if md5_value != self.deps_md5[index]:
                    for task in self.tasks:
                        adcm_project_tasks[task].exec()

                    self.deps_md5[index] = md5_value
                    break

                index += 1
            
            time.sleep(1)

    def get_md5(self, file) -> str:
        self.md5_generator.update(file.read().encode(encoding="UTF-8"))
        return self.md5_generator.hexdigest()



""" ADCM GLOBAL VARIBLES """
adcm_project_name: str = None
adcm_project_tasks: dict = {}
adcm_project_triggers: dict = {}
adcm_project_trigger_threads: dict = {}

""" create a new project """
def new_project(name: str) -> None:
    global adcm_project_name

    if adcm_project_name != None:
        raise RuntimeError("Do not allow to rename project!")
    else:
        adcm_project_name = name

""" add a new task to project """
def add_task(
    name: str,
    commands: list
) -> None:
    global adcm_project_tasks

    if len(commands) == 0:
        raise RuntimeError("Failed to call <add_task> with empty commands argument!")
    
    if name in adcm_project_tasks:
        raise RuntimeError("Failed to create an existed task!")
    
    adcm_project_tasks[name] = ADCM_Task(commands)


""" add a new trigger to project """
def add_trigger(
    name: str,
    dependence: list,
    tasks: list
) -> None:
    global adcm_project_triggers

    if name in adcm_project_tasks:
        raise RuntimeError("Failed to create an existed trigger!")

    if len(dependence) == 0:
        raise RuntimeError("Failed to call <add_trigger> with empty dependence argument!")
    
    if len(tasks) == 0:
        raise RuntimeError("Failed to call <add_trigger> with empty tasks argument!")
    
    
    adcm_project_triggers[name] = ADCM_Trigger(dependence, tasks)
    

""" launch adcm manager """
def launch() -> None:
    global adcm_project_name
    global adcm_project_tasks
    global adcm_project_triggers
    global adcm_project_trigger_threads

    # check workflow integrity
    if adcm_project_name == None:
        raise RuntimeError("Failed to launch adcm as project's name is empty!")
    if len(adcm_project_tasks) == 0:
        raise RuntimeError("Failed to launch adcm as project's task-list is empty!")

    # launch triggers
    stop_sign = threading.Event()
    for index in adcm_project_triggers:
        trigger_thread = threading.Thread(target=adcm_project_triggers[index].run, args=(stop_sign, ))
        adcm_project_trigger_threads[index] = trigger_thread
        trigger_thread.start()

    # create console
    while True:
        cmd = str(input("\033[1;32madcm#{0} >\033[m ".format(adcm_project_name)))

        # empty command
        if len(cmd.replace(" ", "")) == 0:
            continue

        else:
            if cmd == "exit":
                break

            elif cmd == "clear":
                if os.name == "nt":
                    # clear command for Windows CMD
                    os.system("cls")
                else:
                    # clear command for Linux and macOS
                    os.system("clear")

            elif cmd == "task-list":
                col_num = 1
                for index in adcm_project_tasks:
                    if col_num == 6: # NOTICE: max number of displayed names in one row is 5
                        print("") # enter to next line
                        col_num = 1
                    else:
                        col_num += 1

                    print(index + " | ", end="")

                print("") # enter to next line

            elif cmd == "trigger-list":
                for index in adcm_project_trigger_threads:
                    print("| {0} | status: {1}".format(index, "active" if adcm_project_trigger_threads[index].is_alive() else "stopped"))

            # not built-in command, run task
            else:
                if cmd in adcm_project_tasks:
                    adcm_project_tasks[cmd].exec()
                else:
                    print("\033[1;32;31merror: task \"{0}\" is not existed!\033[m ".format(cmd))

    # exit adcm after collecting threads
    stop_sign.set()