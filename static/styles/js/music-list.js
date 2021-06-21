let allMusic = [];
function baseName(str)
{
   var base = new String(str).substring(str.lastIndexOf('/') + 1); 
    if(base.lastIndexOf(".") != -1)       
        base = base.substring(0, base.lastIndexOf("."));
   return base;
}

var ms_list=document.getElementsByClassName("music-titles");
for(var i=0;i<ms_list.length;i++){
  var music_info={}
  //console.log(ms_list[i].textContent);
  var filename=ms_list[i].textContent;
  //var BaseName=baseName(filename);

  music_info.name=baseName(filename);
  music_info.artist=""
  music_info.img=""
  music_info.src=baseName(filename);

  allMusic.push(music_info);
}
console.log(allMusic)



