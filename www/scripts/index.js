/**
 * Created by S on 2017/2/16.
 */
$(function () {
    var gridHeight = ($('#persons').height());
    var dg = $('#person-lists');
    //存放选中的数据行
    var choiceRows = {};

    $("#member-form").submit(function (event) {
        event.preventDefault();
        var formData = $(this).serializeArray();
        var memberInfo = {};
        $.each(formData, function (index, element) {
            memberInfo[element.name] = element.value;
        });
        $.post('/members/', JSON.stringify(memberInfo), function(){})
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
                    iconCls: 'icon-ok',
                    text: '保存',
                    handler: function () {
                        $('#member-form').trigger('submit');
                    }
                }, {
                    text: '取消',
                    handler: function () {
                        $('#member-dialog').closed();
                    }
                }]
            });
        }
    }, '-', {
        text: '删除',
        iconCls: 'icon-cancel',
        handler: function () {
            removeItem();
        }
    }, '-', {
        text: 'Save',
        iconCls: 'icon-save',
        handler: function () {
            alert('save')
        }
    }];

    dg.datagrid({
        iconCls: 'icon-ok',
        height: gridHeight,
        rownumbers: true,
        pageSize: 10,
        nowrap: true,
        striped: true,
        loadMsg: '数据装载中......',
        pagination: true,
        //idField: 'id',
        allowSorts: true,
        remoteSort: true,
        multiSort: true,
        //fitColumn: true,
        toolbar: toolbar,
        columns: [[
            {field: 'ck', checkbox: true},
            {field: '_id', hidden: true},
            {field: '_rev', hidden: true},
            {field: 'name', title: '姓名', width: 110, align: 'left'},
            {field: 'gender', title: '性别', width: 50, align: 'left'},
            {field: 'birthday', title: '出生日期', width: 120, align: 'left'}
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
            var opts = dg.datagrid('options');
            var pager = dg.datagrid('getPager');
            pager.pagination({
                onSelectPage: function (pageNum, pageSize) {
                    opts.pageNumber = pageNum;
                    opts.pageSize = pageSize;
                    pager.pagination('refresh', {
                        pageNumber: pageNum,
                        pageSize: pageSize
                    });
                    dg.datagrid('loadData', data);
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
        onCheck: function (index, row) {
            choiceRows = dg.datagrid("getChecked");
            console.log(choiceRows);
        },
        onUncheck: function (index, row) {
            choiceRows = dg.datagrid("getChecked");
            console.log(choiceRows);
        },
        onCheckAll: function (rows) {
            choiceRows = dg.datagrid("getChecked");
            console.log(choiceRows);
        },
        onUncheckAll: function (rows) {
            choiceRows = null;
            console.log(choiceRows);
        }
    });

    function removeItem() {
        var selectList = idList(choiceRows);

        if(selectList == null || selectList.length <= 0){
            console.log("请选择需要删除的数据")
            return false;
        }
        $.ajax({
            url: '/members',
            type: 'DELETE',
            data: JSON.stringify(selectList),
            success: function (data) {
                dg.datagrid({reload: true});
            },
            error: function (data) {
                console.log("error : " + selectList);
            }
        });
    }

    function idList(choiceRows) {
        var ids = [];
        $.each(choiceRows, function (index, value) {
            ids.push(value._id);
        })
        return ids;
    }

});