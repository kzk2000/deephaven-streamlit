import streamlit as st
from src.streamlit_deephaven import start_server, display_dh
from menu import menu

st.set_page_config(page_title="DH Math Plot Demo", page_icon="📐")

if 'app_group' not in st.session_state:
    st.session_state['app_group'] = __file__

menu()
st.subheader("Deephaven Math Plot Demo")

print("ddd")
start_server(jvm_args=[
    "-Xmx12g",
    "-DAuthHandlers=io.deephaven.auth.AnonymousAuthenticationHandler",
])



seconds = st.selectbox("Seconds", options=[1, 2, 3], index=0)
print(seconds)

# Create a deephaven component with a simple table
# Create a table and display it
from deephaven import time_table, ring_table
from deephaven.plot.figure import Figure

print(f"PT{seconds}S")

t = time_table(f"PT{seconds}S").update(["x=i", "y=Math.sin(x)", "z=Math.cos(x)"])
t = ring_table(t, 10)
display_dh(t, object_id='t', height=400)

f = Figure().plot_xy(series_name="Sine", t=t, x="x", y="y").show()
f = f.plot_xy(series_name="Cosine", t=t, x="x", y="z").show()
display_dh(f, object_id='f', height=400)

