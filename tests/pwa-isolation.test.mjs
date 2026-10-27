import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const manifest=JSON.parse(await readFile(new URL('../manifest.webmanifest',import.meta.url),'utf8'));
const worker=await readFile(new URL('../sw.js',import.meta.url),'utf8');
test('Mindmap manifest has a stable, repo-specific identity and scope',()=>{
  assert.equal(manifest.id,'/261019-1740_pwa-mindmap/');
  assert.equal(manifest.start_url,'./');
  assert.equal(manifest.scope,'./');
});
test('Mindmap activation leaves Sourcebook and unrelated caches intact',async()=>{
  const listeners=new Map(),deleted=[];
  const own=worker.match(/const CACHE\s*=\s*'([^']+)'/)?.[1];
  assert.ok(own);
  const caches={keys:async()=>[own,'mindmap-shell-old','sourcebook-shell-old','some-other-app'],
    delete:async key=>{deleted.push(key);return true;}};
  const self={addEventListener:(name,fn)=>listeners.set(name,fn),clients:{claim:async()=>{}}};
  (new Function('self','caches',worker))(self,caches);
  let task;listeners.get('activate')({waitUntil:promise=>{task=promise;}});
  await task;
  assert.deepEqual(deleted,['mindmap-shell-old']);
});
