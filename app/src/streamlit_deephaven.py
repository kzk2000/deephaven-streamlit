import os
import streamlit.components.v1 as components
from uuid import uuid4
import streamlit as st
from typing import Dict, List, Optional
import __main__

from streamlit_server_state import server_state, server_state_lock


def open_ctx():
    """Open the Deephaven execution context. Required before performing any operations on the server."""
    from deephaven_server import Server
    # We store the execution context as an attribute on the server instance
    if not hasattr(Server.instance, '__deephaven_ctx'):
        print("Initializing Context...")

        from deephaven.execution_context import get_exec_ctx
        Server.instance.__deephaven_ctx = get_exec_ctx()
    print("Opening context...")
    Server.instance.__deephaven_ctx.j_exec_ctx.open()
    return Server.instance.__deephaven_ctx


def start_server(host: Optional[str] = None, port: Optional[int] = None, jvm_args: Optional[List[str]] = None):
    """Initialize the Deephaven server. This will start the server if it is not already running."""
    with server_state_lock["dh__main__"]:
        from deephaven_server import Server
        if Server.instance is None:
            print("Initializing Deephaven Server...")
            s = Server(host=host, port=port, jvm_args=jvm_args)
            s.start()
            print("Deephaven Server listening on port", s.port)
            server_state["dh__main__"] = __main__

    open_ctx()
    return Server.instance


def display_dh(widget, object_id, height=600, width=None):
    """Display a Deephaven widget.

    Parameters
    ----------
    widget: deephaven.table.Table | deephaven.plot.figure.Figure | pandas.core.frame.DataFrame
        The Deephaven widget we want to display
    object_id: string
        The variable name of the Deephaven widget we want to display
    height: int
        The height of the widget in pixels
    width: int
        The width of the widget in pixels

    """
    from deephaven_server import Server

    # add the table to the main modules globals list so it can be retrieved by the iframe
    if "dh__main__" in server_state:
        server_state["dh__main__"].__dict__[object_id] = widget

    # generate the iframe_url from the object type
    server_url = f"http://localhost:{Server.instance.port}"
    iframe_url = f"{server_url}/iframe/widget/?name={object_id}&nonce={id(widget)}"
    components.iframe(iframe_url, height=height, width=width)
