"""Headless Chromium regressions. Uses document injection (not a real PWA origin).

Run: pytest -q tests/test_browser.py
Service-worker lifecycle, OS file handling, and persistent IndexedDB require a separate live-origin test.
"""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def launch_browser(playwright):
    binary = os.environ.get("CHROMIUM_PATH") or shutil.which("chromium") or shutil.which("google-chrome")
    opts = {"executable_path": binary} if binary else {}
    return playwright.chromium.launch(headless=True, args=["--no-sandbox"], **opts)


@pytest.fixture
def browser_page():
    with sync_playwright() as p:
        browser = launch_browser(p)
        context = browser.new_context(accept_downloads=True, viewport={"width": 1440, "height": 900})
        page = context.new_page()
        failures = []
        page.on("pageerror", lambda error: failures.append(str(error)))
        page.set_content((ROOT / "index.html").read_text(), wait_until="load")
        page.wait_for_timeout(120)
        yield page, failures
        assert failures == [], "Uncaught browser errors: " + repr(failures)
        context.close()
        browser.close()


def positions(page):
    return page.locator("#nodeLayer [data-node]").evaluate_all(
        "nodes => nodes.map(n=>({id:n.getAttribute('data-node'),transform:n.getAttribute('transform')}))"
    )


def test_smoke_and_keyboard_nudge_single_undo(browser_page):
    page, _ = browser_page
    nodes = positions(page)
    assert len(nodes) == 6
    page.locator("#nodeLayer [data-node]").first.click(force=True)
    before = positions(page)[0]["transform"]
    page.keyboard.down("ArrowRight")
    for _ in range(4):
        page.evaluate("document.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true,repeat:true}))")
    page.keyboard.up("ArrowRight")
    after = positions(page)[0]["transform"]
    assert after != before, (before, after)
    page.keyboard.press("Control+z")
    assert positions(page)[0]["transform"] == before
    page.keyboard.press("Control+y")
    assert positions(page)[0]["transform"] == after


def test_inline_edit_and_diagram_independence(browser_page):
    page, _ = browser_page
    page.locator("#nodeLayer [data-node]").first.dblclick(force=True)
    editor = page.locator("#editor")
    assert editor.is_visible()
    editor.fill("Edited directly on node")
    page.keyboard.press("Control+Enter")
    assert "Edited directly on node" in page.locator("#nodeLayer").text_content()
    page.locator('#mapActions').click()
    page.locator('#duplicateMap').click()
    assert page.locator('#mapList [data-map]').count()==2
    page.locator("#nodeLayer [data-node]").first.dblclick(force=True)
    page.locator('#editor').fill('Changed only in duplicate')
    page.keyboard.press('Control+Enter')
    page.locator('#mapList [data-map]').first.click()
    assert 'Edited directly on node' in page.locator('#nodeLayer').text_content()
    assert 'Changed only in duplicate' not in page.locator('#nodeLayer').text_content()


def test_recovery_and_autosave_serialization():
    # Use a real save download as the source of a linked-file mock.
    with sync_playwright() as p:
        browser=launch_browser(p)
        ctx=browser.new_context(accept_downloads=True)
        page=ctx.new_page()
        page.evaluate("window.showSaveFilePicker = undefined; window.showOpenFilePicker = undefined;")
        page.set_content((ROOT / "index.html").read_text(), wait_until="load")
        with page.expect_download() as info:
            page.locator('#saveFile').click()
        seed=Path(info.value.path()).read_text()
        assert json.loads(seed)["version"] == 3
        ctx.close()
        ctx=browser.new_context()
        page=ctx.new_page()
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.evaluate("""seed=>{
           const state=window.__testFile={text:seed,stamp:100,writes:[],delay:300,active:0,maxActive:0};
           const file=()=>new File([state.text],'Linked.mindmap',{type:'application/json',lastModified:state.stamp});
           const handle={name:'Linked.mindmap',getFile:async()=>file(),queryPermission:async()=> 'granted',
             createWritable:async()=>{let value='';return {write:async txt=>{value=txt;state.active++;state.maxActive=Math.max(state.maxActive,state.active);await new Promise(r=>setTimeout(r,state.delay))},close:async()=>{state.text=value;state.stamp++;state.writes.push(value);state.active--}}}};
           window.showOpenFilePicker=async()=>[handle];
           window.showSaveFilePicker=async()=>({name:'Copy.mindmap',queryPermission:async()=> 'granted',
             createWritable:async()=>({write:async t=>state.copy=t,close:async()=>{}})});
          }""", seed)
        page.set_content((ROOT / "index.html").read_text(), wait_until="load")
        page.locator('#openFile').click()
        page.wait_for_timeout(200)
        assert page.locator('#nodeLayer [data-node]').count()==6
        # Editing a node after the file is linked triggers autosave, without prompting.
        page.locator('#nodeLayer [data-node]').first.dblclick(force=True)
        page.locator('#editor').fill('Autosave v1')
        page.keyboard.press('Control+Enter')
        page.wait_for_timeout(1900)
        state=page.evaluate('window.__testFile')
        assert len(state['writes'])>=1, state
        assert 'Autosave v1' in state['text']
        # Start an autosave, then initiate a manual save while the first write is in flight.
        page.locator('#nodeLayer [data-node]').first.dblclick(force=True)
        page.locator('#editor').fill('Concurrent edit')
        page.keyboard.press('Control+Enter')
        page.wait_for_timeout(1170)
        page.locator('#nodeLayer [data-node]').first.dblclick(force=True)
        page.locator('#editor').fill('Latest saved text')
        page.keyboard.press('Control+Enter')
        page.locator('#saveFile').click()
        page.wait_for_timeout(1300)
        state=page.evaluate('window.__testFile')
        assert state['maxActive']==1, state
        assert 'Latest saved text' in state['text']
        # Simulate another app changing the file on disk. Autosave must refuse overwriting it.
        page.evaluate("window.__testFile.text+='\\n ';window.__testFile.stamp+=500")
        page.locator('#nodeLayer [data-node]').first.dblclick(force=True)
        page.locator('#editor').fill('Autosave v2')
        page.keyboard.press('Control+Enter')
        count=page.evaluate('window.__testFile.writes.length')
        page.wait_for_timeout(1900)
        assert page.evaluate('window.__testFile.writes.length')==count
        assert page.locator('#unsaved').evaluate("el=>el.classList.contains('visible')")
        # Saving to a different file is still supported.
        page.locator('#saveAs').click()
        page.wait_for_timeout(300)
        assert 'Autosave v2' in page.evaluate('window.__testFile.copy')
        assert errors==[],errors
        ctx.close();browser.close()


def test_duplicate_subgraph_is_one_undo_step(browser_page):
    page, _ = browser_page
    nodes = page.locator('#nodeLayer [data-node]')
    assert nodes.count() == 6
    page.locator('#nodeLayer [data-node]').nth(0).click(force=True)
    page.locator('#nodeLayer [data-node]').nth(1).click(force=True, modifiers=['Shift'])
    page.keyboard.press('Control+d')
    assert page.locator('#nodeLayer [data-node]').count() == 8
    assert page.locator('#edgeLayer [data-edge].hit-edge').count() == 7
    page.keyboard.press('Control+z')
    assert page.locator('#nodeLayer [data-node]').count() == 6
    assert page.locator('#edgeLayer [data-edge].hit-edge').count() == 6
