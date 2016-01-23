import codecs
import difflib
import os.path

import markdown

HERE = os.path.dirname(__file__)


def file_here(fname):
    return os.path.join(HERE, fname)

kwargs = {
    "sections": {
        "extensions": [
            'hydedown.sections',
            'headerid'
        ]
    }
}


def check_extension(ext_name):
    with codecs.open(file_here(ext_name + '.txt'), encoding="utf-8") as f:
        input = f.read()
    with codecs.open(file_here(ext_name + '.html'), encoding="utf-8") as f:
        expected = f.read()

    out = markdown.markdown(input, **kwargs[ext_name])
    diff = [l for l in difflib.unified_diff(expected.splitlines(True),
                                            out.splitlines(True),
                                            n=3)]
    if diff:
        raise Exception('Output for extension "%s" failed to match expected '
                        'output.\n\n%s' % (ext_name, ''.join(diff)))


def test_sections():
    return check_extension('sections')


def test_sections_simple():
    md = """
# Heading 1
## Heading 1.1
### Heading 1.1.1

Some text

## Heading 1.2

Some more text

## Heading 1.3
### Heading 1.3.1

Some more stuff

# Heading 2

New stuff

## Heading 2.1

Some more new stuff

"""
    html = """
<section class="level1 has2" id="section_heading-1"><hgroup class="level1" id="hgroup_heading-1"><h1 id="heading-1">Heading 1</h1>
<h2 id="heading-11">Heading 1.1</h2>
<h3 id="heading-111">Heading 1.1.1</h3>
</hgroup><p>Some text</p>
<section class="level2" id="section_heading-12"><h2 id="heading-12">Heading 1.2</h2>
<p>Some more text</p>
</section><section class="level2" id="section_heading-13"><hgroup class="level2" id="hgroup_heading-13"><h2 id="heading-13">Heading 1.3</h2>
<h3 id="heading-131">Heading 1.3.1</h3>
</hgroup><p>Some more stuff</p>
</section></section><section class="level1 has1" id="section_heading-2"><h1 id="heading-2">Heading 2</h1>
<p>New stuff</p>
<section class="level2" id="section_heading-21"><h2 id="heading-21">Heading 2.1</h2>
<p>Some more new stuff</p>
</section></section>""".strip()

    out = markdown.markdown(md, **kwargs['sections'])
    diff = [l for l in difflib.unified_diff(html.splitlines(True),
                                            out.splitlines(True),
                                            n=3)]
    if diff:
        raise Exception('Output for extension sections failed to match expected '
                        'output.\n\n%s' % ''.join(diff))
