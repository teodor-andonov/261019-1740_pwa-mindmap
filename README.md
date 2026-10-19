# Mindmap V2.4

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

## V2.1 — Motion and interaction polish

- Eased Fit/toolbar zoom; dragging, wheel zoom and physics remain direct and interruptible.
- New node entrance, link tracing, magnetic connection-target glow and subtle drag-release feedback.
- Shelf/restore travel cues and more polished floating panels, menus, cards and simulation control.
- Reduced-motion preference respected in both CSS and JavaScript.
- Existing `.mindmap` schema unchanged; independent diagram and shelf behavior retained.

## V2.2 · Gesture quality

- **Select:** Shift-click nodes, or Shift+drag to draw a marquee. The bottom-toolbar rectangle-selection icon (`V`) enables touch-friendly selection; Ctrl/Cmd+A selects all visible nodes.
- **Touch:** long-press a node for additive selection; two fingers pinch to zoom and pan together. A second touch cancels an unfinished single-finger drag.
- **Move groups:** dragging any selected node moves the selection as a unit and creates one undo checkpoint. Shelf works for the whole selection.
- **Connect:** larger invisible connector hit targets and proximity snapping make it easier to connect on touchscreens; dropping in blank space creates a new connected node.
- **Testing:** desktop Chromium and CDP touch-event tests cover area selection, group move/undo, shelf/undo, link creation, long-press and pinch. Actual Windows/Android device tests remain desirable.

The on-disk document schema remains version 2; existing `.mindmap` files are compatible.


## V2.3 — Smooth links, presets and dark mode

- **Smooth links:** the existing saved polyline bend points now render as smooth, continuous cubic splines passing through every point. Select or hover a link to expose midpoint and bend handles. Drag a midpoint to add a bend; **right-click an authored bend to remove it**, and Ctrl/Cmd+Z to undo. No schema migration.
- **Presets:** a new document starts with three monochrome node styles (black outlines/text and fully transparent fills) and three black link styles. Select a node or link and use **New** in Properties to create a preset. Presets can be renamed, edited, duplicated and deleted. Deleting a preset reassigns affected objects in all diagrams to the first remaining style. Existing documents keep their saved palettes.
- **Opacity:** independently adjust fill, outline, text and link colour via colour picker and opacity slider (0–100%). Six-digit hex is opaque; eight-digit `#RRGGBBAA` stores transparency. The existing `.mindmap` version 2 schema supports both.
- **Dark mode:** the moon/sun button in the top toolbar switches both floating UI and canvas; saved as a browser-only preference. Default black ink is rendered light on dark canvas without modifying its JSON style values. Custom non-black colours remain unchanged.

No additional content types, dependencies, server or build tools. The core file/gesture flows remain unchanged.


## V2.4 interaction contract and file model

- **Left-drag empty space:** box selection; Shift-drag adds to current selection. **Right-drag anywhere:** pan. **Right-click an existing bend:** remove it.
- **Middle-click:** remove a node, link or authored bend under the pointer; Ctrl/Cmd+Z undoes deletion. Keyboard Delete/Backspace remains supported for touch/trackpads.
- Double-click to type directly within a box. Selected objects show a small floating toolbar for styles, pin, shelf and delete instead of permanent selection actions in the bottom bar.
- A newly created node or link inherits the last selected **box or link style** for the active diagram. Presets, overrides and defaults are per diagram; duplicating a diagram deep-copies them. The styles panel has compact discrete choices; the simulation panel is separate.
- **Focus mode (H)** hides all other floating controls while retaining its exit button; Escape also restores the interface.
- **Autosave:** linked files are automatically written after a short idle period only if the browser has already granted write permission. All documents also attempt IndexedDB recovery snapshots, but **browser recovery is not a disk file**. Use Save/Save As to export when direct access is unavailable.
- **File format:** `.mindmap` is now schema v3 (`maps[].styles`, `maps[].defaultNodeStyleId`, `maps[].defaultLinkStyleId`), with automatic migration from V1/V2 files. Back up important old files before saving migrated documents.
- Installable PWA, same URL and static GitHub Pages workflow. No account or backend is introduced.
