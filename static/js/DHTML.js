function setupText(hoverItem){
        hp = document.getElementById("popupword");
        hp.style.display="none";
 	hp = document.getElementById("popupsearch");
	if (hp)        hp.style.display="none";
  	hp = document.getElementById("popuplist");
   	if(hp)     hp.style.display="none";
}
function writeWord(){
hp = document.getElementById("popupword");
      hp.style.display="visible";
        hp.style.display="block";
        hp.style.float="left";
}
function writeList(){
  hp = document.getElementById("popuplist");
  hp.style.display="block";

}
function writeSearch(){
  hp = document.getElementById("popupsearch");
  hp.style.display="block";
  hp.style.float="left";

}

function stopText(el){
hp = document.getElementById(el);
hp.style.display="none";
}
function DHTMLText(text){
 
 hp=document.getElementById("popupword");
     if(hp){
     	hp.style.display="block";
	hp.style.width="15%";
     }
  if (navigator.appName == "Microsoft Internet Explorer")

        hp.innerHTML=text+' <a onclick="stopText()" href="#"> <div style="float:right;"><a onclick=stopText("popupword") href="#"  >Close</a><\div>';
  else if (navigator.appName != "Netscape")

        hp.innerHTML=text+' <div style="float:right;"><a onclick=stopText("popupword") href="#"  >Close</a><\div>';
  else

        hp.innerHTML=text+' <div style="float:right;"><a onclick=stopText("popupword") href="#"  >Close</a><\div> ';



}
function DHTMLSound(surl,text) {

   hp=document.getElementById("popupword");
     if(hp) {
	    hp.style.display="block";
		hp.style.width="35%";
	}
  if (navigator.appName == "Microsoft Internet Explorer")

    	hp.innerHTML=text+' '+surl+'<BGSOUND SRC="' + surl+ '"  type="audio/mpeg"> <a onclick="stopText()" href="#"> <div style="float:right;"><a onclick=stopText("popupword") href="#"  >Close</a><\div>';
  else if (navigator.appName != "Netscape")

	hp.innerHTML=text+' '+'<audio controls autoplay> <source src="' + surl+ '"     type="audio/mpeg"></audio> <div style="float:right;"><a onclick=stopText("popupword") href="#"  >Close</a><\div>';
  else

	hp.innerHTML=text+' '+'<audio controls autoplay> <source height="30px" src="' + surl+ '"    type="audio/mpeg"></audio><div style="float:right;"><a onclick=stopText("popupword") href="#"  >Close</a><\div> ';

}

function DHTMLVideo(vurl){
 hp=document.getElementById("popupword");

 hp.innerHTML='<object height="344"><param name="movie" value="'+vurl+'"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="'+vurl+'" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" height="344"></embed></object>';
  
 hp.style.display="block";
}
