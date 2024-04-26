import __main__
import os
import streamlit.components.v1 as components
from uuid import uuid4
import streamlit as st
from typing import Dict, List, Optional
import base64

TABLE_TYPES = {"deephaven.table.Table", "pandas.core.frame.DataFrame", "pydeephaven.table.Table"}
FIGURE_TYPES = {"deephaven.plot.figure.Figure"}


def _str_object_type(obj):
    """Returns the object type as a string value"""
    return f"{obj.__class__.__module__}.{obj.__class__.__name__}"


def _path_for_object(obj):
    """Return the iframe path for the specified object. Inspects the class name to determine."""
    name = _str_object_type(obj)

    if name in TABLE_TYPES:
        return "table"
    if name in FIGURE_TYPES:
        return "chart"

    # No special handling for this type, just try it as a widget
    return "widget"


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


def start_server(host: Optional[str] = None, port: Optional[int] = None, dh_args: Dict[str, str] = {}):
    """Initialize the Deephaven server. This will start the server if it is not already running."""
    from deephaven_server import Server
    if Server.instance is None:
        print("Initializing Deephaven Server...")
        jvm_args = [
            "-Xmx12g",
            "-DAuthHandlers=io.deephaven.auth.AnonymousAuthenticationHandler",
        ]
        s = Server(host=host, port=port, jvm_args=jvm_args, dh_args=dh_args)
        s.start()
        print("Deephaven Server listening on port", s.port)

    open_ctx()
    return Server.instance


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def display_dh(widget, height=600, width=None, object_id=None, key=None, session=None):
    """Display a Deephaven widget.

    Parameters
    ----------
    widget: deephaven.table.Table | deephaven.plot.figure.Figure | pandas.core.frame.DataFrame | str
        The Deephaven widget we want to display. If a string is passed, a session must be specified.
    height: int
        The height of the widget in pixels
    width: int
        The width of the widget in pixels
    object_id: string
        The variable name of the Deephaven widget we want to display.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    session: pydeephaven.Session
        The session to use when displaying a remote Deephaven widget by name.
        Must be specified if a string is passed as the widget parameter.

    Returns
    -------
    string
        The object_id of the created object

    """
    from deephaven_server import Server

    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.

    # Generate a new table ID using a UUID prepended with a `__w_` prefix if name not specified

    if isinstance(widget, str):
        # a string widget must match the object_id
        object_id = widget
    elif object_id is None:
        object_id = f"__w_{str(uuid4()).replace('-', '_')}"

    params = {"name": object_id}

    if isinstance(widget, str):
        if session is None:
            raise ValueError(
                "session must be specified when using a remote pydeephaven object by name"
            )
        port = session.port
        server_url = f"http://{session.host}:{port}/"
    elif _str_object_type(widget) == "pydeephaven.table.Table":
        session = widget.session

        if b"envoy-prefix" in session._extra_headers:
            params["envoyPrefix"] = session._extra_headers[b"envoy-prefix"].decode(
                "ascii"
            )

        port = widget.session.port
        server_url = f"http://{widget.session.host}:{port}/"

        if hasattr(session, "session_manager"):
            params["authProvider"] = "parent"
            # We have a DnD session, and we can get the authentication and connection details from the session manager
            token = base64.b64encode(
                session.session_manager.auth_client.get_token(
                    "RemoteQueryProcessor"
                ).SerializeToString()
            ).decode("us-ascii")
            server_url = (
                widget.session.pqinfo().state.connectionDetails.staticUrl
            )

        session.bind_table(object_id, widget)
    else:
        port = Server.instance.port
        server_url = f"http://localhost:{port}/"

        # Add the table to the main modules globals list so it can be retrieved by the iframe
        __main__.__dict__[object_id] = widget

    if "DEEPHAVEN_ST_URL" in os.environ:
        server_url = os.environ["DEEPHAVEN_ST_URL"]

    if not server_url.endswith("/"):
        server_url = f"{server_url}/"

    # Generate the iframe_url from the object type
    iframe_url = f"{server_url}iframe/{_path_for_object(widget)}/?name={object_id}"

    # We don't really need the component value in the Deephaven example, since we're just creating a display widget...
    # Maybe if we were making a one click widget, that would make sense...
    # component_value = _component_func(iframe_url=iframe_url, object_type=object_type, width=width, height=height, key=key, default=0)
    return components.iframe(iframe_url, height=height, width=width)


if True:
    import streamlit as st

    start_server()

    st.subheader("Deephaven Component Demo")

    # Create a deephaven component with a simple table
    # Create a table and display it
    from deephaven import time_table
    from deephaven.plot.figure import Figure

    t = time_table("PT1S").update(["x=i", "y=Math.sin(x)", "z=Math.cos(x)"])
    display_dh(t, height=200)

    f = Figure().plot_xy(series_name="Sine", t=t, x="x", y="y").show()
    f = f.plot_xy(series_name="Cosine", t=t, x="x", y="z").show()
    display_dh(f, height=400)