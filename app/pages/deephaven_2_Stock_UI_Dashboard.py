import streamlit as st
from src.streamlit_deephaven import start_server, display_dh
from menu import menu

st.set_page_config(page_title="DH Stock UI Dashboard", page_icon="📐", layout="wide")

if 'app_group' not in st.session_state:
    st.session_state['app_group'] = 'Deephaven Apps'

menu()
st.subheader("Deephaven Stock UI Dashboard")
st.write(__file__)

start_server(
    jvm_args=[
        "-Xmx12g",
        "-DAuthHandlers=io.deephaven.auth.AnonymousAuthenticationHandler",
    ],
    app_id=__file__,
)

# only run these imports AFTER the Deephaven server is up
from deephaven import ui
from deephaven.plot import express as dx
from deephaven.plot.figure import Figure

_stocks = dx.data.stocks()
_cat_stocks = _stocks.where("sym=`CAT`")
_dog_stocks = _stocks.where("sym=`DOG`")
_stocks_plot = (
    Figure()
    .plot_xy("Cat", _cat_stocks, x="timestamp", y="price")
    .plot_xy("Dog", _dog_stocks, x="timestamp", y="price")
    .show()
)

stock_dash = ui.dashboard(
    ui.column(
        ui.row(
            ui.stack(ui.panel(_cat_stocks, title="Cat")),
            ui.stack(ui.panel(_dog_stocks, title="Dog")),
        ),
        ui.stack(ui.panel(_stocks_plot, title="Stocks")),
    )
)

display_dh(stock_dash, "stock_dash", height=750, width=1700, app_id=__file__)
