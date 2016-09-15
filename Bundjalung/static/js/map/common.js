/* Browser sensing */
var isNew = 0;
var isNS4 = 0;
var isIE4 = 0;
var brow = ((navigator.appName) + (parseInt(navigator.appVersion)));
if (parseInt(navigator.appVersion) >= 5) {
isNew = 1}
else if (brow == "Netscape4") {
isNS4 = 1;}
else if (brow == "Microsoft Internet Explorer4") {
isIE4 = 1;}
/* cross-browser DOM */
if (isNS4) {
docObj = 'document.layers' + '[';
styleObj = ']'; }
else if (isIE4) {
docObj = 'document.all' + '[';
styleObj = ']' + '.style';
closeVar = ']';  }
else if (isNew) {
docObj = 'document.getElementById' + '(';
styleObj = ')' + '.style';
closeVar = ')';  }
function show() {
clearTimeout(Fuse);
for (var i=0; i<(show.arguments.length); i++) {
dom = eval(docObj + 'show.arguments[i]' + styleObj);
dom.display = 'inline';
}
}
function hide() {
for (var i=0; i<(hide.arguments.length); i++) {
dom = eval(docObj + 'hide.arguments[i]' + styleObj);
dom.display = 'none';
}
}
var Fuse;
function off(x) {
var str = "hide('"+x+"')";
Fuse = setTimeout(str,400);
}
function offAll() {
hide('');
rollOff('');
}
function chgColor(divID,theClass) {
	dom = eval(docObj + 'divID' + closeVar);
	dom.className = theClass;
}
function goTo(newLoc) {
window.location = newLoc;
}
function popup (url, width, height, windowname) {
	if (!width) var width = 580;
	if (!height) var height = 420;
	if (!windowname) var windowname = 'popup_'+ new Date().getTime();
	if (url.indexOf('?') != -1) url += '&layout=popup';	else url += '?layout=popup';
	var left = screen.width/2 - width/2;
	var top = screen.height/2 - height/2;
	window.open(url, windowname, 'width='+width+',height='+height+',toolbar=0,resizable=1,scrollbars=1,left='+left+',top='+top);
	return false;
}