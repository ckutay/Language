/**
 *  Blame glen for cinerama2
 *  Requires: swfobject 2.2
 */

cinerama_version = "2.08.42";

cinerama_prefix = "http://www.abc.net.au/res/libraries/cinerama2/";


//SWFobject
if (typeof(swfobject) == "undefined") {
	jsInclude("http://www.abc.net.au/res/libraries/swfobject/swfobject-2.2.js");
}

//Cinerama Functions
if (typeof(cinerama) == "undefined") {
	jsInclude(cinerama_prefix + "scripts/cinerama2_functions.js?version=" + cinerama_version);
}

function jsInclude(jsFile){
	document.write('<script type="text/javascript" src="'+ jsFile + '"></scr' + 'ipt>');
}

function cssInclude(cssFile){
	document.write("<link rel='stylesheet' type='text/css' href='"+cssFile+"'/>" );
}




