# Mindmap V3.1

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

## V3.0 — Consistent handwriting and linework

- The visible SVG label now uses the selected handwritten font, just like the in-place editor. The old CSS rule `font-family:inherit` was overriding the SVG's configured font.
- Handwritten text is no longer forced italic, and artificial letter rotation is restrained. The same font/style choices apply in SVG and PNG exports.
- Rounded-rectangle hand-drawn outlines now have smooth, tangent-continuous corners and subtle side variation; hand-drawn underlines have an organic curve plus a light companion stroke.
- **Text only** is a fourth default node style, with no box or underline. Select it from the Styles presets or choose **None (text only)** under Shape. Connections can also have Pattern **No line**, without deleting the underlying links.
- No change to the version-4 `.mindmap` format. Existing files remain compatible.



## V3.1 — Multiple links, Alt+drag and stable relaxation

- Preset names are optional and editable in Styles. New presets start unnamed. Node and link records have an optional text \`type\` (default empty) which agents can use, independently of the visual style.
- Shift-click and marquee-select both nodes and connections. Apply styles to multiple selected links; Delete/Undo work on mixed selections.
- Alt+drag duplicates a selected node or group and its internal links; Alt+drag duplicates connections with separately editable bends. Ctrl/Cmd+D still duplicates.
- The sidebar's tab icons stay visible vertically, even when the content panel is collapsed. Zoom in/out/100% is at bottom-left.
- The force solver skips links to shelved nodes, guards coincident positions and uses more stable damping. Pinned nodes remain fixed.
- Version 4 \`.mindmap\` format is unchanged; new metadata is optional. Desktop and touch regressions should still be verified on actual devices.
