"""A sample streamlit app that displays DataFrames with pyaggrid.

pyaggrid does not have a native Streamlit component yet, so we embed
its HTML representation with st.components.v1.html.

Run it locally with

    streamlit run apps/streamlit/pyaggrid_app.py
"""

import itables_core.sample_dfs
import streamlit as st
import streamlit.components.v1 as components
from pyaggrid import to_html_aggrid

st.set_page_config(page_title="PyAgGrid in Streamlit", layout="wide")
st.title("PyAgGrid in Streamlit")

test_dfs = itables_core.sample_dfs.get_dict_of_test_dfs()
table_selector = st.selectbox(
    "Table", test_dfs.keys(), index=list(test_dfs).index("int_float_str")
)
theme = st.selectbox("Theme", ["quartz", "balham", "material", "alpine"])

df = test_dfs[table_selector]
components.html(to_html_aggrid(df, theme=theme), height=600, scrolling=True)
