"""A sample streamlit app that displays DataFrames with the pyaggrid component.

Run it locally with

    streamlit run apps/pyaggrid/streamlit/app.py
"""

import itables_core.sample_dfs
import streamlit as st
from pyaggrid.streamlit import aggrid

st.set_page_config(page_title="PyAgGrid in Streamlit", layout="wide")
st.title("PyAgGrid in Streamlit")

test_dfs = itables_core.sample_dfs.get_dict_of_test_dfs()
table_selector = st.selectbox(
    "Table", test_dfs.keys(), index=list(test_dfs).index("int_float_str")
)
theme = st.selectbox("Theme", ["quartz", "balham", "material", "alpine"])

df = test_dfs[table_selector]
result = aggrid(df, theme=theme, rowSelection={"mode": "multiRow"})
st.write("Selected rows:", result["selected_rows"])
