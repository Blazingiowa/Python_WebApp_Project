var upmessage = document.getElementById('upload-message');
$("#btnOF").prop("disabled", true);

$(document).ready(function () {
    "use strict";
    $("#file").on("change", function (e) {
        var files = $(this)[0].files;
        upmessage.innerHTML = "";
        if (files.length >= 2) {
            $(".file_label").text(files.length + " Files Ready To Upload");
        } else {
            var fileName = e.target.value.split("\\").pop();
            $(".file_label").text(fileName);

            //ユーザの全ファイル名を取得し配列に格納
            var myvideo_names = [];
            $('.myvideo-name').find('li').each( function( index, element ) {
                myvideo_names.push(element.textContent );
            })

            //アップロードするファイルの名前が既に存在するか判定
            myvideo_names.some(function(value) {
                if(fileName == value){
                    upmessage.innerHTML = "※そのファイル名は既に存在します";
                    $("#btnOF").prop("disabled", true);
                    return true;
                }
                $("#btnOF").prop("disabled", false);    
            });
            
        }
    });
});

document.querySelectorAll('.button').forEach(button => {

    let div = document.createElement('div'),
        letters = button.textContent.trim().split('');

    function elements(letter, index, array) {

        let element = document.createElement('span'),
            part = (index >= array.length / 2) ? -1 : 1,
            position = (index >= array.length / 2) ? array.length / 2 - index + (array.length / 2 - 1) : index,
            move = position / (array.length / 2),
            rotate = 1 - move;

        element.innerHTML = !letter.trim() ? '&nbsp;' : letter;
        element.style.setProperty('--move', move);
        element.style.setProperty('--rotate', rotate);
        element.style.setProperty('--part', part);

        div.appendChild(element);

    }

    letters.forEach(elements);

    button.innerHTML = div.outerHTML;

    button.addEventListener('mouseenter', e => {
        if (!button.classList.contains('out')) {
            button.classList.add('in');
        }
    });

    button.addEventListener('mouseleave', e => {
        if (button.classList.contains('in')) {
            button.classList.add('out');
            setTimeout(() => button.classList.remove('in', 'out'), 950);
        }
    });

});
/* 
function updateProgress(e) {
    if (e.lengthComputable) {
      var percent = e.loaded / e.total;
      //$("#progressBar").attr("value", percent * 100);
      var percent_bar="bar-"+parseInt(percent*100);
      var progress=document.getElementById("progress-bar");
      progress.className=percent_bar;
    }
  }
  
  $(".alternative").on("click", function() {
    var formData = new FormData(document.getElementById("file-form"));
    formData.append("file", document.getElementById("file").files[0]);
  
    var request = new XMLHttpRequest();
    request.upload.addEventListener("progress", updateProgress, false);
    request.open("POST", "/upload_fttb");
    request.setRequestHeader("content-type", "application/x-www-form-urlencoded;charset=UTF-8");
    request.send(formData);
  });
  */

function _(el) {
    return document.getElementById(el);
}

function uploadFile() {
    var file = _("file").files[0];
    var formdata = new FormData(document.getElementById("file-form"));
    formdata.append("file", file);
    var ajax = new XMLHttpRequest();
    ajax.upload.addEventListener("progress", progressHandler, false);
    ajax.open("POST", "/upload_fttb");
    ajax.send(formdata);
}

function progressHandler(e) {
    var percent = e.loaded / e.total;
    //$("#progressBar").attr("value", percent * 100);
    var percent_text = document.getElementById("progress-text");
    var percent_bar = "bar-" + parseInt(percent * 100);
    percent_text.innerHTML = '<p>' + parseInt(percent * 100) + '%</p>';
    var progress = document.getElementById("progress-bar");
    progress.className = percent_bar;
    if (parseInt(percent * 100) >= 100) {
        percent_text.innerHTML = '<p>Complete!</p>';
        $(function () {
            $(".loader").animate({
                opacity: "0"
            }, 1000);
        });
    }
}

$(function () {
    $(".alternative").click(function () {
        uploadFile();
        Progress_Loader();
    });
});

function Progress_Loader() {
    $(function () {
        $(".loader").animate({
            opacity: "1"
        }, 1000);
    });
}