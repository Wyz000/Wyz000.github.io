#!/usr/bin/env python3
"""Build the academic pages using only the Python standard library."""
from pathlib import Path
from html import escape
from urllib.parse import quote
import json
from hashlib import sha256
import re

ROOT = Path(__file__).resolve().parents[1]
PROFILE = json.loads((ROOT / 'data/profile.json').read_text())
PAPERS = json.loads((ROOT / 'data/publications.json').read_text())
NEWS = json.loads((ROOT / 'data/news.json').read_text())
IMAGE_SOURCES = json.loads((ROOT / 'assets/images/mapping.json').read_text())
CSS_VERSION = sha256((ROOT / 'assets/css/site.css').read_bytes()).hexdigest()[:10]
E = lambda value: escape(str(value), quote=True)
AUTHOR_LEGEND = '<p class="author-legend">* co-first author with equal contribution; # Corresponding author.</p>'

ICONS = {
    'email': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
    'scholar': '<path d="m2 9 10-6 10 6-10 6L2 9Z"/><path d="M6 12v5c4 3 8 3 12 0v-5M22 9v8"/>',
    'github': '<path d="M9 19c-4 1-4-2-6-2m12 5v-4c0-1-.3-2-1-2.5 3-.3 6-1.5 6-6A5 5 0 0 0 19 6a5 5 0 0 0 0-4s-1 0-4 2a13 13 0 0 0-6 0C6 2 5 2 5 2a5 5 0 0 0 0 4 5 5 0 0 0-1 3.5c0 4.5 3 5.7 6 6-.7.5-1 1.5-1 2.5v4"/>',
    'moon': '<path d="M20.5 13A9 9 0 0 1 11 3.5 9 9 0 1 0 20.5 13Z"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/>',
    'menu': '<path d="M4 6h16M4 12h16M4 18h16"/>'
}

def icon(name, css=''):
    return f'<svg class="{E(css)}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

def social_links():
    return '<div class="socials">' + ''.join(
        f'<a href="{E(url)}">{icon(key)}<span>{label}</span></a>'
        for key, label, url in [
            ('email', 'Email', 'mailto:' + PROFILE['email']),
            ('scholar', 'Google Scholar', PROFILE['scholar']),
            ('github', 'GitHub', PROFILE['github'])
        ]) + '</div>'

