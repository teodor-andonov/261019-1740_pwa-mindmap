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
