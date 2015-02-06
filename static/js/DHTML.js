function setupText(hoverItem){
        hp = document.getElementById("popupword");
        hp.style.padding="0";
        hp.style.position="relative";
        hp.style.display="none";
        hp.style.background="transparent 0px 0px no-repeat";
                hp.style.margin=0;
          hp.style.width="425px";
          hp.style.top="0px";
          hp.style.left="100px";
          hp.style.fontFamily="arial";
          hp.style.fontSize="12px";
        hp.style.backgroundColor="#B0C4DE";
        hp.style.color="#000";
        hp.style.border="1px solid #000";
        hp.style.padding="5px";
        hp.style.visibility="visible";
        hp.style.zIndex="100";
}

function stopText(){
hp = document.getElementById("popupword");
hp.innerHTML ="test";
hp.style.display="none";
}
function DHTMLSound(surl,text) {

 hp=document.getElementById("popupword");
 if (navigator.appName == "Microsoft Internet Explorer")

    hp.innerHTML=text+' '+surl+'<BGSOUND SRC="' + surl+ '"  type="audio/mpeg"> <a onclick="stopText()" href="#"> <div style="float:right;"><a onclick=stopText()" href="#"  >Close</a><\div>';
else if (navigator.appName != "Netscape")

hp.innerHTML=text+' '+'<audio controls autoplay> <source src="' + surl+ '"     type="audio/mpeg"></audio> <div style="float:right;"><a onclick=stopText()" href="#"  >Close</a><\div>';
else

hp.innerHTML=text+' '+'<audio controls autoplay> <source height="30px" src="' + surl+ '"    type="audio/mpeg"></audio><div style="float:right;"><a onclick=stopText()" href="#"  >Close</a><\div> ';

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

 hp.innerHTML='<object width="425" height="344"><param name="movie" value="'+vurl+'"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="'+vurl+'" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="425" height="344"></embed></object>';
  
 hp.style.display="block";
}

