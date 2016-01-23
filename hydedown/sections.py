#!/usr/bin/python
"""
Sections extension for Python Markdown
=========================================

This extension wraps paragraphs with headers inside `<section>` tags.

Single section:

    >>> import markdown
    >>> text = "# Some Header #"
    >>> md = markdown.markdown(text, ['attr_list', 'headerid', 'hydedown.sections'])
    >>> print md
    <section class="level1" id="section_some-header"><h1 id="some-header">Some Header</h1>
    </section>

Single section with id attribute:

    >>> import markdown
    >>> text = "# Some Header {@id=the_header}"
    >>> md = markdown.markdown(text, ['attr_list', 'headerid', 'hydedown.sections'])
    >>> print md
    <section class="level1" id="section_the_header"><h1 id="the_header">Some Header </h1>
    </section>

Single section with class attribute:

    >>> import markdown
    >>> text = "# Some Header {: .title #the_header}"
    >>> md = markdown.markdown(text, ['attr_list', 'headerid', 'hydedown.sections'])
    >>> print md
    <section class="level1 title" id="section_the_header"><h1 class="title" id="the_header">Some Header</h1>
    </section>

Two sections:

    >>> import markdown
    >>> text = '''
    ... # Some Header #
    ... Some text
    ... ## Some second level header
    ... Some more text
    ... '''
    >>> md = markdown.markdown(text, ['attr_list', 'headerid', 'hydedown.sections'])
    >>> print md
    <section class="level1 has1" id="section_some-header"><h1 id="some-header">Some Header</h1>
    <p>Some text</p>
    <section class="level2" id="section_some-second-level-header"><h2 id="some-second-level-header">Some second level header</h2>
    <p>Some more text</p>
    </section></section>

Three sections:

    >>> import markdown
    >>> text = '''
    ... # Some Header #
    ... Some text
    ... ## Some second level header
    ... Some more text
    ... ## Another second level header
    ... Even more text
    ... '''
    >>> md = markdown.markdown(text, ['attr_list', 'headerid', 'hydedown.sections'])
    >>> print md
    <section class="level1 has2" id="section_some-header"><h1 id="some-header">Some Header</h1>
    <p>Some text</p>
    <section class="level2" id="section_some-second-level-header"><h2 id="some-second-level-header">Some second level header</h2>
    <p>Some more text</p>
    </section><section class="level2" id="section_another-second-level-header"><h2 id="another-second-level-header">Another second level header</h2>
    <p>Even more text</p>
    </section></section>

Multiple level ones:

    >>> import markdown
    >>> text = '''
    ... # Some Header #
    ... Some text
    ... ## Some second level header
    ... Some more text
    ... ## Another second level header
    ... Even more text
    ... # Some Header Two #
    ... Some text two
    ... ## Some second level header Two
    ... Some more text two
    ... ### Third level header Two
    ... Even more text two
    ... '''
    >>> md = markdown.markdown(text, ['attr_list', 'headerid', 'hydedown.sections'])
    >>> print md
    <section class="level1 has2" id="section_some-header"><h1 id="some-header">Some Header</h1>
    <p>Some text</p>
    <section class="level2" id="section_some-second-level-header"><h2 id="some-second-level-header">Some second level header</h2>
    <p>Some more text</p>
    </section><section class="level2" id="section_another-second-level-header"><h2 id="another-second-level-header">Another second level header</h2>
    <p>Even more text</p>
    </section></section><section class="level1 has1" id="section_some-header-two"><h1 id="some-header-two">Some Header Two</h1>
    <p>Some text two</p>
    <section class="level2 has1" id="section_some-second-level-header-two"><h2 id="some-second-level-header-two">Some second level header Two</h2>
    <p>Some more text two</p>
    <section class="level3" id="section_third-level-header-two"><h3 id="third-level-header-two">Third level header Two</h3>
    <p>Even more text two</p>
    </section></section></section>


hgroup three headers:

    >>> import markdown
    >>> text = '''
    ... # Some Header #
    ... ## Some second level header
    ... Some more text
    ... ## Another second level header
    ... Even more text
    ... '''
    >>> md = markdown.markdown(text, ['attr_list', 'headerid', 'hydedown.sections'])
    >>> print md
    <section class="level1 has1" id="section_some-header"><hgroup class="level1" id="hgroup_some-header"><h1 id="some-header">Some Header</h1>
    <h2 id="some-second-level-header">Some second level header</h2>
    </hgroup><p>Some more text</p>
    <section class="level2" id="section_another-second-level-header"><h2 id="another-second-level-header">Another second level header</h2>
    <p>Even more text</p>
    </section></section>


hgroup level two:

    >>> import markdown
    >>> text = '''
    ... # Some Header #
    ... Some text
    ... ## Some second level header
    ... ## Another second level header
    ... Even more text
    ... '''
    >>> md = markdown.markdown(text, ['attr_list', 'headerid', 'hydedown.sections'])
    >>> print md
    <section class="level1 has1" id="section_some-header"><h1 id="some-header">Some Header</h1>
    <p>Some text</p>
    <section class="level2" id="section_some-second-level-header"><hgroup class="level2" id="hgroup_some-second-level-header"><h2 id="some-second-level-header">Some second level header</h2>
    <h2 id="another-second-level-header">Another second level header</h2>
    </hgroup><p>Even more text</p>
    </section></section>

Author:
Hyde contributors for the Hyde project(http://github.com/hyde)     2012-02-16

License: BSD (see ../docs/LICENSE for details)

Dependencies:
* [Python 2.4+](http://python.org)
* [Markdown 2.0+](http://www.freewisdom.org/projects/python-markdown/)

"""

