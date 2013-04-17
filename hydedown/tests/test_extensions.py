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
            'output.\n\n%s' % (ext_name, ''.join(diff))
        )

def test_section():
    return check_extension('sections')