def shell(page, body, description):
    base = './' if page == 'about' else '../'
    paths = {'about': '', 'publications': 'publications/', 'mentoring': 'mentoring/', 'cv': 'cv/'}
    nav = ''.join(f'<a href="{base}{path}"'+(' aria-current="page"' if name == page else '')+f'>{name}</a>' for name, path in paths.items())
    title = 'Yuze Wu · 吴钰泽' if page == 'about' else f'{page.capitalize()} · Yuze Wu'
    canonical = PROFILE['url'] + '/' + paths[page]
    schema = json.dumps({'@context':'https://schema.org','@type':'Person','name':'Yuze Wu','alternateName':'吴钰泽','url':PROFILE['url'],'jobTitle':[PROFILE['role'],PROFILE['academic_role']],'affiliation':[{'@type':'Organization','name':PROFILE['organization'],'url':PROFILE['organization_url']},{'@type':'CollegeOrUniversity','name':'Zhejiang University'}],'alumniOf':{'@type':'CollegeOrUniversity','name':'Zhejiang University'},'sameAs':[PROFILE['scholar'],PROFILE['github']]},ensure_ascii=False)
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(description)}"><meta name="author" content="Yuze Wu">
<link rel="canonical" href="{E(canonical)}"><meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{E(canonical)}"><meta property="og:image" content="{PROFILE['url']}/assets/images/yuze-wu.jpg">
<meta name="theme-color" content="#ffffff"><link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
<script>try{{const t=localStorage.getItem('theme');document.documentElement.dataset.theme=t||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}}catch(e){{}}</script>
<link rel="stylesheet" href="{base}assets/css/site.css?v={CSS_VERSION}"><script src="{base}assets/js/site.js" defer></script>
<script type="application/ld+json">{schema}</script></head>
<body><a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap header-inner"><a class="brand" href="{base}" aria-label="Yuze Wu home"><strong>Yuze Wu</strong></a>
<div class="header-right"><nav id="site-nav" aria-label="Main navigation" data-menu>{nav}</nav>
<button class="icon-button" type="button" data-theme-toggle aria-label="Switch to dark theme">{icon('moon','moon')}{icon('sun','sun')}</button>
<button class="icon-button menu-button" type="button" data-menu-toggle aria-label="Toggle navigation" aria-expanded="false" aria-controls="site-nav">{icon('menu')}</button></div></div></header>
<main id="main" class="wrap">{body}</main>
<footer class="site-footer"><div class="wrap footer-inner"><span>© 2026 <strong>Yuze Wu · <span lang="zh-CN">吴钰泽</span></strong><br>Foundation Model Lead · <a href="{PROFILE['organization_url']}">Differential Robotics</a></span><span>Layout inspired by <a href="https://github.com/alshedivat/al-folio">al-folio</a> · <a href="{base}assets/images/CREDITS.txt">Figure credits</a><br>Original site based on <a href="https://jonbarron.info/">Jon Barron</a> · Updated {E(PROFILE['updated'])}</span></div></footer></body></html>'''

def bibtex(paper):
    kind = 'article' if paper['venue'] == 'arXiv' or 'Letters' in paper['venue'] or 'Nature' in paper['venue'] or 'Science' in paper['venue'] or 'Transactions' in paper['venue'] else 'inproceedings'
    parts = [f"@{kind}{{{paper['id']},", f"  title = {{{{{paper['title']}}}}},", f"  author = {{{' and '.join(paper['authors'])}}},", f"  year = {{{paper['year']}}},"]
    parts.append(f"  {'journal' if kind == 'article' else 'booktitle'} = {{{paper['venue']}}},")
    for key in ['doi', 'volume', 'number', 'pages']:
        if paper.get(key): parts.append(f"  {key} = {{{paper[key]}}},")
    if paper.get('arxiv'): parts.extend([f"  eprint = {{{paper['arxiv']}}},", '  archivePrefix = {arXiv},'])
    if paper.get('paper'): parts.append(f"  url = {{{paper['paper']}}}")
    else: parts.append('  note = {Accepted; final publication details forthcoming}')
    parts.append('}')
    return '\n'.join(parts)

def paper_card(paper, base='./', compact=False):
    title = E(paper['title'])
    show_co_first = 'Yuze Wu' in (paper.get('co_first_authors') or [])
    show_corresponding = 'Yuze Wu' in (paper.get('corresponding_authors') or [])
    author_names = []
    for author in paper['authors']:
        name = '<strong>Yuze Wu</strong>' if author == 'Yuze Wu' else E(author)
        markers, descriptions = [], []
        if show_co_first and author in (paper.get('co_first_authors') or []):
            markers.append('*'); descriptions.append('co-first author with equal contribution')
        if show_corresponding and author in (paper.get('corresponding_authors') or []):
            markers.append('#'); descriptions.append('Corresponding author')
        if markers:
            name += f'<sup class="author-mark" aria-label="{E("; ".join(descriptions))}" title="{E("; ".join(descriptions))}">{",".join(markers)}</sup>'
        author_names.append(name)
    author_html = ', '.join(author_names)
    target = paper.get('project') or paper.get('paper') or paper.get('related_preprint')
    if paper.get('image'):
        image_alt = E(paper.get('image_alt') or paper['title'])
        image = f'<img src="{base}{E(paper["image"])}" data-poster="{base}{E(paper["image"])}" alt="{image_alt}" width="{paper.get("image_width",540)}" height="{paper.get("image_height",348)}" loading="lazy" decoding="async">'
        if paper.get('old_image'):
            media = f'<button type="button" class="pub-media" data-demo="{PROFILE["url"]}/{quote(paper["old_image"])}" aria-label="Play demonstration: {title}" aria-pressed="false">{image}</button>'
        else:
            media = f'<a class="pub-media" href="{E(target)}" aria-label="View {title}">{image}</a>' if target else f'<div class="pub-media">{image}</div>'
    else:
        artwork = E(paper.get('label','Research')).replace(chr(10),'<br>')
        media = f'<a class="pub-art" href="{E(target)}" aria-label="Read {title}">{artwork}</a>' if target else f'<div class="pub-art">{artwork}</div>'
    links = ''.join(f'<a class="pub-link" href="{E(paper[key])}">{label}</a>' for key, label in [('paper','Paper'),('pdf','PDF'),('project','Project'),('code','Code'),('video','Video'),('related_preprint','Earlier version: VLA-AN')] if paper.get(key))
    venue = f'{E(paper["venue"])} · {paper["year"]}'
    if paper['status']=='preprint': venue += ' · Preprint'
    elif paper['status']=='accepted': venue += ' · Accepted'
    details = '' if compact or not paper.get('paper') else f'<details class="pub-details"><summary>BibTeX</summary><pre id="bib-{paper["id"]}">{E(bibtex(paper))}</pre><button class="outline-button" type="button" data-copy="bib-{paper["id"]}">Copy BibTeX</button></details>'
    search = ' '.join([paper['title'],*paper['authors'],str(paper['year']),paper['venue'],paper.get('summary','')]).lower()
    heading = f'<a href="{E(paper["paper"])}">{title}</a>' if paper.get('paper') else title
    summary = '' if compact else f'<p class="summary">{E(paper.get("summary",""))}</p>'
    return f'''<article class="pub" id="{E(paper['id'])}" data-publication data-category="{E(paper['category'])}" data-search="{E(search)}">{media}<div class="pub-info"><h3>{heading}</h3><div class="authors">{author_html}</div><p class="venue"><em>{venue}</em></p>{summary}<div class="pub-links">{links}</div>{details}</div></article>'''

def news_items(items):
    rows = []
    for item in items:
        text = E(item['text'])
        for link in item.get('links', []):
            text = text.replace(E(link['label']), f'<a href="{E(link["url"])}">{E(link["label"])}</a>', 1)
        rows.append(f'<li><time datetime="{E(item["date"])}">[{E(item["label"])}]</time> <span>{text}</span></li>')
    return '<ul class="news-list">' + ''.join(rows) + '</ul>'

def about():
    selected = [
        'hiarm-2026', 'vln-ar-2026', 'diffwam-2026',
        'dynamic-grasp-2026', 'force-grasp-2026', 'shape-adaptive-2025',
        'ring-rotor-2023', 'pathpainter-2026', 'navdreamer-2026',
        'navgen-2026', 'flymirage-2026', 'd-vlc-2026', 'navfom-2026'
    ]
    by_id = {paper['id']:paper for paper in PAPERS}
    cards = ''.join(paper_card(by_id[key],compact=True) for key in selected if key in by_id)
    return f'''<div class="about-body"><figure class="portrait"><img src="./assets/images/yuze-wu.jpg" alt="Yuze Wu" width="400" height="400" fetchpriority="high"><figcaption>Embodied intelligence &amp;<br>robot foundation models</figcaption></figure>
