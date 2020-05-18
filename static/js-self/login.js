;
$(document).ready( function(){
    $(".sign-env").click(function(){
        var btn_target = $(this);
//        不要让用户重复点击导致重复提交
        if(btn_target.hasClass("disabled")){
            layer.alert(" processing~ Don't repeat click~~~~");
            return ;
        };

        var user_name = $("input[id=username]").val();
        var pwd = $("input[id=pwd]").val();
//        验证密码和账号符合基本要求
        if(user_name == undefined || user_name.length < 1){
            layer.alert("Please input user name!");
            return ;
        };
        if(pwd == undefined || pwd.length < 6 ){
            layer.alert("Please enter your password and Password length must be greater than six~");
            return ;
        };
        btn_target.addClass("disabled");
//        通过基本检查之后将数据发送至服务器验证
        $.ajax({
            url:"/",
            type:"POST",
            data:{
                username:user_name,
                password:pwd
            },
            dataType:"json",
            success:function( res ){
                btn_target.removeClass("disabled");
                alert(res.msg);
                if(res.code == 200){
                    window.location.href="/user/dashboard";
                };
            }

        })

    });
});