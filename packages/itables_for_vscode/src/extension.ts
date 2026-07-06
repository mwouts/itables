import * as vscode from "vscode";

const INIT_CELL_MARKER = "# itables-for-vscode:init";
const MISSING_MARKER = "__ITABLES_FOR_VSCODE_MISSING__";
const READY_MARKER = "__ITABLES_FOR_VSCODE_READY__";
const ITABLES_DOCS_URL = "https://mwouts.github.io/itables/quick_start.html";
const INSTALL_ITABLES_SNIPPET = [
  "import subprocess",
  "import sys",
  'subprocess.check_call([sys.executable, "-m", "pip", "install", "itables"])',
].join("\n");

const DEFAULT_INIT_SNIPPET = [
  INIT_CELL_MARKER,
  "import importlib.util",
  'if importlib.util.find_spec("itables") is None:',
  `    print("${MISSING_MARKER}")`,
  "else:",
  "    import itables",
  "    itables.init_notebook_mode(all_interactive=True)",
  `    print("${READY_MARKER}")`,
].join("\n");

class ItablesNotebookInitializer {
  private readonly initializedNotebookKeys = new Set<string>();
  private readonly missingNotebookKeys = new Set<string>();
  private readonly suppressedNotebookKeys = new Set<string>();
  private readonly inFlightNotebookKeys = new Set<string>();

  public resetSessionState(): void {
    this.initializedNotebookKeys.clear();
    this.missingNotebookKeys.clear();
    this.suppressedNotebookKeys.clear();
    this.inFlightNotebookKeys.clear();
  }

  public async maybeInitialize(notebook: vscode.NotebookDocument): Promise<void> {
    if (!this.shouldAutoInitialize(notebook)) {
      return;
    }

    const notebookKey = notebook.uri.toString();
    if (
      this.initializedNotebookKeys.has(notebookKey) ||
      this.missingNotebookKeys.has(notebookKey) ||
      this.inFlightNotebookKeys.has(notebookKey)
    ) {
      return;
    }

    this.inFlightNotebookKeys.add(notebookKey);
    try {
      const initCellIndex = await this.executeSnippetInNotebook(notebook);
      const state = this.getInitState(notebook, initCellIndex);
      if (state === "missing") {
        this.missingNotebookKeys.add(notebookKey);
        if (!this.suppressedNotebookKeys.has(notebookKey)) {
          await this.promptInstallItables(notebook);
        }
        return;
      }

      this.missingNotebookKeys.delete(notebookKey);
      this.suppressedNotebookKeys.delete(notebookKey);
      this.initializedNotebookKeys.add(notebookKey);
    } catch {
      // Ignore transient execution issues (e.g. missing kernel); retry on later events.
    } finally {
      this.inFlightNotebookKeys.delete(notebookKey);
    }
  }

