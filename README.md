# Mindmap V2.9

**The canvas is the application.** One local-first `.mindmap` file holds multiple independent diagrams. No backend or build system.

## Appearance

- **Theme is shared across the entire file:** Precise / Loose / Hand-drawn linework, Sans / Mono / Handwriting typography, background type and colour. It applies to every diagram and to SVG/PNG exports.
- Each diagram independently stores its own box/link style presets and last-used styles.
- A box has one **Ink** colour with opacity for both text and outline; Fill remains independent. Links have separate Ink and stroke patterns.
- Hand-drawn uses smoother but visibly organic box and connection strokes, a subtle second trace, and per-character variation even without a handwritten font installed.
- No magnetic alignment snapping.

## File schema

Version 4 stores `document.theme` and `document.maps`. Map objects have styles, nodes, edges, shelf, viewport and physics, but **no per-map theme**. The application opens v1/v2/v3 files. For old v3 files with different themes, the first diagram's theme becomes document-wide; legacy textColor values are replaced by outline Ink. Save a backup of important older files before upgrading.

## Controls

Left-click/drag selects, right-drag pans, pinch/wheel zooms. Double-click a node for inline text editing; drag its four ports to link or create new nodes. Double-click a link to add a bend; right-click a bend to remove it. Ctrl/Cmd+Z undoes; Ctrl/Cmd+D duplicates selection. Use the left sidebar for Diagrams, Styles, Theme, Simulation and Shelf. Export SVG/PNG in Theme.

## Run and test

Visit https://teodor-andonov.github.io/261019-1740_pwa-mindmap/ or run `python -m http.server 8080` locally. Install test requirements and run `pytest -q tests` with Playwright Chromium. The PWA caches app code only; linked file autosave depends on browser write permissions, and recovery drafts are not replacements for saved files. Physical Windows/Android PWA testing remains outstanding.
