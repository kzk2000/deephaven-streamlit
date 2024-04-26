import streamlit as st
from streamlit_deephaven import start_server, display_dh

start_server(jvm_args=[
    "-Xmx12g",
    "-DAuthHandlers=io.deephaven.auth.AnonymousAuthenticationHandler",
])

st.subheader("Deephaven Component Demo")

# Create a deephaven component with a simple table
# Create a table and display it
from deephaven import time_table
from deephaven.plot.figure import Figure

t = time_table("PT1S").update(["x=i", "y=Math.sin(x) + 15", "z=Math.cos(x) * x"])
display_dh(t, height=200)

f = Figure().plot_xy(series_name="Sine", t=t, x="x", y="y").show()
f = f.plot_xy(series_name="Cosine", t=t, x="x", y="z").show()
display_dh(f, height=400)
