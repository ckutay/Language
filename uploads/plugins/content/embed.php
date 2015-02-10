<?php
/**
* @copyright (C) 2008 Dioscouri Design
* @author Dioscouri Design
* @license http://www.gnu.org/copyleft/gpl.html GNU/GPL
* Inspired by D4J Content Embedding BOT
*/

/** ensure this file is being included by a parent file */
defined( '_JEXEC' ) or die( 'Restricted access' );

$mainframe->registerEvent( 'onPrepareContent', 'plgEmbed' );

require_once( 'embed'.DS.'embedGenericImage.php' );
require_once( 'embed'.DS.'embedFetchContent.php' );


/**
* EMBED Plugin
*
* <b>Usage:</b>
* <code>{jugaaccess [!]group[,group]}...some content...{/jugaaccess}</code>
*
* One or more group name should be passed, you can expressly deny access by putting a '!'
* before the group name in question.  It will keep looping through the list provided until
* it finds a 'true' value so strange results may occur with conflicting group access. 
*
* Examples:
*
*		{jugaaccess Public Access}shows only to Public Access JUGA Group members{/jugaaccess}
*		{jugaaccess !Public Access}shows to all users who are not a member of JUGA Group Public Access{/jugaaccess}
*		{jugaaccess Restricted,!Public Access}shows to all Restricted JUGA Group members members who are NOT members of the Public Access Group{/jugaaccess}
*		{jugaaccess Restricted,Public Access}shows to all members of both JUGA Groups{/jugaaccess}
*
*/

/**
* Process the plugin
*/
// ************************************************************************/
function plgEmbed( &$row, $params='', $page=0 ) {
	global $database, $option, $task;

	//Check whether the plugin should process or not
	if ( JString::strpos( $row->text, 'embed' ) === false ) {
		return true;
	}
	 
	//Get plugin info
	$plugin = &JPluginHelper::getPlugin('content', 'embed');
	 
	//Search for this tag in the content
	$regex = '/{(embed)\s*(.*?)}/i';
	 
	//Access the parameters
	$pluginParams = new JParameter( $plugin->params );
	 
	//Check whether plugin has been unpublished
	if ( !$pluginParams->get( 'enabled', 1 ) ) {
		$row->text = preg_replace( $regex, '', $row->text );
		return true;
	}
	 
	//Find all instances of plugin and put in $matches
	// preg_match_all( $regex, $row->text, $matches );
	preg_match_all( $regex, $row->text, $matches, PREG_SET_ORDER );
		
	// echo "<pre>"; print_r($matches); echo "</pre>";

 	// Number of mambots
	$count = count($matches);

 	// only processes if there are instances 
 	if ( $count ) {
		// echo "count<br />";
		// no duplication
		if ( !isset($GLOBALS['_content_mambot_params']['contentembedding_loaded']) )
			$GLOBALS['_content_mambot_params']['contentembedding_loaded'] = array();
			$GLOBALS['_content_mambot_params']['contentembedding_loaded'][] = $row->id;
		// echo "not isset<br />";
		
		$option = JRequest::getVar( "option", JRequest::getVar( "option", "", "GET" ), "POST");
		$view = JRequest::getVar( "view", JRequest::getVar( "view", "", "GET" ), "POST");
		$task = JRequest::getVar( "task", JRequest::getVar( "task", "", "GET" ), "POST");

		// echo "option: $option, view: $view, task: $task<br />";
	 	// $params = new mosParameters( $mambot->params );
	 	// $params->def( 'processon', 'article' );
		$pluginParams->def( 'processon', 'article' );

	 	if ( ( $option == 'com_content' AND (
	 		($pluginParams->get('processon') == 'article')
	 	) ) ) {
	 		$articles = processEmbed( $row, $pluginParams, $matches, $count );

			// store some vars in globals to access from the replacer
			$GLOBALS['plgContentEmbeddingCount']		= 0;
			$GLOBALS['plgContentEmbeddingArray']		=& $articles;

			// perform the replacement
			$row->text = preg_replace_callback( $regex, 'replaceContentEmbedding', $row->text );

			// clean up globals
			unset( $GLOBALS['plgContentEmbeddingCount'] );
			unset( $GLOBALS['plgContentEmbeddingArray'] );

			return true;
		} else {
			$row->text = preg_replace( '/{embed\s*.*?}/i', '', $row->text );
		}
	}

	return false;
}

