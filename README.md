# Mindmap V2.6

**The canvas is the application.** An offline-capable, local-first PWA for independent diagrams in one portable `.mindmap` file. Static HTML/SVG/JS; no external dependencies or build step.

## Start

Run `python -m http.server 8080` from the project folder and visit `http://localhost:8080`, or use [the published app](https://teodor-andonov.github.io/261019-1740_pwa-mindmap/). The installed PWA works offline after the shell is cached. User diagrams are never uploaded to GitHub Pages.

## Controls

| Action | Gesture / control |
|---|---|
| Select node or link | Left-click; Shift-click to add/remove nodes |
| Box select | Left-drag any empty canvas space; Shift-drag to add to selection |
| Move one or multiple nodes | Drag a selected node |
| Pan canvas | Right-drag anywhere; two-finger drag on touch devices |
| Zoom | Wheel, two-finger pinch, zoom controls |
| Edit text | Double-click node, then type **directly inside its shape**; Ctrl/Cmd+Enter commits, Escape cancels |
| Create a node | Bottom +, `N`, or double-click blank space |
| Connect nodes | Drag the small connector at the centre of the selected node's lower edge; drop on another node or empty canvas |
| Curve a link | Click the link, then drag its midpoint; edit any existing bend |
| Remove an authored bend | Right-click bend point (stationary), middle-click bend point, or Undo |
| Delete node or link | Middle-click directly on it, or select and press Delete/Backspace; Undo restores it |
| Style selection | Select object(s), choose one of the appearance swatches in the **floating selection toolbar** |
| Shelf or pin | Select node(s), then use the contextual shelf / pin icons, or Shift+S / P |
| Edit styles | Expand **Styles** top-right; switch Box/Link; choose style; expand Edit style for limited controls |
| New style | Styles → Add; presets live **within the current diagram** |
| Focus | Bottom focus button or `H`; `Escape` restores controls |
| Relax/freeze | Top-right simulation button or `Space`; separate simulation settings |
| Undo / redo | Ctrl/Cmd+Z, Ctrl/Cmd+Shift+Z |
| Save / Save As | Top-left disk controls, Ctrl/Cmd+S / Ctrl/Cmd+Shift+S |
| Open document | Top-left folder, Ctrl/Cmd+O, or drag `.mindmap` / `.json` onto the app |

**Touch:** long-press a node to extend selection; pinch with two fingers to pan and zoom. Panning on touch remains two-finger to leave one-finger gestures for object operations and selection.

## File model — v3

One document holds independently editable diagrams. **Each diagram owns its node and link styles** plus its *last-used box style* and *last-used link style*. Duplicating a diagram duplicates everything. Changes to a preset affect only objects in that diagram, not other diagrams in the same file.

```json
{
  "version": 3,
  "title": "My research",
  "maps": [{
    "id": "m_1", "name": "Idea study",
    "styles": {
      "nodes": [{ "id": "node-a", "name": "Rounded", "shape": "rounded", "fill": "#ffffff00", "stroke": "#000000", "strokeWidth": 2, "textColor": "#000000", "fontSize": 15, "fontWeight": 600, "radius": 16 }],
      "links": [{ "id": "link-a", "name": "Regular", "stroke": "#000000", "strokeWidth": 2, "dash": "" }]
    },
    "defaultNodeStyleId": "node-a", "defaultLinkStyleId": "link-a",
    "nodes": [{ "id": "n_1", "text": "Idea", "x": 0, "y": 0, "styleId": "node-a", "pinned": false, "shelved": false }],
    "edges": [], "mode": "static", "physics": { "length": 165, "repulsion": 2400, "gap": 22 },
    "viewport": { "x": 300, "y": 200, "zoom": 1 }
  }]
}
```

New objects inherit the active default style for their kind. Selecting another style for an object also sets the default for subsequently created objects *in that diagram*. New documents start with three monochrome box presets and three monochrome link presets; colours accept 8-digit `#RRGGBBAA` alpha.

The app supports both legacy v1 shared-graph JSON files (each view becomes an independent map) and v2 files with document-wide styles (each map gets its own cloned styles on import). On the next save the format becomes v3. **Keep a backup of important v1/v2 documents before saving a migrated version.**

## Autosave, recovery and file association

- If you opened or saved a file through Chromium's File System Access picker, **autosave writes back to that linked file after a brief idle delay**, but only when the browser has already granted write access. It does not pop up a permission dialog automatically.
- Regardless of a file link, the app tries to maintain a local IndexedDB **recovery draft**. On reopening after an unsaved session, it offers to restore it. Browser storage can be cleared by private mode, device cleanup or site-data resets; it is **not** a substitute for a saved `.mindmap` file.
- When direct file access is unsupported or permission is missing, use Save to download a local copy. The orange unsaved indicator remains until a real file save/download succeeds.
- GitHub Pages stores **application code only**, not personal diagrams. The service worker caches the app shell, not document files.
- The installed Windows PWA declares a `.mindmap` file handler, subject to browser/OS support and permission. Ordinary Open still works on unsupported platforms.

## Source

`index.html` is the single application source; `sw.js` is the service worker; `manifest.webmanifest` registers the app/file handler; PNG files are PWA icons. `ROADMAP.md` and `AGENT_BRIEF.md` document product decisions and future changes.

## Known limitations

Real-device Windows/Android behavior, autosave durability and PWA file association need testing outside headless Chromium. The current renderer recreates SVG elements while dragging, and is designed for small/medium maps, not thousands of nodes. Middle-click deletion is reversible but should be used deliberately; trackpad/touch users can use Delete/Backspace instead.


## V2.5 — Monochrome UI and one-sidebar layout
- All application chrome is achromatic; custom diagram style colours remain editable and persist in source JSON.
- Dark mode inverts the entire rendered interface with a single root filter; this deliberately inverts any non-grayscale diagram colours too. No saved document colour values are changed.
- A single collapsible left rail contains four tabs: Diagrams, Styles, Simulation and Shelf. The top file commands and small bottom editing toolbar remain; redundant right panels and floating shelf are retired.
- Four offset connector handles (top, right, bottom, left) have larger visible circles and generous transparent hit regions. Link previews originate at the chosen handle.
- The v3 `.mindmap` schema is unchanged; all older files continue to load.
- Focus mode hides the rail and topbar as before. Test on actual touch hardware and check Chromium PWA file association separately.


## V2.6 — Reliability & keyboard quality
- Saving to a linked file is now serialized: manual Save and autosave cannot interleave writes.
- On supporting file handles, an external modification to a linked file blocks overwrites and prompts Save As.
- Recovery drafts are snapshot-based and ordered, preventing a delayed save from overwriting a newer recovery state.
- Opening/resetting documents invalidates old queued writes; saving during further edits does not incorrectly clear the unsaved indicator.
- Double-click a link to insert an editable spline bend at the closest point. Arrow keys nudge selected nodes 1 canvas unit; Shift+arrow uses 10 units. Consecutive repeats form one Undo step. Enter edits a selected box in place. Ctrl/Cmd+D duplicates the selected nodes and their internal links as an offset group (one Undo step).
- File schema stays at version 3. The IndexedDB recovery draft is **not** a substitute for a saved `.mindmap` file.


## Repeatable browser checks

Install development dependencies with `pip install -r requirements-dev.txt`, then run `pytest -q tests/test_browser.py`. The tests run headless Chromium (use `CHROMIUM_PATH` if required, or install Playwright Chromium with `python -m playwright install chromium`). They exercise editing and duplication, keyboard nudge/Undo, linked-file serial saves, external-file conflict protection, and Save As.

The suite injects the HTML document into a browser page so it also runs in restricted CI environments. **It does not validate** service worker installation, genuine OS file associations, or persistence across real-origin browser restarts; these still need a real-device/manual pass.
## V2.7 — Theme skins and gesture refinement

Theme is now a fifth sidebar tab. It is a presentation skin for the active independent diagram, separate from object Styles, and uses the optional version-3 field `maps[].theme`: `{ "character":"precise", "typeface":"sans", "background":"dots" }`.

Choose Precise, Loose or Hand-drawn linework; Sans, Mono or Handwriting typeface; and Plain, Dots, Grid or Paper background. Organic strokes are deterministic per object ID; saved geometry and curve bend points are never modified. Handwriting uses installed-device font fallbacks rather than a bundled font.

The Theme panel exports clean SVG/PNG of the active diagram using its current appearance (without ports, handles or interface). PNG is rendered entirely locally, at up to 2× pixel scale. Different machines may render system fonts differently.

During drag, node-centre alignment snaps to other visible nodes at roughly a 9-screen-pixel threshold with dashed guides; hold Alt to bypass. Drag a selected node or group onto the Shelf tab to put it away with one-step Undo.

Older V1/V2/V3 files continue to open; missing theme values get Precise/Sans/Dots. On-disk version remains **3**. Test with `pytest -q tests/test_browser.py tests/test_theme.py`. OS-level association and physical touch-device checks remain manual QA tasks.


## V2.8 — Responsive canvas, cleaner styles and themes

- No magnetic alignment or guides. Node dragging follows the pointer exactly; connection targeting remains available.
- Default nodes: Underline, Rounded rectangle and Circle, with fine outlines and transparent white fill. Rectangles use radius for rounding; Equal X/Y produces squares or circles. Old document presets remain unchanged.
- Default links: solid, dashed and genuinely dotted fine strokes, all 50% black (#00000080).
- Theme: Precise, Loose and Hand-drawn affect node outlines AND links, with deterministic, smooth curves. Handwriting affects node text, editor and export. Each diagram has editable background colour, also used on export.
- Performance: panning and zooming change the SVG camera without recreating nodes. Dragging and simulation update existing SVG shapes on animation frames. Physics dimensions are cached per tick.
- File schema remains version 3. Browsers need local handwriting fonts or use cursive fallback. Real Windows/Android tests and large-graph profiling remain outstanding.
