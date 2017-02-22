$(function () {
    var memberInfo = null;
    window.addEventListener("grid-row-selection", function (event) {
        // console.log(event.detail);
        memberInfo = event.detail;
    });

    //学位学历
    var $dataGrid = $("#social-list");
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
            accept();
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
                field: 'socialOrgType',
                title: '社会组织类别',
                width: 60,
                align: 'left',
                editor: {type: 'textbox', options: {}}
            },
            {
                field: 'socialOrgName',
                title: '社会组织名称',
                width: 100,
                align: 'left',
                editor: {
                    type: 'textbox',
                    options: {}
                }
            },
            {
                field: 'socialPositionLevel',
                title: '社会职务级别',
                width: 60,
                align: 'left',
                editor: {type: 'textbox', options: {}}
            },
            {
                field: 'socialPositionName',
                title: '社会职务名称',
                width: 100,
                align: 'left',
                editor: {
                    type: 'textbox',
                    options: {}
                }
            },
            {
                field: 'socialPeriod',
                title: '届次',
                width: 30,
                align: 'left',
                editor: {type: 'textbox', options: {}}
            },
            {field: 'socialBeginDate', title: '开始时间', width: 60, align: 'left', editor: {type: 'datebox', options: {}}},
            {field: 'socialEndDate', title: '结束时间', width: 60, align: 'left', editor: {type: 'datebox', options: {}}},
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

    function onClickRow(index) {
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

    function accept() {
        if (memberInfo == null) {
            return
        }
        if (endEditing()) {
            console.log($dataGrid.datagrid('getRows'));
            memberInfo.social = $dataGrid.datagrid('getRows');
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