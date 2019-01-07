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
        login_status.login_in(name);
        return false;
    });

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
}