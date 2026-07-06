# ITables for VS Code

This extension auto-initializes `itables` in VS Code Jupyter notebooks so pandas and polars DataFrames are rendered as interactive DataTables.

## What it does

For each Python notebook session, the extension runs this Python snippet in the active kernel:

```python
import itables
itables.init_notebook_mode(all_interactive=True)
```

The snippet is executed through a managed initialization cell at the top of the notebook.
That cell is kept (and can be hidden/collapsed) so the initialization output stays available.
If `itables` is missing in the active kernel, the extension shows a prompt with actions to install in the active kernel, open docs, or suppress further prompts for that notebook.

## Commands

- `ITables: Initialize In Active Notebook`
- `ITables: Install In Active Notebook Kernel`
- `ITables: Reset Auto-Init Session State`

## Settings

- `itablesForVscode.enableAutoInit`: enable/disable automatic initialization.
- `itablesForVscode.initSnippet`: custom Python snippet to execute.

## Development

```bash
cd packages/itables_for_vscode
npm install
npm run compile
```

Press `F5` from this folder in VS Code to launch an Extension Development Host.

If that does not work in this monorepo layout, use this flow instead:

1. In VS Code, open `packages/itables_for_vscode` as the workspace root (or open this folder in a new window).
2. Open `src/extension.ts`.
3. Run the command `Debug: Select and Start Debugging` and choose `Run Extension`.

If `Run Extension` is not offered, create `.vscode/launch.json` in `packages/itables_for_vscode` with:

```json
{
	"version": "0.2.0",
	"configurations": [
		{
			"name": "Run Extension",
			"type": "extensionHost",
			"request": "launch",
			"args": ["--extensionDevelopmentPath=${workspaceFolder}"],
			"outFiles": ["${workspaceFolder}/out/**/*.js"],
			"preLaunchTask": "npm: compile"
		}
	]
}
```

## Publish to the VS Code Marketplace

1. Create a publisher in Azure DevOps / VS Code Marketplace.
2. Create a Personal Access Token (PAT) with Marketplace publish permissions.
3. Login once from your local machine:

```bash
cd packages/itables_for_vscode
npx @vscode/vsce login <publisher-name>
```

4. Build and package the extension:

```bash
cd packages/itables_for_vscode
npm install
npm run compile
npx @vscode/vsce package
```

This produces a `.vsix` file that you can also install manually in VS Code (`Extensions: Install from VSIX...`).

5. Publish a new version:

```bash
cd packages/itables_for_vscode
npx @vscode/vsce publish patch
```

Use `minor` or `major` instead of `patch` when needed.

## Ensure `itables` Is Installed In User Environments

An extension cannot strictly guarantee package installation in every kernel (permissions, offline machines, locked environments), but you can make it robust:

1. Document `pip install itables` in your project setup.
2. Recommend environment-managed installs (`requirements.txt`, `environment.yml`, `pyproject.toml`).
3. Use the command `ITables: Install In Active Notebook Kernel` when prompted (or proactively) to install into the currently selected notebook kernel.
