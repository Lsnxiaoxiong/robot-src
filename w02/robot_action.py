import time
import threading
from enum import Enum
from typing import Optional
import logging

from src.utils.resp import CanStartResult
from src.utils.robot_enum import ActionStatus, RobotRespCode

 





class Action:
    _status: ActionStatus
    _thread: Optional[threading.Thread]
    _run_event: threading.Event
    _stop_event: threading.Event
    _lock: threading.Lock
    name: str

    def __init__(self, name="undefined") -> None:
        self._status = ActionStatus.CREATED
        self._thread = None
        self._run_event = threading.Event()
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        
        self.name = name

    def is_created(self) -> bool:
        return self._status == ActionStatus.CREATED

    def is_undefined(self) -> bool:
        return self.name == "undefined"

    def is_running(self) -> bool:
        return self._status == ActionStatus.RUNNING

    def is_paused(self) -> bool:
        return self._status == ActionStatus.PAUSED

    def is_stopped(self) -> bool:
        return self._stop_event.is_set()

    def starting_check(self) -> CanStartResult:
        if self.is_running():
            return CanStartResult.failed(RobotRespCode.ACTION_IS_RUNNING)
        if self.is_paused():
            return CanStartResult.failed(RobotRespCode.ACTION_IS_PAUSED)
        if self.is_stopped():
            return CanStartResult.failed(RobotRespCode.ACTION_IS_STOPPED)
        if self._thread is not None and self._thread.is_alive():
            return CanStartResult.failed(RobotRespCode.ACTION_IS_RUNNING)

        return CanStartResult.success()

    def start(self) -> None:
        if not self.starting_check().can_start:
            return
        with self._lock:
            if not self.starting_check().can_start:
                return
            self._status = ActionStatus.RUNNING
            self._run_event.set()
            try:
                self._thread = threading.Thread(target=self.proxy_method, name=f"{self.name}-thread")
                self._thread.start()
            except:
                self._status = ActionStatus.FAILED
                self._thread = None
                self._run_event.clear()
                raise RuntimeError("Failed to start the thread")

    def pause(self) -> None:
        self._status = ActionStatus.PAUSED
        self._run_event.clear()

    def check_pause(self) -> None:
        self._run_event.wait()

    def resume(self) -> None:
        self._status = ActionStatus.RUNNING
        self._run_event.set()

    def before_stop(self) -> None:
        pass

    def stop(self) -> None:
        self.before_stop()
        self._status = ActionStatus.STOPPED
        self._stop_event.set()
        self._run_event.set()
        if self._thread:
            self._thread.join()
        self._thread = None
        self.after_stop()
        self._status = ActionStatus.CREATED
        self._stop_event.clear()
        self._run_event.clear()
    
    def after_stop(self) -> None:
        pass

    def proxy_method(self) -> None:
        """
        eg:
        while not self.is_stopped():
            for i in range(100):
                self.check_pause()
                print(i)
                time.sleep(1)
        :return: None
        """
        raise NotImplementedError("Please implement the proxy_method in subclass")