<h1 class="profile-name">Yuze Wu <span class="name-zh" lang="zh-CN">吴钰泽</span></h1>
<p class="subtitle">Foundation Model Lead · <a href="{PROFILE['organization_url']}">Differential Robotics <span lang="zh-CN">微分智飞</span></a></p>
<div class="intro"><p>I received my Ph.D. in Control Science and Engineering from <strong>Zhejiang University (ZJU)</strong> in 2026, advised by <a href="http://zju-fast.com/research-group/fei-gao/">Prof. Fei Gao</a> at <a href="http://zju-fast.com/">FAST Lab</a>. Previously, I earned my B.Eng. in Automation from ZJU in 2021. During my studies, I received the Zhejiang University First-Class Scholarship and was named an Outstanding Graduate of Zhejiang Province. As a core team member, I also helped lead a Young Scientist Project under China’s National Key R&amp;D Program.</p>
<p>I am currently the <strong>Foundation Model Lead</strong> at <a href="{PROFILE['organization_url']}">Differential Robotics</a> and a <strong>postdoctoral researcher in a joint program between Differential Robotics and Zhejiang University</strong>. I lead research on embodied intelligence and large-scale AI models, focusing on <strong>robot foundation models, world models, embodied robot swarms, reinforcement learning, and planning &amp; control</strong> for real-world robots. I also <a href="./mentoring/">mentor students</a> and welcome research discussions and collaborations.</p></div>
{social_links()}</div>
<section class="section" aria-labelledby="news-title"><h2 id="news-title">News</h2>{news_items(NEWS[:8])}<details class="earlier-news"><summary>Earlier news</summary>{news_items(NEWS[8:])}</details></section>
<section class="section" aria-labelledby="selected-title"><div class="section-heading"><h2 id="selected-title">Selected publications</h2><a href="./publications/">View publications →</a></div>{AUTHOR_LEGEND}<div class="pub-list">{cards}</div></section>
<section class="section" aria-labelledby="honors-title"><h2 id="honors-title">Honors &amp; awards</h2><ul class="compact-list">{''.join('<li>'+E(award)+'</li>' for award in PROFILE['honors'])}</ul></section>
<section class="section" aria-labelledby="education-title"><h2 id="education-title">Education</h2><ul class="compact-list education-list"><li><span class="education-date">2021.09 – 2026.06</span> <strong>Ph.D. in Control Science and Engineering</strong>, Zhejiang University. <span class="quiet-note">Advisor: Prof. Fei Gao.</span></li><li><span class="education-date">2017.09 – 2021.06</span> <strong>B.Eng. in Automation</strong>, Zhejiang University.</li></ul></section>
<section class="section" aria-labelledby="notes-title"><h2 id="notes-title">Research notes</h2><p class="research-note"><a href="https://wyz000.github.io/blog/gpt6-astra-navigation/">GPT-6 Astra for embodied navigation</a> <span class="quiet-note">— experiments and demonstrations</span></p></section>'''

def publications():
    groups = ''
    for year in sorted({paper['year'] for paper in PAPERS},reverse=True):
        cards = ''.join(paper_card(paper,'../') for paper in PAPERS if paper['year']==year)
        groups += f'<section class="pub-group" aria-labelledby="year-{year}"><h2 class="year-heading" id="year-{year}">{year}</h2><div class="pub-list">{cards}</div></section>'
    return f'''<h1>publications</h1><p class="page-intro">Research on embodied foundation models, world models, embodied robot swarms, and aerial robotics. Preprints are labeled separately from peer-reviewed work. See also <a href="{PROFILE['scholar']}">Google Scholar</a>.</p>{AUTHOR_LEGEND}<div class="pub-controls"><label class="sr-only" for="publication-search">Search publications by title, author, venue or year</label><input class="search-box" type="search" id="publication-search" placeholder="Search by title, author, venue or year…" autocomplete="off"><div class="filters" role="group" aria-label="Filter by research area"><button class="filter" type="button" data-filter="all" aria-pressed="true">All research</button><button class="filter" type="button" data-filter="models" aria-pressed="false">Foundation &amp; world models</button><button class="filter" type="button" data-filter="robotics" aria-pressed="false">Aerial robotics &amp; control</button></div><p class="results-count" id="results-count" aria-live="polite">{len(PAPERS)} publications</p></div>{groups}<p class="empty" id="empty-results" hidden>No publications match this search. Try another title, author or year.</p>'''

def mentoring():
    return f'''<h1>mentoring &amp; collaboration</h1><p class="page-intro">Connecting research ideas with working robotic systems.</p><div class="text-content"><section class="section"><h2>research directions</h2><p>I mentor students working on embodied intelligence and robotics, with a focus on:</p><ul><li><strong>Robot foundation models:</strong> vision-language-action models, language-conditioned navigation, and generalization across environments.</li><li><strong>World models:</strong> visual prediction, generative data, and learning representations that support embodied decisions.</li><li><strong>Embodied robot swarms:</strong> coordination, collaborative perception, and decision-making across robot teams.</li><li><strong>Robot learning and control:</strong> reinforcement learning, planning, adaptive control, and real-world aerial manipulation.</li></ul></section><section class="section"><h2>working together</h2><p>I am interested in research that brings learning and physical interaction together—from model design and simulation to experiments on real robots.</p><p>If you would like to discuss a research idea or potential collaboration, email me with a brief introduction, your research interests, and links to relevant projects or publications.</p><p><a href="mailto:{PROFILE['email']}">{PROFILE['email']}</a></p></section></div>'''

def cv():
    return f'''<div class="cv-title"><h1>curriculum vitae</h1><button class="outline-button print-button" type="button" data-print>Print / save PDF</button></div><p class="page-intro"><strong>Yuze Wu <span lang="zh-CN">吴钰泽</span></strong> · <a href="mailto:{PROFILE['email']}">{PROFILE['email']}</a></p><section class="section"><h2>experience</h2><div class="cv-entry"><time>Current</time><div><h3>Foundation Model Lead</h3><p><a href="{PROFILE['organization_url']}">Differential Robotics · 微分智飞</a></p><p>Leading research and development on embodied intelligence and foundation models; mentoring students in related research.</p></div></div><div class="cv-entry"><time>Current</time><div><h3>Postdoctoral Researcher</h3><p>Joint program · Differential Robotics &amp; Zhejiang University</p><p lang="zh-CN">微分智飞与浙江大学联合培养博士后</p></div></div><div class="cv-entry"><time>Jul 2022 – Jan 2023</time><div><h3>Planning &amp; Control Intern</h3><p>DJI · Flight Systems</p><p>Neural-network-based adaptive control, flight-data collection, model deployment and real-world evaluation.</p></div></div></section><section class="section"><h2>education</h2><div class="cv-entry"><time>2021 – 2026</time><div><h3>Ph.D. in Control Science and Engineering</h3><p>Zhejiang University · FAST Lab</p><p>Advisor: Prof. Fei Gao</p></div></div><div class="cv-entry"><time>2017 – 2021</time><div><h3>B.Eng. in Automation</h3><p>Zhejiang University</p></div></div></section><section class="section text-content"><h2>research</h2><p>Embodied intelligence, robot foundation models, world models, embodied robot swarms, reinforcement learning, motion planning, adaptive control, and aerial manipulation.</p><p>For papers and project resources, see the <a href="../publications/">publications page</a> and <a href="{PROFILE['scholar']}">Google Scholar</a>.</p></section>'''

PAGES = {
    'about': (ROOT / 'index.html',about,'Yuze Wu (吴钰泽), Foundation Model Lead at Differential Robotics and joint postdoctoral researcher with Zhejiang University. Research in embodied intelligence, world models, embodied robot swarms, robot learning and aerial robotics.'),
    'publications': (ROOT / 'publications/index.html',publications,'Publications by Yuze Wu on embodied foundation models, world models, robot swarms, navigation and aerial robotics.'),
    'mentoring': (ROOT / 'mentoring/index.html',mentoring,'Student mentoring and research collaboration with Yuze Wu in embodied intelligence, foundation models, and robot swarms.'),
    'cv': (ROOT / 'cv/index.html',cv,'Academic and professional background of Yuze Wu, Foundation Model Lead at Differential Robotics and joint postdoctoral researcher with Zhejiang University.')
}
if __name__=='__main__':
    for page,(path,render,description) in PAGES.items():
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(shell(page,render(),description),encoding='utf-8')
        print(path.relative_to(ROOT))
    credits = ['Figure credits', '==============', '', 'Thumbnails reproduce original paper figures or author project media. Figures are resized for the website and cropped to complete panels where noted. Scientific content is unchanged.', '']
    image_sources = {entry['thumbnail']: entry for entry in IMAGE_SOURCES.values()}
    for paper in PAPERS:
        source = image_sources.get(paper.get('image'), {})
        credits.extend([paper['title'], 'Authors: ' + ', '.join(paper['authors']), 'Thumbnail: ' + paper.get('image', '')])
        for label, value in [('Figure', source.get('figure')), ('Paper / source page', source.get('source_page') or paper.get('paper')), ('Image source', source.get('source_url') or source.get('url') or source.get('source')), ('Attribution', source.get('credit')), ('License', source.get('license')), ('License URL', source.get('license_url')), ('Processing', source.get('processing') or source.get('note'))]:
            if value: credits.append(label + ': ' + str(value))
        credits.append('')
    credits.extend(['Profile photograph: Yuze Wu, from his original personal homepage.', 'https://wyz000.github.io/photo/self.jpg', ''])
    (ROOT/'assets/images/CREDITS.txt').write_text('\n'.join(credits),encoding='utf-8')
    (ROOT/'publications/papers.bib').write_text('\n\n'.join(bibtex(paper) for paper in PAPERS if paper.get('paper'))+'\n')
    (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{PROFILE["url"]}/{"" if key=="about" else key+"/"}</loc></url>' for key in PAGES)+'</urlset>')
    (ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {PROFILE["url"]}/sitemap.xml\n')
