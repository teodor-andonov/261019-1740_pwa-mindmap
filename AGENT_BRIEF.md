## V2.9 — Current authoritative architecture

The file has one **document-wide Theme**, regardless of the number of independent maps (schema v4). Each diagram keeps independent content and style presets. Text and outline share the same Ink stroke, with independent Fill. Hand-drawn visibly alters node and link geometry with smooth, stable curves and a faint secondary stroke, plus deterministic per-letter variation. Old per-diagram theme and separate text-colour descriptions below refer to earlier versions. The migration from legacy per-map themes chooses the first map's theme.

# Mindmap V2 — Agent context and product intent

## Why

Build a delightfully light, spatial thinking tool that does *one thing well*: put ideas on an infinite canvas, connect them, rearrange them by hand or physics, and try alternative configurations without the overhead of a general whiteboard.

The user wants to sketch an idea without managing a workspace. The canvas is the application; chrome and commands float above it and should hide/collapse whenever possible. Prioritize direct manipulation, discoverability, speed and smooth transitions over feature abundance. Do not fill the screen with explanatory copy or duplicate native PWA/window branding.

## Explicit product decisions (October 2026)

1. **Independent diagrams**, not graph views: each tab contains its own unrelated network. Duplicating a tab copies all nodes, links, positions and shelf states into independent data. The file is simply a collection of diagrams.
2. **Shelf per diagram:** remove nodes from the visible canvas without deleting their records or links. Restore them later by click or drag. An edge is only drawn when both endpoints are visible.
3. **Preset-based appearance, no semantics:** three default box styles and three default link styles. Presets define all appearance properties (shape, fill, outline, thickness, typography, line pattern etc). Nothing about a strong/weak edge is encoded in the model. Simulation is independent of those style presets.
4. **Canvas-first overlay layout:** top-left general file commands, left map-preview rail, top-right contextual properties, right-side separate simulation, bottom centered tool strip, small zoom controls; all collapsible or context-sensitive. Native window title already displays the installed PWA; no app name/icon in the toolbar.
5. **Icon-first:** reveal explanation only through tooltips or dialogs where necessary. Use real discoverable gestures and clear interaction feedback.
6. **Keep types simple:** only text boxes and unlabelled, undirected lines for V2. Prioritize polish and reliability before images or rich notes.
7. **Portable file:** self-contained, readable, versioned JSON stored as `.mindmap`, with desktop PWA file handler declaration plus fallbacks. No cloud or vendor lock-in.

## Technical model

```
Document v2
  title
  styles
    nodes: [node style presets]
    links: [link style presets]
  maps: [diagram]
    id, name, mode, viewport, physics
    nodes: [id, text, x, y, styleId, pinned, shelved, overrides?]
    edges: [id, from, to, styleId, bends, overrides?]
```

Styles are defined **per document**, reused across maps within that document. Presets are references by stable ID. Changing a preset re-renders all referencing objects. Later, support user presets and local overrides; preserve style-reference identity. Never share node/edge data across maps.

V1 migration: V1 had a single global nodes+edges graph and many view layouts. Migration creates **one independent copy of all graph objects per view**, preserving each view's positions/route bends and roughly mapping semantic link strength to a visual preset without retaining semantics. Original node shape and colour go into optional overrides. Migration happens only on file opening; save yields schema v2.

Runtime controls (file handles, hover state, selection, velocities, undo stack) are NOT part of the JSON file. Simulation freezes when opening a file.

## Interaction

- Drag boxes to move. Shift-click multi-select. Drag a small connector port to create a link; dropping onto empty space creates a linked node.
- Hover an edge to expose midpoint; drag to introduce a bend. Drag a bend to edit it.
- Shelf selected or shelf all. Shelving must preserve nodes and incident links; restoring restores connections when both endpoints are visible.
- Right top popover displays only selected node/link properties, separate from right-side simulation toggle/settings.
- Collapse the diagrams sidebar to gain canvas space; expand it to see live SVG preview thumbnails. Undo and redo are part of the first productive workflow.
- Diagram creation and duplication are *not* merely alternate layout modes. They create independent data.

## Engineering guardrails

- No mandatory build system, no npm install, no backend; plain static root assets on GitHub Pages.
- Safe JSON import with validation and V1 migration. Save As must never accidentally overwrite the previous file.
- Browser OS file handler is best-effort; always offer import/download fallback.
- Keep interaction tests covering map independence, shelving and link preservation, preset propagation, undo/redo, save/reopen and migration.
- Prefer user-visible, delightful quality: good hit targets, easing, subtle shadows, responsive layout and keyboard consistency. Respect prefers-reduced-motion.
- Never introduce semantic link types unless a later product decision deliberately requests them.

## Motion & feedback (V2.1)

