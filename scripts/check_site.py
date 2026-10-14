from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import csv,json
root=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.ids=[];self.results=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='tr' and 'data-place' in a:self.results.append(a['data-place'])
  for name in ('href','src'):
   if name in a:self.refs.append(a[name])
p=Page();p.feed((root/'index.html').read_text())
assert len(p.ids)==len(set(p.ids)), 'Duplicate IDs'
for url in p.refs:
 parsed=urlsplit(url)
 if parsed.scheme or parsed.netloc:continue
 if parsed.path:assert (root/unquote(parsed.path)).is_file(),url
 elif parsed.fragment:assert parsed.fragment in p.ids,url
records=json.loads((root/'data/achievements.json').read_text())['records']
core=[r for r in records if r['scope']=='гуманоидная робототехника']
assert len(core)==len(p.results)==83
assert sum(r['place']=='1' for r in core)==p.results.count('1')==33
with (root/'docs/robokit-achievements.csv').open(encoding='utf-8-sig') as f:
 exported=list(csv.DictReader(f,delimiter=';'))
assert len(exported)==len(records)==92
for a,b in zip(records,exported):
 assert all(a[k]==b[k] for k in a if k!='sources')
 assert b['source_urls']==' | '.join(s['url'] for s in a['sources'])
 assert all(s['url'].startswith('https://') for s in a['sources'])
for url in ['https://starkit.su/','https://t.me/robofootball','https://vk.com/roboball']:assert url in p.refs
for path in root.glob('docs/*.pdf'):assert path.read_bytes().startswith(b'%PDF-')
print('PASS: 92 records, 83 humanoid results, 33 wins; CSV matches JSON; local links, anchors and PDFs present.')
