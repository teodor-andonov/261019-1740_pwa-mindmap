"""Browser regressions for V3.1. Run: pytest -q tests/test_v31.py"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from test_browser import ROOT, launch_browser

def test_v31_sidebar_names_and_type(tmp_path):
    with sync_playwright() as p:
        b=launch_browser(p);c=b.new_context(accept_downloads=True,viewport={'width':1365,'height':820});page=c.new_page();errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content((ROOT/'index.html').read_text(),wait_until='load')
        assert page.locator('#railTabs').evaluate('x=>getComputedStyle(x).flexDirection')=='column'
        assert page.locator('#zoom').is_visible()
        page.locator('#rail-styles').click()
        page.locator('#nodeLayer [data-node]').first.click(force=True)
        page.locator('#objectType').fill('research')
        page.locator('#objectType').press('Tab')
        page.locator('#editPreset').click()
        page.locator('#presetName').fill('Research idea')
        page.locator('#presetName').press('Tab')
        with page.expect_download() as dl:page.locator('#saveFile').click()
        obj=json.loads(Path(dl.value.path()).read_text())
        assert obj['version']==4 and obj['maps'][0]['nodes'][0]['type']=='research'
        assert any(x['name']=='Research idea' for x in obj['maps'][0]['styles']['nodes'])
        assert not errors,errors
        b.close()

def test_v31_alt_drag_and_multilink(tmp_path):
    with sync_playwright() as p:
        b=launch_browser(p);c=b.new_context(viewport={'width':1365,'height':820});page=c.new_page();errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content((ROOT/'index.html').read_text(),wait_until='load')
        n=page.locator('#nodeLayer [data-node]').first
        box=n.locator('.node-target').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2
        page.keyboard.down('Alt');page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+80,y+50,steps=7);page.mouse.up();page.keyboard.up('Alt')
        assert page.locator('#nodeLayer [data-node]').count()==7
        page.keyboard.press('Control+z')
        assert page.locator('#nodeLayer [data-node]').count()==6
        def point(i):
            return page.locator('#edgeLayer [data-hit]').nth(i).evaluate('''el=>{const pt=el.getPointAtLength(el.getTotalLength()*.27),m=el.getScreenCTM(),p=new DOMPoint(pt.x,pt.y).matrixTransform(m);return{x:p.x,y:p.y}}''')
        a=point(0);page.mouse.click(a['x'],a['y'])
        d=point(2);page.keyboard.down('Shift');page.mouse.click(d['x'],d['y']);page.keyboard.up('Shift')
        assert page.locator('#edgeLayer [data-edge]:has(.midpoint)').count()>=2
        before=page.locator('#edgeLayer > [data-edge]').count()
        page.keyboard.press('Delete')
        assert page.locator('#edgeLayer > [data-edge]').count()==before-2
        page.keyboard.press('Control+z')
        assert page.locator('#edgeLayer > [data-edge]').count()==before
        assert not errors,errors
        b.close()

def test_v31_simulation_shelved_links_and_pins(tmp_path):
    with sync_playwright() as p:
        b=launch_browser(p);c=b.new_context(accept_downloads=True,viewport={'width':1365,'height':820});page=c.new_page();errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content((ROOT/'index.html').read_text(),wait_until='load')
        with page.expect_download() as dl:page.locator('#saveFile').click()
        data=json.loads(Path(dl.value.path()).read_text());m=data['maps'][0];m['nodes'][2]['shelved']=True;m['nodes'][0]['pinned']=True
        pinned=(m['nodes'][0]['x'],m['nodes'][0]['y'])
        f=tmp_path/'shelved.mindmap';f.write_text(json.dumps(data))
        page.locator('#fileInput').set_input_files(str(f))
        page.locator('#rail-simulation').click();page.locator('#simToggle').click()
        page.wait_for_timeout(450);page.locator('#simToggle').click()
        with page.expect_download() as dl:page.locator('#saveFile').click()
        saved=json.loads(Path(dl.value.path()).read_text())['maps'][0]
        assert (saved['nodes'][0]['x'],saved['nodes'][0]['y'])==pinned
        assert saved['mode']=='static'
        assert all(abs(n['x'])<1e6 and abs(n['y'])<1e6 for n in saved['nodes'])
        assert not errors,errors
        b.close()
