/**
* JCE Utilities 2.2.4
*
* @version 		$Id: jceutilities.js 389 2009-10-08 15:18:30Z happynoodleboy $
* @package 		JCE Utilites
* @copyright 	Copyright (C) 2006-2009 Ryan Demmer. All rights reserved.
* @license 		http://www.gnu.org/copyleft/gpl.html GNU/GPL
* This version may have been modified pursuant
* to the GNU General Public License, and as distributed it includes or
* is derivative of works licensed under the GNU General Public License or
* other free or open source software licenses.
*
*/

/**
 * Based on the Mootools Tips class with additional options - position, opacity
 * Tooltip div is created when the first tooltip is initialized, not on page load
 * Changes to locate function allow tooltip to be positioned relative to the mouse pointer
 * @param {Object} tip
 */
var JCETips = new Class({

	getOptions: function(){
		return {
			onShow: function(tip){
				tip.setStyle('visibility', 'visible');
			},
			onHide: function(tip){
				tip.setStyle('visibility', 'hidden');
			},
			speed: 150,
			position: 'br',
			opacity: 0.8,
			className: 'tooltip',
			offsets: {
				'x': 16,
				'y': 16
			},
			fixed: false
		}
	},
	/**
	 * Initilize the class
	 * @param {Array} elements Array of elements
	 * @param {Object} options Options object
	 */
	initialize: function(elements, options){
		this.setOptions(this.getOptions(), options);
		$$(elements).each(function(el){
			el.addEvents({
				'mouseenter': 	this.start.bindWithEvent(this, el),
				'mousemove':	this.locate.bindWithEvent(this), 
				'mouseleave': 	this.end.bindWithEvent(this, el)
			});
		}.bind(this));
	},
	/**
	 * Create the tooltip div
	 */
	create : function() {
		if (!this.toolTip) {
			this.toolTip = new Element('div', {
				'class': this.options.className,
				'styles': {
					'position': 'absolute',
					'top': '0',
					'left': '0',
					'visibility': 'hidden'
				}
			}).injectInside($E('body'));
		}
	},
	/**
	 * Show the tooltip and build the tooltip text
	 * @param {Object} e  Event
	 * @param {Object} el Target Element
	 */
	start: function(e, el){				
		this.create();
		
		var text = el.title || '', title = '';
			
		if(/::/.test(text)){
			var parts 	= text.split('::');
			title 		= parts[0].trim();
			text 		= parts[1].trim();
		}
		// Inherit parent classes
		var cls 		= el.className.replace(/(jce_?)tooltip/gi, '');		
		// Store original title and remove
		this.toolTip.title 	= el.title;			
		$(el).setProperty('title', '');
		
		this.toolTip.empty();
		
		if (title){
			this.title = new Element('h4').inject(this.toolTip).setHTML(title);
		}
		if (text){
			this.text = new Element('p').inject(this.toolTip).setHTML(text);
		}

		$clear(this.timer);
		this.timer = this.show.delay(this.options.showDelay, this);
	},

	end: function(event, el){
		$clear(this.timer);
		el.setProperty('title', this.toolTip.title);
		this.timer = this.hide.delay(this.options.hideDelay, this);
	},

	/**
	 * Position the tooltip
	 * @param {Object} e Event trigger
	 */
	locate : function(e){				
		this.create();
		
		var o 		= this.options.offsets;
		var page 	= e.page;
		var tip 	= {'x': this.toolTip.offsetWidth, 'y': this.toolTip.offsetHeight};
		var pos 	= {'x': page.x + o.x, 'y': page.y + o.y};
		
		var ah 		= 0;
		
		switch(this.options.position){
			case 'tl':
				pos.x = (page.x - tip.x) - o.x;
				pos.y = (page.y - tip.y) - (ah + o.y);
				break;
			case 'tr':
				pos.x = page.x + o.x;
				pos.y = (page.y - tip.y) - (ah + o.y);
				break;
			case 'tc':
				pos.x = (page.x - Math.round((tip.x / 2))) + o.x;
				pos.y = (page.y - tip.y) - (ah + o.y);
				break;
			case 'bl':
				pos.x = (page.x - tip.x) - o.x;
				pos.y = (page.y + Math.round((tip.y/2))) - (ah + o.y);
				break;
			case 'br':
				pos.x = page.x + o.x;
				pos.y = page.y + o.y;
				break;
			case 'bc':
				pos.x = (page.x - (tip.x/2)) + o.x;
				pos.y = page.y + ah + o.y;
				break;
		}
		$(this.toolTip).setStyles({
			top: pos.y + 'px', 
			left: pos.x + 'px'
		});
	},
	/**
	 * Position the tooltip
	 * @param {Object} element
	 */
	position: function(element){
		var pos = element.getPosition();
		this.toolTip.setStyles({
			'left': pos.x + this.options.offsets.x,
			'top': pos.y + this.options.offsets.y
		});
	},
	/**
	 * Execute the onShow function
	 */
	show: function(){
		if (this.options.timeout) this.timer = this.hide.delay(this.options.timeout, this);
		this.fireEvent('onShow', [this.toolTip]);
	},
	/**
	 * Execute the onHide function
	 */
	hide: function(){
		this.fireEvent('onHide', [this.toolTip]);
	}

});

JCETips.implement(new Events, new Options);

/**
 * JCE Utilities Base Class
 */
