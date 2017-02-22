/**
 * Created by S on 2017/2/21.
 */

$(function () {
    var memberInfo = null;
    window.addEventListener("grid-row-selection", function (event) {
        memberInfo = event.detail;
    });

    var gridHeight = ($('#member-info').height());
    var $achievementsList = $('#achievements-list');
    var toolbar = [
        {
            text: '添加记录',
            iconCls: 'icon-add',
            handler: function () {
                addRow();
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
        }
    ];

    $achievementsList.datagrid({
        iconCls: 'icon-ok',
        height: gridHeight,
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
            {field: 'achievementsName', title: '成果名称', width: 110, align: 'left', editor: 'textbox'},
            {
                field: 'achievementsLevel',
                title: '成果水平',
                width: 110,
                align: 'left',
                editor: {
                    type: 'combobox',
                    options: {
                        valueField: 'value',
                        textField: 'text',
                        method: 'get',
                        url: 'data/resultsLevel.json',
                        prompt: '请选择'
                    }
                }
            },
            {field: 'identificationUnit', title: '鉴定单位', width: 120, align: 'left', editor: 'textbox'},
            {field: 'achievementsRemark', title: '备注', width: 120, align: 'left', editor: 'textbox'}
        ]],
        onClickRow: function (index, row) {
            if (editIndex != index) {
                if (endEditing()) {
                    $achievementsList.datagrid('selectRow', index)
                        .datagrid('beginEdit', index);
                    editIndex = index;
                } else {
                    $achievementsList.datagrid('selectRow', editIndex);
                }
            }
        }
    });

    var editIndex = undefined;

    function endEditing() {
        if (editIndex == undefined) {
            return true
        }
        if ($achievementsList.datagrid('validateRow', editIndex)) {
            $achievementsList.datagrid('endEdit', editIndex);
            editIndex = undefined;
            return true;
        } else {
            return false;
        }
    }

    function addRow() {
        if (memberInfo == null) {
            $.messager.alert('提示信息', '请选择一行社员信息!', 'error');
            return;
        }
        if (endEditing()) {
            $achievementsList.datagrid('appendRow', {});
            editIndex = $achievementsList.datagrid('getRows').length - 1;
            $achievementsList.datagrid('selectRow', editIndex)
                .datagrid('beginEdit', editIndex);
        }
    }

    function removeit() {
        if (editIndex == undefined) {
            return;
        }
        $achievementsList.datagrid('cancelEdit', editIndex).datagrid('deleteRow', editIndex);
        editIndex = undefined;
    }

    function save() {
        if (memberInfo == null) {
            return
        }
        if (endEditing()) {
            memberInfo.achievements = $achievementsList.datagrid('getRows');
            $.ajax({
                url: '/members/tab/' + memberInfo._id,
                type: 'PUT',
                data: JSON.stringify(memberInfo),
                success: function (data) {
                    //删除成功以后，重新加载数据，并将choiceRows置为空。
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
});