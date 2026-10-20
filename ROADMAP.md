# Mindmap — roadmap

## V2.0 · Foundation (current)
- [x] Independent maps per document, deep duplication and preview thumbnails
- [x] Shelf/restore without deleting nodes or their underlying links
- [x] Three document-level node presets and three link presets; purely visual
- [x] Canvas-first floating UI: file controls, collapsible diagram rail, contextual inspector, separate simulation, bottom tools
- [x] Version 2 `.mindmap` JSON, best-effort installed PWA file handler, V1 migration
- [x] Drag/edit/connect/bend, simulation toggle/settings, node pins, basic undo/redo
- [x] Browser smoke tests: duplicate independence, shelf/restore, style changes, V1 import, save/reopen, mobile layout

## V2.1 · Polish and reliability (next)
- [ ] Physical Windows/Android PWA and OS file-association tests; file-open launch queue
- [ ] Genuine touch pinch/pan/port/shelf drag validation
- [ ] Marquee multi-selection, alignment, keyboard nudging, consistent shortcut feedback
- [ ] Continuous-edit undo grouping and conflict-aware file saving; optional linked-file autosave
- [ ] Refine connector geometry and handles, collapse transitions and visual design
- [ ] Replace destructive native confirms with small purposeful UI
- [ ] Improve initial viewport layout and fitting on narrow screens

## V2.2 · Appearance and utility
- [ ] New, duplicate, reorder, remove and rename arbitrary style presets
- [ ] Per-object style overrides, with reset-to-preset action
- [ ] More complete typography, colour, opacity and line-pattern settings
- [ ] Optional overall dark/light canvas appearance, independent of semantic graph attributes
- [ ] SVG/PNG canvas export, searching/selecting nodes, copy/paste between maps
- [ ] More advanced physics/force algorithms for larger diagrams

## V3 · Rich content — intentionally postponed
- [ ] Image and note objects
- [ ] Graphic pad/sketch objects
- [ ] Optional labels/arrows/semantic links
- [ ] Optional graph analysis and agent-native tooling

**Product rule:** fewer features, beautifully done. Canvas remains primary; UI is secondary and collapsible.

## V2.1 — Motion and interaction polish (shipped)

- [x] Gentle, interruptible Fit and toolbar zoom
- [x] Node and edge entrance, connection hover target, node release feedback
- [x] Shelf and restore cues; floating UI transitions and simulation animation
- [x] Respect reduced-motion settings and keyboard focus
- [x] Browser regressions: map independence, shelf and restore, node/link creation, file round-trip, simulated physics, desktop/mobile layout

Still to refine: native touch pinch gestures, diagram hit-target accessibility, larger graph rendering performance, improved undo coverage and OS-level file handler verification. Preserve direct manipulation and restraint.

## V2.2 · Gestures & direct manipulation (completed)
- [x] Shift-drag marquee, selection tool and Ctrl/Cmd+A
- [x] Move groups with one undo checkpoint; shelf/undo integration
- [x] Multi-touch pinch/pan anchored between fingers
- [x] Cancel an in-progress node drag when a pinch begins
- [x] Touch long-press additive selection
- [x] Enlarged connector hit targets and target snapping
- [x] Headless Chromium regression suite (desktop and emulated touch)
- [ ] Manual testing on actual Android and Windows touch/trackpad devices

**Next:** keyboard nudging, line bend hit-area improvements, SVG rendering performance, per-object style overrides, smart shelf drag/drop, and file save conflict protection. Prioritize feel and reliability over feature growth.


## V2.3 · Completed
- [x] Smooth editable curves through stored bend points, with matching hit paths and midpoint handles
- [x] Right-click bend removal and undo
- [x] Custom add/duplicate/delete node and link presets with safe reassignment
- [x] Three black-and-white defaults per category, transparent node fill for new documents
- [x] Independent colour opacity sliders, eight-digit CSS hex saved in JSON
- [x] Dark interface and dark canvas via local preference, no colour mutation in saved files
- [x] Browser regression tests for curve edits, preset creation and transparency file roundtrip
- [ ] Physical touchscreen and Windows installed PWA validation

Next focus: polish handling of many presets, per-object overrides and cross-device gestures.


