#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import re

class Pages:
    def __init__(self):
        self.pages = [
                LogPage(filter='content'),
                LogPage(filter='all'),
                AboutPage()
        ]

    def render(self, lines):
        for page in self.pages:
            page.active = "active"
            page.render(self, lines)
            page.active = ""

    def __iter__(self):
        yield from self.pages

class Page:
    def render(self, pages, lines):
        env = Environment(loader=FileSystemLoader("templates/"))
        log_template = env.get_template(self.template_fn)

        with open("out/{}".format(self.out_fn), 'w') as file:
            file.write(log_template.render(pages=pages, page=self, lines=lines))

class LogPage(Page):
    template_fn = 'log.html'
    
    def __init__(self, filter):
        assert filter in ['content', 'all']
        self.filter = filter

    def use_line(self, line):
        if self.filter == 'content':
            return line.is_content
        else:
            return True

    @property
    def title(self):
        if self.filter == 'content':
            return "#fah Log (Content only)"
        else:
            return "#fah Log (All)"

    @property
    def description(self):
        return "Folding@Home IRC logs"

    @property
    def out_fn(self):
        if self.filter == 'content':
            return "log.content.html"
        else:
            return "log.all.html"

class AboutPage(Page):
    template_fn = 'about.html'
    title = 'About #fah Log'
    description = "About the Folding@Home IRC logs"
    out_fn = "about.html"

class Line:
    not_content_re = "^\d\d:\d\d -!-"
    
    #            timestamp      username         text
    line_re = "^(\d\d:\d\d)\s*<([\s@][\w\-]+)>\s*(.*)"

    #                timestamp    text
    fallback_re = "^(\d\d:\d\d)\s*(.*)"

    def __init__(self, text):
        self.text = text.strip()
        self.is_content = re.match(self.not_content_re, self.text) is None

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

def parse(fn):
    with open(fn) as file:
        lines = [Line(line) for line in file]
    return list(reversed(lines))

def main():
    lines = parse('Freenode/#fah.log')
    Pages().render(lines)

if __name__ == "__main__":
    main()