  public async forceInitializeActiveNotebook(): Promise<void> {
    const editor = vscode.window.activeNotebookEditor;
    if (!editor) {
      void vscode.window.showInformationMessage("Open a notebook to initialize itables.");
      return;
    }

    try {
      const initCellIndex = await this.executeSnippetInNotebook(editor.notebook);
      const state = this.getInitState(editor.notebook, initCellIndex);
      const notebookKey = editor.notebook.uri.toString();

      if (state === "missing") {
        this.missingNotebookKeys.add(notebookKey);
        await this.promptInstallItables(editor.notebook);
      } else {
        this.missingNotebookKeys.delete(notebookKey);
        this.suppressedNotebookKeys.delete(notebookKey);
        this.initializedNotebookKeys.add(notebookKey);
        void vscode.window.showInformationMessage(
          "itables initialized for the active notebook.",
        );
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      void vscode.window.showWarningMessage(
        `Could not initialize itables: ${message}`,
      );
    }
  }

  private shouldAutoInitialize(notebook: vscode.NotebookDocument): boolean {
    if (notebook.notebookType !== "jupyter-notebook") {
      return false;
    }

    const config = vscode.workspace.getConfiguration("itablesForVscode");
    if (!config.get<boolean>("enableAutoInit", true)) {
      return false;
    }

    return this.looksLikePythonNotebook(notebook);
  }

  private looksLikePythonNotebook(notebook: vscode.NotebookDocument): boolean {
    const metadata = notebook.metadata as Record<string, unknown>;
    const kernelspec = metadata["kernelspec"] as
      | Record<string, unknown>
      | undefined;
    const languageInfo = metadata["language_info"] as
      | Record<string, unknown>
      | undefined;

    const kernelspecLanguage = String(kernelspec?.["language"] ?? "").toLowerCase();
    const languageInfoName = String(languageInfo?.["name"] ?? "").toLowerCase();

    if (kernelspecLanguage === "python" || languageInfoName === "python") {
      return true;
    }

    return notebook
      .getCells()
      .some(
        (cell) =>
          cell.kind === vscode.NotebookCellKind.Code && cell.document.languageId === "python",
      );
  }

  public async installInActiveNotebookKernel(): Promise<void> {
    const editor = vscode.window.activeNotebookEditor;
    if (!editor) {
      void vscode.window.showInformationMessage("Open a notebook to install itables.");
      return;
    }

    await this.installItablesInNotebook(editor.notebook);
  }

  private async executeSnippetInNotebook(
    notebook: vscode.NotebookDocument,
  ): Promise<number> {
    const config = vscode.workspace.getConfiguration("itablesForVscode");
    const configuredSnippet = config.get<string>("initSnippet", DEFAULT_INIT_SNIPPET);
    const snippet = configuredSnippet.includes(INIT_CELL_MARKER)
      ? configuredSnippet
      : `${INIT_CELL_MARKER}\n${configuredSnippet}`;

    let initCellIndex = this.findInitCellIndex(notebook);

    if (initCellIndex === undefined) {
      const insertEdit = new vscode.WorkspaceEdit();
      const initCell = new vscode.NotebookCellData(
        vscode.NotebookCellKind.Code,
        snippet,
        "python",
      );
      initCell.metadata = {
        jupyter: {
          source_hidden: true,
          outputs_hidden: true,
        },
        itablesForVscode: {
          isInitCell: true,
        },
      };

      insertEdit.set(notebook.uri, [vscode.NotebookEdit.insertCells(0, [initCell])]);
      await vscode.workspace.applyEdit(insertEdit);
      initCellIndex = 0;
    }

    const initCell = notebook.cellAt(initCellIndex);
    if (initCell.document.getText() !== snippet) {
      const snippetRange = new vscode.Range(
        initCell.document.positionAt(0),
        initCell.document.positionAt(initCell.document.getText().length),
      );
      const updateEdit = new vscode.WorkspaceEdit();
      updateEdit.replace(initCell.document.uri, snippetRange, snippet);
      await vscode.workspace.applyEdit(updateEdit);
    }

    await vscode.commands.executeCommand("notebook.cell.execute", {
      document: notebook.uri,
      ranges: [{ start: initCellIndex, end: initCellIndex + 1 }],
    });

    return initCellIndex;
  }

  private getInitState(
    notebook: vscode.NotebookDocument,
    initCellIndex: number,
  ): "ready" | "missing" | "unknown" {
    if (initCellIndex < 0 || initCellIndex >= notebook.cellCount) {
      return "unknown";
    }

    const cell = notebook.cellAt(initCellIndex);
    const outputText = this.collectCellOutputText(cell);
    if (outputText.includes(MISSING_MARKER)) {
      return "missing";
    }
    if (outputText.includes(READY_MARKER)) {
      return "ready";
    }

    return "unknown";
  }

  private collectCellOutputText(cell: vscode.NotebookCell): string {
    const parts: string[] = [];
    for (const output of cell.outputs) {
      for (const item of output.items) {
        parts.push(Buffer.from(item.data).toString("utf8"));
      }
    }
    return parts.join("\n");
  }

  private async promptInstallItables(notebook: vscode.NotebookDocument): Promise<void> {
    const installLabel = "Install In Active Kernel";
    const docsLabel = "Open ITables Docs";
    const suppressLabel = "Don't Ask Again";
    const choice = await vscode.window.showWarningMessage(
      "itables is not installed in the active notebook kernel. Install itables to enable interactive DataFrame rendering.",
      installLabel,
      docsLabel,
      suppressLabel,
    );

    const notebookKey = notebook.uri.toString();
    if (choice === installLabel) {
      await this.installItablesInNotebook(notebook);
      return;
    }

    if (choice === docsLabel) {
      await vscode.env.openExternal(vscode.Uri.parse(ITABLES_DOCS_URL));
      return;
    }

    if (choice === suppressLabel) {
      this.suppressedNotebookKeys.add(notebookKey);
    }
  }

  private async installItablesInNotebook(
    notebook: vscode.NotebookDocument,
  ): Promise<void> {
    const notebookKey = notebook.uri.toString();
    try {
      await this.runTemporarySnippet(notebook, INSTALL_ITABLES_SNIPPET);
      this.missingNotebookKeys.delete(notebookKey);
      this.suppressedNotebookKeys.delete(notebookKey);
      this.initializedNotebookKeys.delete(notebookKey);

      const initCellIndex = await this.executeSnippetInNotebook(notebook);
      const state = this.getInitState(notebook, initCellIndex);
      if (state === "ready") {
        this.initializedNotebookKeys.add(notebookKey);
        void vscode.window.showInformationMessage(
          "Installed itables in the active kernel and initialized notebook mode.",
        );
      } else {
        void vscode.window.showWarningMessage(
          "itables installation finished, but initialization state is unknown. Re-run initialization if needed.",
        );
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      void vscode.window.showWarningMessage(
        `Could not install itables in the active kernel: ${message}`,
      );
    }
  }

  private async runTemporarySnippet(
    notebook: vscode.NotebookDocument,
    snippet: string,
  ): Promise<void> {
    const insertIndex = notebook.cellCount;
    const insertEdit = new vscode.WorkspaceEdit();
    const installCell = new vscode.NotebookCellData(
      vscode.NotebookCellKind.Code,
      snippet,
      "python",
    );
    insertEdit.set(notebook.uri, [
      vscode.NotebookEdit.insertCells(insertIndex, [installCell]),
    ]);
    await vscode.workspace.applyEdit(insertEdit);

    try {
      await vscode.commands.executeCommand("notebook.cell.execute", {
        document: notebook.uri,
        ranges: [{ start: insertIndex, end: insertIndex + 1 }],
      });
    } finally {
      if (insertIndex < notebook.cellCount) {
        const deleteEdit = new vscode.WorkspaceEdit();
        deleteEdit.set(notebook.uri, [
          vscode.NotebookEdit.deleteCells(new vscode.NotebookRange(insertIndex, insertIndex + 1)),
        ]);
        await vscode.workspace.applyEdit(deleteEdit);
      }
    }
  }

  private findInitCellIndex(notebook: vscode.NotebookDocument): number | undefined {
    for (let index = 0; index < notebook.cellCount; index += 1) {
      const cell = notebook.cellAt(index);
      if (
        cell.kind !== vscode.NotebookCellKind.Code ||
        cell.document.languageId !== "python"
      ) {
        continue;
      }

      const cellMetadata = cell.metadata as Record<string, unknown>;
      const extensionMetadata = cellMetadata["itablesForVscode"] as
        | Record<string, unknown>
        | undefined;

      if (extensionMetadata?.["isInitCell"] === true) {
        return index;
      }

      if (cell.document.getText().includes(INIT_CELL_MARKER)) {
        return index;
      }
    }

    return undefined;
  }
}

export function activate(context: vscode.ExtensionContext): void {
  const initializer = new ItablesNotebookInitializer();

  context.subscriptions.push(
    vscode.workspace.onDidOpenNotebookDocument((notebook) => {
      void initializer.maybeInitialize(notebook);
    }),
  );

  context.subscriptions.push(
    vscode.window.onDidChangeActiveNotebookEditor((editor) => {
      if (!editor) {
        return;
      }
      void initializer.maybeInitialize(editor.notebook);
    }),
  );

  context.subscriptions.push(
    vscode.workspace.onDidChangeConfiguration((event) => {
      if (event.affectsConfiguration("itablesForVscode")) {
        initializer.resetSessionState();
      }
    }),
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      "itablesForVscode.enableForActiveNotebook",
      async () => initializer.forceInitializeActiveNotebook(),
    ),
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      "itablesForVscode.installInActiveKernel",
      async () => initializer.installInActiveNotebookKernel(),
    ),
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("itablesForVscode.resetSessionState", () => {
      initializer.resetSessionState();
      void vscode.window.showInformationMessage("ITables auto-init session state reset.");
    }),
  );

  for (const notebook of vscode.workspace.notebookDocuments) {
    void initializer.maybeInitialize(notebook);
  }
}

export function deactivate(): void {
  // No resources to clean up.
}
