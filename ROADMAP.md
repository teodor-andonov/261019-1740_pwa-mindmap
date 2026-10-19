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
