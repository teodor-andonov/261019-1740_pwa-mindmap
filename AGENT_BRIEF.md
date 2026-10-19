# Mindmap — Product and Implementation Brief

## 01. Why this exists

The goal is **extremely simple mind mapping that can graduate from manual sketching to computational rearrangement**. The user wants to think spatially: write ideas in bubbles, freely connect them, move them by hand, introduce bends in relationships, then let a force simulation discover an alternative configuration. They can keep that as one view, duplicate it, relax it differently, and compare arrangements **without duplicating the actual knowledge**.

The important idea is not another feature-rich whiteboard. It is the separation of:

1. **What exists** (graph semantics, objects and relationships)
2. **How it is arranged** (view-specific geometry, routing, pins)
3. **How it looks** (a swappable visual theme mapping semantics to visual styling)

This separation is the product. Protect it in all future changes.

## 02. Product principles

- **File-first and portable:** exactly one self-contained JSON document per mind map, human-readable, agent-friendly.
- **Local-first:** no login, backend, data sync, vendor storage, or mandatory infrastructure.
- **Minimal-friction creation:** nodes and relationships should emerge from direct manipulation of the canvas.
- **No enforced tree:** the graph is undirected and may contain cycles, multiple centres, or disconnected islands.
- **Semantic before visual:** an edge has the meaning `strong`, `medium`, or `weak`; a theme decides the width/dashes/etc. Changing themes should never change graph semantics.
- **Same data, many arrangements:** tabs are views, not copies of the network.
- **Reversible exploration:** toggle dynamic relaxation on/off; freezing preserves the current arrangement. Duplication gives a safe branch for visual experiments.
- **Thoughtful simplicity:** avoid turning V1 into a Miro/Figma competitor.

## 03. Domain model

### Graph level

- **Node:** stable ID, plain text, shape (`circle`, `ellipse`, `rectangle`, `rounded`), colour; future extensibility for images/content types.
- **Edge:** stable ID, `source`, `target`, undirected, semantic `strength` (`strong`, `medium`, `weak`). Edges are first-class graph entities, though they depend on existing endpoint nodes.
- **Theme:** global visual preset defining semantic strength-to-line mapping and overall rendering. A theme never changes connectivity or positions.

### View level

- **View:** ID, name, mode (`static` or `dynamic`), positions of all nodes, node pin states, optional line bend points, physics settings, viewport/camera transform.
- Node geometry is stored in **view** because the same node can be in two locations in two tabs. Node colour is stored in **graph** because a red node is still red in both tabs.
- Relationship bend points live in **view**, not edge, because different views can use different routes for the same relationship.
- All views currently display all nodes. Per-view node filtering is a deliberate future extension, not part of the core schema yet.
- When a node/edge is created or deleted, the change affects the shared graph and all views. Its position in other views is seeded deterministically or relative to its source node.

### File schema

See `README.md`. The current on-disk schema version is `1` and is entirely JSON-serializable. Preserve stable IDs, explicitly version future migrations, and do not embed runtime physics velocities, selected state, hover state, file handles, or caches in saved JSON.

## 04. Interaction contract

1. **Create node:** action button or double-click empty space, immediately edit text. Drag anywhere on body to reposition.
2. **Link nodes:** drag a connector handle from one node to any other. Avoid reusing body drag for link creation (conflicts with moving nodes). Consider Shift+drag as alternative after UX evaluation.
3. **Extend graph:** drag a connector from a node to empty space to create a connected, immediately editable node.
4. **Bend edges:** on hover/selection show tiny midpoint markers on each line segment; drag a marker to insert a bend. Existing bend markers remain draggable. Repeated use adds more bends.
5. **Semantic link strength:** inspector supports strong/medium/weak. The chosen theme determines their appearance. V1 uses strength as a multiplier in physics attraction, too.
6. **Manual/dynamic:** one toggle on the active view; mode is not a different file format or a different tab type. Dynamic allows dragging and pinning; freeze returns to manual control at the exact current positions.
7. **Multiple tabs:** duplicate view (same positions/routes/settings), create new exploratory view (new starting arrangement and active dynamics), rename/delete view without deleting graph objects.
8. **Navigation:** pan blank space; wheel/pinch zoom where supported; Fit; controls must work on touch devices with pointer events.
9. **Editing:** select node/edge to edit properties; deleting nodes also deletes incident edges globally.
10. **Persistence:** explicit Open/Save of local JSON, file picker when supported and download/import fallback where unavailable. Ctrl+S and Ctrl+O shortcuts.