## V2.4 — Canvas-first simplification
- [x] Left-drag marquee, right-drag pan, right-click bend deletion; middle-click node/link/bend deletion with Undo
- [x] On-object inline text editor; anchored selection style/pin/shelf/delete toolbar
- [x] Per-diagram styles and last-used node/link defaults; independent style changes in duplicated maps
- [x] Version 3 `.mindmap` migration from previous v1/v2 files
- [x] Compact discrete style controls, separate simulation, mobile-collapsed palette
- [x] Focus mode hides floating chrome, retains exit affordance
- [x] Best-effort linked-file autosave (no new permission prompts), IndexedDB session recovery
- [x] Browser tests: gestures, inline editing, preset inheritance, v2 import/v3 save, bend removal, Undo, autosave handle, mobile visual smoke
- [ ] Manual verification on physical Windows/Android hardware; installed file association, touch, and persistent recovery storage
- [ ] Improve late queued/autosave overlapping manual writes, recovery conflict handling and long-label text reflow


## V2.5 — Complete: grayscale, rail, ports

- [x] Full grayscale application chrome; custom canvas object colours remain supported
- [x] Entire-screen dark-mode inversion without changing saved colours
- [x] Consolidate Diagrams, Styles, Simulation, Shelf into one collapsible left sidebar
- [x] Remove duplicate right panels and separate floating shelf
- [x] Four outward-offset connector handles with larger grab regions and accurate link-start origins
- [x] Fix older CSS hover-media nesting bug affecting touch devices
- [x] Preserve version 3 files and bump offline PWA cache

**Next:** validate Windows PWA file association and touch behaviour on actual hardware, improve shelving drag affordance, and harden autosave/recovery races.


## V2.6 — Reliability and keyboard-quality sprint (shipped)
- [x] Serialized linked-file writes, including overlapping manual Save and autosave
- [x] Detect external linked-file modifications and direct users to Save As
- [x] Epoch-gated recovery snapshots and safe unsaved-change status during writes
- [x] Arrow-key nudging (1 unit; Shift 10) as grouped Undo actions
- [x] Double-click links to add spline bends
- [x] Ctrl/Cmd+D to duplicate selected subgraphs and their internal links
- [x] Browser regressions for multi-diagram independence, keyboard Undo, autosave conflicts, and cluster duplication
- [ ] Physical Windows/Android PWA, persistent recovery and OS association validation
- [ ] V2.7: alignment/snapping, further text editing and shelf interaction polish

## V2.7 — Theme / export / direct manipulation (shipped)

- [x] Fifth left sidebar tab for independent, whole-diagram Theme; separate from box/link style presets.
- [x] Precise, Loose and Hand-drawn stable seeded strokes on all outlines and connections.
- [x] Sans, Mono, Handwriting installed-font stacks; Plain, Dots, Grid and Paper backgrounds.
- [x] Vector SVG and local PNG exports of the current diagram and skin, free of editor handles.
- [x] Magnetic centre alignment guides (Alt disables snapping during drag).
- [x] Selected boxes draggable directly to the Shelf tab as an Undo-safe operation.
- [x] Seven headless Chromium regressions passed; four original plus three V2.7-specific.

Next: verify real Windows/Android PWA and tablet gestures; increase coverage for snap cancellation, shelf/restore edges, and export on installed browsers. Keep object content and geometry independent from the rendering skin.


## V2.8 — Responsive canvas, cleaner styles and themes

- No magnetic alignment or guides. Node dragging follows the pointer exactly; connection targeting remains available.
- Default nodes: Underline, Rounded rectangle and Circle, with fine outlines and transparent white fill. Rectangles use radius for rounding; Equal X/Y produces squares or circles. Old document presets remain unchanged.
- Default links: solid, dashed and genuinely dotted fine strokes, all 50% black (#00000080).
- Theme: Precise, Loose and Hand-drawn affect node outlines AND links, with deterministic, smooth curves. Handwriting affects node text, editor and export. Each diagram has editable background colour, also used on export.
- Performance: panning and zooming change the SVG camera without recreating nodes. Dragging and simulation update existing SVG shapes on animation frames. Physics dimensions are cached per tick.
- File schema remains version 3. Browsers need local handwriting fonts or use cursive fallback. Real Windows/Android tests and large-graph profiling remain outstanding.


## V2.9 — Theme and rendering repair
- [x] One overall Theme per document (v4), for every diagram and export.
- [x] Single Ink colour for box outline and text.
- [x] Visible, smooth hand-drawn shapes, links and per-character text treatment.
- [x] Preserve old document migration and undo/save behaviour.
- [ ] Verify fonts and gesture performance on physical Windows/Android installs.

