def _():
    """
    the mambo jambo here makes sure that
    PluginManager.wiki.xxx is also exposed as plugin_wiki_xxx
    this is to minimize Storage lookup
    """
    if not 'db' in globals() or not 'auth' in globals():
        raise HTTP(500,"plugin_wiki requires 'db' and 'auth'")
    from gluon.tools import PluginManager
    #prefix='plugin_spreadsheet'
    #keys=dict(item for item in DEFAULT.items() if not prefix+item[0] in globals())
    #plugins = PluginManager('spreadsheet',**keys)
    #globals().update(dict((prefix+key,keys[key]) for key in keys))
_()


## Menus
response.menu_spread = [
    ['Index', False,
     URL(request.application,'plugin_spreadsheet','index'), []],
    ]

response.menu_edit=[
  ['Edit', False, URL('admin', 'default', 'design/%s' % request.application),
   [
            ['Controller', False,
             URL('admin', 'default', 'edit/%s/controllers/default.py' \
                     % request.application)],
            ['View', False,
             URL('admin', 'default', 'edit/%s/views/%s' \
                     % (request.application,response.view))],
            ['Layout', False,
             URL('admin', 'default', 'edit/%s/views/layout.html' \
                     % request.application)],
            ['Stylesheet', False,
             URL('admin', 'default', 'edit/%s/static/base.css' \
                     % request.application)],
            ['DB Model', False,
             URL('admin', 'default', 'edit/%s/models/db.py' \
                     % request.application)],
            ['Menu Model', False,
             URL('admin', 'default', 'edit/%s/models/menu.py' \
                     % request.application)],
            ['Database', False,
             URL(request.application, 'appadmin', 'index')],
            ]
   ],
  ]

