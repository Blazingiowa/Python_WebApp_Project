var video_elem = document.getElementById("my_video_1");

video_elem.addEventListener('timeupdate', function () {
  console.log(video_elem.currentTime);
});

const animateButton = e => {
  e.preventDefault;
  e.target.classList.remove('animate'); //reset animation

  e.target.classList.add('animate');
  setTimeout(() => e.target.classList.remove('animate'), 400);
};

const bubblyButtons = document.getElementsByClassName('bubbly-button');

for (let i = 0; i < bubblyButtons.length; i++) {
  bubblyButtons[i].addEventListener('click', animateButton, false);
}

//Ajaxでいいね押された時の処理
$(function () {
  $(".goodbutton").click(function () {
    //いいねの数取得
    var SpanText=$("#counter").text();
    var NumberOfLikes=parseInt(SpanText)
    //いいねの数を+1
    NumberOfLikes+=1

    //HTMLに反映
    $("#counter").text(NumberOfLikes);
    ConnectMySQLThrowNumberOfLikes(NumberOfLikes);
  });
});

function ConnectMySQLThrowNumberOfLikes(Likes){
  /*var data={"likes_number":Likes}
  xhr=new XMLHttpRequest();
  xhr.open("POST","/likes")
  xhr.send(data);*/

  $.ajax({
    url:'/likes',
    type:'POST',
    data:{
      number_of_likes:Likes
    }
  })
}