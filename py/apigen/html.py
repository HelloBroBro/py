
from py.xml import html

# HTML related stuff
class H(html):
    class Content(html.div):
        pass # style = html.Style(margin_left='15em')

    class Description(html.div):
        pass
    
    class NamespaceDescription(Description):
        pass

    class NamespaceItem(html.div):
        pass

    class NamespaceDef(html.h1):
        pass

    class ClassDescription(Description):
        pass

    class ClassDef(html.h1):
        pass

    class MethodDescription(Description):
        pass

    class MethodDef(html.h2):
        pass

    class FunctionDescription(Description):
        def __init__(self, localname, argdesc, docstring, valuedesc, csource,
                     callstack):
            fd = H.FunctionDef(localname, argdesc)
            ds = H.Docstring(docstring or '*no docstring available*')
            fi = H.FunctionInfo(valuedesc, csource, callstack)
            super(H.FunctionDescription, self).__init__(fd, ds, fi)

    class FunctionDef(html.h2):
        def __init__(self, name, argdesc):
            super(H.FunctionDef, self).__init__('def %s%s:' % (name, argdesc))

    class FunctionInfo(html.div):
        def __init__(self, valuedesc, csource, callstack):
            super(H.FunctionInfo, self).__init__(
                H.Hideable('funcinfo', 'funcinfo', valuedesc, csource,
                           callstack))

    class ParameterDescription(html.div):
        pass

    class Docstring(html.pre):
        style = html.Style(width='100%')
        pass

    class Navigation(html.div):
        #style = html.Style(min_height='99%', float='left', margin_top='1.2em',
        #                   overflow='auto', width='15em', white_space='nowrap')
        pass

    class NavigationItem(html.div):
        def __init__(self, linker, linkid, name, indent, selected):
            href = linker.get_lazyhref(linkid)
            super(H.NavigationItem, self).__init__((indent * 2 * u'\xa0'),
                                                 H.a(name, href=href))
            if selected:
                self.attr.class_ = 'selected'

    class BaseDescription(html.a):
        pass

    class SourceSnippet(html.div):
        def __init__(self, text, href, sourceels=None):
            if sourceels is None:
                sourceels = []
            link = text
            if href:
                link = H.a(text, href=href)
            super(H.SourceSnippet, self).__init__(
                link, H.div(class_='code', *sourceels))
    
    class SourceDef(html.div):
        pass

    class NonPythonSource(html.pre):
        pass # style = html.Style(margin_left='15em')

    class DirList(html.div):
        pass # style = html.Style(margin_left='15em')

    class DirListItem(html.div):
        pass

    class ValueDescList(html.ul):
        def __init__(self, *args, **kwargs):
            super(H.ValueDescList, self).__init__(*args, **kwargs)

    class ValueDescItem(html.li):
        pass

    class CallStackDescription(Description):
        def __init__(self, callstackdiv):
            super(H.CallStackDescription, self).__init__(
                H.Hideable('callsites', 'callsites', csdiv))

    class CallStackItem(html.div):
        def __init__(self, filename, lineno, traceback):
            super(H.CallStackItem, self).__init__(
                H.Hideable("stack trace %s - line %s" % (filename, lineno),
                           'callstackitem', traceback))

    class Hideable(html.div):
        def __init__(self, name, class_, *content):
            super(H.Hideable, self).__init__(
                H.div(H.a('show/hide %s' % (name,),
                          href='#',
                          onclick=('showhideel(getnextsibling(this));'
                                   'return false;')),
                      H.div(style='display: none',
                            class_=class_,
                            *content)))
