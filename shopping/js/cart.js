$(function () {
        //全选和取消
        var isChecked = false;
        $(".checkAll").click(function () {
            isChecked = !isChecked;
            if (isChecked) {
                // 切换图片样式}
                $(this).attr("src", "../images/cart/product_true.png");
                $(".checkImg").attr("src", "../images/cart/product_true.png").attr("checked", "true")
            } else {
                $(this).attr("src", "../images/cart/product_normal.png");
                $(".checkImg").attr("src", "../images/cart/product_normal.png").removeAttr("checked")
            }
            total();

        });
        // 反选
        $(".checkImg").click(function () {
            if ($(this).attr("checked")) {
                $(this).attr("src", "../images/cart/product_normal.png").removeAttr("checked");

            } else {
                $(this).attr("checked", "true").attr("src", "../images/cart/product_true.png")
            }
            total();
            // console.log(($(this).attr('checked')));
            if ($("img[checked]").length == $(".checkImg").length) {
                $(".checkAll").attr("src", "../images/cart/product_true.png");
                isChecked = true
            } else {
                $(".checkAll").attr("src", "../images/cart/product_normal.png");
                isChecked = false
            }
            total();

        });
        // 数量加减
        $(".add").click(function () {
            var value = $(this).prev().val();
            $(this).prev().val(++value);
            //价格变化,取单价，算总价，显示
            var pstr = $(this).parents(".item").find(".gprice span").html().substring(1);
            var price = (value * pstr).toFixed(2);
            $(this).parents(".item").find(".gsum b").html("￥" + price);
            total();
        });
        $(".minus").click(function () {
            var value = $(this).next().val();
            value--;
            if (value < 1) {
                value = 1;
            }
            $(this).next().val(value);
            var pstr = $(this).parents(".item").find(".gprice span").html().substring(1);
            var price = (value * pstr).toFixed(2);
            $(this).parents(".item").find(".gsum b").html("￥" + price);
            total();
        });
        // 监听输入框
        $(".gcount input").blur(function () {
            // 输入框的值为数值并且是正整数
            var value = $(this).val();
            var r1 = Number(value);
            var r2 = value > 1;
            var r3 = value.split('.').length === 1;
            if (r1 && r2 && r3) {
            } else {
                $(this).val(1);
                value = 1;
            }
            $(this).next().val(value);
            var pstr = $(this).parents(".item").find(".gprice span").html().substring(1);
            var price = (value * pstr).toFixed(2);
            $(this).parents(".item").find(".gsum b").html("￥" + price);
            total();
        });
        //移除
        $(".item .action").click(function () {
            $(this).parent().remove();
            total();
        });


    }
);

//总数统计
function total() {
    var num = 0;
    var sum = 0;
    // 获取总数和总价
    $("img[checked]").each(function () {
        console.log(this);
        var n = Number($(this).parents(".item").find(".gcount input").val());
        var pstr = $(this).parents(".item").find(".gsum b").html();
        var price = Number(pstr.substring(1));
        num += n;
        sum += price;

    });
    //显示
    $(".total-num").html(num);
    $(".total-price").html(sum + "元");
}