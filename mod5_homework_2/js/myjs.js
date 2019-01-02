
function add() {
    var sss=document.getElementById('top_input');
    var content = sss.value;
    sss.value='';

    var detail_list=document.getElementById('detail_list');
    var new_todo = new_todo_element(content);
    if(detail_list.children.length==0){
        detail_list.append(new_todo);
    } else{
        detail_list.insertBefore(new_todo,detail_list.children[0]);
    }
}

function new_todo_element(content) {
    var new_e = document.createElement('li');
    var time = new Date();
    new_e.innerText=time+' '+content;
    return new_e
}
function bind_onload() {
    var top_input=document.getElementById('top_input');
    top_input.onkeyup=add;
}
function add2() {
    alert(2222)
}

alert('??');
window.onload=bind_onload;