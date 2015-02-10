<?php
/**
* @copyright (C) 2008 Dioscouri Design
* @author Dioscouri Design
* @license http://www.gnu.org/copyleft/gpl.html GNU/GPL
* Inspired by D4J Content Embedding BOT
*/

/** ensure this file is being included by a parent file */
defined( '_JEXEC' ) or die( 'Restricted access' );

if (!defined('_EMBED_GENERIC_IMAGE')) {
	define('_EMBED_GENERIC_IMAGE', 1);

	class embedGenericImage {
		/**********************************************************************
		* Function to calculate new image dimension based on:
		*
		* $src_img			- server path to the source image
		* $w				- targeted width
		* $h				- targeted height
		* $keep_ratio		- 0: resize source image to the targeted width and height
		*					- 1: keep image aspect ratio and resize it to fit only the targeted width
		*					- 2: keep image aspect ratio and resize it to fit only the targeted height
		*					- 3: keep image aspect ratio and resize it to fit both the targeted width and height
		* $process_menthod	- 0: reduce image which has dimension larger than the targeted dimension only
		*					- 1: enlarge image which has dimension smaller than the targeted dimension only
		*					- 2: resize image when the targeted dimension differs from the original dimension
		*
		* Return value		- false if any error occured
		*					- array( array($sourceImageWidth, $sourceImageHeight), array($resizedWidth, $resizedHeight) )
		**********************************************************************/
		function resizeImage($src_img, $w, $h, $keep_ratio, $process_menthod) {
			// get source image dimension
			$img_size = getimagesize($src_img);
			if (is_array($img_size)) {
				$new_x = $img_size[0];
				$new_y = $img_size[1];
			} else {
				return false;
			}

			switch ($keep_ratio) {
				case '1': // fit predefined width
					if (
						($process_menthod == 0 AND $img_size[0] > $w)
						OR ($process_menthod == 1 AND $img_size[0] < $w)
						OR ($process_menthod == 2 AND $img_size[0] != $w)
					) {
						$new_x = $w;
						$size_ratio = (double) ($w / $img_size[0]);
						$new_y = (int) ($img_size[1] * $size_ratio);
					}
					break;
				case '2': // fit predefined height
					if (
						($process_menthod == 0 AND $img_size[1] > $h)
						OR ($process_menthod == 1 AND $img_size[1] < $h)
						OR ($process_menthod == 2 AND $img_size[1] != $h)
					) {
						$new_y = $h;
						$size_ratio = (double) ($h / $img_size[1]);
						$new_x = (int) ($img_size[0] * $size_ratio);
					}
					break;
				case '3': // fit both predefined width and height
					if (
						($process_menthod == 0 AND ($img_size[0] > $w OR $img_size[1] > $h))
						OR ($process_menthod == 1 AND ($img_size[0] < $w OR $img_size[1] < $h))
						OR ($process_menthod == 2 AND ($img_size[0] != $w OR $img_size[1] != $h))
					) {
						if ($process_menthod == 0) { // Reduce Only
							if ($img_size[0] > $w AND $img_size[1] > $h) {
								if ( ($img_size[0] / $img_size[1]) > ($w / $h) ) {
									$new_x = $w;
									$size_ratio = (double) ($w / $img_size[0]);
									$new_y = (int) ($img_size[1] * $size_ratio);
								} elseif ( ($img_size[0] / $img_size[1]) < ($w / $h) ) {
									$new_y = $h;
									$size_ratio = (double) ($h / $img_size[1]);
									$new_x = (int) ($img_size[0] * $size_ratio);
								} else {
									$new_x = $w;
									$new_y = $h;
								}
							} elseif ($img_size[0] > $w) {
								$new_x = $w;
								$size_ratio = (double) ($w / $img_size[0]);
								$new_y = (int) ($img_size[1] * $size_ratio);
							} elseif ($img_size[1] > $h) {
								$new_y = $h;
								$size_ratio = (double) ($h / $img_size[1]);
								$new_x = (int) ($img_size[0] * $size_ratio);
							}
						} elseif ($process_menthod == 1) { // Enlarge Only
							if ($img_size[0] < $w AND $img_size[1] < $h) {
								if ( ($img_size[0] / $img_size[1]) > ($w / $h) ) {
									$new_x = $w;
									$size_ratio = (double) ($w / $img_size[0]);
									$new_y = (int) ($img_size[1] * $size_ratio);
								} elseif ( ($img_size[0] / $img_size[1]) < ($w / $h) ) {
									$new_y = $h;
									$size_ratio = (double) ($h / $img_size[1]);
									$new_x = (int) ($img_size[0] * $size_ratio);
								} else {
									$new_x = $w;
									$new_y = $h;
								}
							} elseif ($img_size[0] < $w) {
								$new_x = $w;
								$size_ratio = (double) ($w / $img_size[0]);
								$new_y = (int) ($img_size[1] * $size_ratio);
							} elseif ($img_size[1] < $h) {
								$new_y = $h;
								$size_ratio = (double) ($h / $img_size[1]);
								$new_x = (int) ($img_size[0] * $size_ratio);
							}
						} elseif ($process_menthod == 2) { // Both Reduce/Enlarge
							if (
								($img_size[0] > $w AND $img_size[1] > $h)
								OR ($img_size[0] < $w AND $img_size[1] < $h)
							) {
								if ( ($img_size[0] / $img_size[1]) > ($w / $h) ) {
									$new_x = $w;
									$size_ratio = (double) ($w / $img_size[0]);
									$new_y = (int) ($img_size[1] * $size_ratio);
								} elseif ( ($img_size[0] / $img_size[1]) < ($w / $h) ) {
									$new_y = $h;
									$size_ratio = (double) ($h / $img_size[1]);
									$new_x = (int) ($img_size[0] * $size_ratio);
								} else {
									$new_x = $w;
									$new_y = $h;
								}
							} elseif ($img_size[0] > $w) {
								$new_x = $w;
								$size_ratio = (double) ($w / $img_size[0]);
								$new_y = (int) ($img_size[1] * $size_ratio);
							} elseif ($img_size[1] > $h) {
								$new_y = $h;
								$size_ratio = (double) ($h / $img_size[1]);
								$new_x = (int) ($img_size[0] * $size_ratio);
							}
						}
					}
					break;
				case '0': // fix to predefined width and height without keeping aspect ratio
				default:
					if (
						($process_menthod == 0 AND ($img_size[0] > $w OR $img_size[1] > $h))
						OR ($process_menthod == 1 AND ($img_size[0] < $w OR $img_size[1] < $h))
						OR ($process_menthod == 2 AND ($img_size[0] != $w OR $img_size[1] != $h))
					) {
						$new_x = $w;
						$new_y = $h;
					}
					break;
			}
			return array( $img_size, array($new_x, $new_y) );
		}

		/**********************************************************************
		* Function to create new image based on:
		*
		* $src_img			- server path to the source image
		* $desc_img			- server path to store target image
		* $desc_dimension	- array( $descWidth, $descHeight )
		* $image_lib		- use GD2 or ImageMagick or NetPBM to create new image?
		* $lib_path			- server path to where ImageMagick / NetPBM image processing software is installed
		*
		* Return value		- false if any error occured
		*					- true if new image created successful
		**********************************************************************/
		function createThumbnail($src_img, $desc_img, $desc_dimension, $image_lib, $lib_path = '') {
			if ($lib_path != '')
				$lib_path = str_replace('\\', '/', $lib_path);

			if (!file_exists($desc_img)) $created = false; else {
				$imginfo = getimagesize($desc_img);
				if (!is_array($imginfo) OR ($imginfo[0] != $desc_dimension[0] OR $imginfo[1] != $desc_dimension[1])) {
					@unlink($desc_img);
					$created = false;
				} else
					$created = true;
			}

			if (!$created) {
				switch ($image_lib) {
					case 'imagemagick':
						$created = embedGenericImage::createThumbnail_ImageMagick($src_img, $desc_img, $desc_dimension, $lib_path);
						break;
					case 'netpbm':
						$created = embedGenericImage::createThumbnail_NetPBM($src_img, $desc_img, $desc_dimension, $lib_path);
						break;
					case 'gd2':
					default:
						$created = embedGenericImage::createThumbnail_GD2($src_img, $desc_img, $desc_dimension);
						break;
				}
			}

			return $created;
		}
		/**********************************************************************
		* Create new image using GD2 library
		**********************************************************************/
		function createThumbnail_GD2($src_img, $desc_img, $desc_dimension) {
			$imageTypes = array( 1 => 'gif', 2 => 'jpeg', 3 => 'png', 4 => 'swf', 5 => 'psd', 6 => 'bmp', 7 => 'tiff', 8 => 'tiff', 9 => 'jpc', 10 => 'jp2', 11 => 'jpx', 12 => 'jb2', 13 => 'swc', 14 => 'iff', 15 => 'wbmp', 16 => 'xbm');

			$imgInfo = getimagesize($src_img);
			if (!is_array($imgInfo)) return false;

			// convert $type into a usable string
			list( $sourceWidth, $sourceHeight, $type ) = $imgInfo;
			$type = $imageTypes[$type];

			// check if we can read this type of file
			if (!function_exists( "imagecreatefrom$type")) return false;

			// load source image file into a resource
			$loadImg = "imagecreatefrom$type";
			$sourceImg = $loadImg($src_img);
			if (!$sourceImg) return false;

			// create target resource
			$targetImg = imagecreatetruecolor($desc_dimension[0], $desc_dimension[1]);

			// resize from source resource image to target
			if ( !imagecopyresampled($targetImg, $sourceImg, 0, 0, 0, 0, $desc_dimension[0], $desc_dimension[1], $sourceWidth, $sourceHeight) )
				return false;

			// write the image
			if ( !imagejpeg($targetImg, $desc_img, '80') ) return false;

			return true;
		}
		/**********************************************************************
		* Create new image using ImageMagick software
		**********************************************************************/
		function createThumbnail_ImageMagick($src_img, $desc_img, $desc_dimension, $lib_path) {
			if (!file_exists("$lib_path/convert") AND !file_exists("$lib_path/convert.exe"))
				return false;

			$cmd = "$lib_path/convert -resize $desc_dimension[0] $src_img $desc_img";
			exec( $cmd, $results, $return );

			if ($return > 0)
				return false;
			else
				return true;
		}
		/**********************************************************************
		* Create new image using NetPBM software
		**********************************************************************/
		function createThumbnail_NetPBM($src_img, $desc_img, $desc_dimension, $lib_path) {
			if (!file_exists("$lib_path/anytopnm"))
				return false;

			$cmd = "$lib_path/anytopnm $src_img | $lib_path/pnmscale -width=$desc_dimension[0] | $lib_path/pnmtojpeg -quality=80 > $desc_img";
			@exec( $cmd );

			if (file_exists($desc_img))
				return true;
			else
				return false;
		}
	}
}
?>