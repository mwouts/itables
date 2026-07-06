"""
Run this app with:

pixi run -e streamlit-app streamlit run apps/streamlit/pydatatables_app.py
"""

from typing import Optional

import pyarrow  # type: ignore
import streamlit as st
from pydatatables.typing import Unpack

try:
    from st_aggrid import AgGrid  # type: ignore
except ImportError as e:
    import_error = e

    class AgGrid:
        def __init__(self, *args, **kwargs):  # type: ignore
            raise import_error


import pydatatables
from pydatatables.streamlit import datatable
from streamlit.errors import StreamlitAPIException

st.set_page_config(
    page_title="ITables in Streamlit",
    page_icon="https://raw.githubusercontent.com/mwouts/itables/main/src/itables/logo/loading.svg",
)
st.logo(
    "https://raw.githubusercontent.com/mwouts/itables/main/src/itables/logo/logo.svg",
    link="https://mwouts.github.io/itables/streamlit.html",
)
st.markdown(
    "![ITables](https://raw.githubusercontent.com/mwouts/itables/main/src/itables/logo/wide.svg)"
)
st.sidebar.markdown(
    """
                    # ITables in Streamlit
                    ![Stars](https://img.shields.io/github/stars/mwouts/itables)
                    """
)
st.sidebar.caption(f"ITables version: {pydatatables.__version__}")

caption = st.sidebar.text_input("Caption", value="Countries")
select = st.sidebar.toggle("Row selection", value=True)
classes = st.sidebar.multiselect(
    "Classes",
    options=["display", "nowrap", "compact", "cell-border", "stripe"],
    default=pydatatables.javascript.get_expanded_classes(pydatatables.options.classes),
)
buttons = st.sidebar.multiselect(
    "Buttons",
    options=["pageLength", "copyHtml5", "csvHtml5", "excelHtml5", "colvis"],
    default=["copyHtml5", "csvHtml5", "excelHtml5", "colvis"],
)

style = st.sidebar.text_input(
    "Style", value=pydatatables.javascript.get_compact_style(pydatatables.options.style)
)

render_with = st.sidebar.selectbox(
    "Render with", ["st.dataframe", "streamlit-aggrid", "pydatatables"], index=2
)

include_html = st.sidebar.checkbox("Include HTML")
df = pydatatables.sample_dfs.get_countries(html=include_html)

it_args: pydatatables.PyDataTablesOptions = {}
if select:
    it_args["select"] = True
    it_args["selected_rows"] = [0, 1, 2, 100, 207]
if classes != pydatatables.javascript.get_expanded_classes(
    pydatatables.options.classes
):
    it_args["classes"] = classes
if style != pydatatables.options.style:
    it_args["style"] = style

if buttons:
    it_args["buttons"] = buttons

if render_with == "st.dataframe":

    def render_table(df, key: str, caption: Optional[str], **not_used):  # type: ignore
        return st.dataframe(df, key=key)  # type: ignore

    snippet = """st.dataframe(df)
"""

elif render_with == "streamlit-aggrid":

    def render_table(df, key: str, caption: Optional[str], **not_used):  # type: ignore
        return AgGrid(df, key=key)  # type: ignore

    snippet = """from st_aggrid import AgGrid

AgGrid(df, key=None)
"""
else:
    formatted_args = ["df"] + [
        f"{key}='{value}'" if isinstance(value, str) else f"{key}={value}"
        for key, value in it_args.items()
    ]
    formatted_args = ",\n                  ".join(formatted_args)

    def render_table(
        df: pydatatables.DataFrameOrSeries,
        key: str,
        caption: Optional[str],
        **it_args: Unpack[pydatatables.PyDataTablesOptions],
    ):
        return datatable(df, key=key, caption=caption, **it_args)

    snippet = f"""from pydatatables.streamlit import datatable

datatable(df, caption='{caption}', {formatted_args})
"""

st.markdown(
    f"""```python
{snippet}
```
"""
)

t = render_table(df, caption=caption, key="my_table", **it_args)

if render_with == "pydatatables":
    st.header("Table state")
    st.markdown(
        """The value returned by `datatable` is
    a dict that contains the index of the selected rows:"""
    )
    st.write(t)  # type: ignore

st.header("More sample dataframes")
test_dfs = pydatatables.sample_dfs.get_dict_of_test_dfs()
tabs = st.tabs(list(test_dfs.keys()))

for (name, df), tab in zip(test_dfs.items(), tabs):
    with tab:
        try:
            render_table(df, caption=None, key=name)
        except (
            # ITables
            NotImplementedError,
            # st.dataframe
            ValueError,
            # streamlit-aggrid
            pyarrow.lib.ArrowInvalid,  # pyright: ignore[reportUnknownMemberType,reportAttributeAccessIssue]
            StreamlitAPIException,
        ) as e:  # pyright: ignore[reportUnknownVariableType]
            st.warning(e)  # pyright: ignore[reportUnknownArgumentType]
