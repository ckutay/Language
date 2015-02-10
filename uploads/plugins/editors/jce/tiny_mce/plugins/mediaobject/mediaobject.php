<?php
/**
* @version $Id: mediaobject.php 2008-01-07 $
* @package MediaObject
* @copyright Copyright (C) 2006/2007/2008 Ryan Demmer. All rights reserved.
* @license http://www.gnu.org/copyleft/gpl.html GNU/GPL, see LICENSE.php
* This version may have been modified pursuant
* to the GNU General Public License, and as distributed it includes or
* is derivative of works licensed under the GNU General Public License or
* other free or open source software licenses.
*/

defined( '_JEXEC' ) or die( 'Restricted access' );

jimport( 'joomla.plugin.plugin');

/**
* JCE Utiltiies Plugin
*
* @package 		JCE Utilities
* @subpackage	System
*/
class plgSystemMediaobject extends JPlugin
{
	/**
	 * Constructor
	 *
	 * For php4 compatability we must not use the __constructor as a constructor for plugins
	 * because func_get_args ( void ) returns a copy of all passed arguments NOT references.
	 * This causes problems with cross-referencing necessary for the observer design pattern.
	 *
	 * @param	object		$subject The object to observe
	 * @param 	array  		$config  An array that holds the plugin configuration
	 * @since	1.0
	 */
	function plgSystemMediaobject(&$subject, $config)  {
		parent::__construct($subject, $config);
		
		// load plugin parameters
        $this->_plugin = JPluginHelper::getPlugin( 'system', 'mediaobject' );
        $this->_params = new JParameter( $this->_plugin->params );
	}
	
	function renderParams( $params ){
		$html = '';
		$i = 0;
		foreach( $params as $k => $v ){
			if( !is_numeric( $v ) ){
				$v = '"'. $v .'"';
			}
			if( $i < count( $params ) -1 ){
				$v .= ',';
			}
			$html .= "'". $k ."':". $v;
			$i++;
		}
		return $html;
	}
		
	function onAfterRoute(){
		global $mainframe;

		if ($mainframe->isAdmin()) {
			return;
		}
		
		$versions = array(
			'flash'			=>	$this->_params->get( 'flash', '9,0,124,0' ),
			'windowmedia'	=>	$this->_params->get( 'windowmedia', '5,1,52,701' ),
			'quicktime'		=>	$this->_params->get( 'quicktime', '6,0,2,0' ),
			'realmedia'		=>	$this->_params->get( 'realmedia', '7,0,0,0' ),
			'shockwave'		=>	$this->_params->get( 'shockwave', '8,5,1,0' )
		);
	
		$document =& JFactory::getDocument();
		$document->addScript( JURI::base() . 'plugins/system/mediaobject/js/mediaobject-150.js' );
		$html   = "\tMediaObject.init({";
		$html  .= $this->renderParams( $versions );
		$html  .= "});";
						
		$document->addScriptDeclaration( $html );
		return true;
	}	
}
?>