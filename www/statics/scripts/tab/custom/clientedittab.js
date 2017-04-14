$(function () {

    var $dataGrid = $('#client_edit_tab_table');

    var toolbar = [{
        text: '添加列',
        iconCls: 'icon-add',
        handler: function () {
            append();
        }
    }, '-', {
        text: '移除列',
        iconCls: 'icon-remove',
        handler: function () {
            removeit();
        }
    }, '-', {
        text: '保存tab',
        iconCls: 'icon-save',
        handler: function () {
            save();
        }
    }, '-', {
        text: '删除tab',
        iconCls: 'icon-cancel',
        handler: function () {
            deleteTab();
        }
    }];

    $dataGrid.datagrid({
        iconCls: 'icon-ok',
        height: 280,
        rownumbers: true,
        nowrap: true,
        striped: true,
        fitColumns: true,
        loadMsg: '数据装载中......',
        allowSorts: true,
        remoteSort: true,
        multiSort: true,
        singleSelect: true,
        toolbar: toolbar,
        columns: [[
            {field: 'col_id', title: 'col_id', width: 20, hidden: true},
            {field: 'field', title: 'field', width: 20, hidden: true},
            {field: 'title', title: '列名', width: 200, align: 'left', editor: 'textbox'},
            {
                field: 'editor',
                title: '列类型(文本/时间)',
                width: 200,
                align: 'left',
                editor: {
                    type: 'combobox',
                    options: {
                        data: [
                            {value: 'textbox', text: '文本'},
                            {value: 'datebox', text: '时间'}
                        ],
                        panelHeight: 'auto',
                        prompt: '请选择'
                    }
                }
            }
        ]],
        onClickRow: function (index, row) {
            if (editIndex != index) {
                if (endEditing()) {
                    $dataGrid.datagrid('selectRow', index).datagrid('beginEdit', index);
                    editIndex = index;
                } else {
                    $dataGrid.datagrid('selectRow', editIndex);
                }
            }
        },
        onBeginEdit: function (index, row) {
            $(".combo").click(function () {
                $(this).prev().combobox("showPanel");
            });
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
        if (endEditing()) {
            var tab = {};
            var tree = $("#tab_edit_title").combotree('tree'); // 得到树对象
            var choiceNode = tree.tree('getSelected');
            var gridTitle = choiceNode.text;
            if (gridTitle == null || gridTitle == '') {
                return;
            }

            var list = $dataGrid.datagrid('getRows')
            for (var i = 0; i < list.length; i++) {
                list[i].align = 'left';
                list[i].width = 100;
                // list[i].field = 'file_' + i;
            }
            tab.gridTitle = gridTitle;
            tab._id = choiceNode.id;
            tab.columns = list;
            $.post('/tabedit/', JSON.stringify(tab), function (data) {
                if (data.success) {
                    $('#client_edit_tab').dialog('close');
                    $.messager.alert('提示信息', '更新tab成功！', 'info');
                    window.location.href = '/'; //成功以后刷新页面
                } else if (!data.success) {
                    $.messager.alert('提示信息', data.content, 'warning');
                } else {
                    $.messager.alert('提示信息', "更新tab失败", 'error');
                }

            })
        }
    }

    function deleteTab() {

        var tab = {};
        var tree = $("#tab_edit_title").combotree('tree'); // 得到树对象
        var choiceNode = tree.tree('getSelected');
        var gridTitle = choiceNode.id;
        if (gridTitle == null || gridTitle == '') {
            return;
        }
        $.messager.confirm('删除提示', '该删除操作将会删除自定义tab及社员中包含该自定义tab数据，请谨慎删除！如确定删除，请点击“确定按钮”', function (r) {
            if (r) {
                $.ajax({
                    type: "DELETE",
                    url: '/tab/' + gridTitle,
                    dataType: 'json',
                    success: function (data) {
                        if (data.success) {
                            window.location.href = '/'; //成功以后刷新页面
                            $('#client_edit_tab').dialog('close');
                            $.messager.alert('提示信息', '删除tab成功！', 'info');
                        } else {
                            $.messager.alert('提示信息', data.content, 'warning');
                        }
                    },
                    error: function () {
                        $('#client_edit_tab').dialog('close');
                        $.messager.alert('提示信息', "刪除tab失败", 'error');
                    }

                });
            }
        });
    }
});