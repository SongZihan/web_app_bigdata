;
$(document).ready( function(){
   $(".log-out").click(function(){
       var logOut = true;
       $.ajax({
           url:"/user/dashboard",
           type:"POST",
           data:{
               log_out:logOut
           },
           dataType:"json",
           success:function( res ){
               alert(res.msg);
               if(res.code == 200){
                   window.location.href="/";
               };
           }

       });

   });


}
);