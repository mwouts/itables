window.__itables_render = async (table_id, dt_args) => {
  await initializeDataTables();
  $(table_id).DataTable(dt_args);
}

async function initializeDataTables() {
  if ($.prototype.DataTable) {
    return;
  };
};
