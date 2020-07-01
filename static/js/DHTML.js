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
function stopText(){
hp=document.getElementById("popupword");
         hp.innerHTML="";
        hp.style.display="none";
        hp.style.width="0%";
}
function stopText(component){
hp = document.getElementById(component);
         hp.innerHTML="";
        hp.style.display="none";
        hp.style.width="0%";
}
function DHTMLText(text){
 
 hp=document.getElementById("popupword");
     if(hp){
     	hp.style.display="block";
	hp.style.width="15%";
     }
  if (navigator.appName == "Microsoft Internet Explorer")

        hp.innerHTML=text+' <a onclick="<div style="float:right;"><a onclick=stopText("popupword") >Close</a><\div>';
  else if (navigator.appName != "Netscape")

        hp.innerHTML=text+' <div style="float:right;"><a onclick=stopText("popupword")  >Close</a><\div>';
  else

        hp.innerHTML=text+' <div style="float:right;"><a onclick=stopText("popupword")   >Close</a><\div> ';



}

function  DHTMLSoundnoTextFull(surl){

	DHTMLSound(surl,"");


}
function DHTMLSound(surl,text) {

   hp=document.getElementById("popupword");
     if(hp) {
	    hp.style.display="none";
		hp.style.width="35%";
	}
  if (navigator.appName == "Microsoft Internet Explorer")

    	hp.innerHTML=text+' '+surl+'<BGSOUND SRC="' + surl+ '"  type="audio/mpeg"> <div style="float:right;"><a onclick=stopText("popupword")  >Close</a><\div>';
  else if (navigator.appName != "Netscape")

	hp.innerHTML=text+' '+'<audio controls="None" autoplay> <source src="' + surl+ '"     type="audio/mpeg"></audio> <div style="float:right;"><a onclick=stopText("popupword")  >Close</a><\div>';
  else

	hp.innerHTML=text+' '+'<audio controls="None" autoplay> <source height="30px" src="' + surl+ '"    type="audio/mpeg"></audio><div style="float:right;"><a onclick=stopText("popupword")  >Close</a><\div> ';

}

function DHTMLFrontSound(surl,text) {
	console.log("Front page Sound file");
   hp=document.getElementById("popupword");
     if(hp) {
            hp.style.display="block";
	 hp.style.background="grey";
                hp.style.width="100%";
        }
   surl="/Dharug/sounds/"+surl;
  if (navigator.appName == "Microsoft Internet Explorer")

        hp.innerHTML=text+' '+surl+'<BGSOUND SRC="' + surl+ '"  type="audio/mpeg"> <div style="float:right;"><a onclick=stopText("popupword")  ></a><\div>';
  else if (navigator.appName != "Netscape")

        hp.innerHTML=text+' '+'<audio controls autoplay> <source src="' + surl+ '"     type="audio/mpeg"></audio> <div style="float:right;"><a onclick=stopText("popupword")  ></a><\div>';
  else

        hp.innerHTML=text+' '+'<audio controls autoplay> <source height="30px" src="' + surl+ '"    type="audio/mpeg"></audio><div style="float:right;"><a onclick=stopText("popupword")  ></a><\div> ';

}
function DHTMLVideo(vurl){
 hp=document.getElementById("popupword");

 hp.innerHTML='<object height="344"><param name="movie" value="'+vurl+'"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="'+vurl+'" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" height="344"></embed></object>';
  
 hp.style.display="block";
}
