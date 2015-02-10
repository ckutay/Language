<?php
/**
* @copyright (C) 2008 Dioscouri Design
* @author Dioscouri Design
* @license http://www.gnu.org/copyleft/gpl.html GNU/GPL
* Inspired by D4J Content Embedding BOT
*/

/** ensure this file is being included by a parent file */
defined( '_JEXEC' ) or die( 'Restricted access' );

if (!defined('_D4J_CONTENT_FETCHING')) {
	define('_D4J_CONTENT_FETCHING', 1);

	// require_once( _JOOMLA_ROOT.'/components/com_content/content.html.php' );

	class embedFetchContent {
		var $params		= '';
		var $except		= array();
		var $rows		= array();
		var $internal	= true;
		var $jroot		= '';
		var $output		= '';

		function embedFetchContent( $settings, $joomlaLocation, $except = array() ) {
			$this->except	= $except;
			$this->jroot	= $joomlaLocation;

			// $this->params = new mosParameters('');
			$this->params = new JParameter( '' );
			foreach ($settings AS $k => $v)
				$this->params->set($k, $v);

			switch ($this->params->get('where')) {
				// source is newsfeed category/item
				case 'newsfeed':
				case 'newsfeed_item':
					$this->internal = false;
					$this->parseExternalContents();
					break;
				// source is content section/category/item
				case 'related':
				case 'section':
				case 'category':
				case 'content':
				default:
					$this->internal = true;
					$this->parseInternalContents();
					break;
			}
		}

		function parseInternalContents() {
			global $mainframe;
			$mosConfig_offset = '';
			$database = &JFactory::getDBO();
			$my 	= &JFactory::getUser();

			// $now		= defined(_CURRENT_SERVER_TIME) ? _CURRENT_SERVER_TIME : date('Y-m-d H:i:s', time() + $mosConfig_offset * 60 * 60);
			$now = date("Y-m-d");
			$access		= !$mainframe->getCfg( 'shownoauth' );
			$nullDate	= method_exists($database, 'getNullDate') ? $database->getNullDate() : '0000-00-00 00:00:00';

			// no duplication?
			if (count($this->except))
				$exception ="\n AND ( a.id NOT IN (".implode(',', $this->except).') )';
			else
				$exception = '';

			// is eZine "Read more..." handler or com_content?
			if ($this->params->get('handler') == 'com_ezine') {
				if ($this->params->get('where') == 'section')
					$selectType = "ec.content_type = 'section' AND ec.contentid = a.sectionid";
				elseif ($this->params->get('where') == 'category')
					$selectType = "ec.content_type = 'category' AND ec.contentid = a.catid";
				else
					$selectType = "(ec.content_type = 'category' AND ec.contentid = a.catid) OR (ec.content_type = 'section' AND ec.contentid = a.sectionid)";
				$extra_query1 = ", ec.pageid, ec.id AS cat_id, m.id AS itemid";
				$extra_query2 = "\nINNER JOIN #__ezine_category AS ec ON $selectType";
				$extra_query2 .= "\nINNER JOIN #__menu AS m ON m.link = CONCAT('index.php?option=com_ezine&task=view&page=', ec.pageid, '&category=', ec.id)";
			} else {
				$extra_query1 = '';
				$extra_query2 = '';
			}

			// select between section, category, content item or related
			switch ( $this->params->get('where') ) {
				case 'related':
					// only affect full article reading page
					$option = JRequest::getVar( "option", JRequest::getVar( "option", "", "GET" ), "POST");
					$task = JRequest::getVar( "task", JRequest::getVar( "task", "", "GET" ), "POST");

					$aid = JRequest::getVar( "id", JRequest::getVar( "id", "", "GET" ), "POST");

					if ( ($option == 'com_content' AND $task == 'view' AND $aid > 0)
					OR ($option == 'com_ezine' AND $task == 'read' AND $aid > 0) ) {
						if ( $this->params->get('where_id') == 'same_section' ) {
							// retrieve related article based on content section
							$database->setQuery( "SELECT sectionid FROM #__content WHERE id = '$aid'", 0, 1 );
							$sectionID = $database->loadResult();
							if (!$sectionID) {
								return;
							}
							$where_clause = "\n AND ( a.sectionid = '$sectionID' )";
						} elseif ( $this->params->get('where_id') == 'same_category' ) {
							// retrieve related article based on content category
							$database->setQuery( "SELECT catid FROM #__content WHERE id = '$aid'", 0, 1 );
							$categoryID = $database->loadResult();
							if (!$categoryID) {
								return;
							}
							$where_clause = "\n AND ( a.catid = '$categoryID' )";
						} else {
							// retrieve related article based meta keyword
							$database->setQuery( "SELECT metakey FROM #__content WHERE id = '$aid'", 0, 1 );
							$metaKeywords = $database->loadResult();
							if (!$metaKeywords) {
								return;
							}
							$metaKeywords = explode( ',', $metaKeywords );
							foreach ($metaKeywords AS $metaKeyword) {
								$metaKeyword = trim($metaKeyword);
								$likeQuery[] = "(a.metakey LIKE '$metaKeyword,%' OR a.metakey LIKE '%,$metaKeyword,%' OR a.metakey LIKE '%,$metaKeyword')";
							}
							$where_clause = "\n AND ( ".implode(' OR ', $likeQuery)." )";
						}
					} else {
						return;
					}
					break;
				case 'content':
					$where_clause = "\n AND ( a.id IN (". $this->params->get('where_id') .") )";
					break;
				case 'section':  // retrieve content item from specified section
					$where_clause = "\n AND ( a.sectionid IN (". $this->params->get('where_id') .") )";
					break;
				case 'category':  // retrieve content item from specified category
				default:
					$where_clause = "\n AND ( a.catid IN (". $this->params->get('where_id') .") )";
					break;
			}

			// preparing order control
			switch ( $this->params->get('ordering') ) {
				case 'random':
					$orderby = 'RAND()';
					break;
				case 'date':
					$orderby = 'a.created';
					break;
				case 'rdate':
					$orderby = 'a.created DESC';
					break;
				case 'alpha':
					$orderby = 'a.title';
					break;
				case 'ralpha':
					$orderby = 'a.title DESC';
					break;
				case 'hits':
					$orderby = 'a.hits DESC';
					break;
				case 'rhits':
					$orderby = 'a.hits ASC';
					break;
				case 'order':
				default:
					$orderby = 'a.ordering';
					break;
			}

			$query = "SELECT a.id, a.title, a.introtext, a.fulltext, a.created, a.created_by, a.created_by_alias,"
			. "\n a.images, a.attribs AS `params`" . $extra_query1 . ", u.name AS author"
			. "\n FROM #__content AS a" . $extra_query2
			. "\n INNER JOIN #__users AS u ON u.id = a.created_by"
			. "\n WHERE ( a.state = '1' AND a.checked_out = '0' AND a.sectionid > '0' )"
			. "\n AND ( a.publish_up = '$nullDate' OR a.publish_up <= '$now' )"
			. "\n AND ( a.publish_down = '$nullDate' OR a.publish_down >= '$now' )"
		   	. ( $access ? "\n AND a.access <= '$my->gid'" : '' )
			. $where_clause . $exception
			. "\n ORDER BY $orderby LIMIT 0," . $this->params->get('count')
			;
			
			$database->setQuery( $query );
			// $rows = $database->loadObjectList();
			$this->rows = $database->loadObjectList();
			// echo "<pre>"; print_r($query); echo "</pre>";
			
		}

		function parseExternalContents() {
			global $database, $mosConfig_absolute_path, $mosConfig_cachepath;

			// check if cache directory is writeable
			$cacheDir = "$mosConfig_cachepath/";
			if ( !is_writable($cacheDir) ) {
				$this->output .= "<div class=\"message\">The <b>$cacheDir</b> is not writeable.<br/>Please notify administrator to correct this. Thank you!</div>";
				return;
			}

			// full RSS parser used to access image information
			require_once( "$mosConfig_absolute_path/includes/domit/xml_domit_rss.php" );
			$LitePath = "$mosConfig_absolute_path/includes/Cache/Lite.php";

			if ($this->params->get('where') == 'newsfeed_item') {
				$condition = "AND id IN (".$this->params->get('where_id').")";
			} else {
				$condition = "AND catid IN (".$this->params->get('where_id').")";
			}

			$database->setQuery( "SELECT name, link, numarticles, cache_time"
			. "\n FROM #__newsfeeds"
			. "\n WHERE published='1' AND checked_out='0' $condition"
			. "\n ORDER BY ordering"
			);
			$newsfeeds = $database->loadObjectList();

			$displayed = 0;

			foreach ($newsfeeds as $newsfeed) {
				if ($displayed >= $this->params->get('count')) break; else {
					// full RSS parser used to access image information
					$rssDoc = new xml_domit_rss_document();
					$rssDoc->setRSSTimeout(5);
					$rssDoc->useCacheLite( true, $LitePath, $cacheDir, $newsfeed->cache_time );
					$success = $rssDoc->loadRSS( $newsfeed->link );

					// collect items
					if ($success) {
						$totalChannels = $rssDoc->getChannelCount();
						for ($i = 0; $i < $totalChannels; $i++) {
							$currChannel	=& $rssDoc->getChannel($i);

							$actualItems	= $currChannel->getItemCount();
							$setItems		= $newsfeed->numarticles;
							if ( $setItems > $actualItems ) {
								$totalItems = $actualItems;
							} else {
								$totalItems = $setItems;
							}

							for ($j = 0; $j < $totalItems; $j++) {
								if ($displayed >= $this->params->get('count')) break; else {
									$row		= new stdClass();
									$currItem	=& $currChannel->getItem($j);

									$row->title = $currItem->getTitle();
									$row->title = mosCommonHTML::newsfeedEncoding($rssDoc, $row->title);

									// START fix for RSS enclosure tag url not showing
									if ($currItem->getLink()) {
										$row->link = ampReplace( $currItem->getLink() );
									} elseif ($currItem->getEnclosure()) {
										$enclosure = $currItem->getEnclosure();
										$row->link = ampReplace( $enclosure->getUrl() );
									}  elseif ( $currItem->getEnclosure() AND $currItem->getLink() ) {
										$enclosure = $currItem->getEnclosure();
										$row->link = ampReplace( $currItem->getLink() );
										$row->linkEnclosure = ampReplace( $enclosure->getUrl() );
									}
									// END fix for RSS enclosure tag url not showing

									$row->introtext = $currItem->getDescription();
									$row->introtext = mosCommonHTML::newsfeedEncoding( $rssDoc, $row->introtext );
									$row->fulltext = '';

									$this->rows[] = $row;
									$displayed++;
								}
							}
						}
					}
				}
			}
		}

		function produceOutput() {
			$total_count = count($this->rows);

			if ($total_count) {
				$col_width = (int) (100 / $this->params->get('rowcount'));
				$cur_index = 0;
				$width_remain = 100;

				// module wrapper
				$this->output .= '<div style="width:'.$this->params->get('width').';clear:both">'."\n";

				// process items retrieved
				foreach ( $this->rows AS $row ) {
					$cur_index++;

					// has horizontal separator defined or not?
					if ($this->params->get('hseparator') != '')
						$hsep = ';background:url('.$this->params->get('hseparator').') right top repeat-y';
					else
						$hsep = '';

					//has vertical separator defined or not?
					if ($this->params->get('vseparator') != '')
						$vsep = "\t<div style=\"width:100%;background:url(".$this->params->get('vseparator').") left center repeat-x;margin-top:".$this->params->get('vtopspace')."px;margin-bottom:".$this->params->get('vbottomspace')."px\">&nbsp;</div>\n";
					else
						$vsep = '';

					// prepare padding if separator defined
					if ($hsep AND ($cur_index % $this->params->get('rowcount')) != 1) {
						// if horizontal separator defined and this is not the first item in a row then apply padding left
						$paddingL = 'padding-left:'.$this->params->get('hleftspace').'px;';
					} else
						$paddingL = '';

					if ($hsep AND ($cur_index % $this->params->get('rowcount')) != 0 AND $cur_index != $total_count) {
						// if horizontal separator defined and this is not the last item in a row then apply padding right
						$paddingR = 'padding-right:'.$this->params->get('hrightspace').'px';
					} else
						$paddingR = '';

					// if character limitation defined
					if ($this->params->get('chars')) {
						if (strlen($row->introtext) >= $this->params->get('chars')) {
							$row->introtext = substr($row->introtext, 0, $this->params->get('chars')).'...';
							$row->fulltext = '';
						} elseif ($this->internal) {
							if (!$this->params->get('onlyintro'))
								$row->fulltext = substr($row->fulltext, 0, $this->params->get('chars') - strlen($row->introtext)).'...';
						}
					}

					// if word limitation defined
					if ($this->params->get('words')) {
						$word_arr = str_word_count($row->introtext, 2);
						$introwords = count($word_arr);
						if ($introwords >= $this->params->get('words')) {
							$c = 0;
							foreach ($word_arr AS $k => $v) {
								if ($c == $this->params->get('words')) {
									$row->introtext = substr($row->introtext, 0, $k).'...';
									break;
								}
								$c++;
							}
							$row->fulltext = '';
						} elseif ($this->internal) {
							if (!$this->params->get('onlyintro')) {
								$word_arr = str_word_count($row->fulltext, 2);
								$c = 0;
								foreach ($word_arr AS $k => $v) {
									if ($c == ($this->params->get('words') - $introwords)) {
										$row->fulltext = substr($row->fulltext, 0, $k).'...';
										break;
									}
									$c++;
								}
							}
						}
					}

					if ($this->internal) {
						global $mainframe;
						$mosConfig_live_site = $mainframe->getCfg('live_site');

						// loadbots?
						if ($this->params->get('onlyintro'))
							$row->text = $row->introtext;
						else
							$row->text = $row->introtext.'<-intro|full->'.$row->fulltext;

						if ($this->params->get('bots') AND $this->params->get('display') != 0) {
							$content_params = new JParameter( $row->params );

							$content_params->def( 'link_titles', 	$this->params->get('linked') );
							$content_params->def( 'pdf', 			$this->params->get('pdf') );
							$content_params->def( 'print', 			$this->params->get('print') );
							$content_params->def( 'email', 			$this->params->get('email') );
							$content_params->def( 'icons', 			$this->params->get('icons') );
							$content_params->def( 'readmore', 		$this->params->get('more') );
							$content_params->def( 'author', 		$this->params->get('author') );
							$content_params->def( 'createdate', 	$this->params->get('showdate') );
							$content_params->def( 'modifydate', 	!$mainframe->getCfg( 'hideModifyDate' ) );
							$content_params->def( 'rating', 		$mainframe->getCfg( 'vote' ) );

							$content_params->def( 'pageclass_sfx', 	$this->params->get('class_sfx') );
							$content_params->def( 'item_title', 	($this->params->get('display') != 1 ? 1 : 0) );
							$content_params->def( 'introtext', 		($this->params->get('display') != 0 ? 1 : 0) );
							$content_params->def( 'image', 			$this->params->get('bots') );
							$content_params->def( 'section', 		0 );
							$content_params->def( 'section_link', 	0 );
							$content_params->def( 'category', 		0 );
							$content_params->def( 'category_link', 	0 );
							$content_params->def( 'url', 			1 );

							// process bots
							// global $_MAMBOTS;
							// $_MAMBOTS->loadBotGroup( 'content' );
							// JPluginHelper::importPlugin( 'content', null, false );
							// $_MAMBOTS->trigger( 'onPrepareContent', array( &$row, &$content_params, 0 ), true );
							// JDispatcher::trigger( 'onPrepareContent' );
						} elseif ($this->params->get('display') != 0)
							$row->text = preg_replace('/{([a-zA-Z0-9\-_]*)\s*(.*?)}/i', '', $row->text);

						if ($this->params->get('onlyintro'))
							$row->introtext = $row->text;
						else
							list($row->introtext,$row->fulltext) = explode('<-intro|full->', $row->text, 2);
						// show date published?
						if ($this->params->get('showdate') AND $this->params->get('display') != 1) {
							$itemTimeStamp = mktime(substr($row->created, 11, 2), substr($row->created, 14, 2), substr($row->created, 17, 2), substr($row->created, 5, 2), substr($row->created, 8, 2), substr($row->created, 0, 4));
							$datePublished = date($this->params->get('dateform'), $itemTimeStamp);
							if ($this->params->get('datepos') != 'joomla')
								$datePublished = '<span class="createdate'.$this->params->get('class_sfx').'">'.$datePublished.'</span>';
						}

						// is eZine "Read more..." handler or com_content?
						if ($this->params->get('handler') == 'com_ezine') {
							$row->link = sefRelToAbs( "index.php?option=com_ezine&task=read&page=$row->pageid&category=$row->cat_id&article=$row->id&Itemid=$row->itemid" );
						} else {
							// needed to reduce queries used by getItemid for Content Items
							$bs		= $mainframe->getBlogSectionCount();
							$bc		= $mainframe->getBlogCategoryCount();
							$gbs	= $mainframe->getGlobalBlogSectionCount();
							$Itemid	= $mainframe->getItemid( $row->id, 1, 1, $bs, $bc, $gbs );

							// Blank itemid check for SEF
							if ($Itemid == NULL)
								$Itemid = '';
							else
								$Itemid = "&amp;Itemid=$Itemid";
							
							$url = 'index.php?option=com_content&amp;task=view&amp;id='.$row->id.$Itemid;
							// $row->link = sefRelToAbs( $url );
							$row->link = JRoute::_($url);
						}
					}

					// browser navigation
					if ($this->params->get('openin') == 1)
						$row->link .= '" target="_blank';
					elseif ($this->params->get('openin') == 2)
						$row->link .= '" onclick="window.open(\''.$row->link.'\', \'\', \'toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=780,height=550\'); return false';

					if ($this->internal) {
						// create thumbnail
						if ($this->params->get('showthumb')) {
							$thumbURL = $this->params->get('thumbdefault') ? $mosConfig_live_site.'/'.$this->params->get('thumbdefault') : '';
							$dimensions = embedGenericImage::resizeImage($this->jroot.'/'.$this->params->get('thumbdefault'), $this->params->get('thumbwidth'), $this->params->get('thumbheight'), $this->params->get('thumbratio'), $this->params->get('thumbmethod'));
							$thumbStyle = ' style="width:'.$dimensions[1][0].'px;height:'.$dimensions[1][1].'px;';
							if ($row->images) {
								$itemImg = explode( "\n", $row->images, 2 );
								$firstImg = explode( '|', $itemImg[0] );
								$dimensions = embedGenericImage::resizeImage($this->jroot.'/images/stories/'.$firstImg[0], $this->params->get('thumbwidth'), $this->params->get('thumbheight'), $this->params->get('thumbratio'), $this->params->get('thumbmethod'));
								if (is_array($dimensions)) {
									$sourceDimension = $dimensions[0];
									$thumbDimension = $dimensions[1];
									$thumbURL = $mosConfig_live_site.'/images/stories/'.$firstImg[0].'" width="'.$thumbDimension[0].'" height="'.$thumbDimension[1];

									if ($this->params->get('realthumb') AND ($sourceDimension[0] != $thumbDimension[0] OR $sourceDimension[1] != $thumbDimension[1])) {
										if (!is_dir($this->jroot.'/'.$this->params->get('thumbpath'))) {
											mkdir($this->jroot.'/'.$this->params->get('thumbpath'));
										}

										$thumbPath = $this->jroot.'/'.$this->params->get('thumbpath').'/'.preg_replace("/(\.\w{3,4})$/i", '_'.$thumbDimension[0].'x'.$thumbDimension[1].'.jpg', basename($firstImg[0]));
										if (embedGenericImage::createThumbnail($this->jroot.'/images/stories/'.$firstImg[0], $thumbPath, $thumbDimension, $this->params->get('imagelib')))
											$thumbURL = $mosConfig_live_site.'/'.$this->params->get('thumbpath').'/'.preg_replace("/(\.\w{3,4})$/i", '_'.$thumbDimension[0].'x'.$thumbDimension[1].'.jpg', basename($firstImg[0]));
									}

									// reset thumbnail style
									$thumbStyle = ' style="';

									// clear first {mosimage} bot tag and image params
									$row->text = $row->introtext.'<-intro|full->'.$row->fulltext;
									$row->text = preg_replace('/{(mosimage)\s*(.*?)}/i', '', $row->text, 1);
									list($row->introtext,$row->fulltext) = explode('<-intro|full->', $row->text, 2);
									$row->images = isset($itemImg[1]) ? $itemImg[1] : '';
								}
							}

							// prepare for thumbnail position
							if ($this->params->get('thumbpos') == 'float_left')
								$thumbStyle .= 'float:left;margin-right:0.25em'.($paddingL != '' ? ';'.str_replace('padding', 'margin', $paddingL) : '').'"';
							elseif ($this->params->get('thumbpos') == 'float_right')
								$thumbStyle .= 'float:right;margin-left:0.25em'.($paddingR != '' ? ';'.str_replace('padding', 'margin', $paddingR) : '').'"';
							else
								$thumbStyle .= 'margin:0.25em 0"';

							// thumbnail HTML code
							if ($thumbURL) {
								$thumbCode = '<img src="'.$thumbURL.'" border="0" alt="'.((isset($firstImg) AND isset($firstImg[4])) ? $firstImg[4] : $row->title).'"'.$thumbStyle.' />';

								if (isset($firstImg) AND ($sourceDimension[0] != $thumbDimension[0] OR $sourceDimension[1] != $thumbDimension[1])) {
									// linked thumbnail?
									if ($this->params->get('linkedthumb') == 2) {
										$sourceURL = $mosConfig_live_site.'/images/stories/'.$firstImg[0];
										$thumbCode = '<a href="javascript:void(0)" onclick="window.open(\''.$sourceURL.'\', \'\', \'toolbar=no,location=no,status=no,menubar=no,scrollbars=no,resizable=no,width='.($sourceDimension[0] + 16).',height='.($sourceDimension[1] + 16).'\'); return false">'.$thumbCode.'</a>';
									}
								}
								unset($firstImg);
								unset($sourceDimension);
								unset($thumbDimension);

								if ($this->params->get('linkedthumb') == 1)
									$thumbCode = '<a href="'.$row->link.'">'.$thumbCode.'</a>';
							}
						}
					}

					// linked title or not?
					if ($this->params->get('linked') AND $this->params->get('display') != 1) {
						if ( isset($datePublished) AND $this->params->get('datelinked') ) {
							if ($this->params->get('datepos') == 'before')
								$row->title = $datePublished.'&nbsp;'.$row->title;
							elseif ($this->params->get('datepos') == 'after')
								$row->title = $row->title.'&nbsp;'.$datePublished;
						}
						$row->title = '<a class="contentpagetitle'.$this->params->get('class_sfx').'" href="'.$row->link.'">'.$row->title.'</a>';
						if ( isset($datePublished) AND !($this->params->get('datelinked')) ) {
							if ($this->params->get('datepos') == 'before')
								$row->title = $datePublished.'&nbsp;'.$row->title;
							elseif ($this->params->get('datepos') == 'after')
								$row->title = $row->title.'&nbsp;'.$datePublished;
						}
					} elseif (isset($datePublished) AND $this->params->get('display') != 1) {
						if ($this->params->get('datepos') == 'before')
							$row->title = $datePublished.'&nbsp;'.$row->title;
						elseif ($this->params->get('datepos') == 'after')
							$row->title = $row->title.'&nbsp;'.$datePublished;
					}

					if ($this->internal) {
						// show author?
						if ($this->params->get('author') AND $this->params->get('display') != 1)
							$authorCode = '<span class="small'.$this->params->get('class_sfx').'">'._WRITTEN_BY.' '.($row->created_by_alias ? $row->created_by_alias : $row->author).'</span>&nbsp;&nbsp;';

						// check if any button is defined to show?
						if ( ($this->params->get('pdf') OR $this->params->get('print') OR $this->params->get('email')) AND $this->params->get('display') != 1 ){
							$pdfButton		= '';
							$printButton	= '';
							$emailButton	= '';

							if ($this->params->get('pdf')) {
								$status	= 'status=no,toolbar=no,scrollbars=yes,titlebar=no,menubar=no,resizable=yes,width=640,height=480,directories=no,location=no';
								$link	= "$mosConfig_live_site/index2.php?option=com_content&amp;do_pdf=1&amp;id=$row->id";

								if ($this->params->get('icons'))
									$pdfButton = mosAdminMenus::ImageCheck( 'pdf_button.png', '/images/M_images/', NULL, NULL, _CMN_PDF, _CMN_PDF );
								else
									$pdfButton = _CMN_PDF;

								$pdfButton = '<a href="'.$link.'" target="_blank" onclick="window.open(\''.$link.'\',\'win2\',\''.$status.'\'); return false;" title="'._CMN_PDF.'">'.$pdfButton.'</a>';
							}
							if ($this->params->get('print')) {
								$status	= 'status=no,toolbar=no,scrollbars=yes,titlebar=no,menubar=no,resizable=yes,width=640,height=480,directories=no,location=no';
								$link	= "$mosConfig_live_site/index2.php?option=com_content&amp;task=view&amp;id=$row->id&amp;pop=1";

								if ($this->params->get('icons'))
									$printButton = mosAdminMenus::ImageCheck( 'printButton.png', '/images/M_images/', NULL, NULL, _CMN_PRINT, _CMN_PRINT );
								else
									$printButton = _CMN_PRINT;

								$printButton = '<a href="'.$link.'" target="_blank" onclick="window.open(\''.$link.'\',\'win2\',\''.$status.'\'); return false;" title="'._CMN_PRINT.'">'.$printButton.'</a>';
								if (!$this->params->get('icons'))
									$printButton = (($this->params->get('buttonarrange') != 'vertical' AND $pdfButton) ? '&nbsp;'._ICON_SEP.'&nbsp;&nbsp;' : '').$printButton;
							}
							if ($this->params->get('email')) {
								$status	= 'status=no,toolbar=no,scrollbars=yes,titlebar=no,menubar=no,resizable=yes,width=400,height=250,directories=no,location=no';
								$link	= "$mosConfig_live_site/index2.php?option=com_content&amp;task=emailform&amp;id=$row->id";

								if ($this->params->get('icons'))
									$emailButton = mosAdminMenus::ImageCheck( 'emailButton.png', '/images/M_images/', NULL, NULL, _CMN_EMAIL, _CMN_EMAIL );
								else
									$emailButton = _CMN_EMAIL;

								$emailButton = '<a href="'.$link.'" target="_blank" onclick="window.open(\''.$link.'\',\'win2\',\''.$status.'\'); return false;" title="'._CMN_EMAIL.'">'.$emailButton.'</a>';
								if (!$this->params->get('icons'))
									$emailButton = (($this->params->get('buttonarrange') != 'vertical' AND ($pdfButton OR $printButton)) ? '&nbsp;'._ICON_SEP.'&nbsp;&nbsp;' : '').$emailButton;
							}

							// finalize button code
							if ($this->params->get('buttonarrange') == 'horizontal') {
								if ($this->params->get('buttonpos') == 'beside')
									$buttonsCode = ($pdfButton ? '<td class="buttonheading'.$this->params->get('class_sfx').'" align="right" valign="top" width="100%">'.$pdfButton.'</td>' : '')
									.($printButton ? '<td class="buttonheading'.$this->params->get('class_sfx').'" align="right" valign="top" width="100%">'.$printButton.'</td>' : '')
									.($emailButton ? '<td class="buttonheading'.$this->params->get('class_sfx').'" align="right" valign="top" width="100%">'.$emailButton.'</td>' : '');
								else
									$buttonsCode = ($pdfButton ? '<div style="display:inline;margin:0 0.25em">'.$pdfButton.'</div>' : '')
									.($printButton ? '<div style="display:inline;margin:0 0.25em">'.$printButton.'</div>' : '')
									.($emailButton ? '<div style="display:inline;margin:0 0.25em">'.$emailButton.'</div>' : '');
							} else {
								if ($this->params->get('buttonpos') == 'beside')
									$buttonsCode = '<td class="buttonheading'.$this->params->get('class_sfx').'" align="right" valign="top" width="100%">';
								else
									$buttonsCode = '';
								$buttonsCode .= ($pdfButton ? '<div style="margin:0.25em 0">'.$pdfButton.'</div>' : '')
								.($printButton ? '<div style="margin:0.25em 0">'.$printButton.'</div>' : '')
								.($emailButton ? '<div style="margin:0.25em 0">'.$emailButton.'</div>' : '');
								if ($this->params->get('buttonpos') == 'beside')
									$buttonsCode .= '</td>';
							}
						}
					}

					// content wrapper
					if ( ($cur_index % $this->params->get('rowcount')) == 0 OR $cur_index == $total_count )
						$this->output .= "\t<div style=\"float:left;width:$width_remain%\">\n";
					else {
						$this->output .= "\t<div style=\"float:left;width:$col_width%$hsep\">\n";
						$width_remain -= intval($col_width);
					}

					// has padding defined or not?
					if ($paddingL != '' OR $paddingR != '')
						$paddingCode = " style=\"$paddingL$paddingR\"";
					else
						$paddingCode = '';

					// thumbnail position is float left or float right?
					if (isset($thumbCode) AND $this->params->get('thumbpos') == 'float_left') {
						$this->output .= '<table border="0" cellpadding="3" cellspacing="3"><tr><td valign="top" width="'.$this->params->get('thumbwidth').'">';
						$this->output .= $thumbCode;
						$this->output .= '</td><td valign="middle">';
					} elseif (isset($thumbCode) AND $this->params->get('thumbpos') == 'float_right') {
						$this->output .= '<table border="0" cellpadding="3" cellspacing="3"><tr><td valign="middle">';
					}

					if ($this->params->get('display') != 1) { // not set to show text only => show title
						$this->output .= '<table class="contentpaneopen'.$this->params->get('class_sfx').'"'.$paddingCode.' width="100%"><tr>';
						// thumbnail position is above title?
						if (isset($thumbCode) AND $this->params->get('thumbpos') == 'title_above')
							$this->output .= '<td style="text-align:center">'.$thumbCode.'</td></tr><tr>';
						$this->output .= '<td class="contentheading'.$this->params->get('class_sfx').'" width="100%" valign="top">'.$row->title.'</td>';
						if (isset($buttonsCode) AND $this->params->get('buttonpos') == 'beside')
							$this->output .= $buttonsCode;
						$this->output .= '</tr></table>';

						// button position is below title?
						if (isset($buttonsCode) AND $this->params->get('buttonpos') == 'below')
							$this->output .= '<div style="text-align:right'.($paddingR != '' ? ';'.str_replace('padding', 'margin', $paddingR) : '').'">'.$buttonsCode.'</div>';

						// thumbnail position is below title?
						if (isset($thumbCode) AND $this->params->get('thumbpos') == 'title_below')
							$this->output .= $thumbCode;
					}
					if ($this->params->get('display') != 0 OR $this->params->get('more')) { // not set to show title only or read more is set to show => write table code
						$this->output .= '<table class="contentpaneopen'.$this->params->get('class_sfx').'"'.$paddingCode.'>';
						if (isset($authorCode))
							$this->output .= '<tr><td colspan="2" align="left" valign="top" width="70%">'.$authorCode.'</td></tr>';
						if (isset($datePublished) AND $this->params->get('datepos') == 'joomla')
							$this->output .= '<tr><td colspan="2" class="createdate'.$this->params->get('class_sfx').'" valign="top">'.$datePublished.'</td></tr>';
						if ($this->params->get('display') != 0) { // not set to show title only => show text
							// thumbnail position is above intro?
							if (isset($thumbCode) AND $this->params->get('thumbpos') == 'intro_above')
								$this->output .= '<tr><td colspan="2" style="text-align:center">'.$thumbCode.'</td</tr>';
							$this->output .= '<tr><td colspan="2" valign="top">'.$row->introtext.'</td></tr>';
							// thumbnail position is below intro?
							if (isset($thumbCode) AND $this->params->get('thumbpos') == 'intro_below')
								$this->output .= '<tr><td colspan="2" style="text-align:center">'.$thumbCode.'</td</tr>';
							// if not intro only, show full text
							if ($this->internal) {
								if (!$this->params->get('onlyintro')) {
									$this->output .= '<tr><td colspan="2" valign="top">'.$row->fulltext.'</td></tr>';
									// thumbnail position is below full?
									if (isset($thumbCode) AND $this->params->get('thumbpos') == 'full_below')
										$this->output .= '<tr><td colspan="2" style="text-align:center">'.$thumbCode.'</td</tr>';
								}
							}
						}
						if ($this->params->get('more')) { // show read more link
							// thumbnail position is above read more?
							if (isset($thumbCode) AND $this->params->get('thumbpos') == 'full_below' AND $this->params->get('onlyintro'))
								$this->output .= '<tr><td colspan="2" style="text-align:center">'.$thumbCode.'</td</tr>';
							$this->output .= '<tr><td colspan="2" align="left"><a class="readon'.$this->params->get('class_sfx').'" href="'.$row->link.'">'.JText::_( 'More' ).'</a></td></tr>';
							// thumbnail position is below read more?
							if (isset($thumbCode) AND $this->params->get('thumbpos') == 'more_below')
								$this->output .= '<tr><td colspan="2" style="text-align:center">'.$thumbCode.'</td</tr>';
						}
						$this->output .= '</table>';
					}

					// thumbnail position is float left or float right?
					if (isset($thumbCode) AND $this->params->get('thumbpos') == 'float_left') {
						$this->output .= '</td></tr></table>';
					} elseif (isset($thumbCode) AND $this->params->get('thumbpos') == 'float_right') {
						$this->output .= '</td><td valign="top" width="'.$this->params->get('thumbwidth').'">';
						$this->output .= $thumbCode;
						$this->output .= '</td></tr></table>';
					}

					// end of content wrapper
					if ( $cur_index == $total_count )
						$this->output .= "\t</div>\n\t<div style=\"clear:left\"><!-- --></div>\n";
					else
						$this->output .= "\t</div>\n";

					// begin new content row?
					if ( ($cur_index % $this->params->get('rowcount')) == 0 AND $cur_index != $total_count ) {
						$this->output .= "\t<div style=\"clear:left\"><!-- --></div>\n$vsep";
						$width_remain = 100;
					}

					// store loaded internal item
					if ($this->internal)
						$this->except[] = $row->id;
				}

				// end of module wrapper
				$this->output .= "</div>\n";
			}

			return $this->output;
		}

		function loadedArticle() {
			return $this->except;
		}
	}
}
?>