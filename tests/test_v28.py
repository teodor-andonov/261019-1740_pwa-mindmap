import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from test_browser import launch_browser, ROOT

def test_v28_defaults_and_theme(tmp_path):
    with sync_playwright() as p:
        browser=launch_browser(p)
        ctx=browser.new_context(accept_downloads=True,viewport={"width":1440,"height":900})
        page=ctx.new_page()
        page.set_content((ROOT/"index.html").read_text(),wait_until="load")
        with page.expect_download() as d: page.locator("#saveFile").click()
        data=json.loads(Path(d.value.path()).read_text())
        node=data["maps"][0]["styles"]["nodes"]
        link=data["maps"][0]["styles"]["links"]
        assert [s["name"] for s in node]==["Underline","Rounded","Circle"]
        assert [s["name"] for s in link]==["Solid","Dashed","Dotted"]
        assert link[2]["dash"]=="0.1 5"
        assert all(s["stroke"]=="#00000080" for s in link)
        assert all(s["fill"]=="#ffffff00" for s in node)
        page.locator("#rail-theme").click()
        page.locator("#themeBgColor").fill("#eee4d5")
        page.locator('[data-theme-key="character"][data-theme-value="hand-drawn"]').click()
        page.locator('[data-theme-key="typeface"][data-theme-value="handwritten"]').click()
        assert page.locator("#edgeLayer [data-ink]").first.get_attribute("d")!=page.locator("#edgeLayer [data-hit]").first.get_attribute("d")
        assert page.locator("#nodeLayer .node-label").first.get_attribute("font-style")=="italic"
        with page.expect_download() as d: page.locator('[data-export="svg"]').click()
        svg=Path(d.value.path()).read_text()
        assert "#eee4d5" in svg and "Comic Neue" in svg
        browser.close()

def test_v28_camera_pan_preserves_nodes():
    with sync_playwright() as p:
        browser=launch_browser(p)
        page=browser.new_page(viewport={"width":1440,"height":900})
        page.set_content((ROOT/"index.html").read_text(),wait_until="load")
        page.evaluate("window.savedNode=document.querySelector('#nodeLayer [data-node]')")
        start=page.locator("#camera").get_attribute("transform")
        page.mouse.move(800,700)
        page.mouse.down(button="right")
        page.mouse.move(850,740,steps=5)
        page.mouse.up(button="right")
        assert page.locator("#camera").get_attribute("transform")!=start
        assert page.evaluate("window.savedNode===document.querySelector('#nodeLayer [data-node]')")
        assert page.locator(".snap-guide").count()==0
        browser.close()
