"""
This code is copied from the original code of Werkzeug.
link : https://github.com/pallets/werkzeug/blob/main/src/werkzeug/serving.py
"""


import typing as t
import os
from nc_console import Console
from werkzeug.serving import (
    WSGIRequestHandler, 
    _TSSLContextArg,
    prepare_socket,
    make_server,
    is_running_from_reloader,
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
    reloader_type: str = "auto",
    threaded: bool = False,
    processes: int = 1,
    request_handler: t.Optional[t.Type[WSGIRequestHandler]] = None,
    static_files: t.Optional[t.Dict[str, t.Union[str, t.Tuple[str, str]]]] = None,
    passthrough_errors: bool = False,
    ssl_context: t.Optional[_TSSLContextArg] = None,
) -> None:
    """Start a development server for a WSGI application. Various
    optional features can be enabled.

    .. warning::

        Do not use the development server when deploying to production.
        It is intended for use only during local development. It is not
        designed to be particularly efficient, stable, or secure.

    :param hostname: The host to bind to, for example ``'localhost'``.
        Can be a domain, IPv4 or IPv6 address, or file path starting
        with ``unix://`` for a Unix socket.
    :param port: The port to bind to, for example ``8080``. Using ``0``
        tells the OS to pick a random free port.
    :param application: The WSGI application to run.
    :param use_reloader: Use a reloader process to restart the server
        process when files are changed.
    :param use_debugger: Use Werkzeug's debugger, which will show
        formatted tracebacks on unhandled exceptions.
    :param use_evalex: Make the debugger interactive. A Python terminal
        can be opened for any frame in the traceback. Some protection is
        provided by requiring a PIN, but this should never be enabled
        on a publicly visible server.
    :param extra_files: The reloader will watch these files for changes
        in addition to Python modules. For example, watch a
        configuration file.
    :param exclude_patterns: The reloader will ignore changes to any
        files matching these :mod:`fnmatch` patterns. For example,
        ignore cache files.
    :param reloader_interval: How often the reloader tries to check for
        changes.
    :param reloader_type: The reloader to use. The ``'stat'`` reloader
        is built in, but may require significant CPU to watch files. The
        ``'watchdog'`` reloader is much more efficient but requires
        installing the ``watchdog`` package first.
    :param threaded: Handle concurrent requests using threads. Cannot be
        used with ``processes``.
    :param processes: Handle concurrent requests using up to this number
        of processes. Cannot be used with ``threaded``.
    :param request_handler: Use a different
        :class:`~BaseHTTPServer.BaseHTTPRequestHandler` subclass to
        handle requests.
    :param static_files: A dict mapping URL prefixes to directories to
        serve static files from using
        :class:`~werkzeug.middleware.SharedDataMiddleware`.
    :param passthrough_errors: Don't catch unhandled exceptions at the
        server level, let the serve crash instead. If ``use_debugger``
        is enabled, the debugger will still catch such errors.
    :param ssl_context: Configure TLS to serve over HTTPS. Can be an
        :class:`ssl.SSLContext` object, a ``(cert_file, key_file)``
        tuple to create a typical context, or the string ``'adhoc'`` to
        generate a temporary self-signed certificate.
    """
    if not isinstance(port, int):
        raise TypeError("port must be an integer")

    if static_files:
        from werkzeug.middleware.shared_data import SharedDataMiddleware

        application = SharedDataMiddleware(application, static_files)

    if use_debugger:
        from werkzeug.debug import DebuggedApplication

        application = DebuggedApplication(application, evalex=use_evalex)

    if not is_running_from_reloader():
        s = prepare_socket(hostname, port)
        fd = s.fileno()
        os.environ["WERKZEUG_SERVER_FD"] = str(fd)
    else:
        fd = int(os.environ["WERKZEUG_SERVER_FD"])

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

    if not is_running_from_reloader():
        srv.log_startup()

    if use_reloader:
        from werkzeug._reloader import run_with_reloader

        run_with_reloader(
            srv.serve_forever,
            extra_files=extra_files,
            exclude_patterns=exclude_patterns,
            interval=reloader_interval,
            reloader_type=reloader_type,
        )
    else:
        srv.serve_forever()