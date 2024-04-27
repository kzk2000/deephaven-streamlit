import streamlit as st
from streamlit_deephaven import start_server, display_dh

start_server(jvm_args=[
    "-Xmx12g",
    "-DAuthHandlers=io.deephaven.auth.AnonymousAuthenticationHandler",
])

st.subheader("Deephaven Component Demo")

seconds = st.selectbox("Seconds", options=[1, 2, 3], index=0)
print(seconds)

# Create a deephaven component with a simple table
# Create a table and display it
from deephaven import time_table, ring_table
from deephaven.plot.figure import Figure

print(f"PT{seconds}S")

t = time_table(f"PT{seconds}S").update(["x=i", "y=Math.sin(x)", "z=Math.cos(x)"])
t = ring_table(t, 25)
display_dh(t, height=200)

f = Figure().plot_xy(series_name="Sine", t=t, x="x", y="y").show()
f = f.plot_xy(series_name="Cosine", t=t, x="x", y="z").show()
display_dh(f, height=400)
