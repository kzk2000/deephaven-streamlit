import __main__
import logging
import threading
from typing import List, Optional
import streamlit as st

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(filename)s:%(lineno)s -> %(funcName)12s()] %(message)s", level=logging.INFO)

lock = threading.RLock()
logger.info(f"thread_id={threading.get_native_id()}: init lock")
logger.info(f"thread_id={threading.get_native_id()}: {__main__.__dict__['__file__']=}")


def open_ctx():
    """
    Thread-safe opening of the Deephaven execution context which is
    required before performing any operations on the server.
    """
    from deephaven_server import Server

    if not hasattr(Server.instance, '__deephaven_ctx'):
        # only lock if you made it his far
        with lock:
            if not hasattr(Server.instance, '__deephaven_ctx'):
                logger.info(f"thread_id={threading.get_native_id()}: initializing context")

                # store the execution context as an attribute on the server instance
                from deephaven.execution_context import get_exec_ctx
                Server.instance.__deephaven_ctx = get_exec_ctx()
            else:
                logger.info(f"thread_id={threading.get_native_id()}: context already set")

    logger.info(f"thread_id={threading.get_native_id()}: opening context...")
    Server.instance.__deephaven_ctx.j_exec_ctx.open()
    return Server.instance.__deephaven_ctx


def start_server(
        host: Optional[str] = None,
        port: Optional[int] = None,
        jvm_args: Optional[List[str]] = None,
        app_id: Optional[str] = None,
):
    """
    Initialize the Deephaven server. This will start the server if it is not already running.
    """
    from deephaven_server import Server

    if Server.instance is None:
        # only lock if you made it his far
        with lock:
            if Server.instance is None:
                st.write(f"acquired lock for {app_id=}")
                logger.info(f"thread_id={threading.get_native_id()}: acquired lock")
                logger.info(f"thread_id={threading.get_native_id()}: starting Deephaven Server using thread_id=")
                s = Server(host=host, port=port, jvm_args=jvm_args)
                s.start()
                open_ctx()  # seems redundant but seem most thread-safe (no errors when having 20+ tabs open)
                logger.info(f"thread_id={threading.get_native_id()}: Deephaven Server is listening on port={s.port}")
            else:
                logger.info(f"thread_id={threading.get_native_id()}: Deephaven Server is already live.")

    open_ctx()
    return Server.instance


def display_dh(widget, object_id, app_id, height=600, width=None, main_dict={}):
    """Display a Deephaven widget.

    Parameters
    ----------
    widget: deephaven.table.Table | deephaven.plot.figure.Figure | pandas.core.frame.DataFrame
        Deephaven widget we want to display
    object_id: string
        Deephaven server variable name, usually the widget variable as string
    app_id: string
        usually __file__ of the applet script, must be set to get proper Deephaven __main__ reference
    height: int
        height of the widget in pixels
    width: int
        width of the widget in pixels
    """
    from deephaven_server import Server

    # this assigns the widget to the Deephaven server
    st.write(f"thread_id={threading.get_native_id()}: {__main__.__dict__['__file__']=}")
    __main__.__dict__[object_id] = widget

    # generate the iframe_url from the object type
    server_url = f"http://localhost:{Server.instance.port}"
    iframe_url = f"{server_url}/iframe/widget/?name={object_id}&nonce={id(widget)}"
    logger.info(f"thread_id={threading.get_native_id()}: {app_id=}, {iframe_url=}")
    return st.components.v1.iframe(iframe_url, height=height, width=width)
