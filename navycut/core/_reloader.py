"""
This code is copied from the original code of Werkzeug.
link : https://github.com/pallets/werkzeug/blob/main/src/werkzeug/_reloader.py
"""


import os
import sys
import time
import threading
import subprocess
import typing as t
from itertools import chain
from nc_console import Console
from werkzeug._reloader import (ReloaderLoop as _ReloaderLoop,
                        _get_args_for_reloading,
                        _find_stat_paths,
                        _find_watchdog_paths,
                        ensure_echo_on
                        )


class ReloaderLoop(_ReloaderLoop):
    def __init__(self, *wargs, **kwargs):
        super(ReloaderLoop, self).__init__(*wargs, **kwargs)

    def restart_with_reloader(self) -> int:
        """Spawn a new Python interpreter with the same arguments as the
        current one, but running the reloader thread.
        """
        while True:
            Console.log.Info(f"Restarting with {self.name}")
            args = _get_args_for_reloading()
            new_environ = os.environ.copy()
            new_environ["WERKZEUG_RUN_MAIN"] = "true"
            exit_code = subprocess.call(args, env=new_environ, close_fds=False)

            if exit_code != 3:
                return exit_code

    def log_reload(self, filename: str) -> None:
        filename = os.path.abspath(filename)
        Console.log.Info(f"Detected change in {filename!r}, reloading")


class StatReloaderLoop(ReloaderLoop):
    name = "stat"

    def __enter__(self) -> ReloaderLoop:
        self.mtimes: t.Dict[str, float] = {}
        return super().__enter__()

    def run_step(self) -> None:
        for name in chain(_find_stat_paths(self.extra_files, self.exclude_patterns)):
            try:
                mtime = os.stat(name).st_mtime
            except OSError:
                continue

            old_time = self.mtimes.get(name)

            if old_time is None:
                self.mtimes[name] = mtime
                continue

            if mtime > old_time:
                self.trigger_reload(name)


class WatchdogReloaderLoop(ReloaderLoop):
    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        from watchdog.observers import Observer
        from watchdog.events import PatternMatchingEventHandler

        super().__init__(*args, **kwargs)
        trigger_reload = self.trigger_reload

        class EventHandler(PatternMatchingEventHandler):  # type: ignore
            def on_any_event(self, event):  # type: ignore
                trigger_reload(event.src_path)

        reloader_name = Observer.__name__.lower()

        if reloader_name.endswith("observer"):
            reloader_name = reloader_name[:-8]

        self.name = f"watchdog ({reloader_name})"
        self.observer = Observer()
        # Extra patterns can be non-Python files, match them in addition
        # to all Python files in default and extra directories. Ignore
        # __pycache__ since a change there will always have a change to
        # the source file (or initial pyc file) as well. Ignore Git and
        # Mercurial internal changes.
        extra_patterns = [p for p in self.extra_files if not os.path.isdir(p)]
        self.event_handler = EventHandler(
            patterns=["*.py", "*.pyc", "*.zip", *extra_patterns],
            ignore_patterns=[
                "*/__pycache__/*",
                "*/.git/*",
                "*/.hg/*",
                *self.exclude_patterns,
            ],
        )
        self.should_reload = False

    def trigger_reload(self, filename: str) -> None:
        # This is called inside an event handler, which means throwing
        # SystemExit has no effect.
        # https://github.com/gorakhargosh/watchdog/issues/294
        self.should_reload = True
        self.log_reload(filename)

    def __enter__(self) -> ReloaderLoop:
        self.watches: t.Dict[str, t.Any] = {}
        self.observer.start()
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore
        self.observer.stop()
        self.observer.join()

    def run(self) -> None:
        while not self.should_reload:
            self.run_step()
            time.sleep(self.interval)

        sys.exit(3)

    def run_step(self) -> None:
        to_delete = set(self.watches)

        for path in _find_watchdog_paths(self.extra_files, self.exclude_patterns):
            if path not in self.watches:
                try:
                    self.watches[path] = self.observer.schedule(
                        self.event_handler, path, recursive=True
                    )
                except OSError:
                    # Clear this path from list of watches We don't want
                    # the same error message showing again in the next
                    # iteration.
                    self.watches[path] = None

            to_delete.discard(path)

        for path in to_delete:
            watch = self.watches.pop(path, None)

            if watch is not None:
                self.observer.unschedule(watch)


reloader_loops: t.Dict[str, t.Type[ReloaderLoop]] = {
    "stat": StatReloaderLoop,
    "watchdog": WatchdogReloaderLoop,
}


def run_with_reloader(
    main_func: t.Callable[[], None],
    extra_files: t.Optional[t.Iterable[str]] = None,
    exclude_patterns: t.Optional[t.Iterable[str]] = None,
    interval: t.Union[int, float] = 1,
    reloader_type: str = "auto",
) -> None:
    """Run the given function in an independent Python interpreter."""
    import signal

    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
    reloader = reloader_loops[reloader_type](
        extra_files=extra_files, exclude_patterns=exclude_patterns, interval=interval
    )

    try:
        if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
            ensure_echo_on()
            t = threading.Thread(target=main_func, args=())
            t.daemon = True

            # Enter the reloader to set up initial state, then start
            # the app thread and reloader update loop.
            with reloader:
                t.start()
                reloader.run()
        else:
            sys.exit(reloader.restart_with_reloader())
    except KeyboardInterrupt:
        pass