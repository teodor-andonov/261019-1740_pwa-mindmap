"""V2.7 diagram skin, SVG/PNG export and Shelf drag regression tests."""
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
from test_browser import launch_browser, ROOT

@pytest.fixture
def page_v27():
    with sync_playwright() as p:
        browser=launch_browser(p)
        context=browser.new_context(accept_downloads=True, viewport={"width":1440,"height":900})
        page=context.new_page()
        errors=[]
        page.on("pageerror",lambda error:errors.append(str(error)))
        page.set_content((ROOT/"index.html").read_text(),wait_until="load")
        page.wait_for_timeout(140)
        yield page
        assert errors==[],errors
        context.close()
        browser.close()

def positions(page):
    return page.locator("#nodeLayer [data-node]").evaluate_all("els=>els.map(el=>[el.dataset.node,el.getAttribute('transform')])")

def test_theme_applies_to_whole_diagram_without_geometry_changes(page_v27):
    page=page_v27
    before=positions(page)
    page.locator("#rail-theme").click()
    page.locator('[data-theme-value="hand-drawn"]').click()
    page.locator('[data-theme-value="mono"]').click()
    page.locator('[data-theme-value="paper"]').click()
    assert positions(page)==before
    assert page.locator("#stage").get_attribute("data-background")=="paper"
    assert page.locator("#nodeLayer .node-art path").count()>0
    assert "monospace" in page.locator("#nodeLayer .node-label").first.get_attribute("font-family")
    page.locator("#rail-diagrams").click()
    page.locator("#mapActions").click()
    page.locator("#duplicateMap").click()
    page.locator("#rail-theme").click()
    page.locator('[data-theme-value="precise"]').click()
    page.locator("#rail-diagrams").click()
    page.locator("#mapList [data-map]").first.click()
    page.locator("#rail-theme").click()
    assert page.locator('[data-theme-value="hand-drawn"]').get_attribute("aria-pressed")=="true"
    assert positions(page)==before

def test_svg_and_png_export_current_skin(page_v27, tmp_path):
    page=page_v27
    page.locator("#rail-theme").click()
    page.locator('[data-theme-value="hand-drawn"]').click()
    with page.expect_download() as download:
        page.locator('[data-export="svg"]').click()
    file=tmp_path/"diagram.svg"
    download.value.save_as(file)
    svg=file.read_text()
    assert "<svg" in svg and "<path" in svg
    assert 'class="port"' not in svg and "data-node=" not in svg
    with page.expect_download() as download:
        page.locator('[data-export="png"]').click()
    file=tmp_path/"diagram.png"
    download.value.save_as(file)
    assert file.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")

def test_drag_selected_node_onto_shelf_and_undo(page_v27):
    page=page_v27
    box=page.locator("#nodeLayer [data-node]").first.bounding_box()
    shelf=page.locator("#rail-shelf").bounding_box()
    assert box and shelf
    x=box["x"]+box["width"]/2; y=box["y"]+box["height"]/2
    dx=shelf["x"]+shelf["width"]/2; dy=shelf["y"]+shelf["height"]/2
    page.mouse.move(x,y);page.mouse.down()
    for i in range(1,11):
        page.mouse.move(x+(dx-x)*i/10,y+(dy-y)*i/10)
    page.mouse.up()
    assert page.locator("#nodeLayer [data-node]").count()==5
    assert page.locator("#shelfItems [data-restore]").count()==1
    page.keyboard.press("Control+z")
    assert page.locator("#nodeLayer [data-node]").count()==6
