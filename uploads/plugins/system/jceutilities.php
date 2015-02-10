<?php
/**
* @version $Id$
* @package JCE Utilites
* @copyright Copyright (C) 2006-2009 Ryan Demmer. All rights reserved.
* @license http://www.gnu.org/copyleft/gpl.html GNU/GPL, see LICENSE.php
* This version may have been modified pursuant
* to the GNU General Public License, and as distributed it includes or
* is derivative of works licensed under the GNU General Public License or
* other free or open source software licenses.
*
* Light Theme inspired by Slimbox by Christophe Beyls
* @ http://www.digitalia.be
*
* Shadow Theme inspired by ShadowBox
* @ http://mjijackson.com/shadowbox/
*
* Squeeze theme inspired by Squeezebox by Harald Kirschner
* @ http://digitarald.de/project/squeezebox/
*
*/

defined('_JEXEC') or die('Restricted access');

jimport('joomla.plugin.plugin');

/**
* JCE Utiltiies Plugin
*
* @package 		JCE Utilities
* @subpackage	System
*/
class plgSystemJCEUtilities extends JPlugin
{
	var $version 	= '2.2.4';
	
	/**
	 * Constructor
	 *
	 * For php4 compatability we must not use the __constructor as a constructor for plugins
	 * because func_get_args (void) returns a copy of all passed arguments NOT references.
	 * This causes problems with cross-referencing necessary for the observer design pattern.
	 *
	 * @param	object		$subject The object to observe
	 * @param 	array  		$config  An array that holds the plugin configuration
	 * @since	1.0
	 */
	function plgSystemJCEUtilities(&$subject, $config)  
	{
		parent::__construct($subject, $config);
	}
    
    /**
     * Returns $version.
     *
     * @see plgSystemJCEUtilities::$version
     */
    function getVersion()
    {
		return preg_replace('/[^\w]/', '', $this->version);
    }
    
    /**
     * Sets $version.
     *
     * @param object $version
     * @see plgSystemJCEUtilities::$version
     */
    function setVersion($version)
    {
        $this->version = $version;
    }

