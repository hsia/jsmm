$(function () {

    var memberInfo = null;
    window.addEventListener("grid-row-selection", function (event) {
        // console.log(event.detail);
        memberInfo = event.detail;
        if (!$.isEmptyObject(memberInfo)) {
            if (!$.isEmptyObject(memberInfo.award)) {
                $dataGrid.datagrid('loadData', memberInfo.award);
            }
        }
    });

    //学位学历
    var $dataGrid = $("#award-list");
    var gridHeight = $("#member-info").height();
    var toolbar = [{
        text: '添加记录',
        iconCls: 'icon-add',
        handler: function () {
            append();
        }
    }, '-', {
        text: '移除记录',
        iconCls: 'icon-remove',
        handler: function () {
            removeit();
        }
    }, '-', {
        text: '保存记录',
        iconCls: 'icon-save',
        handler: function () {
            save();
        }
    }];
    $dataGrid.datagrid({
        iconCls: 'icon-ok',
        height: gridHeight,
        rownumbers: true,
        pageSize: 10,
        nowrap: true,
        striped: true,
        fitColumns: true,
        loadMsg: '数据装载中......',
        // pagination: true,
        allowSorts: true,
        remoteSort: true,
        multiSort: true,
        singleSelect: true,
        toolbar: toolbar,
        columns: [[
            {
                field: 'awardProjectName',
                title: '获奖项目名称',
                width: 150,
                align: 'left',
                editor: {
                    type: 'textbox',
                    options: {}
                }
            },
            {
                field: 'awardDate',
                title: '获奖日期',
                width: 60,
                align: 'left',
                editor: {type: 'datebox', options: {}}
            },
            {
                field: 'awardNameAndLevel',
                title: '获奖名称及级别',
                width: 120,
                align: 'left',
                editor: {type: 'textbox', options: {}}
            },
            {
                field: 'awardRoleInProject',
                title: '项目中角色',
                width: 50,
                align: 'left',
                editor: {type: 'textbox', options: {}}
            },
            {
                field: 'awardCompany',
                title: '授予单位',
                width: 100,
                align: 'left',
                editor: {
                    type: 'textbox',
                    options: {}
                }
            },
            {
                field: 'awardMemo',
                title: '备注',
                width: 150,
                align: 'left',
                editor: {
                    type: 'textbox',
                    options: {}
                }
            }
        ]],
        onClickRow: function (index, row) {
            if (editIndex != index) {
                if (endEditing()) {
                    $dataGrid.datagrid('selectRow', index)
                        .datagrid('beginEdit', index);
                    editIndex = index;
                } else {
                    $dataGrid.datagrid('selectRow', editIndex);
                }
            }
        }
    });

    var editIndex = undefined;

    function endEditing() {
        if (editIndex == undefined) {
            return true
        }
        if ($dataGrid.datagrid('validateRow', editIndex)) {
            $dataGrid.datagrid('endEdit', editIndex);
            editIndex = undefined;
            return true;
        } else {
            return false;
        }
    }

    function append() {
        if (memberInfo == null) {
            $.messager.alert('提示信息', '请选择一行社员信息!', 'error');
            return;
        }
        if (endEditing()) {
            $dataGrid.datagrid('appendRow', {});
            editIndex = $dataGrid.datagrid('getRows').length - 1;
            $dataGrid.datagrid('selectRow', editIndex)
                .datagrid('beginEdit', editIndex);
        }
    }

    function removeit() {
        if (editIndex == undefined) {
            return
        }
        $dataGrid.datagrid('cancelEdit', editIndex)
            .datagrid('deleteRow', editIndex);
        editIndex = undefined;
    }

    function save() {
        if (memberInfo == null) {
            return
        }
        if (endEditing()) {
            memberInfo.award = $dataGrid.datagrid('getRows');
            $.ajax({
                url: '/members/tab/' + memberInfo._id,
                type: 'PUT',
                data: JSON.stringify(memberInfo),
                success: function (data) {
                    if (data.success) {
                        $.messager.alert('提示', '数据保存成功!', 'info');
                    }
                },
                error: function (data) {
                    alert("success");
                    $.messager.alert('提示', '数据更新失败!', 'error');
                }
            });
        }
    }


})