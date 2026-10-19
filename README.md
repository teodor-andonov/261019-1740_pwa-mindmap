# Mindmap V2

**The canvas is the application.** A local-first PWA for independent mind maps stored together in one portable file.

## Run
Published app: https://teodor-andonov.github.io/261019-1740_pwa-mindmap/

Or locally, run `python -m http.server 8080` from the repository root. No npm, build step, backend or account.

## Architecture
- A `.mindmap` file is plain JSON (`version: 2`), holding multiple **independent diagrams**. Duplicate creates entirely separate nodes, edges and positions; changes do not propagate between diagrams.
- Each diagram owns its shelf, nodes, undirected links, routes, viewport, pins and physics. Shelf hides nodes without deleting them or their connections.
- The document stores **three default node styles and three default link styles**; each node or link references a preset via `styleId`. Presets define appearance only, never connection semantics. Changing a preset affects all its objects in the current file. The JSON schema also supports local overrides, and the UI can reset them.
- Opening an old V1 `.json` converts each of its former shared-graph views into a **separate independent V2 diagram**. Then save the result as `.mindmap`.
- Versioned service worker caches only the static app shell, not your document.

## Canvas controls
| Action | How |
|---|---|
| New node | Bottom +, N, or double-click empty canvas |
| Edit / move | Double-click node / drag it |
| Multi-select | Shift-click |
| Connect | Drag a node's port to another node |
| Connected node | Drag a port to empty canvas |
| Link bends | Hover/select line, drag segment midpoint; drag bend to reposition |
| Shelf / restore | Select nodes → archive; open shelf and click/drag saved nodes |
| Shelf all | Shelf drawer archive button |
| Diagram management | Left preview rail: +, three-dot menu, double-click to rename |
| Physics | Right separate Relax/Freeze control (Space), settings via slider icon |
| Pin | Select node → pin or P |
| Pan / zoom / fit | Drag empty background, wheel, fit or F |
| Undo / redo | Ctrl+Z / Ctrl+Shift+Z or Ctrl+Y |
| Save / Save As / Open | Ctrl+S / Ctrl+Shift+S / Ctrl+O |

Top-left floating file controls show the document name, but deliberately no redundant app branding. The sidebar, shelf and property/simulation panels can be collapsed, and most tools are icon-first with tooltips.

## File association
The PWA manifest declares `.mindmap` and `.json` file handlers on supporting desktop Chromium installs. Registration depends on OS/browser support and user permissions. If file associations or direct file access aren't available, the app still opens local files and downloads portable `.mindmap` files. Saving is explicit (amber dot shows unsaved edits).

## Files
- `index.html` — complete dependency-free app and renderer
- `manifest.webmanifest` — installation and file handlers
- `sw.js` — offline app-shell cache
- `AGENT_BRIEF.md` — design intent, architecture and decisions
- `ROADMAP.md` — next milestones and quality work

GitHub Pages deploys directly from `main` / `/(root)`; no custom Actions.

## Known limits
This is a foundation release. Touch/pinch gestures, per-object style override editing, arbitrary preset creation, conflict-safe autosaving and large-graph physics need further work. No images, rich text, collaboration or cloud sync yet.
