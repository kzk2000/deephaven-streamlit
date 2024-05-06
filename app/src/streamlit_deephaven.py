import __main__
from typing import List, Optional

import streamlit as st
from streamlit_server_state import server_state_lock
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def open_ctx(app_id):
    """
    Thread-safe opening of the Deephaven execution context.
    Required before performing any operations on the server.
    """
    from deephaven_server import Server

    if not hasattr(Server.instance, '__deephaven_ctx'):
        with server_state_lock["open_ctx" + app_id]:
            if not hasattr(Server.instance, '__deephaven_ctx'):
                logger.info("initializing context...")

                # store the execution context as an attribute on the server instance
                from deephaven.execution_context import get_exec_ctx
                Server.instance.__deephaven_ctx = get_exec_ctx()

    logger.info("opening context...")
    Server.instance.__deephaven_ctx.j_exec_ctx.open()
    return Server.instance.__deephaven_ctx


@st.cache_resource
def get_main(context: str):
    """
    Caches __main__ for given context that's shared across all users, sessions, and reruns
    via decorator st.cache_resource
    """
    logger.info(f"global caching __main__ for context={context}")
    return __main__


def start_server(
        host: Optional[str] = None,
        port: Optional[int] = None,
        jvm_args: Optional[List[str]] = None,
        app_id: Optional[str] = None,
):
    """Initialize the Deephaven server. This will start the server if it is not already running."""
    from deephaven_server import Server

    logger.info(f'outside server_state_lock with {app_id=}')
    if Server.instance is None:
        with server_state_lock["dh__main__"]:
            if Server.instance is None:
                st.write(f"lock for {app_id}")
                logger.info(f'server_state_lock is active for id={app_id}')

                logger.info("Initializing Deephaven Server...")
                s = Server(host=host, port=port, jvm_args=jvm_args)
                s.start()
                logger.info(f"Deephaven Server listening on port={s.port}")
            else:
                logger.info(f'server already running when hitting with id={app_id}')

    with server_state_lock["dh__main__"]:
        _ = get_main(context='deephaven' + app_id)  # caches DH __main__ ONLY ONCE applet
        open_ctx(app_id)
    return Server.instance


def display_dh(widget, object_id, app_id, height=600, width=None):
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
    get_main(context='deephaven' + app_id).__dict__[object_id] = widget

    # generate the iframe_url from the object type
    server_url = f"http://localhost:{Server.instance.port}"
    iframe_url = f"{server_url}/iframe/widget/?name={object_id}&nonce={id(widget)}"
    st.components.v1.iframe(iframe_url, height=height, width=width)
