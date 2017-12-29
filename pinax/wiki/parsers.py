from __future__ import unicode_literals

import creole

from .utils import binders_map, object_slug


class PinaxWikiHtmlEmitter(creole.HtmlEmitter):

    def __init__(self, wiki, root, link_rules=None):
        self.wiki = wiki
        super(PinaxWikiHtmlEmitter, self).__init__(root, link_rules)

    def link_emit(self, node):
        target = node.content
        if node.children:
            inside = self.emit_children(node)
        else:
            inside = self.html_escape(target)
        m = self.link_rules.addr_re.match(target)
        if m:
            if m.group("extern_addr"):
                return '<a href="{}">{}</a>'.format(self.attr_escape(target), inside)
            elif m.group("inter_wiki"):
                raise NotImplementedError
        slug = object_slug(self.wiki)
        page_url = binders_map()[slug].page_url(self.wiki, target)
        return '<a href="{}">{}</a>'.format(self.attr_escape(page_url), inside)


def creole_parse(wiki, text):
    document = creole.CreoleParser(text, blog_line_breaks=True).parse()
    return PinaxWikiHtmlEmitter(wiki, document).emit()
