# Troubleshooting

If the table just says "Loading...", then maybe
- You loaded a notebook that is not trusted (run "Trust Notebook" in View / Activate Command Palette)
- Or you are offline?

At the moment `itables` does not have an [offline mode](https://github.com/mwouts/itables/issues/8). While the table data is embedded in the notebook, the `jquery` and `datatables.net` are loaded from a CDN, see our [require.config](https://github.com/mwouts/itables/blob/main/itables/javascript/load_datatables_connected.js) and our [table template](https://github.com/mwouts/itables/blob/main/itables/datatables_template.html), so an internet connection is required to display the tables.
