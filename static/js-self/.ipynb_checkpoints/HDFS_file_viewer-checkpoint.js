;
function make_path(path_list){
    //构建完整路径信息
    var compelte_path = "";
    for (var i in path_list) {
				compelte_path = compelte_path + "/" + path_list[i]
			}
    return compelte_path
};

function set_path(path){
    //展示当前路径
    $("#path").text(path);
};

function refresh_path(res){
    //接收路径信息并展示
    var getdata = res.data["path"];
    $("li").remove(".list_content");
    // 实时更新目录列表
    for (var i in getdata) {
        $("#welcome").prepend(getdata[i])
    }
};


$(document).ready(function() {
	//     欢迎界面
	var path_list = [];
    //显示当前路径
//     for (var i in path_list) {
//         compelte_path = compelte_path + "/" + path_list[i]
//     };
//     $("#welcome").text(compelte_path);
    //需要修改
    
	$("li").remove(".list_content");
			$.ajax({
				url: '/user/hdfs_res',
				type: 'POST',
				data: {
					first_get: true
				},
				dataType: "json",
				success: function(res){
                    refresh_path(res);
                }
			})
	// 	接收ajax动态加载的页面元素
	;
	$("body").on("click", ".list",
		function() {
			var first_path = $(this).text();
			//         构建完整路径信息
			path_list.push(first_path);
            compelte_path = make_path(path_list);
			$.ajax({
				url: '/user/hdfs_res',
				type: 'POST',
				data: {
					path: compelte_path
				},
				dataType: "json",
				success: function(res) {
					refresh_path(res);
                    set_path(compelte_path);
				}
			})
		}
	);
	// 后退按钮的功能
	$("body").on("click", ".go_back",
        function() {
        var this_path = path_list;
        this_path.pop();
        compelte_path = make_path(this_path);
		$.ajax({
			url: '/user/hdfs_res',
			type: 'POST',
			data: {
				path_back: compelte_path
			},
			dataType: "json",
			success: function(res) {
				refresh_path(res);
                set_path(compelte_path);
			}
		})
	});
    // 上传文件
    $('input[type="file"]').change(function(f){
        console.log(f.currentTarget.files[0])
        compelte_path = make_path(path_list);
        var formData = new FormData();
        formData.append('file', f.currentTarget.files[0]);
        formData.append('path', compelte_path);
        $.ajax({
            url: '/user/hdfs_upload_file',
            type: 'POST',
            cache: false,
//             使用ajax同步传输文件
            async: false,
            data: formData,
            processData: false,
            contentType: false
        }).done(function(res) {
            alert(res.msg);
            refresh_path(res);
            
        })
});
    
    
    
    //管理被选中的目录元素
    $("body").on("click", ".list_content",
    function(){
        $("li").removeClass("yellow");
        $(this).addClass("yellow");
        //实时更新a的路径信息
        var this_path = $(".yellow").children(".name").text();
        //合成文件路径
        compelte_path = make_path(path_list);
        true_compelte_path = compelte_path + "/" + this_path;
        k = $(this).attr("class").substr(0,7);
        if(k == "is_file"){
            $(".download").children("a").attr("href","/user/download" + true_compelte_path);
        }else{
            $(".download").children("a").attr("href","#");
        }
//         $(".download").children("a").attr("download",this_path);
        
    });
    //管理删除文件
    $("body").on("click",".delete",function(){
        var this_path = $(".yellow").children(".name").text();
        if (this_path == ""){
            alert("you should select an item to delete")
        }
        else{
            //合成文件路径
            compelte_path = make_path(path_list);
            true_compelte_path = compelte_path + "/" + this_path;
            $.ajax({
			url: '/user/hdfs_manage_file',
			type: 'POST',
			data: {
                // 上一级目录
                previous_path : compelte_path,
				path: true_compelte_path,
                action: "delete"
			},
			dataType: "json",
			success: function(res) {
                if (res.code == -1){
                    alert(res.msg);
                }
                else{
                    alert(res.msg);
                    refresh_path(res);
                }
			}
		})
        }
    });
    
    // 新建文件夹功能
    $("body").on("click",".mkdir",function(){
        var dir_name = prompt("Input your directory name(Englisth):");
        if (dir_name != "" && dir_name != null ){
        // 需要定义取消功能
        compelte_path_p = make_path(path_list);
        compelte_path = compelte_path_p + "/" + dir_name;
        $.ajax({
			url: '/user/hdfs_manage_file',
			type: 'POST',
			data: {
                previous_path:compelte_path_p,
				path: compelte_path,
                action: "mkdir"
			},
			dataType: "json",
			success: function(res) {
				alert(res.msg);
                refresh_path(res);
			}
		});
        }
        // else
    });
    // 管理下载请求
//     $("body").on("click",".download",function(){
//         var this_path = $(".yellow").children(".name").text();
//         if (this_path == ""){
//             alert("you should select an item to delete")
//         }
//         else{
//             compelte_path = make_path(path_list);
//             true_compelte_path = compelte_path + "/" + this_path;
//             $.ajax({
// 			url: '/user/hdfs_manage_file',
// 			type: 'POST',
//             async: false,
// 			data: {
// 				path: true_compelte_path,
//                 action: "download"
// 			},
// 			dataType: "json",
// 			success: function(data, status, xhr) {

//                     console.log("=========");
//                     console.log(data)
                   
//         }
//             })}
//     })

});
