;
$(document).ready( function(){
    $(".rg-env").click(function(){
        var btn_target = $(this);
//        不要让用户重复点击导致重复提交
        if(btn_target.hasClass("disabled")){
            layer.alert(" processing~ Don't repeat click~~~~");
            return ;
        };

        var user_name = $("input[id=inputUserName]").val();
        var pwd = $("input[id=inputPassword3]").val();
        var repeat_pwd = $("input[id=inputPassword4]").val();
        if(user_name == undefined || user_name.length < 1){
            layer.alert("Please input user name!");
            return ;
        };
        if(pwd == undefined || pwd.length < 6 ){
            layer.alert("Please enter your password and Password length must be greater than six~");
            return ;
        };
        if(pwd != repeat_pwd){
            layer.alert("Inconsistent passwords");
        };

        btn_target.addClass("disabled");

        $.ajax({
            url:"/registered",
            type:"POST",
            data:{
                username:user_name,
                password:pwd,
                repeat_pwd:repeat_pwd
            },
            dataType:"json",
            success:function( res ){
                btn_target.removeClass("disabled");
                alert(res.msg);
                if(res.code == 200){
                    window.location.href="/";
                };
            }

        })

    });
});