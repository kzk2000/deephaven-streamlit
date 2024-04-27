import __main__
import os
import streamlit.components.v1 as components
from uuid import uuid4
import streamlit as st
from typing import Dict, List, Optional

DEV_MODE = os.environ.get("DH_DEV_MODE", False)


def _str_object_type(obj):
    """Returns the object type as a string value"""
    return f"{obj.__class__.__module__}.{obj.__class__.__name__}"


def _path_for_object(obj):
    """Return the iframe path for the specified object. Inspects the class name to determine."""
    name = _str_object_type(obj)

    if name in ('deephaven.table.Table', 'pandas.core.frame.DataFrame'):
        return 'table'
    if name == 'deephaven.plot.figure.Figure':
        return 'chart'
    raise TypeError(f"Unknown object type: {name}")


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
    from deephaven_server import Server
    if Server.instance is None:
        print("Initializing Deephaven Server...")
        s = Server(host=host, port=port, jvm_args=jvm_args)
        s.start()
        print("Deephaven Server listening on port", s.port)

    open_ctx()
    return Server.instance


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def display_dh(widget, height=600, width=None, object_id=None):
    """Display a Deephaven widget.

    Parameters
    ----------
    widget: deephaven.table.Table | deephaven.plot.figure.Figure | pandas.core.frame.DataFrame
        The Deephaven widget we want to display
    height: int
        The height of the widget in pixels
    width: int
        The width of the widget in pixels
    object_id: string
        The variable name of the Deephaven widget we want to display

    Returns
    -------
    string
        The object_id of the created object

    """
    from deephaven_server import Server

    # generate a new table ID using a UUID prepended with a `__w_` prefix if name not specified
    if object_id is None:
        object_id = f"__w_{str(uuid4()).replace('-', '_')}"

    # generate the iframe_url from the object type
    server_url = f"http://localhost:{Server.instance.port}"
    iframe_url = f"{server_url}/iframe/widget/?name={object_id}"

    # add the table to the main modules globals list so it can be retrieved by the iframe
    __main__.__dict__[object_id] = widget
    return components.iframe(iframe_url, height=height, width=width)