	function renderParams($name, $params, $end)
	{
		$html = '';
		if ($name) {
			$html .= $name .":{";
		}
		$i = 0;
		foreach ($params as $k => $v) {
			// not objects or arrays or functions or numbers
            if (!preg_match('/(\[[^\]*]\]|\{[^\}]*\}|function\([^\}]*\})/', $v)) {
            	if (!is_numeric($v)) {
            		$v = '"'.$v.'"'; 
            	}             
            }
			if ($i < count($params) -1) {
				$v .= ',';
			}
			if (preg_match('/\s+/', $k)) {
				$html .= "'". $k ."':". $v;
			} else {
				$html .= $k .":". $v;
			}
			
			$i++;
		}
		if ($name) {
			$html .= "}";
		}
		if (!$end) {
			$html .= ",";
		}
		return $html;
	}	
	function getThemeCSS($vars)
	{
		jimport('joomla.environment.browser');
		jimport('joomla.filesystem.file');
		
		$document =& JFactory::getDocument();
		$theme = $vars['theme'] == 'custom' ? $vars['themecustom'] : $vars['theme'];
		
		$version = $this->getVersion();
		
		// Load template css file
		if (JFile::exists(JPATH_ROOT .DS. $vars['themepath'] . '/' .$theme. '/css/style.css')) {
			$document->addStyleSheet(JURI::base(true).'/' . $vars['themepath'] . '/' .$theme.'/css/style.css?version='.$version);
		} else {
			$document->addStyleSheet(JURI::base(true).'/' . $vars['themepath'] . '/standard/css/style.css?v='.$version);
		}
		// Load any ie6 variation
		jimport('joomla.environment.browser');
		$browser = &JBrowser::getInstance();
		if ($browser->getBrowser() == 'msie' && intval($browser->getMajor()) < 7) {
			if (JFile::exists(JPATH_ROOT .DS. $vars['themepath'] . '/' .$theme. '/css/style_ie6.css')) {
				$document->addStyleSheet(JURI::base(true).'/' . $vars['themepath'] . '/' .$theme.'/css/style_ie6.css?v='.$version);
			}
		}
	}
	function onAfterRoute()
	{
		global $mainframe;

		if ($mainframe->isAdmin()) {
			return;
		}
		
		$db =& JFactory::getDBO();
		
		// Causes issue in Safari??
		$pop 	= JRequest::getVar('pop', 0, 'int');
		$task 	= JRequest::getVar('task');
		$tmpl	= JRequest::getVar('tmpl');
		
		if ($pop || ($task == 'new' || $task == 'edit') || $tmpl == 'component') {
			return;
		}
		$params = $this->params;	
		
		$components = $params->get('components', '');
		if ($components) {
			$excluded 	= explode(',', $components);
			$option 	= JRequest::getVar('option', '');
			foreach ($excluded as $exclude) {
				if ($option == 'com_'. $exclude || $option == $exclude) {
					return;
				}
			}
		}
		
		$theme = $params->get('theme', 'standard');
			
		if ($params->get('dynamic_themes')) {
			$theme = JRequest::getWord('theme', $params->get('theme', 'standard'));
		}
		
		$popup = array(
			'legacy'			=>	$params->get('legacy', 0),
			//'convert'			=>	$params->get('convert', 0),
			'resize'			=>	$params->get('resize', 1),
			'icons'				=>	$params->get('icons', 1),
			'overlay'			=>	$params->get('overlay', 1),
			'overlayopacity'	=>	$params->get('overlayopacity', 0.8),
			'overlaycolor'		=>	$params->get('overlaycolor', '#000000'),
			'fadespeed'			=>	$params->get('fadespeed', 500),
			'scalespeed'		=>	$params->get('scalespeed', 500),
			'hideobjects'		=>	$params->get('hideobjects', 1),
			'scrollpopup'		=>	$params->get('scrollpopup', 1)
		);
		$tooltip = array(
			'className'			=>	$params->get('tipclass', 'tooltip'),
			'opacity'			=>	$params->get('tipopacity', 1),
			'speed'				=>	$params->get('tipspeed', 150),
			'position'			=>	$params->get('tipposition', 'br'),
			'offsets'			=>	"{x: ". $params->get('tipoffsets_x', 16) .", y: ". $params->get('tipoffsets_y', 16) ."}",
		);
		$standard = array(
			'imgpath'			=>	$params->get('imgpath', 'plugins/system/jceutilities/img'),
			//'pngfix'			=>	$params->get('pngfix', 0),
			//'wmode'			=>	$params->get('wmode', 0),
			'theme'				=>	$theme,
			'themecustom'		=>	$params->get('themecustom', ''),
			'themepath'			=>	$params->get('themepath', 'plugins/system/jceutilities/themes')
		);
		
		$media_versions = array(
			'flash'			=>	$params->get('flash', '10,0,22,87'),
			'windowmedia'	=>	$params->get('windowmedia', '5,1,52,701'),
			'quicktime'		=>	$params->get('quicktime', '6,0,2,0'),
			'realmedia'		=>	$params->get('realmedia', '7,0,0,0'),
			'shockwave'		=>	$params->get('shockwave', '8,5,1,0')
		);
		
		$document =& JFactory::getDocument();
		
		JHTML::_('behavior.mootools');
		jimport('joomla.environment.browser');
		jimport('joomla.filesystem.file');

		// Mediaobject plugin loaded?
		$mediaobject = JPluginHelper::isEnabled('system', 'mediaobject');

		$version = $this->getVersion();

		if (!$mediaobject) {
			$document->addScript(JURI::base(true).'/plugins/system/jceutilities/js/mediaobject.js?v='.$version);
		}
		
		$document->addScript(JURI::base(true).'/plugins/system/jceutilities/js/jceutilities.js?v='.$version);
		$document->addStyleSheet(JURI::base(true).'/plugins/system/jceutilities/css/jceutilities.css?v='.$version);
		// IE6 variation
		$browser = &JBrowser::getInstance();
		if ($browser->getBrowser() == 'msie' && intval($browser->getMajor()) < 7) {
			if (JFile::exists(JPATH_ROOT .DS. 'plugins/system/jceutilities/css/jceutilities_ie6.css?v='.$version)) {
				$document->addStyleSheet(JURI::base(true).'/plugins/system/jceutilities/css/jceutilities_ie6.css?v='.$version);
			}
		}
		$this->getThemeCss($standard);

		$html = "\t";
		if (!$mediaobject) {
			$html .= "MediaObject.init({";
			$html .= $this->renderParams('', $media_versions, true);
			$html .= "});";
		}
		$html .= "window.addEvent('domready', function(){window.jcepopup=new JCEUtilities({";
		$html .= $this->renderParams('popup', $popup, false);
		$html .= $this->renderParams('tooltip', $tooltip, false);
		$html .= $this->renderParams('', $standard, true);
		$html .= "});";
		$html .= "});";
						
		$document->addScriptDeclaration($html);
		return true;
	}	
}
?>