/**
 * Created by wt03201 on 2017-03-31.
 */
$(function () {
    $('#loginSubmit').click(function () {
        var formData = $("#loginForm").serializeArray();
        var userinfo = {};
        $.each(formData, function (index, element) {
            userinfo[element.name] = element.value;
        });

        $.post('/login', JSON.stringify(userinfo), function (data) {
            if (data.success) {
                window.location.href = '/';
            } else {
                $.messager.alert('提示信息', '用户名或者密码错误！', 'error');
            }
        })
    })
})