Use motion to explain placement, transitions and state, not to decorate the canvas. Fit/toolbar zoom may ease toward a target, but gestures (drag, wheel, physics) must update immediately and remain interruptible. New nodes/links get brief one-shot entrances; selection, shelf/restore and simulation have unobtrusive feedback. Respect reduced-motion preferences in CSS and JavaScript. Never put animation state or transient effects into the portable JSON document. Test pointer capture and performance for direct manipulation after any rendering change.

## Gestures — V2.2 decisions

- **Selection:** Shift-click toggles nodes; Shift+drag draws an additive selection marquee; the bottom-toolbar selection tool enables region selection without modifiers; Ctrl/Cmd+A selects visible nodes. Selection never mutates the document and is not serialized.
- **Moving groups:** dragging a selected node moves every selected node at once; save the positions in one undo checkpoint. Do not animate or lag the dragged geometry relative to the pointer.
- **Touch:** two active pointers control zoom and pan around their midpoint; entering pinch must cancel any in-progress single-pointer drag before changing the camera. A touch long press adds the touched node to selection. Prioritise gesture arbitration and prevent accidental node creation during pinch.
- **Connecting:** enlarged invisible hit target around the visible port; use proximity snapping to a valid node and visual feedback during drag. Do not create a linked node when dropping onto a floating panel or back onto the source node.
- **Accessibility:** controls have labels/tooltips and selected tool has `aria-pressed`; respect reduced motion; preserve normal text-input editing and keyboard shortcuts.
- **Testing:** headless Chromium renders plus mouse selection / undo and Chrome DevTools Protocol real-touch-event emulation. Physical Android and Windows tablet tests remain advisable. The portable JSON schema is still v2.

## V2.3 — design/implementation decisions

- Curves are **a rendering of the existing bend-point polyline**, not an additional set of editable Bézier handles. A bounded Catmull–Rom-to-cubic interpolation passes through node boundary endpoints and every user bend, with C1-continuous tangents. SVG hit paths use the exact same curve as visible strokes. Hover/selection midpoint indicators follow curve segment geometry. Right-click a user-defined bend to remove it. All edits should be undoable.
- New document defaults are black-and-white only (black ink and three line/node treatments; completely transparent node fills). This does not recolour previously saved projects. Preserve other document styles and overrides.
- Document style definitions contain named presets; IDs remain stable, and `styleId` references are document-wide (across independent diagrams). New presets duplicate an existing style and receive a new unique ID. Removing a preset safely retargets references in every map. Preset properties are editable, not semantic categories.
- Colours use CSS-compatible 8-digit hex (`#RRGGBBAA`) for alpha, plus existing opaque 6-digit form. Editing the RGB channels must preserve the chosen opacity; editing opacity must preserve RGB. Apply to node fill, outline, text and link stroke.
- UI dark mode is an app preference (browser localStorage), separate from the portable document. Default black ink is **visually lightened at render time** against the dark canvas without mutating stored style data. Avoid unexpected recolouring of custom non-black colours. Keep controls floating and collapsible.
- Regression criteria: save and reopen custom presets and transparency; existing v2 files load; bend deletion/Undo works; spline passes through all bends with tangent continuity; no console errors or hidden file mutations on theme switches.

## V2.4 — Interaction simplification (supersedes conflicting earlier assumptions)

**Latest authoritative direction:** An independent diagram owns its *entire* appearance system; styles are now **per diagram, not per file**. Schema v3 replaces `document.styles` with `map.styles` and adds `map.defaultNodeStyleId` and `map.defaultLinkStyleId`. Importing v2 clones its shared styles into every map; v1 import is chained through v2 migration. These changes supersede the earlier document-wide preset decision above.

- Default left-click selects; dragging left on empty canvas creates a marquee. Shift-click and Shift-drag add to selection. Right-drag anywhere pans; right-click on an authored bend deletes it only if there was no drag. Two-finger pinch still navigates on touch.
- Middle-click deletes a node, link, or existing bend immediately. Every deletion must be undoable. The keyboard Delete/Backspace remains fully supported for trackpads and touch users. Avoid hijacking mouse interaction over floating chrome.
- Editing text occurs **in place** over the visible SVG node with a transparent textarea; its screen size, font, ink and position follow the node. No detached editing popup. Commit on blur or Ctrl+Enter, cancel with Escape.
- Selection reveals a tiny floating contextual toolbar directly above selected objects. It contains available preset swatches, pin, shelf and delete. Selection actions must NOT also occupy permanent bottom toolbar space.
- The right panel is a **style palette/editor only**, independent of selection. Simulation stays in its own panel. The palette uses a small, bounded set of choices; detailed style editing stays collapsed until requested. The bottom toolbar includes a focus button that hides everything except its own return control.
- Selecting a style for objects updates the diagram's last-used preset of that type. A newly created box or line inherits that value. Duplicated diagrams copy their styles and defaults, then evolve independently.
- Autosave is two-tier: write to a linked file only if write permission was **already granted**, plus best-effort IndexedDB recovery snapshots. A recovery snapshot does NOT mean a real local file was saved. Unlinked docs still require explicit Save/download. Never store file handles, history or runtime pointers in JSON.
- Preserve existing `.mindmap` data by importing v1 and v2 into schema v3 rather than rewriting objects in place without validation. Theme preference remains local UI state, not file data.

