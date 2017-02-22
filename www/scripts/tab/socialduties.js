/**
 * Created by S on 2017/2/22.
 */

$(function () {
    var memberInfo = null;
    window.addEventListener("grid-row-selection", function (event) {
        memberInfo = event.detail;
    });
    var gridHeight = ($('#member-info').height());
    var $socialDuties = $('#socialDuties-list');
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

    $socialDuties.datagrid({
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
            {field: 'socialOrganizationCategory', title: '社会组织类别', width: 110, align: 'left', editor: 'textbox'},
            {field: 'socialOrganizationName', title: '社会组织名称', width: 110, align: 'left', editor: 'textbox'},
            {field: 'socialOrganizationLevel', title: '社会职务级别', width: 120, align: 'left', editor: 'textbox'},
            {field: 'socialOrganizationJob', title: '社会职务名称', width: 120, align: 'left', editor: 'textbox'},
            {field: 'socialTheTime', title: '届次', width: 120, align: 'left', editor: 'textbox'},
            {field: 'socialStartTime', title: '开始时间', width: 120, align: 'left', editor: 'datebox'},
            {field: 'socialEndTime', title: '结束时间', width: 120, align: 'left', editor: 'datebox'}
        ]],
        onClickRow: function (index, row) {
            if (editIndex != index) {
                if (endEditing()) {
                    $socialDuties.datagrid('selectRow', index)
                        .datagrid('beginEdit', index);
                    editIndex = index;
                } else {
                    $socialDuties.datagrid('selectRow', editIndex);
                }
            }
        }
    });

    var editIndex = undefined;

    function endEditing() {
        if (editIndex == undefined) {
            return true
        }
        if ($socialDuties.datagrid('validateRow', editIndex)) {
            $socialDuties.datagrid('endEdit', editIndex);
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
            $socialDuties.datagrid('appendRow', {});
            editIndex = $socialDuties.datagrid('getRows').length - 1;
            $socialDuties.datagrid('selectRow', editIndex)
                .datagrid('beginEdit', editIndex);
        }
    }

    function removeit() {
        if (editIndex == undefined) {
            return;
        }
        $socialDuties.datagrid('cancelEdit', editIndex).datagrid('deleteRow', editIndex);
        editIndex = undefined;
    }

    function save() {
        if (memberInfo == null) {
            return
        }
        if (endEditing()) {
            memberInfo.socialduties = $socialDuties.datagrid('getRows');
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