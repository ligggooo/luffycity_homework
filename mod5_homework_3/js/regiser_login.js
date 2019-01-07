// 登陆框绑定
var login_status={
    name:'',status:false,
    login_in:function (name) {
        this.name=name;
        this.status=true;
    },
    log_out:function () {
        this.name='';
        this.status=false;
    }
};

function login_bind() {
    $('a.login').click(function () {
        $('div.login_mask').css('display', 'block');
        return false;
    });

    $('.login_form button.close').click(function () {
        $('div.login_mask').css('display', 'none');
        return false;
    });

    $('.login_form').submit(function () {
        let name = $(this).children('input[name=username]').val();
        let pswd = $(this).children('input[name=password]').val();
        console.log(name+pswd);
        $('div.login_mask').css('display', 'none');
        let msg={username:name,password:pswd};
        send_data(msg);
        // 一顿操作登上了 修改topbar
        $('.topBar a.login').text(`${name} 在线`);
        $('.topBar a.register').parent('li').css('display','none');
        $('.topBar a.logout').parent('li').css('display','block');
        login_status.login_in(name);
        return false;
    });

    $('.topBar a.logout').click(function () {
        $('.topBar a.login').text(`登陆`);
        login_status.log_out();
        $('.topBar a.register').parent('li').css('display','block');
        $('.topBar a.logout').parent('li').css('display','none');
        return false;
    })

}
// 注册框绑定
function register_bind() {
    $('a.register').click(function () {
        $('div.register_mask').css('display', 'block');
        return false;
    });

    $('.register_form button.close').click(function () {
        $('div.register_mask').css('display', 'none');
        return false;
    });

    $('.register_form').submit(function () {
        let name = $(this).children('input[name=username]').val();
        let pswd_1 = $(this).children('input[name=passwd_1]').val();
        let pswd_2 = $(this).children('input[name=passwd_2]').val();
        console.log(name+pswd_1+pswd_2);
        if(pswd_1!==pswd_2){
            alert('两次密码不一致');
            return false;
        }
        $('div.register_mask').css('display', 'none');
        let msg={username:name,password:pswd_1};
        send_data(msg);
        // 一顿操作成功注册了账户
        alert(`成功注册账户"${name}"`);
        return false;
    });
}