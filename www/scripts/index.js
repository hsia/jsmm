/**
 * Created by S on 2017/2/16.
 */
$(function () {
    $('#organization-tree').tree({
        onSelect: function(node) {
            console.log('Selected: ', node);
        }
    });

    var gridHeight = ($('#members').height());
    var $memberList = $('#member-list');

    //保存社员数据
    $("#member-form").submit(function (event) {
        event.preventDefault();
        var formData = $(this).serializeArray();
        var memberInfo = {};
        $.each(formData, function (index, element) {
            memberInfo[element.name] = element.value;
        });
        $.post('/members/', JSON.stringify(memberInfo), function (data) {
            if (data.success == "true") {
                $('#member-dialog').dialog('close');
                $('#member-form').form('clear');
                $memberList.datagrid('reload');
                $.messager.alert('提示信息', '添加社员成功！', 'info');
            }
        })
    });

    $("#memberEdit-form").submit(function (event) {
        event.preventDefault();

        var currentPage = $memberList.datagrid('options').pageNumber;
        var formData = $(this).serializeArray();
        var memberInfo = {};
        $.each(formData, function (index, element) {
            memberInfo[element.name] = element.value;
        });
        console.log(memberInfo);
        $.ajax({
            url: '/members/' + memberInfo._id,
            type: 'PUT',
            data: JSON.stringify(memberInfo),
            success: function (data) {
                $('#memberEdit-dialog').dialog('close');
                //删除成功以后，重新加载数据，并将choiceRows置为空。
                $memberList.datagrid('gotoPage',currentPage).datagrid('reload');
                $.messager.alert('提示', '数据更新成功!', 'info');
            },
            error: function (data) {
                $.messager.alert('提示', '数据更新失败!', 'error');
            }
        });
    });

    var toolbar = [{
        text: '添加',
        iconCls: 'icon-add',
        handler: function () {
            $('#member-dialog').dialog({
                width: 800,
                height: 630,
                title: '添加社员',
                closed: false,
                cache: false,
                modal: true,
                buttons: [{
                    iconCls: 'icon-save',
                    text: '保存',
                    handler: function () {
                        $('#member-form').trigger('submit');
                    }
                }, {
                    iconCls: 'icon-cancel',
                    text: '取消',
                    handler: function () {
                        $('#member-form').form('clear');
                        $('#member-dialog').dialog('close');
                    }
                }]
            });
        }
    }, '-', {
        text: '编辑',
        iconCls: 'icon-edit',
        handler: function () {
            //后台查询需要编辑的数据的详细信息，并将返回的数据放入到memeberEdit-form中
            editInfo();
        }
    }, '-', {
        text: '删除',
        iconCls: 'icon-cancel',
        handler: function () {
            confirmRemove();
        }
    }];

    $memberList.datagrid({
        iconCls: 'icon-ok',
        height: gridHeight,
        rownumbers: true,
        pageSize: 10,
        nowrap: true,
        striped: true,
        fitColumns: true,
        loadMsg: '数据装载中......',
        pagination: true,
        allowSorts: true,
        remoteSort: true,
        multiSort: true,
        singleSelect: true,
        toolbar: toolbar,
        columns: [[
            {field: '_id', hidden: true},
            {field: '_rev', hidden: true},
            {field: 'name', title: '姓名', width: 110, align: 'left'},
            {field: 'gender', title: '性别', width: 50, align: 'left'},
            {field: 'birthday', title: '出生日期', width: 120, align: 'left'},
            {field: 'nation', title: '民族', width: 120, align: 'left'},
            {field: 'idCard', title: '身份证号', width: 120, align: 'left'},
            {field: 'branch', title: '所属支社', width: 120, align: 'left'},
            {field: 'organ', title: '所属基层组织', width: 120, align: 'left'},
            {field: 'branchTime', title: '入社时间', width: 120, align: 'left'}
        ]],
        loader: function (param, success) {
            var defaultUrl = '/members';
            $.get(defaultUrl, function (data) {
                success(data)
            });
        },
        loadFilter: function (data) {
            if (typeof data.length == 'number' && typeof data.splice == 'function') {
                data = {
                    total: data.length,
                    rows: data
                }
            }
            var opts = $memberList.datagrid('options');
            var pager = $memberList.datagrid('getPager');
            pager.pagination({
                onSelectPage: function (pageNum, pageSize) {
                    opts.pageNumber = pageNum;
                    opts.pageSize = pageSize;
                    pager.pagination('refresh', {
                        pageNumber: pageNum,
                        pageSize: pageSize
                    });
                    $memberList.datagrid('loadData', data);
                }
            });
            if (!data.originalRows) {
                data.originalRows = (data.rows);
            }
            var start = (opts.pageNumber - 1) * parseInt(opts.pageSize);
            var end = start + parseInt(opts.pageSize);
            data.rows = (data.originalRows.slice(start, end));
            return data;
        },
        onSelect: function (rowIndex, rowData) {
            memberInfo(rowData);
            var event = new CustomEvent("grid-row-selection",{
                detail: rowData
            });
            window.dispatchEvent(event);
        }
    });

    //社员信息详情
    function memberInfo(rowData) {
        var html = `
<div class="member-detail">
    <div class="member-picture"><img src="/styles/th5RFQH01A.jpg" style="width:100%;"></div>
    <div class="member-column">
        <div class="member-item"><span class="member-item-title">外文姓名: </span>${rowData.foreignName || ""}</div>
        <div class="member-item"><span class="member-item-title">曾用名: </span>${rowData.usedName || ""}</div>
        <div class="member-item"><span class="member-item-title">籍贯: </span>${rowData.nativePlace || ""}</div>
        <div class="member-item"><span class="member-item-title">出生地: </span>${rowData.birthPlace || ""}</div>
        <div class="member-item"><span class="member-item-title">健康状态: </span>${rowData.health || ""}</div>
        <div class="member-item"><span class="member-item-title">婚姻状况: </span>${rowData.marriage || ""}</div>
        <div class="member-item"><span class="member-item-title">有效证件类别: </span>${rowData.idType || ""}</div>
        <div class="member-item"><span class="member-item-title">证件号码: </span>${rowData.idNo || ""}</div>
        <div class="member-item"><span class="member-item-title">移动电话: </span>${rowData.mobile || ""}</div>
    </div>
    <div class="member-column">
        <div class="member-item"><span class="member-item-title">党派交叉: </span>${rowData.partyCross || ""}</div>
        <div class="member-item"><span class="member-item-title">单位名称: </span>${rowData.companyName || ""}</div>
        <div class="member-item"><span class="member-item-title">参加工作时间: </span>${rowData.jobTime || ""}</div>
        <div class="member-item"><span class="member-item-title">工作部门: </span>${rowData.department || ""}</div>
        <div class="member-item"><span class="member-item-title">办理退休手续: </span>${rowData.retire || ""}</div>
        <div class="member-item"><span class="member-item-title">职务: </span>${rowData.duty || ""}</div>
        <div class="member-item"><span class="member-item-title">职称: </span>${rowData.jobTitle || ""}</div>
        <div class="member-item"><span class="member-item-title">学术职务: </span>${rowData.academic || ""}</div>
        <div class="member-item"><span class="member-item-title">电子邮箱: </span>${rowData.email || ""}</div>
    </div>
    <div class="member-column">
        <div class="member-item"><span class="member-item-title">家庭地址: </span>${rowData.homeAddress || ""}</div>
        <div class="member-item"><span class="member-item-title">家庭地址邮编: </span>${rowData.homePost || ""}</div>
        <div class="member-item"><span class="member-item-title">家庭电话: </span>${rowData.homeTel || ""}</div>
        <div class="member-item"><span class="member-item-title">公司地址: </span>${rowData.companyAddress || ""}</div>
        <div class="member-item"><span class="member-item-title">公司邮编: </span>${rowData.companyPost || ""}</div>
        <div class="member-item"><span class="member-item-title">单位电话: </span>${rowData.companyTel || ""}</div>
        <div class="member-item"><span class="member-item-title">通信地址: </span>${rowData.commAddress || ""}</div>
        <div class="member-item"><span class="member-item-title">通信地址邮编: </span>${rowData.commPost || ""}</div>
        <div class="member-item"><span class="member-item-title">爱好: </span>${rowData.hobby || ""}</div>
    </div>
</div>
`;
        $('#member-info').html(html);
    }

    //编辑数据
    function editInfo() {
        //1、先判断是否有选中的数据行
        var $member = $memberList.datagrid('getSelected');
        if ($member == null) {
            $.messager.alert('提示', '请选择需要编辑的数据!', 'error');
            return;
        }
        // 2、 发送异步请求，获得信息数据
        $.getJSON("/members/" + $member._id, function (data, status) {
            if (status) {
                $('#memberEdit-form').form('clear');
                $('#memberEdit-form').form('load', data);
                $('#memberEdit-dialog').dialog({
                    width: 800,
                    height: 630,
                    title: '编辑社员',
                    closed: false,
                    cache: false,
                    modal: true,
                    buttons: [{
                        iconCls: 'icon-ok',
                        text: '保存',
                        handler: function () {
                            $('#memberEdit-form').trigger('submit');
                        }
                    }, {
                        text: '取消',
                        handler: function () {
                            $('#memberEdit-dialog').dialog('close');
                        }
                    }]
                });
            } else {
                $.messager.alert('提示', '数据请求失败!', 'error');
            }
        })
    }

    //确认删除
    function confirmRemove() {
        //1、先判断是否有选中的数据行
        var member = $memberList.datagrid('getSelected');
        if (member == null) {
            $.messager.alert('提示', '请选择需要删除的数据!', 'error');
            return;
        }
        //2、将选中数据的_id放入到一个数组中
        var id = member._id;
        //3、提示删除确认
        $.messager.confirm('删除提示', '确定删除选中的数据?', function (r) {
            if (r) {
                //4、确认后，删除选中的数据
                removeItem(id)
            }
        });
    }

    //删除数据行
    function removeItem(id) {
        $.ajax({
            url: '/members/' + id,
            type: 'DELETE',
            success: function (data) {
                //删除成功以后，重新加载数据，并将choiceRows置为空。
                $memberList.datagrid('reload');

                var eventDelete = new CustomEvent("grid-row-deleteRow", {
                    detail: {success: true}
                });
                window.dispatchEvent(eventDelete);

                memberInfo({});

                $.messager.alert('提示', '数据删除成功!', 'info');
            },
            error: function (data) {
                $.messager.alert('提示', '数据删除失败!', 'error');
            }
        });
    }
});