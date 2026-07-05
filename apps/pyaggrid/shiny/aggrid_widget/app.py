from itables_core.sample_dfs import get_dict_of_test_dfs
from pyaggrid.widget import AgGrid
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import reactive_read, render_widget

dfs = get_dict_of_test_dfs()

ui.page_opts(title="Using the AgGrid widget in a Shiny App", fillable=True)

with ui.card():
    with ui.layout_sidebar():
        with ui.sidebar():
            ui.input_select(
                "table_selector",
                "Table",
                choices=list(dfs.keys()),
                selected="int_float_str",
            )

        @render_widget  # pyright: ignore[reportArgumentType]
        def my_table():
            """
            This function creates the "my_table" widget.
            """
            return AgGrid(rowSelection={"mode": "multiRow"})

        @reactive.effect
        def _():
            """
            This "reactive.effect" calls the "update" method of the AgGrid
            widget to update the widget with the new inputs.
            """
            df = dfs[input.table_selector()]
            my_table.widget.update(df)  # pyright: ignore[reportOptionalMemberAccess]

        ui.markdown("Selected rows")

        @render.code
        def selected_rows():
            """
            Here we read the "selected_rows" attribute of the AgGrid widget
            """
            return str(
                reactive_read(
                    my_table.widget,  # pyright: ignore[reportOptionalMemberAccess]
                    "selected_rows",
                )
            )
