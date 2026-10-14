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
assert len(core)==len(p.results)==94
assert sum(r['place']=='1' for r in core)==p.results.count('1')==38
with (root/'docs/robokit-achievements.csv').open(encoding='utf-8-sig') as f:
 exported=list(csv.DictReader(f,delimiter=';'))
assert len(exported)==len(records)==104
for a,b in zip(records,exported):
 assert all(a[k]==b[k] for k in a if k!='sources')
 assert b['source_urls']==' | '.join(s['url'] for s in a['sources'])
 assert all(s['url'].startswith('https://') for s in a['sources'])
for url in ['https://starkit.su/','https://t.me/robofootball','https://vk.com/roboball']:assert url in p.refs
for path in root.glob('docs/*.pdf'):assert path.read_bytes().startswith(b'%PDF-')
print('PASS: 104 records, 94 humanoid results, 38 wins; CSV matches JSON; local links, anchors and PDFs present.')
from collections import Counter
stats=json.loads((root/'data/award-statistics.json').read_text())
fields={'1':'first','2':'second','3':'third','III степень':'degree_iii','победа':'victory_unspecified','призёр':'prize_unspecified'}
for label,rr in [('core',core),('all',records)]:
 c=Counter(r['place'] for r in rr)
 assert stats[label]['records']==len(rr)
 for result,field in fields.items():assert stats[label][field]==c[result]
for year,s in stats['by_year'].items():
 rr=[r for r in records if r['year']==year];assert s['records']==len(rr)
 for result,field in fields.items():assert s[field]==sum(r['place']==result for r in rr)
assert sum(s['records'] for s in stats['by_scope'].values())==len(records)
print('PASS: statistics reconcile by year, scope and award type.')

from lxml import html
import re
for name,lang in [('index.html','ru'),('en.html','en')]:
 doc=html.parse(str(root/name)); page=Page();page.feed((root/name).read_text())
 assert doc.getroot().get('lang')==lang
 assert len(page.results)==94 and page.results.count('1')==38
 assert not doc.xpath('//*[contains(@class,"scope-heading")]')
 for u in page.refs:
  parts=urlsplit(u)
  if not parts.scheme and not parts.netloc:
   if parts.path:assert (root/unquote(parts.path)).is_file(),u
   elif parts.fragment:assert parts.fragment in page.ids,u
 if lang=='en':
  assert not re.search('[А-Яа-яЁё]', ' '.join(doc.xpath('//text()[not(ancestor::script) and not(ancestor::style)]')))
 assert len(doc.xpath('//article[@class="competition-item"]'))==27
 assert sum(int(x) for x in doc.xpath('//*[@class="stats-table"]/tbody/tr[last()]/td/text()')[:3])==98
print('PASS: RU/EN pages, 94 results each, 27 events, navigation and English UI.')
