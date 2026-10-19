# Mindmap

**One graph, many maps.** A lightweight, offline-capable, local-first mind mapping PWA.

Mindmap deliberately uses a simple data model: **nodes**, **undirected relationships**, and **views**. Each view can place the same graph differently, switch between manual and force-relaxed positioning, and freeze an interesting arrangement.

## Start

No installation, npm, build tool, or third-party dependencies required.

1. Unzip the project.
2. Run a local server from the project directory:
   ```bash
   python -m http.server 8080
   ```
3. Open `http://localhost:8080/` in Chrome or Edge.
4. Use **Save** to create your local JSON file. On supported browsers the app can continue writing to that file during the current session, each time you click Save.

You can open `index.html` directly for quick experiments, but PWA installation and direct file access require HTTPS or localhost. For browsers without the direct file picker, opening and saving uses file input and JSON downloads.

## Main gestures

| Action | Interaction |
|---|---|
| Add node | `+ Node` or double-click empty canvas |
| Edit text | Double-click node or edit in properties panel |
| Move node | Drag node |
| Create a relationship | Drag small circular connector on a selected / hovered node onto another node |
| Create a linked node | Drag connector into empty space, then type |
| Select/edit relationship | Click line, set semantic strength in properties panel |
| Bend line | Hover or select line, drag small midpoint handle; repeat for additional bends |
| Adjust bend | Drag solid bend handle |
| Pan | Drag empty canvas |
| Zoom | Mouse wheel, `+/-` controls, Fit |
| Arrange dynamically | **Relax**; adjust spring, repulsion, gap in properties panel |
| Freeze | **Freeze** (maintains current positions) |
| Anchor node | Select node → Pin node |
| Duplicate view | `⧉` next to view tabs |
| Experimental view | `+` next to view tabs, which starts an altered live layout |
| Delete | Select node or edge → `Delete` key |
| Save | `Ctrl+S` or Save button |
| Open | `Ctrl+O`, Open button, or drag/drop JSON file |

## Data ownership

- One portable `.json` file is the source of truth for one map.
- The app does **not** use a backend, account, cloud sync, or proprietary file format.
- No persistent user content is stored in browser storage. Unsaved changes are held in memory only.
- Saving is explicit, not automatic. Close the file only after saving it.
- The PWA service worker only caches **application code and icon files** so the interface can load offline, never your project JSON.

## Architecture

- `index.html`: all UI, styling, graph editing, SVG rendering and force simulation in one file
- `sw.js`: offline application-shell service worker
- `manifest.webmanifest`: PWA manifest
- `icon-192.png`, `icon-512.png`: installable app icons
- `AGENT_BRIEF.md`: product rationale, data contract, future iterations

## JSON schema

```json
{
  "version": 1,
  "id": "map_...",
  "title": "My map",
  "theme": "minimal",
  "nodes": [
    { "id": "n_a", "text": "Idea A", "shape": "rounded", "color": "#4055bf" },
    { "id": "n_b", "text": "Idea B", "shape": "ellipse", "color": "#1c9e89" }
  ],
  "edges": [
    { "id": "e_ab", "source": "n_a", "target": "n_b", "strength": "medium" }
  ],
  "views": [
    {
      "id": "v_1", "name": "My first view", "mode": "static",
      "positions": {
        "n_a": { "x": -100, "y": 0, "pinned": false },
        "n_b": { "x": 100, "y": 0, "pinned": true }
      },
      "routes": { "e_ab": [{ "x": 0, "y": -40 }] },
      "physics": { "length": 165, "repulsion": 2400, "gap": 20 },
      "viewport": { "x": 400, "y": 250, "zoom": 1 }
    }
  ]
}
```

Node styling and relationship strength are **global graph data**; node positions, pins and route bends are **per view**. Themes are global. If a new node is created in one view, it is also made available in all the others.

The file is plain JSON and human/agent-editable. IDs must be unique. Links with missing endpoints are ignored on load. Dynamic views reopen frozen at their saved positions, to avoid unexpected movement on file opening.

## Publish to GitHub Pages

1. Create a **public** repository, e.g. `mindmap-pwa`.
2. Add `index.html`, `sw.js`, `manifest.webmanifest`, both icon files, `README.md`, and `AGENT_BRIEF.md` to the repository root.
3. In repository **Settings → Pages**, select **Deploy from a branch**, `main`, `/(root)` and Save.
4. Visit the URL GitHub Pages provides. The PWA can be installed on compatible browsers. The web host stores only application code; your JSON maps stay on your own device.

GitHub Pages' HTTPS and project sub-path work with the relative asset paths in this package. The repository is already created; configure GitHub Pages in **Settings → Pages** to make the site live.

## Limitations of this prototype

- The in-house physics engine is designed for small/medium diagrams, not thousands of nodes.
- Layout is 2D, with undirected edges only. Edge strength influences spring length, but there are no arrowheads or hierarchy.
- Each view shows the full graph (no per-view filters/hidden nodes yet).
- Manual route points are absolute 2D coordinates per view. No obstacle-avoiding smart edge routing.
- No undo/redo, multi-select, rich text, labels on edges, group containers, attachments, collaboration, or image nodes yet.
- No autosave. Use Save often.
- The app is built and interaction-tested in headless Chromium; installation via GitHub Pages and offline lifecycle are not yet live-deployment tested.

## Testing

JavaScript syntax checks, browser rendering, creating nodes and links, editing text, switching views, pinning, physics freezing, bending edges, and exporting / reopening JSON were exercised in headless Chromium. A full accessibility, touch/mobile, and offline-network test pass remains appropriate before treating this as production software.