#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import re

class Line:

    not_content = "^\d\d:\d\d -!-"
    
    #            timestamp      username     text
    line_re = "^(\d\d:\d\d)\s*<([\s@]\w+)>\s*(.*)"
    fallback_re = "^(\d\d:\d\d)\s*(.*)"

    def __init__(self, text):
        self.text = text.strip()
        self.is_content = re.match(self.not_content, self.text) is None

        ma = re.match(self.line_re, self.text)
        if ma is not None:
            self.timestamp = ma.group(1)
            self.username = ma.group(2)
            self.text = ma.group(3)
            return

        ma = re.match(self.fallback_re, self.text)
        if ma is not None:
            self.timestamp = ma.group(1)
            self.username = ""
            self.text = ma.group(2)
            return

        self.timestamp = ""
        self.username = ""




def render(lines, out_fn, content_only):
    env = Environment(loader=FileSystemLoader("."))
    log_template = env.get_template("log.template.html")

    with open(out_fn, 'w') as file:
        file.write(log_template.render(lines=lines, content_only=content_only))


def parse(fn):
    with open(fn) as file:
        lines = [Line(line) for line in file]
    return lines

def main():
    lines = parse('Freenode/#fah.log')
    render(lines, 'log.html', content_only=False)
    render(lines, 'log.content.html', content_only=True)

if __name__ == "__main__":
    main()
