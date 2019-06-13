//轮播图

$(function () {
    //保存图片路径
    var baseUrl = "../images/index/";
    var arr = ["index_banner2.jpg", "index_banner1.jpg", "index_banner3.jpg", "index_banner4.jpg", "index_banner5.jpg"];
    var index = 0;
    var timer = setInterval(autoPlay, 1000);

    //循环轮播
    function autoPlay() {
        $("#banner li").eq(index).css("background", "white");
        index++;
        if (index == arr.length) {
            index = 0
        }
        var url = baseUrl + arr[index];
        $("#banner img").attr("src", url);
        //索引修改
        $("#banner li").eq(index).css("background", "red");
    }

    //鼠标移入移出
    $("#banner").mouseover(function () {
        clearInterval(timer)
    }).mouseout(function () {
        //重启定时器
        timer = setInterval(autoPlay, 1000)
    });
    //前后翻图片
    $("#banner a.left").click(function () {
        $("#banner li").eq(index).css("background", "white")
        index--;
        if (index < 0) {
            index = arr.length - 1
        }
        var url = baseUrl + arr[index];
        $("#banner img").attr("src", url);
        $("#banner li").eq(index).css("background", "red");
    });
    $("#banner a.right").click(function () {
        autoPlay()
    })
    //遍历li,添加属性ind
    var i=0;
    for (i;i<arr.length;i++){
        $("#banner li").eq(i).ind = i;
    }
    $("#banner li").click(function () {
        console.log($(this).ind)
    })

});
