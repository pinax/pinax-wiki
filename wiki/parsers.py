import creole

from creole.html_emitter import HtmlEmitter

from .utils import binders_map, object_slug


class PinaxWikiHtmlEmitter(HtmlEmitter):

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
            if m.group('extern_addr'):
                return u'<a href="%s">%s</a>' % (
                    self.attr_escape(target), inside)
            elif m.group('inter_wiki'):
                raise NotImplementedError
        slug = object_slug(self.wiki)
        page_url = binders_map()[slug].page_url(self.wiki, target)
        return u'<a href="{0}">{1}</a>'.format(self.attr_escape(page_url), inside)


def creole_parse(wiki, text):
    return PinaxWikiHtmlEmitter(wiki, creole.Parser(text).parse()).emit()


def creole_wikiword_parse(wiki, text):
    rules = creole.Rules(wiki_words=True)
    return PinaxWikiHtmlEmitter(wiki, creole.Parser(text, rules).parse()).emit()
