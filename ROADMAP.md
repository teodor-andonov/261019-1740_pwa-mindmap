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
