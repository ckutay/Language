try:
    from docutils import core
    from docutils import nodes
    from docutils.readers import standalone
    from docutils.transforms import Transform
    from docutils.writers.html4css1 import Writer, HTMLTranslator
    
    class WikiLinkResolver(nodes.SparseNodeVisitor):
        ":Ignore: yes"
    
        def visit_reference(self, node):
            if node.resolved or not node.hasattr('refname'):
                return
            wikiname = node['name']
            node.resolved = 1
            node['class'] = 'wiki'
            node['refuri'] = URL(r=request,c='plugin_wiki', f='page',args=[wikiname])
            del node['refname']
    
    class WikiLink(Transform):
        ":Ignore: yes"
    
        default_priority = 800
    
        def apply(self):
            visitor = WikiLinkResolver(self.document)
            self.document.walk(visitor)
    
    class Reader(standalone.Reader):
        ":Ignore: yes"
    
        supported = standalone.Reader.supported + ('wiki',)
    
        def get_transforms(self):
            return standalone.Reader.get_transforms(self) + [WikiLink]
    
    def renderHtml(string):
        class NoHeaderHTMLTranslator(HTMLTranslator):
            def __init__(self, document):
                HTMLTranslator.__init__(self,document)
                self.head_prefix = ['','','','','']
                self.body_prefix = []
                self.body_suffix = []
                self.stylesheet = []
        w = Writer()
        w.translator_class = NoHeaderHTMLTranslator
        r = Reader()
        return core.publish_string(string,writer=w,reader=r)
    
    WIKI = lambda text: XML(renderHtml(text))
    MARKUP = XML('<a href="http://docutils.sourceforge.net/rst.html">reST</a>')
except:
    from gluon.contrib.markdown import WIKI
    MARKUP = XML('<a href="http://daringfireball.net/projects/markdown">markdown</a>')
