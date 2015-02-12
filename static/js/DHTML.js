function setupText(hoverItem){
        hp = document.getElementById("popupword");
        hp.style.display="none";
 hp = document.getElementById("popupsearch");
if (hp)        hp.style.display="none";
  hp = document.getElementById("popuplist");
   if(hp)     hp.style.display="none";
}
function writeAjax(){
hp = document.getElementById("popupword");
hp.style.display="block";
hp.style.float="left";
}
function writeList(){
  hp = document.getElementById("popuplist");
  hp.style.display="block";
  hp.style.left="70%";

}
function writeSearch(){
  hp = document.getElementById("popupsearch");
  hp.style.display="block";
  hp.style.float="left";

}

function stopText(el){
hp = document.getElementById(el);
hp.innerHTML ="test";
hp.style.display="none";
}
function DHTMLSound(surl,text) {

 hp=document.getElementById("popupword");
 if (navigator.appName == "Microsoft Internet Explorer")

    hp.innerHTML=text+' '+surl+'<BGSOUND SRC="' + surl+ '"  type="audio/mpeg"> <a onclick="stopText()" href="#"> <div style="float:right;"><a onclick=stopText("popupword") href="#"  >Close</a><\div>';
else if (navigator.appName != "Netscape")

hp.innerHTML=text+' '+'<audio controls autoplay> <source src="' + surl+ '"     type="audio/mpeg"></audio> <div style="float:right;"><a onclick=stopText("popupword") href="#"  >Close</a><\div>';
else

hp.innerHTML=text+' '+'<audio controls autoplay> <source height="30px" src="' + surl+ '"    type="audio/mpeg"></audio><div style="float:right;"><a onclick=stopText("popupword") href="#"  >Close</a><\div> ';

///{
//text= text.concat('<audio autoplay="true" ><src="');
//text=text.concat(surlfull);
//text=text.concat('" type="audio/mp3"/ > Audio not supported</audio>');
//hp.innerHTML=text;
//}
hp.style.display="visible";
hp.style.display="block";
}

function DHTMLVideo(vurl){
 hp=document.getElementById("popupword");

 hp.innerHTML='<object height="344"><param name="movie" value="'+vurl+'"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="'+vurl+'" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" height="344"></embed></object>';
  
 hp.style.display="block";
}
