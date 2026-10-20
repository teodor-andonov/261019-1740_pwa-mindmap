"""Regression checks for canvas/editor handwriting, drawn outlines and text-only nodes."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from test_browser import ROOT, launch_browser

def test_handwritten_label_uses_editor_font(tmp_path):
    with sync_playwright() as p:
        browser=launch_browser(p)
        ctx=browser.new_context(accept_downloads=True,viewport={"width":1440,"height":900})
        page=ctx.new_page(); errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.set_content((ROOT/"index.html").read_text(),wait_until="load")
        page.locator("#rail-theme").click()
        page.locator('[data-theme-key="character"][data-theme-value="hand-drawn"]').click()
        page.locator('[data-theme-key="typeface"][data-theme-value="handwritten"]').click()
        label=page.locator("#nodeLayer text.node-label").first
        family=label.evaluate("el=>getComputedStyle(el).fontFamily")
        assert "Segoe Print" in family
        assert label.get_attribute("font-style")=="normal"
        page.locator("#nodeLayer [data-node]").first.dblclick(force=True)
        assert page.locator("#editor").evaluate("el=>getComputedStyle(el).fontFamily")==family
        assert page.locator("#editor").evaluate("el=>getComputedStyle(el).fontStyle")=="normal"
        page.locator("#editor").press("Escape")
        with page.expect_download() as d: page.locator('[data-export="svg"]').click()
        svg=Path(d.value.path()).read_text()
        assert 'font-style="normal"' in svg and "Segoe Print" in svg
        assert not errors,errors
        ctx.close();browser.close()

def test_drawn_rounded_underline_and_hidden_styles(tmp_path):
    with sync_playwright() as p:
        browser=launch_browser(p)
        ctx=browser.new_context(accept_downloads=True,viewport={"width":1440,"height":900})
        page=ctx.new_page(); errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.set_content((ROOT/"index.html").read_text(),wait_until="load")
        page.locator("#rail-theme").click()
        page.locator('[data-theme-key="character"][data-theme-value="precise"]').click()
        underline=page.locator("#nodeLayer [data-node]").filter(has=page.locator(".node-label",has_text="Big idea")).first
        rounded=page.locator("#nodeLayer [data-node]").filter(has=page.locator(".node-label",has_text="Research")).first
        straight=underline.locator(".node-art > path").last.get_attribute("d")
        page.locator('[data-theme-key="character"][data-theme-value="hand-drawn"]').click()
        assert underline.locator(".node-art > path").last.get_attribute("d")!=straight
        assert underline.locator(".node-art > path").count()==2
        rect=rounded.locator(".node-art > path").last.get_attribute("d")
        assert rect.count(" C")==8 and rect.endswith(" Z") and "NaN" not in rect
        with page.expect_download() as d: page.locator("#saveFile").click()
        doc=json.loads(Path(d.value.path()).read_text())
        assert doc["maps"][0]["styles"]["nodes"][3]["shape"]=="none"
        doc["maps"][0]["nodes"][0]["styleId"]="node-d"
        doc["maps"][0]["styles"]["links"][0]["dash"]="none"
        f=tmp_path/"text-only.mindmap";f.write_text(json.dumps(doc))
        page.locator("#fileInput").set_input_files(str(f))
        node=page.locator("#nodeLayer [data-node]").first
        assert node.locator(".node-label").count()==1
        assert node.locator(".node-art > path, .node-art > rect:not(.node-target), .node-art > ellipse").count()==0
        assert node.locator(".node-target").count()==1
        edge=page.locator("#edgeLayer [data-edge]").first
        assert edge.locator("[data-ink]").get_attribute("stroke")=="none"
        assert edge.locator("[data-hit]").count()==1
        assert not errors,errors
        ctx.close();browser.close()
