
function add() {
    // 添加项目
    let top_input=document.getElementById('top_input');//取得顶部输入框输入
    let task = top_input.value;//取得输入值
    top_input.value=''; //清空输入框

    let time = new Date(); // 添加时间戳
    let content=[time.toLocaleDateString()+' '+time.toLocaleTimeString(),task];
    let new_todo = new_todo_element(content);

    data.todo.push([time,content]);  //存入全局变量

    set_list(new_todo); //插入式更新列表
    save_data(data); //保存数据
}

function new_todo_element(content) {  // 这个函数需要增强
    // 创建列表元素
    let new_e = document.createElement('li');
    let time_string =content[0];
    let task =content[1];
    new_e.innerHTML = time_string+'<textarea class=\"task\" spellcheck=\"false\">'+task+'</textarea> <button class=\"remove\">×</button> <button class=\"done\">√</button><button class="set">SET</button>';
    // 2019/1/3 下午1:03:05 <span class="task">2323</span> <button class="remove">×</button> <button class="done">√</button>
    return new_e;
}


function load_data(){
    // 载入数据
    let data_tmp = JSON.parse(localStorage.getItem('todolist'));
    if (!data_tmp){return reset_data();}//若不存在，创建一个
    else {return data_tmp;} //若存在，载入

}

function save_data(data) {
    //保存数据
    localStorage.setItem('todolist', JSON.stringify(data));
    // alert(data.todo+data.done);
}

function reset_data() {
    //初始化全局变量
    return {'todo':[],'done':[]};
}

function clear_data() {
    // 清除变量 与清除按钮绑定
    if (confirm('Clear All DATA ?')){
    localStorage.removeItem('todolist');
    data= reset_data();
    set_list();
    alert('All data cleared.')}
}

function set_list(new_todo) {
// initialize the list
    let detail_list=document.getElementById('detail_list');

    if (!new_todo){ // 不传参时，说明需要重载ul
        detail_list.innerHTML=''; //先删除所有的子节点
        for(i=0;i<data.todo.length;i++){
            let content = data.todo[i][1];
            let new_todo = new_todo_element(content);
            detail_list.append(new_todo);
            new_todo.index = i;
            bind_click(new_todo,'todo');
        }
    }
    else { // 传参数时，插入式更新
        detail_list.append(new_todo);
        new_todo.index = detail_list.children.length-1;
        bind_click(new_todo,'todo');
    }

        // 更新已完成列表
    let done_list=document.getElementById('finished_list');
    done_list.innerHTML='';
    for(i=0;i<data.done.length;i++){
        let content = data.done[i][1];
        let new_done = new_todo_element(content);
        done_list.append(new_done);
        new_done.index = i;
        bind_click(new_done,'done');
    }
}

function bind_onload() {
    // 绑定 top栏事件
    set_list(); //初始化完成和未完成列表

    let top_form=document.getElementById('top_input').parentElement;
    top_form.action="javascript:add();";
    let clear_all = document.getElementById('clear_all');
    clear_all.onclick=clear_data;
}

function bind_click(new_node,flag) {
    // 绑定 列表元素按钮事件
    let remove = new_node.getElementsByClassName('remove')[0];
    let done = new_node.getElementsByClassName('done')[0];
    let set = new_node.getElementsByClassName('set')[0];
    if (flag==='todo'){
        remove.onclick = remove_todo;
        done.onclick = done_todo;
        set.onclick = set_todo;
        }
    else if(flag==='done'){
        remove.onclick = remove_done;
        set.onclick = set_done;
    }
}

function remove_todo() {
    // 点击未完成的叉叉事件处理
    let parent = this.parentElement.parentElement;
    let child = this.parentElement;
    let index = this.parentElement.index;
    parent.removeChild(child);
    data.todo.splice(index,1);
    set_list();
    save_data(data);
}
function remove_done() {
    //点击已完成的叉叉事件处理
    let parent = this.parentElement.parentElement;
    let child = this.parentElement;
    let index = this.parentElement.index;
    parent.removeChild(child);
    data.done.splice(index,1);
    set_list();
    save_data(data);
}
function done_todo() {
    //点击事件完成小绿勾
    let parent = this.parentElement.parentElement;
    let child = this.parentElement;
    let index = this.parentElement.index;
    parent.removeChild(child);
    let data_done = data.todo[index];
    data.todo.splice(index,1);
    data.done.push(data_done);
    set_list();
    save_data(data);
}

function set_todo() {
    //点击编辑完成set按钮
    let li = this.parentElement;
    let index = this.parentElement.index;
    let task =li.getElementsByClassName('task')[0].value;
    data.todo[index][1][1]=task;
    save_data(data);
}
function set_done() {
    //点击编辑完成set按钮
    let li = this.parentElement;
    let index = this.parentElement.index;
    let task =li.getElementsByClassName('task')[0].value;
    data.done[index][1][1]=task;
    save_data(data);
}


var data= load_data();//重开页面，需要初始化  //全局变量
window.onload=bind_onload;//绑定事件