import markdown
from markdown.util import etree

from collections import deque
from itertools import izip_longest, tee


def is_true(s, default=False):
    """ Convert a string to a booleen value. """
    s = str(s)
    if s.lower() in ['0', 'f', 'false', 'off', 'no', 'n']:
        return False
    elif s.lower() in ['1', 't', 'true', 'on', 'yes', 'y']:
        return True
    return default


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip_longest(a, b)


class SectionsAssember(object):

    def __init__(self, md, config):
        self.md = md
        self.config = config
        self.section_stack = []
        self.current_section = None
        self.current_level = 0
        self.class_prefix = self._get_config_value('class_prefix')
        self.max_level = int(self._get_config_value('max_level'))
        self.allheaders = ['h%d' % level for level in range(1, 7)]
        self.headers = ['h%d' % level for level in range(1, self.max_level+1)]

    def _get_config_value(self, key):
        try:
            val = self.md.Meta[key]
        except (AttributeError, KeyError):
            val = self.config[key]
        return val

    def get_level(self, header):
        return int(header.tag[-1])

    def get_atts_from_header(self, header, id_prefix):
        atts = {}
        header_id = header.get('id', None)
        if header_id:
            atts['id'] = id_prefix + header_id
        css_class = ''
        if self.class_prefix:
            css_class = '%s%d' % (self.class_prefix, self.get_level(header))
        header_class = header.get('class', None)
        if header_class:
            css_class = css_class + ' ' + header_class
        atts['class'] = css_class.strip()
        return atts

    def make_section(self, header, parent):
        atts = self.get_atts_from_header(header, 'section_')
        return etree.SubElement(parent, 'section', atts)

    def hgroup(self, first, second, parent):
        if parent.tag == 'hgroup':
            parent.append(second)
            return parent
        else:
            atts = self.get_atts_from_header(first, 'hgroup_')
            new_hgroup = etree.SubElement(parent, 'hgroup', atts)
            new_hgroup.append(first)
            new_hgroup.append(second)
            return new_hgroup

    def begin_section(self, header, parent):
        level = self.get_level(header)
        while (self.current_section is not None and
               self.current_level >= level):
                self.end_section()
        if self.current_section is not None:
            self.section_stack.append((self.current_section, self.current_level))
            parent = self.current_section
            css_classes = self.current_section.get('class', 'has0').split(' ')
            count = 0
            for css_class in css_classes:
                if css_class.startswith('has'):
                    count = int(css_class.replace('has', ''))
            has_class = 'has{count}'.format(count=count)
            if has_class in css_classes:
                css_classes.remove(has_class)
            count = count + 1
            css_classes.append('has' + str(count))
            self.current_section.set('class', ' '.join(css_classes))

        if parent is not None and header in parent:
            parent.remove(header)

        self.current_section = self.make_section(header, parent)
        self.current_level = level

    def end_section(self):
        if self.current_section is None:
            return
        if len(self.section_stack):
            self.current_section, self.current_level = self.section_stack.pop()
        else:
            self.current_level = 0
            self.current_section = None

    def remove_element(self, element, parents):
        for parent in parents:
            if parent is not None and element in parent:
                parent.remove(element)

    def assemble(self, elem):
        queue = deque()
        queue.append(elem)
        while True:
            try:
                section, hgroup, child = None, None, queue.popleft()
            except IndexError:
                break
            children = list(child)
            for first, second in pairwise(children):
                if hgroup is None and first.tag in self.headers:
                    self.begin_section(first, elem)
                    self.remove_element(first, {elem})
                    section = self.current_section
                    section.append(first)

                if first.tag in self.allheaders and\
                   second is not None and\
                   second.tag in self.allheaders:

                    self.remove_element(first, {section, elem})
                    self.remove_element(second, {section, elem})
                    hgroup = self.hgroup(first,
                                         second,
                                         hgroup
                                         if hgroup is not None
                                         else section)

                if first in elem and section is not None:
                    self.remove_element(first, {elem})
                    section.append(first)

                if second is None or second.tag not in self.allheaders:
                    hgroup = None

                queue.append(first)


class SectionsTreeprocessor(markdown.treeprocessors.Treeprocessor):

    def __init__(self):
        markdown.treeprocessors.Treeprocessor.__init__(self)

    def run(self, doc):
        """
        Look for a header. If found begin a section block.
        """
        assember = SectionsAssember(self.md, self.config)
        assember.assemble(doc)


class SectionsExtension(markdown.Extension):

    def __init__(self, configs):
        # set defaults
        self.config = {
                'max_level': ['3', 'Maximum header level for adding sections.'],
                'class_prefix': ['level', 'Prefix for section\'s class attribute.']
            }

        for key, value in configs:
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        """ Add SectionsTreeProcessor to the Markdown instance. """
        md.registerExtension(self)
        self.processor = SectionsTreeprocessor()
        self.processor.md = md
        self.processor.config = self.getConfigs()
        md.treeprocessors.add('sections',
                              self.processor,
                              "_end")


def makeExtension(**configs):
    return SectionsExtension(configs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
