from typing import Any, List

from .worker import celery


def _get_tasks():
    tasks = celery.control.inspect().scheduled()
    return tasks[list(tasks.keys())[0]] if tasks is not None else []


def has_reserved_task(name: str, args: List[Any]):
    tasks = _get_tasks()
    tasks = list(filter(lambda t: t['request']['name'] == name and t['request']['args'] == args, tasks))
    return len(tasks) != 0
