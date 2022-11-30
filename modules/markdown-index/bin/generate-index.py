import re
import os
import json
import sys
from base64 import b64encode


TOC_LIST_PREFIX = "-"
HEADER_LINE_RE = re.compile("^(#+)\s*(.*?)\s*(#+$|$)", re.IGNORECASE)
HEADER1_UNDERLINE_RE = re.compile("^-+$")
HEADER2_UNDERLINE_RE = re.compile("^=+$")


def strtobool(val):
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))


def toggles_block_quote(line):
    n_block_quote = line.count("```")
    return n_block_quote > 0 and line.count("```") % 2 != 0


def get_headers(file_data):
    in_block_quote = False
    results = []
    last_line = ""

    for line in file_data.splitlines():
        if toggles_block_quote(line):
            in_block_quote = not in_block_quote

        if in_block_quote:
            continue

        found_header = False
        header_level = 0

        match = HEADER_LINE_RE.match(line)
        if match is not None:
            header_level = len(match.group(1))
            title = match.group(2)
            found_header = True

        if not found_header:
            match = HEADER1_UNDERLINE_RE.match(line)
            if match is not None:
                header_level = 1
                title = last_line.rstrip()
                found_header = True

        if not found_header:
            match = HEADER2_UNDERLINE_RE.match(line)
            if match is not None:
                header_level = 2
                title = last_line.rstrip()
                found_header = True

        if found_header:
            results.append((header_level, title))

        last_line = line

    return results


class GenerateIndex:

    def __init__(self, docs_dir, markdown_files, headings, wikilinks):
        headings = strtobool(headings)
        wikilinks = strtobool(wikilinks)
        markdown_files = json.loads(markdown_files)
        base_len = len(docs_dir)
        base_level = docs_dir.count(os.sep)
        md_lines = []
        for root, files in markdown_files.items():
            level = root.count(os.sep) - base_level
            indent = '  ' * level
            if root != docs_dir:
                indent = '  ' * (level - 1)
                md_lines.append('{0} {2} **{1}/**\n'.format(indent, os.path.basename(root), TOC_LIST_PREFIX))
            
            rel_dir = '.{1}{0}'.format(os.sep, root[base_len:])
                                        
            for file_name, file_data in files.items():
                indent = '  ' * level
                if wikilinks:
                    md_lines.append('{0} {3} [[{2}{1}]]\n'.format(indent, os.path.splitext(file_name)[0], rel_dir, TOC_LIST_PREFIX))
                else:
                    md_lines.append('{0} {3} [{1}]({2}{1})\n'.format(indent, file_name, rel_dir, TOC_LIST_PREFIX))
                    if headings:
                        results = get_headers(file_data)
                        if len(results) > 0:
                            min_header_level = min(results, key=lambda e: e[0])[0]
                            for header in results:
                                header_level = header[0] - min_header_level + level + 2
                                indent = '  ' * header_level
                                md_lines.append("{}{} {}\n".format(indent, TOC_LIST_PREFIX, header[1]))
        
        self.md_lines = md_lines
    

    def generate(self):
        return os.linesep.join(self.md_lines)


    @classmethod
    def from_stdin(cls):
        inp = json.load(sys.stdin)
        return cls(**inp)


def main():
    gi = GenerateIndex.from_stdin()
    result = {
        "index": b64encode(json.dumps(gi.generate()).encode("utf-8")).decode("utf-8")
    }

    sys.stdout.write(json.dumps(result))


if __name__ == '__main__':
    main()