var JCEUtilities = new Class({
	getOptions : function(){
		return {			
			popup : {
				legacy				: 0,
				//convert			: 0,
				overlay				: 1,
				overlayopacity 		: 0.8,
				overlaycolor		: '#000000',
				resize				: 1,	
				icons				: 1,
				fadespeed			: 500,
				scalespeed			: 500,
				hideobjects			: 1,
				scrollpopup			: 1,
				onclose				: Class.empty
			},
			tooltip : {
				className			: 'tooltip',
				speed				: 150,
				offsets				: {x: 16, y : 16},
				position			: 'br',
				opacity				: 0.8,
				background			: '#000000',
				color				: '#ffffff'
			},
			theme				: 'standard',
			themecustom			: '',
			themepath			: 'plugins/system/jceutilities/themes',
			//pngfix				: 1,
			//wmode				: 0,
			imgpath				: 'plugins/system/jceutilities/img'
		};
	},
	/**
	 * Get the site url from javascript source file
	 * @return Site URL
	 */
	getSite : function(){
		var s = $E('script[src*=jceutilities.js]').src;
		/*
		$ES('script[src*jceutilities.js').each(function(el){
			if (/jceutilities\.js/.test(el.src)) {
				s = el.src;
			}
		});*/
		
		s = s.substring(0, s.lastIndexOf('plugins/system/jceutilities/js')) || '';
		if (/:\/\//.test(s)) {
			s = s.match(/.*:\/\/[^\/]+(.*)/)[1];
		}
		
		var site 	= document.location.href;			
		var parts 	= site.split(':\/\/');
		
		var port 	= parts[0];
		var url 	= parts[1];
	
		return port + '://' + url.substr(0, url.indexOf(s)) + s;
	},
	/**
	 * Initialise the Class
	 * @param {Object} options Class options
	 */
	initialize : function(options){	
		this.setOptions(this.getOptions(), options);		
		this.popup();
		this.tooltip();
		/*if(this.options.pngfix == 1 && window.ie6){
			this._pngFix();	
		}
		if(options.wmode == 1){
			this._wmodeFix();	
		}*/
		
		return this;
	},
	/**
	 * Get client window width
	 */
	_getWidth: function(){
		return document.documentElement.clientWidth || document.body.clientWidth || this.innerWidth || 0;
	},
	/**
	 * Get client window height
	 */	
	_getHeight: function(){
		return document.documentElement.clientHeight || document.body.clientHeight || this.innerHeight || 0;
	},
	/**
	 * Get client window scroll height
	 */
	_getScrollHeight: function(){
		return document.documentElement.scrollHeight || document.body.scrollHeight || 0;
	},
	/**
	 * Get client window scroll width
	 */	
	_getScrollWidth: function(){
		return document.documentElement.scrollWidth || document.body.scrollWidth || 0;
	},
	/**
	 * Get client window scroll top
	 */
	_getScrollTop: function(){
		return document.documentElement.scrollTop || this.pageYOffset || document.body.scrollTop || 0;
	},
	/**
	 * IE png fix
	 */
	_pngFix : function(){
		var s, bg, site = this.getSite();
		// Images
		$ES('img[src$=.png]', $E('body')).each( function(el) {
			$(el).setStyle('filter', "progid:DXImageTransform.Microsoft.AlphaImageLoader(src='" + el.src + "', sizingMethod='')");			
			el.src = site + 'plugins/system/jceutilities/img/blank.gif';
		});
		// CSS Background Images
		$ES('*', $E('body')).each(function(el){
			s = $(el).getStyle('background-image');
			if(s && /\.png/i.test(s)){
				bg = /url\("(.*)"\)/.exec(s)[1];
				$(el).setStyle('background-image', 'none');
				$(el).setStyle('filter', "progid:DXImageTransform.Microsoft.AlphaImageLoader(src='" + bg + "',sizingMethod='')");	
			}
		});
	},
	/**
	 * IE Wmode Fix
	 */
	_wmodeFix : function(){			
		$ES('object').each(function(el){
			if(el.classid.toLowerCase() == 'clsid:d27cdb6e-ae6d-11cf-96b8-444553540000' || el.type.toLowerCase() == 'application/x-shockwave-flash'){
				if(!el.wmode || el.wmode.toLowerCase() == 'window'){
					el.wmode = 'opaque';	
					if(typeof el.outerHTML == 'undefined'){
						$(el).replaceWith($(el).clone(true));	
					}else{
						el.outerHTML = el.outerHTML;
					}
				}
			}
		});
		$ES('embed[type=application/x-shockwave-flash]').each(function(el){
			var wm = $(el).getProperty('wmode');
			if(!wm || wm.toLowerCase() == 'window'){
				$(el).setProperty('wmode', 'opaque');
				if(typeof el.outerHTML == 'undefined'){
					$(el).replaceWith($(el).clone(true));	
				}else{
					el.outerHTML = el.outerHTML;
				}
			}
		});
	},
	/**
	 * Create a new tooltip using JCETips Class
	 */
	tooltip : function(){
		new JCETips($ES('.jcetooltip, .jce_tooltip'), this.options.tooltip);
	},
	/**
	 * Convert legacy popups to new format
	 */
	convert : function(){
		this.site = this.getSite();
		$ES('a[href*=com_jce]').each(function(el){
			var p, s;
			s = this._cleanEvent($(el).getProperty('onclick')).replace(/&amp;/g,'&').replace(/&#39;/g,"'").split("'").filter(function(item, index){
				return /\&/.test(item);
			});
			p = this._params(s[0]);
			
			img 	= p['img']		|| '';
			title 	= p['title'] 	|| '';
			
			if(img) {
				if(!/http:\/\//.test(img)){
					if(img.charAt(0) == '/'){
						img = img.substr(1);	
					}
					img = this.site.replace(/http:\/\/([^\/]+)/, '') + img;	
				}
				el.setProperties({
					'href': img,
					'title': title.replace(/_/, ' '),
					'onclick': ''
				}).addClass('jcepopup').removeProperty('onclick');
			}
																			  
		}.bind(this));
	},
	/**
	 * Get the file type from the url, type attribute or className
	 * @param {Object} el
	 */
	_getType : function(el) {
		if (/(youtube|videoplay|googleplayer|metacafe|vimeo|\.swf)/i.test(el.href)) {
			return 'flash';	
		}
		// Image
		if (/\.(jpg|jpeg|png|gif|bmp|tif)$/i.test(el.href)) {
			return 'image';
		}
		if (/(director|windowsmedia|mplayer|quicktime|real|divx|flash)/.test(el.type)) {
			return /(director|windowsmedia|mplayer|quicktime|real|divx|flash)/.exec(el.type)[1];
		}
		// Other from classname
		if (/(director|windowsmedia|mplayer|quicktime|real|divx|flash|iframe|ajax|image)/.test(el.className)) {
			return /(director|windowsmedia|mplayer|quicktime|real|divx|flash|iframe|ajax|image)/.exec(el.className)[1];
		}
		return el.type || 'iframe';
	},
	/**
	 * Get the page scrollbar width
	 */
	_getScrollbarWidth: function() {
        if (this.scrollbarWidth) {
			return this.scrollbarWidth;
		}
		
		var inner = new Element('div').setStyles({
			width	: '100%', 
			height	: 200,
			border	: 0,
			margin	: 0,
			padding	: 0
		});
        var outer = new Element('div').setStyles({
			position	: 'absolute', 
			visibility	: 'hidden', 
			width		: 200,
			height		: 200,
			border		: 0,
			margin		: 0,
			padding		: 0,
			overflow	: 'hidden'
		}).injectInside(document.body).adopt(inner);
        var w1 = parseInt(inner.offsetWidth);
        outer.style.overflow = 'scroll';
        var w2 = parseInt(inner.offsetWidth);
        if(w1 == w2){
			w2 = parseInt(outer.clientWidth);
		}
        outer.remove();
		return (w1 - w2);
    },
	/**
	 * Clean an onclick event
	 * Private function - Regular expression syntax from TinyMCE DOMUtils.js getAttrib function. Copyright (c) 2004-2008, Moxiecode Systems AB
	 * @param {Object} s
	 */
	_cleanEvent : function(s) {
		return s.replace(/^function\s+anonymous\(\)\s+\{\s+(.*)\s+\}$/, '$1');
	},
	/**
	 * Process a parameter string into an object
	 * @param {Object} s
	 */
	_params : function(s){
		var a = [], x = [];
		
		if($type(s) == 'array') {
			x = s;
		} else {
			if (s.indexOf('&') != -1) {
				x = s.split(/&(amp;)?/g);
			} else {
				x = s.split(/;/g);
			}
		}
				
        x.each(function(n){
			if (n) {
				n = n.replace(/^([^\[]+)(\[|=|:)([^\]]*)(\]?)$/, function(a, b, c, d){
					if (d) {
                        if (!/[^0-9]/.test(d)) {
                            return '"' + b + '":' + parseInt(d);
                        }
                        return '"' + b + '":"' + d + '"';
                    }
                    return '';
                });
                if (n) {
                    a.push(n);
                }
            }
        });
        return Json.evaluate('{' + a.join(',') + '}');
	},
	/**
	 * Returns a styles object from a parameter
	 * @param {Object} o
	 */
	_styles : function(o){
		var v, s, x = [];
		if(!o)
			return {};
			
		o.split(';').each(function(s){
			s = s.replace(/(.*):(.*)/, function(a, b, c){
				return "'" + b + "':'" + c + "'";
			});
			x.push(s);
		});
		return Json.evaluate('{'+ x.join(',') +'}');
	},
	/**
	 * IE6 PNG Fix
	 * @param {Object} el
	 */
	_png : function(el){
		var s;
		// If its an image
		if(el.nodeName == 'IMG'){
			s = el.src;
			if(/\.png$/i.test(s)){
				$(el).setProperty('src', this.site + 'plugins/system/jceutilities/img/blank.gif').setStyle('filter', 'progid:DXImageTransform.Microsoft.AlphaImageLoader(src=\'' + s + '\'');
			}
		}else{
			s = $(el).getStyle('background-image');
			if(/\.png/i.test(s)){
				var bg = /url\("(.*)"\)/.exec(s)[1];
				$(el).setStyles({'background-image': 'none', 'filter': "progid:DXImageTransform.Microsoft.AlphaImageLoader(src='" + bg + "')"});
			}
		}
	},
	/**
	 * Create a popup zoom icon
	 * @param {Object} el
	 */
	_zoom : function(el){
		var s, m, x, y;
		var child 	= $E('img', el);
		var zoom 	= new Element('span');
		if(child){
			var w = $(child).getProperty('width') 	|| $(child).getStyle('width')	|| 0;
			var h = $(child).getProperty('height') 	|| $(child).getStyle('height') 	|| 0;
			
			var align 	= $(child).getProperty('align');
			var vspace 	= $(child).getProperty('vspace');
			var hspace 	= $(child).getProperty('hspace');
			
			var styles = {
				width 	: parseInt(w),
				height 	: parseInt(h)
			};
			// Correct from deprecated align attribute
			if(align){
				$extend(styles, {
					'float'			:	/left|right/.test(align) 		? align : '',
					'text-align'	:	/top|middle|bottom/.test(align) ? align : ''
				});
			}
			// Correct from deprecated vspace attribute
			if(vspace){
				$extend(styles, {
					'margin-top'	:	vspace + 'px',
					'margin-bottom'	:	vspace + 'px'
				});
			}
			// Correct from deprecated hspace attribute
			if(hspace){
				$extend(styles, {
					'margin-left'	:	hspace + 'px',
					'margin-right'	:	hspace + 'px'
				});
			}
			
			// Private internal function
			function _buildIcon(el, zoom, child, styles){
				var lft, top, w = styles.width, h = styles.height;
				// Clone image as object element
				var span = new Element('span').setStyles($(child).style.cssText).setStyles(styles).adopt(child).adopt(zoom);
				// Remove (deprecated) attributes that may affect layout
				$each(['style', 'align', 'border', 'hspace', 'vspace'], function(s){
					child.removeProperty(s);
				});
				// Insert border if 0
				if(parseInt(span.getStyle('border-width')) == 0)
					child.setStyle('border', 0);
				
				m = el.className.match(/icon-(top-right|top-left|bottom-right|bottom-left|left|right)/) || ['icon-right', 'right'];
	
				switch(m[1]){
					case 'top-right':
						lft = w - 20;
						top = -h;
						break;
					case 'top-left':
						lft = 0;
						top = -h;
						break;
					default:
					case 'right':
					case 'bottom-right':
						lft = w - 20;
						top = - 20;
						break;
					case 'left':
					case 'bottom-left':
						lft = 0;
						top = -20;
						break;
				}					
				$(zoom).setStyles({'margin-left': lft, 'margin-top': top}).addClass('zoom-image');			
				el.adopt(span);		
			}
			// No dimensions?
			if(/^(0|auto)/.test(w) || /^(0|auto)/.test(h)){
				x = new Image();
				x.src = $(child).src;
				x.onload = function(){
					$extend(styles, {
						width 	: parseInt(x.width), 
						height	: parseInt(x.height)
					});
					_buildIcon(el, zoom, child, styles);	
				} 
			}else{
				_buildIcon(el, zoom, child, styles);
			}
		}else{				
			$(zoom).addClass('zoom-link');
			if(/icon-left/.test(el.className)){
				$(zoom).injectTop(el);
			}else{
				$(zoom).injectInside(el);
			}
		}
		if(window.ie6){
			s = $(zoom).getStyle('background-image');
			if(s && /\.png/i.test(s)){
				s = /url\("(.+)"\)/.exec(s)[1];
				$(zoom).setStyle('background-image', 'none');
				$(zoom).setStyle('filter', "progid:DXImageTransform.Microsoft.AlphaImageLoader(src='" + s + "')");
			}
		}else{
			$(zoom).setStyle('position', 'relative');
		}
	},
	/**
	 * Create popups from links with trigger class
	 */
	popup : function(){
		var t = this, auto = false;
		this.popups = [], this.popuptheme = '', this.site = this.getSite();

		// Converts a legacy (window) popup into an inline popup
		if(this.options.popup.legacy == 1){
			this.convert();
		}
		$ES('.jcebox, .jcelightbox, .jcepopup').each(function(el, i){
			if(!el.hasClass('nopopup')){
				// Create zoom icon
				if(this.options.popup.icons == 1 && el.nodeName == 'A' && !/(noicon|icon-none|noshow)/.test(el.className) && el.style.display != 'none'){
					this._zoom(el);					   
				}
				// Hide popup link if specified in class
				if (el.hasClass('noshow')) {
					el.setStyle('display', 'none');
				}
				
				var group = '', p = '';
				
				// Auto popup on page load
				if (!auto && el.id) {
					//auto = el.hasClass('autopopup');
					if(c = el.className.match(/autopopup-(single|multiple)/)) {
						auto = c[0];
					}
				}
				
				// Fix title and rel and move parameters
				var title 	= el.title || '';
				var rel 	= el.rel || '';
				// Process title attribute
				if(title && /(\w+\[.*\])/.test(title)){
					// get parameters
					p = this._params(title);
					$(el).setProperty('title', p.title || '');
					group = p.group || '';
				}
				// Process rel attribute
				if(rel && /(\w+\[.*\])/.test(rel)){
					var args = [];
					rel = rel.replace(/\b((\w+)\[(.*?)\])(;?)/g, function(a, b, c){
						args.push(b);
						return '';
					});
					
					// get parameters
					p = this._params(args);

					$(el).setProperty('rel', rel || p.rel || '');
					group = p.group || '';
										
				} else {
					var rx = 'alternate|stylesheet|start|next|prev|contents|index|glossary|copyright|chapter|section|subsection|appendix|help|bookmark|nofollow|licence|tag|friend';
					var lb = '(lightbox(\[(.*?)\])?)';
					var lt = '(lyte(box|frame|show)(\[(.*?)\])?)';
					
					group = rel.replace(new RegExp('\s*(' + rx + '|' + lb + '|' + lt + ')\s*'), '', 'gi');
				}
				// Get AREA parameters from URL if not set
				if(el.nodeName == 'AREA') {
					if (!p) {
						p = this._params(el.href);
					}
					// Set AREA group
					group = group || 'AREA_ELEMENT';
				}
				// Popup object
				var o = {
					'href'  	: el.href,
					'title'		: p.title || title,
					'group' 	: el.hasClass('nogroup') ? '' : group,
					'type'		: p.type || t._getType(el),
					'params' 	: p || {},
					'id'		: el.id || '',
					'auto'		: auto
				};
				// Add to global popups array
				this.popups.push(o);
				
				$(el).addEvent('click', function(e){
					e = new Event(e);
					e.stop();
					return this._start(o, i);
				}.bind(this));
				// Reset auto popup value
				auto = false;
			}
		}.bind(this));
		
		// Load the popup theme	
		var theme = this.options.theme == 'custom' ? this.options.themecustom : this.options.theme;
		new Ajax(this.site + this.options.themepath + '/' + theme + '/popup.html', {
			method : 'get',
			onComplete : function(data){
				var re = /<!-- THEME START -->([\s\S]*?)<!-- THEME END -->/;
				if(re.test(data)){
					data = re.exec(data)[1];	
				}
				this.popuptheme = data;
				// Process auto popups
				this._auto();
			}.bind(this)
		}).request();
	},
	/**
	 * Public Function : Open a popup Example : jcepopup.open('http://www.joomlacontenteditor.net', 'JCE', 'joomla_sites', 'iframe', {width:800});
	 * @param {String} url
	 * @param {String} title
	 * @param {String} group
	 * @param {String} type
	 * @param {Object} params
	 */
	open : function(url, title, group, type, params){
		var link = {
			'href'  	: url,
			'title'		: title,
			'group' 	: group,
			'type'		: type,
			'params' 	: params
		};
		this.popups.push(link);
		return this._start(link);
	},
	/**
	 * Process autopopups
	 */
	_auto : function() {
		this.popups.each(function(el){
			if(el.auto) {
				if(el.auto == 'autopopup-single') {
					var cookie = Cookie.get('jceutilities_autopopup_' + el.id);
					if (!cookie) {
						Cookie.set('jceutilities_autopopup_' + el.id, 1);
						this._start(el);
					}
				} else if(el.auto == 'autopopup-multiple') {
					this._start(el);
				}
			}
		}.bind(this));
	},
	/**
	 * Build Popup structure
	 */
	_build : function(){
		var t = this;
		this.page = new Element('div', {
			id : 'jcepopup-page'
		}).injectInside(document.body);
		
		if(this.options.popup.overlay == 1){
			this.overlay = new Element('div', {
				'id' 	: 'jcepopup-overlay',
				styles 	: {
					opacity	: '0',
					'background-color': this.options.popup.overlaycolor
				},
				events : {
					click : function(){
						this.close();	
					}.bind(this)	
				}
			}).injectInside(this.page);			
		}
		
		this.frame = new Element('div', {
			id : 'jcepopup-frame'
		}).injectInside(this.page);
		
		if(window.ie6 || !this.options.popup.scrollpopup){
			$(this.overlay).setStyle('height', this._getScrollHeight());
			$(this.page).setStyle('position', 'absolute').setStyle('top', this._getScrollTop());
		}
		
		// Default theme layout
		if(!this.popuptheme){
			this.popuptheme  = '<div id="jcepopup-container">';
			this.popuptheme += '<div id="jcepopup-loader"></div>';
			this.popuptheme += '<div id="jcepopup-content"></div>';
			this.popuptheme += '<a id="jcepopup-closelink" href="javascript:;" title="Close"></a>';
			this.popuptheme += '<div id="jcepopup-info">';
			this.popuptheme += '<div id="jcepopup-caption"></div>';
			this.popuptheme += '<div id="jcepopup-nav">';
			this.popuptheme += '<a id="jcepopup-prev" href="javascript:;" title="Previous"></a>';
			this.popuptheme += '<a id="jcepopup-next" href="javascript:;" title="Next"></a>';
			this.popuptheme += '<span id="jcepopup-numbers"></span>';
			this.popuptheme += '</div>';
			this.popuptheme += '</div>';
			this.popuptheme += '</div>';
		}
		// Remove comments
		this.popuptheme = this.popuptheme.replace(/<!--(.*?)-->/g, '');
		// Insert theme html into the DOM
		$(this.frame).adopt(new Element('div', {id : 'jcepopup-body'}).setHTML(this.popuptheme));
		// Create objects
		['body', 'container', 'content', 'loader', 'closelink', 'cancellink', 'info-top', 'info-bottom', 'caption', 'next', 'prev', 'numbers'].each(function(s){
			if($('jcepopup-' + s))
				t[s] = $('jcepopup-' + s).setStyle('display', 'none');
		});			
		if(this.closelink){
			$(this.closelink).addEvent('click', function(){
				this.close();
			}.bind(this));
		}
		if(this.cancellink){
			$(this.cancellink).addEvent('click', function(){
				this.close();
			}.bind(this));
		}
		if(this.next){
			$(this.next).addEvent('click', function(){
				this._next();
			}.bind(this));
		}
		if(this.prev){
			$(this.prev).addEvent('click', function(){
				this._previous();
			}.bind(this));
		}
		if(window.ie6){
			this._png(this.body);
			$ES('*', this.body).each(function(el){
				if(el.id == 'jcepopup-content') return;
				this._png(el);
			}.bind(this));
		}
	},
	/**
	 * Start a popup window. Build popup structure and process groups
	 * @param {Object} p Popup object
	 */
	_start: function(p, i){			
		var t = this, n = 0, x = 0, items = [];	
		
		// Store scrollbar width
		this.scrollbarWidth = this._getScrollbarWidth();
		
		// build popup window
		this._build();
		
		if (p.group) {
			this.popups.each(function(o, x){
				if(o.group == p.group) {
					items.push(o);
					if(i && x == i) {
						n = items.indexOf(o);
					}
				}
			});
		} else {
			items.push(p);
		}
		return this._open(items, n);
	},
	/**
	 * Open the popup window
	 * @param {Object} items
	 * @param {Object} n
	 */
	_open: function(items, n){
		var t = this;
		this.items = items;
		//this._position();
		this._bind(true);
		
		$(this.body).setStyle('display', '').setStyle('top', (this._getHeight() - this._outerHeight(this.body)) / 2);
		
		if(this.options.popup.overlay == 1 && $(this.overlay)){
			new Fx.Style(this.overlay, 'opacity', {duration : this.options.popup.fadespeed}).start(0, this.options.popup.overlayopacity);
		}
		// load item
		return this._change(n);
	},	
	/**
	 * Create event / key bindings
	 * @param {Boolean} open
	 */	
	_bind: function(open){
		var t = this;
		if(window.ie6){
			$ES('select').each(function(el){
				if(open){
					el.tmpStyle = el.style.visibility;
				}
				el.setStyle('visibility', open ? 'hidden' : el.tmpStyle);
			}.bind(this));
		}
		if(this.options.popup.hideobjects){
			$ES('object,embed').each(function(el){
				if(el.id == 'jcepopup-object') return;
				if(open){
					el.tmpStyle = el.style.visibility;
				}
				el.style.visibility = open ? 'hidden' : el.tmpStyle;
			}.bind(this));
		}
		var scroll = this.options.popup.scrollpopup;
		if(open){
			$(document).addEvent('keydown', function(e){
				e = new Event(e);
				this._listener(e);
			}.bind(this));
			if(window.ie6 || !scroll){
				window.addEvent('scroll', function(){
					$(this.overlay).setStyle('height', this._getScrollHeight());	
					//$(this.page).setStyle('height', this._getScrollHeight());
				}.bind(this));
				window.addEvent('resize', function(){
					$(this.overlay).setStyle('width', this._getScrollWidth());	
					//$(this.page).setStyle('height', this._getScrollHeight());
				}.bind(this));
			}
			if(!scroll){
				this.page.setStyle('position', 'absolute');
			}
		}else{
			if(window.ie6 || !scroll){
				window.removeEvent('scroll');
				window.removeEvent('resize');
			}
			$(document).removeEvent('keydown');
		}
	},
	/**
	 * Keyboard listener
	 * @param {Object} e Event
	 */	
	_listener: function(e){
		switch (e.code){
			case 27: case 88: case 67: this.close(); break;
			case 37: case 80: this._previous(); break;	
			case 39: case 78: this._next(); break;
		}
	},
	/**
	 * Determine media type and properties
	 * @param {Object} c
	 */
	_media : function(c){
		var ci, cb, mt;

		c = /(director|windowsmedia|mplayer|quicktime|real|divx|flash)/.exec(c);
		
		switch (c[1]) {
			case 'director':
			case 'application/x-director':
				ci = '166b1bca-3f9c-11cf-8075-444553540000';
				cb = 'http://download.macromedia.com/pub/shockwave/cabs/director/sw.cab#version=8,5,1,0';
				mt = 'application/x-director';
				break;
			case 'windowsmedia':
			case 'mplayer':
			case 'application/x-mplayer2':
				ci = '6bf52a52-394a-11d3-b153-00c04f79faa6';
				cb = 'http://activex.microsoft.com/activex/controls/mplayer/en/nsmp2inf.cab#Version=5,1,52,701';
				mt = 'application/x-mplayer2';
				break;
			case 'quicktime':
			case 'video/quicktime':
				ci = '02bf25d5-8c17-4b23-bc80-d3488abddc6b';
				cb = 'http://www.apple.com/qtactivex/qtplugin.cab#version=6,0,2,0';
				mt = 'video/quicktime';
				break;
			case 'real':
			case 'realaudio':
			case 'audio/x-pn-realaudio-plugin':
				ci = 'cfcdaa03-8be4-11cf-b84b-0020afbbccfa';
				cb = 'http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=7,0,0,0';
				mt = 'audio/x-pn-realaudio-plugin';
				break;
			case 'divx':
			case 'video/divx':
				ci = '67dabfbf-d0ab-41fa-9c46-cc0f21721616';
				cb = 'http://go.divx.com/plugin/DivXBrowserPlugin.cab';
				mt = 'video/divx';
				break;
			default:
			case 'flash':
			case 'application/x-shockwave-flash':
				ci = 'd27cdb6e-ae6d-11cf-96b8-444553540000';
				cb = 'http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,124,0';
				mt = 'application/x-shockwave-flash';
				break;
		}
		return {'classid' : ci, 'codebase': cb, 'mediatype': mt};
	},
	/**
	 * Determine whether the url is local
	 * @param {Object} s
	 */
	_local : function(s){
		if (/^(\w+):\/\//.test(s)) {
			return new RegExp('^(' + this.site + ')').test(s);
		} else {
			return true;
		}
	},
	/**
	 * Get the outerwidth of an element
	 * @param {Object} n Element
	 */
	_outerWidth : function(n){
		var i, x = 0;
		['padding-left', 'padding-right', 'border-left', 'border-right', 'width'].each(function(s){
			i = parseInt($(n).getStyle(s));
			i = /[^0-9]/.test(i) ? 0 : i;
			
			x = x + i;
		});
		return x;
	},
	/**
	 * Get the outerheight of an Element
	 * @param {Object} n Element
	 */
	_outerHeight : function(n){
		var i, x = 0;
		['padding-top', 'padding-bottom', 'border-top', 'border-bottom', 'height'].each(function(s){
			i = parseInt($(n).getStyle(s));
			i = /[^0-9]/.test(i) ? 0 : i;
			
			x = x + i;
		});
		return x;
	},
	/**
	 * Get the width of the container frame
	 */
	_frameWidth : function(){
		var w = 0;
		['left', 'right'].each(function(s){
			w = w + parseInt($(this.frame).getStyle('padding-' + s));					
		}.bind(this));
		
		return parseInt($(this.frame).clientWidth) - w;
	},
	/**
	 * Get the width of the container frame
	 */
	_frameHeight : function(){
		var h = 0;
		['top', 'bottom'].each(function(s){
			h = h + parseInt($(this.frame).getStyle('padding-' + s));					
		}.bind(this));
		h = h + ((window.ie6 || window.ie7) ? this.scrollbarWidth : 0);
		return parseInt(this._getHeight()) - h;
	},
	/**
	 * Get the width of the usable window
	 */
	_width : function(){
		return this._frameWidth() - this.scrollbarWidth;
	},
	/**
	 * Get the height of the usable window less info divs
	 */
	_height : function(){
		var h = 0;
		['top', 'bottom'].each(function(s){
			if(this['info-' + s]){
				h = h + parseInt(this._outerHeight(this['info-' + s]));
			}
		}.bind(this));
		
		return this._frameHeight() - (h + this.scrollbarWidth);
	},
	/**
	 * Process the next popup in the group
	 */
	_next : function(){
		if(this.items.length == 1) return false;
		var n = this.index + 1;
		
		if(n < 0 || n >= this.items.length){
			return false;
		}
		return this._queue(n);
	},
	/**
	 * Process the previous popup in the group
	 */
	_previous : function(){
		if(this.items.length == 1) return false;
		var n = this.index - 1;
		
		if(n < 0 || n >= this.items.length){
			return false;
		}
		return this._queue(n);
	},
	/**
	 * Process a popup in the group queue
	 * @param {Object} n Queue position
	 */
	_queue: function(n){
		var fs = this.options.popup.fadespeed, ss = this.options.popup.scalespeed;
		
		/*if(window.opera || window.ie6){
			// Optional element
			['top', 'bottom'].each(function(s){
				if(this['info-' + s]){
					$(this['info-' + s]).setStyle('display', 'none');
				}
			}.bind(this));
			$(this.content).setStyle('display', 'none');
			return this._change(n);
		}else{*/
			var t = this;
			// Optional element
			var changed = false;
			['top', 'bottom'].each(function(s){
				var el = $(this['info-' + s]);
				if(el){
					var h = this._outerHeight(el);
					var m = s == 'top' ? 'bottom' : 'top';
					// Show items Optional Element
					el.setStyle('z-index', -1);			
					new Fx.Style(el, m, {duration : ss, onComplete : function(){
							if(!changed){
								changed = true;
								return this._change(n);	
							}
						}.bind(this)
					}).start(-h);
				}
			}.bind(this));
		//}
	},
	/**
	 * Set the popup information (caption, title, numbers)
	 */
	_info : function(){
		// Optional Element Caption/Title
        
        if (this.caption) {
            var title = this.active.title || '', caption = '';
            if (/:\/\//.test(title)) {
                title = '<a href="' + title + '" target="_blank">' + title + '</a>';
            }
            caption = '<p>' + title + '</p>';
            if (/::/.test(title)) {
                var parts = title.split('::');
                caption = '<h4>' + parts[0] + '</h4>';
                if (parts[1]) {
                    caption += '<p>' + parts[1] + '</p>';
                }
            }
            $(this.caption).setHTML(caption).setStyle('display', '');
        }
		// Optional Element
		//if(this.nav){
		var html = '', i, len = this.items.length;
		if(len > 1){
			for(i=0; i<len; i++){
				var n = i + 1;
				html += '<a href="javascript:;"';
				if(this.index == i){
					html += ' class="active"';
				}
				html += '>' + n + '</a>';
			}
			if(this.prev){
				if(this.index > 0){
					$(this.prev).setStyle('display', '');
				}else{
					$(this.prev).setStyle('display', 'none');	
				}
			}
			if(this.next){
				if(this.index < len - 1 ){
					$(this.next).setStyle('display', '');
				}else{
					$(this.next).setStyle('display', 'none');	
				}
			}
		}
		if(this.numbers){
			$(this.numbers).setHTML(html).getChildren().each(function(el){
				if(el.nodeName == 'A'){
					if(!$(el).hasClass('active')){
						$(el).addEvent('click', function(){
							this._queue(parseInt($(el).getText()) - 1);
						}.bind(this));	
					}
					$(el).setStyle('display', '');
				}
			}.bind(this));
			$(this.numbers).setStyle('display', '');
		}
		//}
		['top', 'bottom'].each(function(s){
			if(this['info-' + s]){
				$(this['info-' + s]).setStyles({'display' : '', 'visibility' : 'hidden'});	
			}
		}.bind(this));
		// Close link / button
		if(this.closelink){
			$(this.closelink).setStyle('display' , '');
		}
	},
	/**
	 * Change the popup
	 * @param {Integer} n Popup number
	 */
	_change: function(n){			
		var t = this, p = {}, s, i, w, h;
		if(n < 0 || n >= this.items.length){
			return false;
		}
		this.index 	= n;
		this.active = {};
		
		// Show Container
		$(this.container).setStyle('display', '');	
		// Show Loader
		if(this.loader){
			$(this.loader).setStyle('display', '');	
		}
		// Show Cancel
		if(this.cancellink){
			$(this.cancellink).setStyle('display', '');	
		}
		
		if(this.object){
			this.object = null;
		}
		
		$(this.content).empty();
		
		i = this.items[n];
		
		// Private / internal
		/*function getParams(t, i){
			// get parameters
			if(i.rel && /(\w+\[.*\])/.test(i.rel)){
				return t._params(i.rel);
			// Legacy
			} else if (i.title && /(\w+\[.*\])/.test(i.title)) {
				return t._params(i.title);
			} else {
				s = i.href;
				if (/\?/.test(s)) {
					s = s.replace(/^[^\?]+\??/, '').replace(/&amp;/gi, '&');
				}
				return t._params(s);
			}	
		}*/
		
		//p = getParams(this, i);
		p = i.params;
		
		//p.width 	= parseInt(p.width);
		//p.height 	= parseInt(p.height);
		
		$extend(this.active, {
			'src'		: 	i.href,
			'title'		:	i.title,
			'type'		:	i.type,
			'params'	: 	p || {},
			'width'		:	p.width		|| 0,
			'height'	:	p.height 	|| 0
		});
		
		// Setup info
		this._info();
		
		switch(this.active.type) {
			case 'image':
				this.img = new Image();
				this.img.onload = function(){
					return t._setup();
				};
				this.img.src = this.active.src;
				break;
			case 'flash':
			case'director':
			case'shockwave':
			case'mplayer':
			case'windowsmedia':
			case'quicktime':
			case'realaudio':
			case'real':
			case'divx':
				p.src 		= this.active.src;		
				var base	= /:\/\//.test(p.src) ? '' : this.site;
				this.object = '';
	
				w = this._width();
				h = this._height();
				
				// Youtube
				if(/youtube(.+)\/(watch\?v=|v\/)(.+)/.test(p.src)){					
					p.src = p.src.replace(/watch\?v=/, 'v/');
					
					w = this.active.width 	|| 425;
					h = this.active.height 	|| 344;
				}
				// Google Video
				if(/google(.+)\/(videoplay|googleplayer\.swf)\?docid=(.+)/.test(p.src)){					
					p.src = p.src.replace(/videoplay/, 'googleplayer.swf');
					
					w = this.active.width 	|| 425;
					h = this.active.height 	|| 326;
				}
				// Metacafe
				if(/metacafe(.+)\/(watch|fplayer)\/(.+)/.test(p.src)){
					var s = p.src.trim();
					if(!/\.swf/i.test(s)){						
						if(s.charAt(s.length-1) == '/'){
							s = s.substring(0, s.length-1);	
						}
						s = s + '.swf';		
					}
					p.src = s.replace(/watch/i, 'fplayer');
					
					w = this.active.width 	|| 400;
					h = this.active.height 	|| 345;
				}
				// Vimeo
				if(/vimeo.com\/([0-9]+)/.test(p.src)){
					p.src = p.src.replace(/vimeo.com\/([0-9]+?)/, 'vimeo.com/moogaloop.swf?clip_id=$1');
					
					w = this.active.width 	|| 400;
					h = this.active.height 	|| 300;	
				}							
				//this.active.title 	= p.title || '';
	
				var mt = this._media(this.active.type);
				
				if(this.active.type == 'flash'){
					p.wmode = 'transparent';
					p.base 	= base;
					//if($.browser.msie){
						//p.movie = p.src;
						//delete p.src;
					//}
				}
				if(/(mplayer|windowsmedia)/i.test(this.active.type)){
					p.baseurl = base;
					if(window.ie){
						p.url = p.src;
						delete p.src;
					}
				}
				// delete some parameters
				delete p.title;
				delete p.group;
				
				// Set width/height
				p.width 	= this.active.width 	= p.width 	|| w;
				p.height 	= this.active.height 	= p.height 	|| h;
	
				// Create object
				this.object = '<object id="jcepopup-object" ';
				if(/flash/i.test(this.active.type)){
					this.object += 'type="'+ mt.mediatype +'" data="'+ p.src +'" ';	
				}else{
					this.object += 'codebase="' + mt.codebase + '" classid="clsid:' + mt.classid + '" ';
				}
				for (n in p){
					if(p[n] !== ''){
						if (/(id|name|width|height|style)$/.test(n)){
							t.object += n + '="' + decodeURIComponent(p[n]) + '"';	
						}
					}
				}
				this.object += '>';
				for (n in p){
					if(p[n] !== ''){
						if (!/(id|name|width|height|style)$/.test(n)){
							t.object += '<param name="' + n + '" value="' + decodeURIComponent(p[n]) + '">';
						}
					}
				}
				if(!window.ie && !/flash/i.test(this.active.type)){
					this.object += '<object type="'+ mt.mediatype +'" data="'+ p.src +'" ';
					for (n in p){
						if(p[n] !== ''){
							t.object += n + '="' + decodeURIComponent(p[n]) + '"';
						}
					}
					this.object += '></object>';	
				}
				this.object += '</object>';
				// set type
				this.active.type = 'media';
				
				this._setup();
				break;
			case 'ajax':
			case 'text/html':
			case 'text/xml':
				this.active.width 	= this.active.width 	|| this._width();
				this.active.height 	= this.active.height 	|| this._height();

				if (this._local(this.active.src)) {
					if(!/tmpl=component/i.test(this.active.src)){
						this.active.src += /\?/.test(this.active.src) ? '&tmpl=component' : '?tmpl=component';
					}
					this.active.type = 'ajax';
				} else {
					this.active.type = 'iframe';
					this._setup();
				}
				
				this.ajax = new Element('div', {
					id : 'jcepopup-ajax', 
					styles  : $merge(this._styles(p.styles), {display : 'none'})
				}).injectInside($(this.content));
				
				if (window.ie6) {
					this.ajax.setStyle('margin-right', this.scrollbarWidth);
				}
				
				if (window.ie7) {
					this.ajax.setStyle('padding-right', this.scrollbarWidth);
				}

				new Ajax(this.active.src, {
					onComplete : function(data){
						var html = data, re = /<body[^>]*>([\s\S]*?)<\/body>/;
						if(re.test(data)){
							html = re.exec(data)[1];	
						}
						this.ajax.innerHTML = html;
						if(this.loader){
							$(this.loader).setStyle('display', 'none');
						}
						// Re-direct links
						$ES('a', $(this.content)).each(function(el){
							el.addEvent('click', function(){
								if(el.href && el.href.indexOf('#') == -1){
									this.close();
								}
							}.bind(this))										
						}.bind(this));
						// setup
						return this._setup();
					}.bind(this)
				}).request();
				break;
			case 'iframe':
			default:
				if (this._local(this.active.src)) {
					if (!/tmpl=component/i.test(this.active.src)) {
						this.active.src += /\?/.test(this.active.src) ? '&tmpl=component' : '?tmpl=component';
					}
				}
				
				this.active.width 	= this.active.width 	|| this._width();
				this.active.height 	= this.active.height 	|| this._height();
				
				this.active.type = 'iframe';
				this._setup();
				break;
		}
		
		return false;
	},
	/**
	 * Pre-animation setup. Resize images, set width / height
	 */
	_setup: function(){
		var t = this, w, h;
		
		// Reisze image
		if(this.active.type == 'image'){
			w = this.active.width 	|| this.img.width;
			h = this.active.height 	|| this.img.height;

			// Resize image
			if(this.options.popup.resize == 1){	
				var x =  this._width();
				var y =  this._height();
				if(w > x){
					h = h * (x / w); 
					w = x; 
					if(h > y){ 
						w = w * (y / h); 
						h = y; 
					}
				}else if (h > y){ 
					w = w * (y / h); 
					h = y; 
					if(w > x){ 
						h = h * (x / w); 
						w = x;
					}
				}
			}
			w = Math.round(w);
			h = Math.round(h);
			// Img element
			$(this.content).setStyles({display : 'none', width : w, height : h}).setHTML('<img id="jcepopup-img" src="' + this.active.src + '" title="' + this.active.title + '" width="' + w + '" height="' + h + '" />');
		}else{
			$(this.content).setStyles({
				width 			: this.active.width, 
				height 			: this.active.height,
				display			: 'none'
			});
		}
		// Animate box
		return this._animate();						   
	},
	/**
	 * Animate the popup
	 */
	_animate : function(){
		var t = this, ss = this.options.popup.scalespeed, fs = this.options.popup.fadespeed;
		
		var cw 	= this._outerWidth(this.content);
		var ch 	= this._outerHeight(this.content);
		var ih = 0;		
		['top', 'bottom'].each(function(s){
			if(this['info-' + s]){
				ih = ih + this._outerHeight(this['info-' + s]);
			}
		}.bind(this));

		// Animate width
		new Fx.Styles(this.body, {
			duration : ss,
			onComplete : function(){
				// Animate fade in
				$(this.content).setStyles({'display' : '', 'opacity' : 0});
				if(this.active.type == 'ajax'){
					$(this.ajax).setStyle('display', '');
				}
				['top', 'bottom'].each(function(s){
					var el = $(this['info-' + s]);
					if(el){
						var h = this._outerHeight(el);
						var m = s == 'top' ? 'bottom' : 'top';
						el.setStyle('z-index', -1);
						el.setStyle(m, -h);
						// Show items Optional Element
						el.setStyle('visibility', 'visible');			
						new Fx.Style(el, m, {duration : ss,
							onComplete : function(){
								el.setStyle('z-index', 0);
							}.bind(this)
						}).start(0);
					}
				}.bind(this));
				new Fx.Style(this.content, 'opacity', {duration : fs, 
					onComplete : function(){
						// Hide loader
						if(this.loader){
							$(this.loader).setStyle('display', 'none');
						}
						// If media
						if(this.active.type == 'media' && this.object){
							$(this.content).setHTML(this.object);
						}
						$(this.content).setStyle('display', '').focus();
						// Iframe
						if(this.active.type == 'iframe'){
							new Element('iframe', {
								id : 'jcepopup-iframe',
								frameBorder: 0,
								scrolling: this.active.params.scrolling || 'auto',
								allowTransparency: true,
								styles  : {
									width:  this.active.width, 
									height: this.active.height	
								}
							}).injectInside($(this.content)).setProperty('src', this.active.src);
						}
					}.bind(this)
				}).start(0, 1);
			}.bind(this)
		}).start({height : ch, top : (this._frameHeight() / 2) - ((ch + ih) / 2), width : cw});
	},
	/**
	 * Close the popup window. Destroy all objects
	 */
	close: function(){		
		// Destroy objects
		['img', 'object', 'iframe', 'ajax'].each(function(o){
			this[o] = null;								
		});
		// Hide closelink
		if(this.closelink){
			$(this.closelink).setStyle('display', 'none');
		}
		// Empty content div
		$(this.content).empty();
		// Hide info div
		['top', 'bottom'].each(function(s){
			if(this['info-' + s]){
				$(this['info-' + s]).setStyle('display', 'none');	
			}
		}.bind(this));
		
		$(this.page).remove();
		
		// Fade out overlay
		if(this.overlay){
			if(window.ie6){	
				// Remove event bindings
				this._bind();
				// Remove body, ie: popup
				$(this.overlay).remove();
			}else{
				new Fx.Style(this.overlay, 'opacity', {
					duration : this.options.popup.fadespeed, 
					onComplete : function(){
						this._bind();	
						$(this.overlay).remove();
					}.bind(this)
				}).start(this.options.popup.overlayopacity, 0);
			}
		}
		// Future use
		this.options.popup.onclose.call(this);
		return false;
	}
}, this);
JCEUtilities.implement(new Options, new Events);