/**
* Process the plugin
*/
// ************************************************************************/
function processEmbed( &$row, &$params, &$matches, $count ) {
	global $_MAMBOTS;
	$articles = array();
	$args = array();

	for ( $i = 0; $i < $count; $i++ ) {
		// get params defined in bot tag
		if (isset($matches[$i][2])) {
 			parse_str( str_replace( '&amp;', '&', $matches[$i][2] ), $args );

 		}

		// echo "<pre>"; print_r($args); echo "</pre>";
		
		$settings['class_sfx'] =
			trim( isset($args['class_sfx'])		? $args['class_sfx']	: $params->get('class_sfx', '') );
		$settings['handler'] =
			trim( isset($args['handler'])		? $args['handler']		: $params->get('handler', '') );

		$settings['where'] =
			trim( isset($args['where'])			? $args['where']		: $params->get('where', 'category') );
		$settings['where_id'] =
			trim( isset($args['where_id'])		? $args['where_id']		: $params->get('where_id', '') );
		$settings['nodup'] =
			trim( isset($args['nodup'])			? $args['nodup']		: $params->get('nodup', 1) );
		$settings['ordering'] =
			trim( isset($args['ordering'])		? $args['ordering']		: $params->get('ordering', 'order') );
		$settings['count'] =
			intval( isset($args['count'])		? $args['count']		: $params->get('count', 5) );
		$settings['rowcount'] =
			intval( isset($args['rowcount'])	? $args['rowcount']		: $params->get('rowcount', 1) );
		$settings['bots'] =
			intval( isset($args['bots'])		? $args['bots']			: $params->get('bots', 1) );

		$settings['width'] =
			trim( isset($args['width'])				? $args['width']		: $params->get('width', '100%') );
		$settings['display'] =
			intval( isset($args['display'])			? $args['display']		: $params->get('display', 2) );
		$settings['hseparator'] =
			trim( isset($args['hseparator'])		? $args['hseparator']	: $params->get('hseparator', '') );
		$settings['hleftspace'] =
			intval( isset($args['hleftspace'])		? $args['hleftspace']	: $params->get('hleftspace', 5) );
		$settings['hrightspace'] =
			intval( isset($args['hrightspace'])		? $args['hrightspace']	: $params->get('hrightspace', 10) );
		$settings['vseparator'] =
			trim( isset($args['vseparator'])		? $args['vseparator']	: $params->get('vseparator', '') );
		$settings['vtopspace'] =
			intval( isset($args['vtopspace'])		? $args['vtopspace']	: $params->get('vtopspace', 5) );
		$settings['vbottomspace'] =
			intval( isset($args['vbottomspace'])	? $args['vbottomspace']	: $params->get('vbottomspace', 10) );

		$settings['showdate'] =
			intval( isset($args['showdate'])	? $args['showdate']		: $params->get('date', 1) );
		$settings['datepos'] =
			trim( isset($args['datepos'])		? $args['datepos']		: $params->get('datepos', 'after') );
		$settings['dateform'] =
			trim( isset($args['dateform'])		? $args['dateform']		: $params->get('dateform', '(d.m.Y)') );
		$settings['datelinked'] =
			intval( isset($args['datelinked'])	? $args['datelinked']	: $params->get('datelinked', 0) );

		$settings['showthumb'] =
			intval( isset($args['showthumb'])	? $args['showthumb']	: $params->get('thumbnail', 1) );
		$settings['thumbpos'] =
			trim( isset($args['thumbpos'])		? $args['thumbpos']		: $params->get('thumbpos', 'float_left') );
		$settings['thumbdefault'] =
			trim( isset($args['thumbdefault'])	? $args['thumbdefault']	: $params->get('thumbdefault', 'images/M_images/arrow.png') );
		$settings['linkedthumb'] =
			intval( isset($args['linkedthumb'])	? $args['linkedthumb']	: $params->get('linkedthumb', 0) );
		$settings['thumbwidth'] =
			intval( isset($args['thumbwidth'])	? $args['thumbwidth']	: $params->get('thumbwidth', 64) );
		$settings['thumbheight'] =
			intval( isset($args['thumbheight'])	? $args['thumbheight']	: $params->get('thumbheight', 48) );
		$settings['thumbmethod'] =
			intval( isset($args['thumbmethod'])	? $args['thumbmethod']	: $params->get('thumbmethod', 0) );
		$settings['thumbratio'] =
			intval( isset($args['thumbratio'])	? $args['thumbratio']	: $params->get('thumbratio', 3) );
		$settings['realthumb'] =
			intval( isset($args['realthumb'])	? $args['realthumb']	: $params->get('realthumb', 0) );
		$settings['thumbpath'] =
			trim( isset($args['thumbpath'])		? $args['thumbpath']	: $params->get('thumbpath', 'images/thumbnails') );
		$settings['imagelib'] =
			trim( isset($args['imagelib'])		? $args['imagelib']		: $params->get('imagelib', 'gd2') );
		$settings['imglibpath'] =
			trim( isset($args['imglibpath'])	? $args['imglibpath']	: $params->get('imglibpath', '') );

		$settings['linked'] =
			intval( isset($args['linked'])		? $args['linked']			: $params->get('linked', 0) );
		$settings['pdf'] =
			intval( isset($args['pdf'])			? $args['pdf']				: $params->get('pdf', 0) );
		$settings['print'] =
			intval( isset($args['print'])		? $args['print']			: $params->get('print', 0) );
		$settings['email'] =
			intval( isset($args['email'])		? $args['email']			: $params->get('email', 0) );
		$settings['icons'] =
			intval( isset($args['icons'])		? $args['icons']			: $params->get('icons', 1) );
		$settings['buttonpos'] =
			trim( isset($args['buttonpos'])		? $args['buttonpos']		: $params->get('buttonpos', 'beside') );
		$settings['buttonarrange'] =
			trim( isset($args['buttonarrange'])	? $args['buttonarrange']	: $params->get('buttonarrange', 'horizontal') );
		$settings['author'] =
			intval( isset($args['author'])		? $args['author']			: $params->get('author', 0) );
		$settings['onlyintro'] =
			intval( isset($args['onlyintro'])	? $args['onlyintro']		: $params->get('onlyintro', 1) );
		$settings['chars'] =
			intval( isset($args['chars'])		? $args['chars']			: $params->get('chars', 0) );
		$settings['words'] =
			intval( isset($args['words'])		? $args['words']			: $params->get('words', 0) );
		$settings['more'] =
			intval( isset($args['more'])		? $args['more']				: $params->get('more', 1) );
		$settings['openin'] =
			intval( isset($args['openin'])		? $args['openin']			: $params->get('openin', 0) );


		
		// no duplication check
		if ($settings['nodup']) {
			// is any article loaded?
			global $mainframe;
			$loaded = $mainframe->get("plgContentFetching_loaded", false);
			if (!$loaded) {
				$loaded = $GLOBALS['_content_mambot_params']['contentembedding_loaded'];
				$mainframe->set("plgContentFetching_loaded", $loaded);
			} else
				$loaded = array_merge($loaded, $GLOBALS['_content_mambot_params']['contentembedding_loaded']);
		} else {
			// prevent loading of current article to ignore forever loop
			$loaded = $GLOBALS['_content_mambot_params']['contentembedding_loaded'];
		}

		$retrieving = new embedFetchContent($settings, JPATH_BASE, $loaded);
		$articles[] = $retrieving->produceOutput();

		// no duplication check
		if ($settings['nodup']) {
			// store loaded article
			$loaded = $retrieving->loadedArticle();
			$mainframe->set("embedFetchContent_loaded", $loaded);
		}

		unset($retrieving);
	}

	return $articles;
}

/**
* Process the plugin
*/
// ************************************************************************/
function replaceContentEmbedding( &$matches ) {
	$i = $GLOBALS['plgContentEmbeddingCount']++;

	return @$GLOBALS['plgContentEmbeddingArray'][$i];
}

// ************************************************************************/
// ************************************************************************/
// ************************************************************************/
// ************************************************************************/
// ************************************************************************/
?>