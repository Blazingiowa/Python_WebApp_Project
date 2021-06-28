var message = document.getElementById('DL-message');
var filetxt;

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

function downloadFile() {
    document.getElementById('taihi_file').value = filetxt;

    $(function(){
        $("#taihi_form").submit()
    })
}

$(function () {   
    $(".alternative").click(function () {

        var input_names = document.querySelectorAll("input[name=names]:checked");
        
        if(0 >= input_names.length){
            message.innerHTML = "※ダウンロードするものを選択してください";
        }
        else{
            downloadFile();
        }
    });
});
$("[name='names']").on("click",function(){
    if($(this).prop('checked')){
        $("[name='names']").prop('checked',false);
        $(this).prop('checked',true);
        //チェックを付けた動画の名前を格納
        filetxt = $(this).parent().prev().prev().text();
        message.innerHTML = "";
    }
});