## 05. Dynamic layout behaviour

Force-directed relaxation using an intentionally small, understandable engine. Every tick:

- **Repulsion** pushes every pair of nodes apart. A collision/minimum gap term prevents overlap.
- **Attraction** acts along relationships, pulling related nodes toward a target link length. Strength changes their spring influence: strong > medium > weak.
- **Damping** stabilizes motion; gentle centring prevents drift.
- **Pins** suppress movement entirely for pinned nodes. Dragging a node in active mode temporarily fixes it for the duration of the drag.
- **Freeze** stops integration immediately and retains the current positions in the active view's layout.
- Dynamic simulations must never alter positions in another view.

**Important conceptual detail:** semantic strength affects physics as well as line styling, while *the visual theme* affects only line styling. That maintains the meaning/style separation.

An advanced future approach could use d3-force or a Web Worker, but do not introduce either merely for dependency sophistication unless performance or behavior justifies it.

## 06. Visual direction

- Calm, minimal interface with plenty of canvas. Toolbar + tabs + right-side contextual inspector.
- Nodes are restrained, softly coloured, with strong legibility and uncluttered lines.
- `minimal` theme: strong/medium/weak mapped to three levels of visual weight (weak dashed).
- `sketch` theme: warm paper and slightly irregular paths, without shaking geometry on re-render.
- `blueprint` theme: dark drafting board and technical relationship styling.
- Consistent use of IDs and semantic classes over hardcoded style fragments for future theme work.

## 07. V1 acceptance checklist

- [x] Create/edit/move/delete nodes
- [x] Shapes and colours
- [x] Undirected relationships, no duplicate links, no self links
- [x] Drag handle onto node or empty canvas
- [x] Repeated user-authored edge bends
- [x] Edge strength semantics and themed rendering
- [x] Tabs reference a shared graph, independent geometric arrangements
- [x] Manual ↔ dynamic with simple physics sliders and pinning
- [x] JSON import/export with browser file picker fallback
- [x] PWA manifest, icons, and offline application-shell cache
- [x] Usable small-screen responsive layout
- [ ] Live GitHub Pages deployment (requires a new repo)
- [ ] Full touch/device and offline-installed testing

## 08. Suggested next iterations (not V1 scope)

**First:** undo/redo; more refined inline editing; a reliable context menu; tests for mobile drag, pinch zoom and handling very long node labels; explicit Save As and optional conflict awareness; command palette / keyboard shortcuts.

**Next:** selectable node subsets per view; per-view hide/show and filtering; search; align/distribute; group/cluster containers; smart edge endpoints/route styles; optional edge label. Consider controlled theme token customization rather than arbitrary per-edge styling: semantic labels should remain the data source of truth.

**Later:** rich content node types (notes, sketches, image nodes); edges with custom semantics; graph algorithms, clustering, generated layouts and external agent tools. Keep semantic objects distinct from view instances to support these without migrations that break core assumptions.

## 09. Non-goals and anti-patterns

- No compulsory parents, roots, arrows, trees, or hierarchies.
- Do not duplicate nodes/edges when adding a view.
- Do not encode semantics solely as visual pixels or stroke widths.
- Do not mix absolute view coordinates into node objects.
- Do not store JS classes, handles or physics runtime state in file JSON.
- Do not require online libraries, hosted APIs or a server for the app's core interactions.
- Do not require a complex build, publish pipeline or unnecessary GitHub Actions.

## 10. Implementation status and remaining risks

A functioning dependency-free prototype is included in this package. The application is currently one `index.html` plus static PWA supporting files. In headless Chromium it was tested for node creation, connector-to-blank auto node, moving an object in one view without moving it in another, edge bend routing kept per view, pinned positions not moving under physics, changing edge strength, exporting a JSON snapshot and reopening it. Browser console exhibited no JavaScript page errors during those tests.

Current code still needs proper development tooling and regression tests if it is to grow beyond a prototype. Main architectural risks: line-routing geometry when nodes are large, physics performance on large graphs, mobile pointer/gesture design, file-writing UX, and versioned schema migrations.

The target publishing setup is a plain static GitHub Pages repository; no bundle step or CI deployment action required. Source is tracked in the GitHub repository. GitHub Pages publishing is controlled from repository Settings → Pages.