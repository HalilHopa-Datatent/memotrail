import * as vscode from 'vscode';
import { execFile } from 'child_process';
import { promisify } from 'util';

const execFileAsync = promisify(execFile);

// ── Helpers ──────────────────────────────────────────────────────

function getMemotrailPath(): string {
    return vscode.workspace.getConfiguration('memotrail').get('pythonPath', 'memotrail');
}

function getSearchLimit(): number {
    return vscode.workspace.getConfiguration('memotrail').get('searchLimit', 10);
}

async function runMemotrail(args: string[]): Promise<string> {
    const cmd = getMemotrailPath();
    try {
        const { stdout } = await execFileAsync(cmd, args, { timeout: 30000 });
        return stdout;
    } catch (error: any) {
        const message = error.stderr || error.message || 'Unknown error';
        throw new Error(`MemoTrail error: ${message}`);
    }
}

// ── Tree Data Providers ─────────────────────────────────────────

class SessionItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly detail: string,
        public readonly sessionId: string,
    ) {
        super(label, vscode.TreeItemCollapsibleState.None);
        this.tooltip = detail;
        this.description = detail;
        this.iconPath = new vscode.ThemeIcon('comment-discussion');
    }
}

class SessionTreeProvider implements vscode.TreeDataProvider<SessionItem> {
    private _onDidChangeTreeData = new vscode.EventEmitter<SessionItem | undefined>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;
    private sessions: SessionItem[] = [];

    refresh(): void {
        this._onDidChangeTreeData.fire(undefined);
    }

    setSessions(sessions: SessionItem[]): void {
        this.sessions = sessions;
        this.refresh();
    }

    getTreeItem(element: SessionItem): vscode.TreeItem {
        return element;
    }

    getChildren(): SessionItem[] {
        return this.sessions;
    }
}

class SearchResultItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly content: string,
        public readonly score: number,
    ) {
        super(label, vscode.TreeItemCollapsibleState.None);
        this.tooltip = content;
        this.description = `Score: ${score.toFixed(2)}`;
        this.iconPath = new vscode.ThemeIcon('search');
        this.command = {
            command: 'memotrail.showResult',
            title: 'Show Result',
            arguments: [content],
        };
    }
}

class SearchTreeProvider implements vscode.TreeDataProvider<SearchResultItem> {
    private _onDidChangeTreeData = new vscode.EventEmitter<SearchResultItem | undefined>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;
    private results: SearchResultItem[] = [];

    refresh(): void {
        this._onDidChangeTreeData.fire(undefined);
    }

    setResults(results: SearchResultItem[]): void {
        this.results = results;
        this.refresh();
    }

    getTreeItem(element: SearchResultItem): vscode.TreeItem {
        return element;
    }

    getChildren(): SearchResultItem[] {
        return this.results;
    }
}

// ── Extension Activation ────────────────────────────────────────

export function activate(context: vscode.ExtensionContext) {
    const sessionProvider = new SessionTreeProvider();
    const searchProvider = new SearchTreeProvider();

    vscode.window.registerTreeDataProvider('memotrail.sessions', sessionProvider);
    vscode.window.registerTreeDataProvider('memotrail.search', searchProvider);

    // Search conversations (semantic)
    context.subscriptions.push(
        vscode.commands.registerCommand('memotrail.search', async () => {
            const query = await vscode.window.showInputBox({
                prompt: 'Search past conversations',
                placeHolder: 'e.g., Why did we switch to Redis?',
            });
            if (!query) { return; }

            try {
                const output = await runMemotrail(['search', query, '-n', String(getSearchLimit())]);
                const items = parseSearchOutput(output);
                searchProvider.setResults(items);
                vscode.window.showInformationMessage(`Found ${items.length} result(s)`);
            } catch (err: any) {
                vscode.window.showErrorMessage(err.message);
            }
        })
    );

    // Keyword search
    context.subscriptions.push(
        vscode.commands.registerCommand('memotrail.searchKeyword', async () => {
            const query = await vscode.window.showInputBox({
                prompt: 'Keyword search (BM25)',
                placeHolder: 'e.g., TypeError NoneType',
            });
            if (!query) { return; }

            try {
                const output = await runMemotrail(['search', query, '-n', String(getSearchLimit())]);
                const items = parseSearchOutput(output);
                searchProvider.setResults(items);
                vscode.window.showInformationMessage(`Found ${items.length} result(s)`);
            } catch (err: any) {
                vscode.window.showErrorMessage(err.message);
            }
        })
    );

    // Recent sessions
    context.subscriptions.push(
        vscode.commands.registerCommand('memotrail.recentSessions', async () => {
            try {
                const output = await runMemotrail(['stats']);
                const doc = await vscode.workspace.openTextDocument({
                    content: output,
                    language: 'text',
                });
                await vscode.window.showTextDocument(doc);
            } catch (err: any) {
                vscode.window.showErrorMessage(err.message);
            }
        })
    );

    // Stats
    context.subscriptions.push(
        vscode.commands.registerCommand('memotrail.stats', async () => {
            try {
                const output = await runMemotrail(['stats']);
                vscode.window.showInformationMessage(output.trim());
            } catch (err: any) {
                vscode.window.showErrorMessage(err.message);
            }
        })
    );

    // Index now
    context.subscriptions.push(
        vscode.commands.registerCommand('memotrail.indexNow', async () => {
            try {
                vscode.window.showInformationMessage('MemoTrail: Indexing sessions...');
                const output = await runMemotrail(['index']);
                vscode.window.showInformationMessage(`MemoTrail: ${output.trim().split('\n').pop()}`);
            } catch (err: any) {
                vscode.window.showErrorMessage(err.message);
            }
        })
    );

    // Show result content
    context.subscriptions.push(
        vscode.commands.registerCommand('memotrail.showResult', async (content: string) => {
            const doc = await vscode.workspace.openTextDocument({
                content: content,
                language: 'markdown',
            });
            await vscode.window.showTextDocument(doc, { preview: true });
        })
    );

    // Load recent sessions on startup
    loadRecentSessions(sessionProvider);
}

async function loadRecentSessions(provider: SessionTreeProvider): Promise<void> {
    try {
        const output = await runMemotrail(['stats']);
        const lines = output.trim().split('\n');
        const items: SessionItem[] = [];

        for (const line of lines) {
            if (line.includes(':')) {
                const [key, value] = line.split(':').map(s => s.trim());
                if (key && value) {
                    items.push(new SessionItem(key, value, ''));
                }
            }
        }

        provider.setSessions(items);
    } catch {
        // MemoTrail not installed or not configured — silently skip
    }
}

function parseSearchOutput(output: string): SearchResultItem[] {
    const results: SearchResultItem[] = [];
    const blocks = output.split('--- Result ');

    for (let i = 1; i < blocks.length; i++) {
        const block = blocks[i];
        const scoreMatch = block.match(/score: ([\d.]+)/);
        const sessionMatch = block.match(/Session: (\S+)/);
        const projectMatch = block.match(/Project: (\S+)/);
        const contentMatch = block.match(/Content:\n([\s\S]*?)(?=\n---|\n*$)/);

        const score = scoreMatch ? parseFloat(scoreMatch[1]) : 0;
        const session = sessionMatch ? sessionMatch[1] : 'unknown';
        const project = projectMatch ? projectMatch[1] : 'unknown';
        const content = contentMatch ? contentMatch[1].trim() : block.trim();

        results.push(new SearchResultItem(
            `${project} (${session})`,
            content,
            score,
        ));
    }

    return results;
}

export function deactivate() {}
