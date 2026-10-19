# Mindmap V2 — Agent context and product intent

## Motivation
Build a small, enjoyable, spatial thinking tool: create textual ideas on an infinite canvas, link them, move them manually, optionally relax their positions with graph physics, and experiment freely. It must not become a complicated whiteboard. Prioritize direct manipulation, simplicity, smooth transitions, hit targets, predictable file handling and readable local source.

The canvas is the **actual interface**. Other UI surfaces should float above it, be context-sensitive and collapse away. Avoid explanatory prose on screen. Use tooltips rather than text labels where practical. Do not duplicate the app icon/title inside a PWA's toolbar.

## Settled decisions (October 2026)
1. **Independent diagrams, not views:** each tab/map owns unrelated nodes, links, layout and shelf. Duplicating creates deep copies. A file is only a collection of diagrams.
2. **Shelf:** hides existing nodes without deleting their data. Their links remain recorded but are drawn only when both endpoints are visible; restore later by click/drag. A shelf is diagram-local.
3. **No semantic types:** exactly three default node *style* presets and three default link *style* presets; any property—shape, fill, outline, thickness, font size, text colour, dash etc—belongs to the style. Preset identity maps to appearance, not meaning. Simulation parameters are separate.
4. **Floating chrome:** top-left general/file controls, collapsible left thumbnails, contextual properties top-right, separate simulation below/right, central bottom tools and small zoom cluster.
5. **Local files:** human-readable versioned JSON in `.mindmap` extension; best-effort PWA file association on desktop, manual import/download fallback everywhere.
6. **Scope:** only text nodes and undirected plain links until the core editor is truly polished. No agents, images, sketches, notes, rich semantics or excessive feature bloat now.

## Data schema v2
```text
Document { version: 2, title, styles: {nodes: [...], links: [...]}, maps: [...] }
Map { id, name, mode, viewport, physics, nodes: [...], edges: [...] }
Node { id, text, x, y, pinned, shelved, styleId, overrides? }
Edge { id, from, to, styleId, bends: [{x,y}], overrides? }
```
Presets are document-level: changing a style updates all referencing objects across diagrams **in the same document**. Objects are not shared between maps. Runtime hover, selection, file handles, velocities and undo stacks never belong in saved JSON.

V1 compatibility: each former view of a shared graph is converted into an independent V2 map with the same view positions and bends. Original node shape/colour are preserved as overrides; former link strengths are approximated with the three appearance presets. It is a deliberate migration, not silently shared data.

## Interaction contract
- Drag node to move; Shift-click to multi-select; drag connector port to another node or blank canvas to connect/create.
- Hover an edge for midpoint handles; drag to insert bends. Existing bends remain editable.
- Shelf selection/shelf all, undo/redo, drag/drop return from shelf, freeze/relax and pinning.
- Node/edge preset properties are editable in a separate contextual panel; simulation toggle/settings never intrude into selected-object properties.
- Preserve smoothness, keyboard controls, desktop and touch adaptability, reduced-motion support. No need for forced parenting, arrows or graph hierarchy.

## Engineering priorities
Keep a dependency-free static GitHub Pages PWA if possible. Test map isolation, shelf/restore and retained links, presets propagation, edge routing, undo/redo, file round-trips, V1 migration and offline install lifecycle. Use versioned app-shell cache. Save As must not overwrite the previous file. File association support differs by OS/browser, so never rely on it as the only entry point.

See `ROADMAP.md` for iterative work. The emphasis for V2.x is **craft, not complexity**.

## Motion & feedback (V2.1)

Motion must clarify placement and state instead of decorating the canvas. Fit and toolbar zoom may ease; pointer drag, wheel zoom and physics are immediate and interruptible. New nodes/links briefly enter; selected, shelved and restored ideas provide feedback. Respect reduced-motion preferences in CSS and JavaScript. Animation never belongs in the portable JSON file. Test pointer capture after rendering changes.

## V2.2 Gesture contract

