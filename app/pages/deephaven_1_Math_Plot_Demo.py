import streamlit as st
from menu import menu
from src.streamlit_deephaven import start_server, display_dh

st.set_page_config(page_title="DH Math Plot Demo", page_icon="📐")

if 'app_group' not in st.session_state:
    st.session_state['app_group'] = 'Deephaven Apps'

menu()
st.subheader("Deephaven Math Plot Demo")
st.write(__file__)

start_server(
    jvm_args=[
        "-Xmx12g",
        "-DAuthHandlers=io.deephaven.auth.AnonymousAuthenticationHandler",
    ],
    app_id=__file__,
    file_dict=locals(),
)

seconds = st.selectbox("Seconds", options=[1, 2, 3], index=0)

# only run these imports AFTER the Deephaven server is up
from deephaven import time_table, ring_table
from deephaven.plot.figure import Figure

t = time_table(f"PT{seconds}S").update(["x=i", "y=Math.sin(x)", "z=Math.cos(x)"])
t = ring_table(t, 10)
display_dh(t, object_id='t', app_id=__file__, height=400)

f = Figure().plot_xy(series_name="Sine", t=t, x="x", y="y").show()
f = f.plot_xy(series_name="Cosine", t=t, x="x", y="z").show()
display_dh(f, object_id='f', app_id=__file__, height=400)
