import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from test_browser import ROOT, launch_browser

def test_global_theme_and_shared_ink():
    with sync_playwright() as p:
        browser=launch_browser(p)
        ctx=browser.new_context(accept_downloads=True)
        page=ctx.new_page()
        page.set_content((ROOT/'index.html').read_text(),wait_until='load')
        page.locator('#rail-styles').click()
        page.locator('#editPreset').click()
        assert page.locator('[data-style-prop="textColor"]').count()==0
        page.locator('[data-style-prop="stroke"]').fill('#bb2244')
        assert page.locator('#nodeLayer .node-label').first.get_attribute('fill')=='#bb2244'
        page.locator('#rail-theme').click()
        page.locator('[data-theme-value="hand-drawn"]').click()
        assert page.locator('#edgeLayer [data-ghost]').count()>0
        assert page.locator('#nodeLayer .node-label tspan[rotate]').count()>0
        page.locator('#rail-diagrams').click()
        page.locator('#mapActions').click()
        page.locator('#duplicateMap').click()
        page.locator('#rail-theme').click()
        page.locator('[data-theme-value="precise"]').click()
        page.locator('#rail-diagrams').click()
        page.locator('#mapList [data-map]').first.click()
        page.locator('#rail-theme').click()
        assert page.locator('[data-theme-value="precise"]').get_attribute('aria-pressed')=='true'
        with page.expect_download() as download: page.locator('#saveFile').click()
        doc=json.loads(Path(download.value.path()).read_text())
        assert doc['version']==4
        assert len(doc['maps'])==2
        assert all('theme' not in m for m in doc['maps'])
        assert all('textColor' not in st for m in doc['maps'] for st in m['styles']['nodes'])
        ctx.close();browser.close()