- Independent diagrams and the portable JSON v2 schema are unchanged.
- Selection is transient: Shift-click toggles, Shift-drag draws an additive marquee, a select-tool button enables rectangle selection, Ctrl/Cmd+A selects visible nodes. No selection state in the JSON file.
- Dragging a selected node moves the selected group directly under the pointer and forms one undo checkpoint; no easing/lag during drag.
- Two active touch pointers zoom/pan around their midpoint. A second touch rolls back unfinished single-pointer object drag; finger release must not accidentally add nodes or connections. Touch long-press adds a node to selection.
- Node connection handles have enlarged invisible targets; candidate node snapping highlights a valid destination. Drop on blank canvas creates a linked node; dropping over floating controls or onto the source does not.
- Use native keyboard semantics in input fields, meaningful icon labels, reduced-motion support, and browser gesture regression tests. Real devices still need manual validation.


## V2.3 decisions

Curved connections are an SVG representation of existing `bends` coordinates, using a C1-continuous interpolating spline through node boundary endpoints and user bend points; no extra Bézier handles or file migration. Hit-testing must use exactly the visible curve. Existing bend handles remain draggable; right-click one to delete it, with undo support.

Style presets are document-wide definitions referenced across independent diagrams. New files get three black/white transparent-fill node styles and three black link styles; old files retain custom colour schemes. Arbitrarily many presets are supported. On preset deletion, references in every diagram are reassigned safely. Colour editing preserves opacity when RGB changes and vice versa; use `#RRGGBBAA` for alpha. Dark mode is an app preference, separate from portable file data, and makes default black ink legible without mutating styles.


## V2.4 — authoritative decisions (supersede earlier contrary guidance)

**Styles are per diagram** now: document v3 contains only title, maps; each map carries styles, defaultNodeStyleId and defaultLinkStyleId. Duplicating a diagram clones styles and its node/link data. V2 files with document-wide styles migrate by cloning styles into every map. V1 still migrates via v2.

The canvas owns the experience: left drag blank area marquee-selects, right drag anywhere pans, Shift modifies selection, right-click on a bend deletes it. Middle-click directly deletes nodes, edges or authored bends and must always be undoable. Keep mouse gestures immediate and avoid moving the camera on left click.

Double-click edits the label *inside the shape* with typography, bounds and colours matched to that node, not a detached popup. Selecting objects reveals a small anchored toolbar with style swatches, pin, shelf and delete. Keep the right floating panel for styles only, with a compact preset editor and a separate simulation panel; remove duplicate toolbar actions. A focus toggle hides the chrome, retaining an accessible exit control.

The last-selected preset in each category becomes the active default for subsequent nodes/links in that diagram. Prefer sparse discrete type sizes, weights, strokes, rounding and opacity stops over arbitrarily fine controls.

Autosave is conditional: a previously approved File System Access handle can be written without re-prompting. Independently maintain an IndexedDB session recovery draft; it is not equivalent to saving a portable file, and the unsaved indicator must only clear after a successful disk write or explicit download. The service worker caches app assets only.

V2.4 regression scope: default marquee, right pan, bend deletion, middle click + undo, group drag, inline editing, style defaults, independent-map preset edits, V2→V3 migration, saved JSON roundtrip, mobile collapsed controls, focus, reduced motion and offline cache update.


## V2.5 interface contract

- The editor is a canvas-first application: **one unified, collapsible left sidebar** (Diagrams, Styles, Simulation, Shelf), a quiet file toolbar above, and a minimal bottom tool strip. Do not resurrect separate right properties/simulation panels.
- Every *application chrome* colour must be neutral/achromatic. Styles stored for graph objects can contain arbitrary RGBA hex colours.
- Dark mode uses **one root inversion filter**; it must not do additional per-object dark ink substitution or edit the stored JSON. Check colour controls and chrome after inversion.
- When a node is selected or hovered, show four visibly larger connector ports at top/right/bottom/left **offset outward** from the object's outline, with generous invisible hit zones. Connecting from a port should visually start at that port. Keep the selection toolbar clear of the top port.
- Interaction tests must cover mobile/touch CSS, gesture hit-testing, new-node drag, shelf restoration, simulation, dark invert, save/reopen, and v3 compatibility.
