"""
This code is copied from the original code of Werkzeug.
link : https://github.com/pallets/werkzeug/blob/main/src/werkzeug/serving.py
"""


import typing as t
import socket
import os
from nc_console import Console
from werkzeug.serving import (WSGIRequestHandler, 
                        _TSSLContextArg,
                        get_interface_ip,
                        make_server,
                        is_running_from_reloader,
                        can_open_by_fd,
                        select_address_family,
                        get_sockaddr,
                        af_unix,
                        )


if t.TYPE_CHECKING:
    from _typeshed.wsgi import WSGIApplication

LISTEN_QUEUE = 128


def _navycut_base_logger() -> None:
    from ..conf import settings
    
    Console.log.Info("Started Navycut Development server.")
    Console.log.Info(f"Project Name: {settings.PROJECT_NAME}")
    Console.log.Info(f"Settings file: {settings.SETTINGS_FILE_NAME}")
    Console.log.Warning(f"Debug Mode: {'on' if settings.DEBUG else 'off'}")

def _running_on_all_addr_logger() -> None:
    Console.log.Info("Running on all addresses.")
    Console.log.Warning("This is a development server. Do not use it in a production deployment.")

def _run_base_server_logger(ssl_context, addr, port) -> None:
    Console.log.Success(f"Running on {ssl_context}://{addr}:{port}/ (Press CTRL+C to quit)")


def run_simple_wsgi(
            hostname: str,
            port: int,
            application: "WSGIApplication",
            use_reloader: bool = False,
            use_debugger: bool = False,
            use_evalex: bool = True,
            extra_files: t.Optional[t.Iterable[str]] = None,
            exclude_patterns: t.Optional[t.Iterable[str]] = None,
            reloader_interval: int = 1,
            reloader_type: str = "stat",
            threaded: bool = False,
            processes: int = 1,
            request_handler: t.Optional[t.Type[WSGIRequestHandler]] = None,
            static_files: t.Optional[t.Dict[str, t.Union[str, t.Tuple[str, str]]]] = None,
            passthrough_errors: bool = False,
            ssl_context: t.Optional[_TSSLContextArg] = None,
            ) -> None:
    """Start a WSGI application. Optional features include a reloader,
    multithreading and fork support.

    :param hostname: The host to bind to, for example ``'localhost'``.
        If the value is a path that starts with ``unix://`` it will bind
        to a Unix socket instead of a TCP socket..
    :param port: The port for the server.  eg: ``8080``
    :param application: the WSGI application to execute
    :param use_reloader: should the server automatically restart the python
                         process if modules were changed?
    :param use_debugger: should the werkzeug debugging system be used?
    :param use_evalex: should the exception evaluation feature be enabled?
    :param extra_files: a list of files the reloader should watch
                        additionally to the modules.  For example configuration
                        files.
    :param exclude_patterns: List of :mod:`fnmatch` patterns to ignore
        when running the reloader. For example, ignore cache files that
        shouldn't reload when updated.
    :param reloader_interval: the interval for the reloader in seconds.
    :param reloader_type: the type of reloader to use.  The default is
                          auto detection.  Valid values are ``'stat'`` and
                          ``'watchdog'``. See :ref:`reloader` for more
                          information.
    :param threaded: should the process handle each request in a separate
                     thread?
    :param processes: if greater than 1 then handle each request in a new process
                      up to this maximum number of concurrent processes.
    :param request_handler: optional parameter that can be used to replace
                            the default one.  You can use this to replace it
                            with a different
                            :class:`~BaseHTTPServer.BaseHTTPRequestHandler`
                            subclass.
    :param static_files: a list or dict of paths for static files.  This works
                         exactly like :class:`SharedDataMiddleware`, it's actually
                         just wrapping the application in that middleware before
                         serving.
    :param passthrough_errors: set this to `True` to disable the error catching.
                               This means that the server will die on errors but
                               it can be useful to hook debuggers in (pdb etc.)
    :param ssl_context: an SSL context for the connection. Either an
                        :class:`ssl.SSLContext`, a tuple in the form
                        ``(cert_file, pkey_file)``, the string ``'adhoc'`` if
                        the server should automatically create one, or ``None``
                        to disable SSL (which is the default).
    """
    if not isinstance(port, int):
        raise TypeError("port must be an integer")
    if use_debugger:
        from werkzeug.debug import DebuggedApplication

        application = DebuggedApplication(application, use_evalex)
    if static_files:
        from werkzeug.middleware.shared_data import SharedDataMiddleware

        application = SharedDataMiddleware(application, static_files)

    def log_startup(sock: socket.socket) -> None:
        _navycut_base_logger()

        if sock.family == af_unix: 
            Console.log.Info(f"Running on {hostname} (Press CTRL+C to quit)")
        else:
            if hostname == "0.0.0.0":
                _running_on_all_addr_logger()
                display_hostname = get_interface_ip(socket.AF_INET)
            elif hostname == "::":
                _running_on_all_addr_logger()
                display_hostname = get_interface_ip(socket.AF_INET6)
            else:
                display_hostname = hostname

            if ":" in display_hostname:
                display_hostname = f"[{display_hostname}]"
            
            _run_base_server_logger("http" if ssl_context is None else "https",
                                display_hostname,
                                sock.getsockname()[1]
                                )

    def inner() -> None:
        try:
            fd: t.Optional[int] = int(os.environ["WERKZEUG_SERVER_FD"])
        except (LookupError, ValueError):
            fd = None
        srv = make_server(
            hostname,
            port,
            application,
            threaded,
            processes,
            request_handler,
            passthrough_errors,
            ssl_context,
            fd=fd,
        )
        if fd is None:
            log_startup(srv.socket)
        srv.serve_forever()

    if use_reloader:
        # If we're not running already in the subprocess that is the
        # reloader we want to open up a socket early to make sure the
        # port is actually available.
        if not is_running_from_reloader():
            if port == 0 and not can_open_by_fd:
                raise ValueError(
                    "Cannot bind to a random port with enabled "
                    "reloader if the Python interpreter does "
                    "not support socket opening by fd."
                )

            # Create and destroy a socket so that any exceptions are
            # raised before we spawn a separate Python interpreter and
            # lose this ability.
            address_family = select_address_family(hostname, port)
            server_address = get_sockaddr(hostname, port, address_family)
            s = socket.socket(address_family, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(server_address)
            s.set_inheritable(True)

            # If we can open the socket by file descriptor, then we can just
            # reuse this one and our socket will survive the restarts.
            if can_open_by_fd:
                os.environ["WERKZEUG_SERVER_FD"] = str(s.fileno())
                s.listen(LISTEN_QUEUE)
                log_startup(s)
            else:
                s.close()
                if address_family == af_unix:
                    server_address = t.cast(str, server_address)
                    Console.log.Info(f"Unlinking {server_address}")
                    os.unlink(server_address)

        from ._reloader import run_with_reloader as _rwr

        _rwr(
            inner,
            extra_files=extra_files,
            exclude_patterns=exclude_patterns,
            interval=reloader_interval,
            reloader_type=reloader_type,
        )
    else:
        inner()