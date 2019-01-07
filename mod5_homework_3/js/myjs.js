var section_chosen_index;
var sort_chosen_index;
var username='';


function page_init() {
    //    默认选中“最热栏目” 和 “即时排序”
    section_chosen_index=0;
    sort_chosen_index=2;
    $(".content .content_nav_ul li").eq(section_chosen_index).addClass('content_nav_li_chosen');
    $(".content .content_detail>div").eq(section_chosen_index).addClass('content_detail_div_chosen');
    $('.content .content_nav_controllers button.sort').eq(sort_chosen_index).addClass('button_sort_chosen');

    // 载入测试用评论
    load_testdata();

    //绑定各种事件
    $(".content .content_nav_ul li").click(section_chosen);

    $('.content .content_nav_controllers button[id!=user_submit]').click(sort_chosen);

    $('.fixedHelper a').click(function () {
        // console.log(111);
        $('html , body').animate({scrollTop: 0},'fast');
        return false;
    });


    // 登陆框绑定
    $('a.login').click(function () {
        $('div.login_mask').css('display','block');
        return false;
    });

    $('.login_form button.close').click(function () {
        $('div.login_mask').css('display','none');
        return false;
    });
    // 发表框绑定
    $('.content .content_nav_controllers button[id=user_submit]').click(article_submit_form_open);
    $('.article_submit_form button.close').click(article_submit_form_close);
    $('.article_submit_form input[type=submit]').click(article_submit);



    // 注册框绑定
    $('a.register').click(function () {
        $('div.register_mask').css('display','block');
        return false;
    });

    $('.register_form button.close').click(function () {
        $('div.register_mask').css('display','none');
        return false;
    });


}

function section_chosen(event){
    let i = $(this).index();
    $(".content .content_nav_ul li").eq(section_chosen_index).removeClass('content_nav_li_chosen');
    $(".content .content_detail>div").eq(section_chosen_index).removeClass('content_detail_div_chosen');
    section_chosen_index=i;
    $(".content .content_nav_ul li").eq(section_chosen_index).addClass('content_nav_li_chosen');
    $(".content .content_detail>div").eq(section_chosen_index).addClass('content_detail_div_chosen');
    return false;
}

function sort_chosen(event){
    let i = $(this).index();
    console.log(i);
    $('.content .content_nav_controllers button.sort').eq(sort_chosen_index).removeClass('button_sort_chosen');
    sort_chosen_index=i-1;
    $('.content .content_nav_controllers button.sort').eq(sort_chosen_index).addClass('button_sort_chosen');
    return false;
}

function article_submit_form_open() {
    $('div.article_submit_mask').css('display','block');
    return false;
}
function article_submit_form_close() {
    $('div.article_submit_mask').css('display','none');
    return false;
}
function article_submit() {
    let topic_input = $('.article_submit_form input#topic');
    let data = topic_input.val();
    if(!data){
        return false;
    }
    else{
        topic_input.val('');
        console.log(data);
        //接下来发送数据到服务器
        let msg = {
            username:username,
            topic:data
        };
        send_data(msg);
        //显示新帖子
        // add_new_topic(username,data);
        let time = new Date();
        add_new_topic('小王','年终奖什么时候发啊？？',time); //测试
        // 关闭发文窗口
        article_submit_form_close();
        return false;
    }
}

function add_new_topic(username,data,time) { // todo
    let new_node =$(`<div class="t">
            <p class="topic"> ${data} + ${username} + ${time}</p>
            <form action="" class="comment"> 
            <ul></ul> 
            <input type="text" name="" placeholder="整两句">
            <input type="submit" value="提交">
            </form>
       </div>`);
    new_node.prependTo($('.content_detail .section_1'));

    // 绑主题展开方法
    new_node.find('p').click(function () {
        // alert('sss');
        $(this).siblings('form').stop().slideToggle(100);
        event.stopPropagation();
    });
    //帮评论方法
    new_node.find('input[type=submit]').click(function () {
        let comment=$(this).siblings('input[type=text]').val();
        let t=new Date();
        $(this).siblings('input[type=text]').val('');
        if(comment){
            $(this).siblings('ul').append(`<li>${comment}<span>${t}</span></li>`);
        }else{
            alert('提交之前整两句先');
        }
        return false;
    });

}

function add_new_topic_from_obj(node_data){ // 完善中
    console.log(node_data);
    let data = node_data.topic;
    let username= node_data.user;
    let time= node_data.time;
    let comments = node_data.comments;
    let likes = node_data.likes;
    let dislikes = node_data.dislikes;

    let new_node =$(`<div class="t">
            <p class="topic"> ${data} + ${username} + <span class="time">${time}</span></p>
            <form action="" class="comment"> 
            <ul></ul> 
            <input type="text" name="" placeholder="整两句">
            <input type="submit" value="提交">
            </form>
       </div>`);
    new_node.prependTo($('.content_detail .section_1'));

    for(let i=0;i<comments.length;i++){
        let comment=comments[i];
        let t=new Date();
        if(comment){
            new_node.find('ul').append(`<li>${comment}<span class="time">${t}</span></li>`);
        }
    }

    // 绑主题展开方法
    new_node.find('p').click(function () {
        // alert('sss');
        $(this).siblings('form').stop().slideToggle(100);
        event.stopPropagation();
    });
    //帮评论方法
    new_node.find('input[type=submit]').click(function () {
        let comment=$(this).siblings('input[type=text]').val();
        let t=new Date();
        $(this).siblings('input[type=text]').val('');
        if(comment){
            $(this).siblings('ul').append(`<li>${comment}<span class="time">${t}</span></li>`);
        }else{
            alert('提交之前整两句先');
        }
        return false;
    });
}

function load_testdata() {
    alert('载入测试用数据');
    $.getJSON('./data/data.json','',function (data) {
        console.log(data);
        for(let i=0;i<data.length;i++){
            add_new_topic_from_obj(data[i]);
        }
    });
}
function save_data_for_test() {
    let data=[{topic:'我们村里杀年猪！！！',comments:['沙发','板凳','楼主傻逼','66666'],user:'zuckberg',time:new Date(),likes:35,dislikes:12},
        {topic:'你们的年终奖发了多少啊？',comments:['发了个p','好几亿','厉害了','......'],user:'jellybitch',time:new Date(),likes:135,dislikes:12}];
    let data_json = JSON.stringify(data);
    let html=`<p>${data_json}</p>`;
    let newwindow = window.open('', "_blank",'');
    newwindow.document.write(html);
    newwindow.alert('保存为data.json');
}

function send_data(msg) {
    $.ajax({
        url: '/index/data_api',
        type: 'post',
        data: msg,
        success: function (data) {
            console.log(data);
        },
        error: function (error) {
            console.log(error)
        }
    })
}

