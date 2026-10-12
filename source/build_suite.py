from pathlib import Path
import re

folder = Path(__file__).parent
layout = (folder / 'suite-layout.html').read_text(encoding='utf-8')
navigation = '<nav aria-label="Website navigation"><a href="#home" data-page="home">HOME</a><a href="#portfolio" data-page="portfolio">PORTFOLIO</a><a href="#experience" data-page="experience">EXPERIENCE</a><a href="#about" data-page="about">ABOUT</a></nav>'
for page, filename in [('home', 'homepage-source.html'), ('portfolio', 'portfolio-source.html'), ('experience', 'experience-source.html'), ('about', 'about-source.html')]:
    content = (folder / filename).read_text(encoding='utf-8-sig')
    content = re.sub(r'<nav.*?</nav>', lambda _: navigation, content, flags=re.S)
    if page == 'home':
        content = content.replace('<button type="button" class="mp-primary">View portfolio</button>', '<button type="button" class="mp-primary" data-page="portfolio">View portfolio</button>')
        content = content.replace('<button type="button">View resume</button>', '<button type="button" data-page="experience">View resume</button>')
        content = content.replace('<span>LinkedIn</span><span>GitHub</span><span>Email</span>', '<a href="https://www.linkedin.com/in/thomas-serd" target="_blank" rel="noopener noreferrer">LinkedIn</a><a href="https://github.com/tserd-io" target="_blank" rel="noopener noreferrer">GitHub</a><a href="mailto:tom.serd@gmail.com">Email</a>')
    layout = layout.replace('__' + page.upper() + '__', content)
assert all('__' + page + '__' not in layout for page in ['HOME', 'PORTFOLIO', 'EXPERIENCE', 'ABOUT'])
assert layout.count('data-suite-page=') == 4
for script in re.findall(r'<script>(.*?)</script>', layout, re.S):
    assert 'window.openai' not in script
(folder / 'suite-source.html').write_text(layout, encoding='utf-8')
(folder / 'suite-check.js').write_text('\n'.join(re.findall(r'<script>(.*?)</script>', layout, re.S)), encoding='utf-8')
print('Suite assembled: four pages with shared navigation.')