## Test contract for V2.4

Area-selection must not pan, and right-drag panning must not select. Selection is ephemeral. Group drag creates one undo checkpoint. No action may accidentally create a node during a right-button pan. Selected style -> next created object inherits it, for both nodes and links; duplicating a map and editing a preset leaves the original map unchanged. Editing text does not change object positions. Saving and reopening a v3 file roundtrips styles/defaults; importing v2 migrates cleanly. Focus mode must have an accessible exit control and work at mobile widths. Check all variants under both UI themes and reduced-motion settings.


## V2.5 — Monochrome UI and one-sidebar layout
- All application chrome is achromatic; custom diagram style colours remain editable and persist in source JSON.
- Dark mode inverts the entire rendered interface with a single root filter; this deliberately inverts any non-grayscale diagram colours too. No saved document colour values are changed.
- A single collapsible left rail contains four tabs: Diagrams, Styles, Simulation and Shelf. The top file commands and small bottom editing toolbar remain; redundant right panels and floating shelf are retired.
- Four offset connector handles (top, right, bottom, left) have larger visible circles and generous transparent hit regions. Link previews originate at the chosen handle.
- The v3 `.mindmap` schema is unchanged; all older files continue to load.
- Focus mode hides the rail and topbar as before. Test on actual touch hardware and check Chromium PWA file association separately.


## V2.6 quality contract
- Keep current `.mindmap` v3 JSON backward compatible; content data only, never include browser handles.
- All writes to a linked file must be serialized. Check linked-file metadata where available, and never silently overwrite an external modification.
- Recovery drafts are last-resort IndexedDB data, not files. Protect them against stale async completions when opening new documents.
- Editing in flight must not clear the unsaved indicator after an older snapshot has been written.
- Arrow nudges, cluster duplicate, inline edit, and curve bend edits must stay undoable, without introducing permanent toolbar controls.
- Maintain the browser regression suite, and do not mistake document-injection tests for full PWA installation/OS integration tests.
## V2.7 — Diagram-wide visual presentation

Per-diagram object **Styles** are factual formatting presets: fill, stroke, weight, type size, line style. The new optional `maps[].theme` is a non-destructive, diagram-wide skin, providing `character` (`precise|loose|hand-drawn`), `typeface` (`sans|mono|handwritten`) and `background` (`plain|dots|grid|paper`). Changes never mutate nodes/edges/bends or other diagrams. V3 validation defaults unknown/missing values safely.

Loose/hand-drawn paths use deterministic seeded noise based on object ID; interaction hit paths remain precise. SVG export is constructed from standalone geometry, never screenshots or UI chrome; PNG is rasterized from SVG in-browser. Fonts use installed OS fallbacks, not hosted assets.

Dragging selected nodes has an optional centre-axis magnetic alignment threshold (Alt bypass). Dropping the selection on the Shelf tab shelves nodes and groups the move as one Undo action. Retain direct pointer tracking and the static file / offline PWA architecture.


## V2.8 development contract

Do not reintroduce magnetic alignment, snapping or alignment guides. New default node presets are Underline, Rounded rectangle and Circle; base shape families are underline, rectangle and ellipse, with radius and Equal X/Y settings. Keep compatibility for legacy rounded/circle style values. New link defaults are fine, half-black solid, dashed and dotted. Hand-drawn linework must affect BOTH nodes and links and use stable smoothly joined curves. The per-diagram skin controls background colour, linework and typography, and must be honoured by SVG/PNG exports. Frequent pointer and physics frames update existing SVG elements, not the full canvas DOM. Keep the version-3 document compatible.

### V3.0 renderer contract
- Never add `.node-label{font-family:inherit}`: a CSS font-family declaration overrides the SVG element's presentation attribute and makes text look wrong until the inline editor opens. Display, edit and export must use the same font stack and normal font-style.
- `inkShape` owns node outline/underline appearance in Precise, Loose and Hand-drawn modes. Rounded corners are tangent-continuous cubic arcs. Underlines also receive style-dependent variation and optional ghost stroke.
- A `shape:'none'` node is text-only and remains selectable through its invisible hit area. A link `dash:'none'` has no visible ink but remains in JSON and keeps its hit path. Preserve existing IDs and document schema v4.

