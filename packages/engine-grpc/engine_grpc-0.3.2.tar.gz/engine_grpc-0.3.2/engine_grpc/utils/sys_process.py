import psutil


def get_process_name_lists():
    """Get a list of process names"""
    process_name_list = []
    for proc in psutil.process_iter():
        try:
            process_name_list.append(proc.name())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_name_list


def kill_process_by_name(process_name):
    """Kill a process by name"""
    for proc in psutil.process_iter():
        try:
            if proc.name() == process_name:
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
