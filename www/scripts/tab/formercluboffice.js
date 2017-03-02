/**
 * Created by S on 2017/2/22.
 */

$(function () {
    var memberInfo = null;
    window.addEventListener("grid-row-selection", function (event) {
        memberInfo = event.detail;
        if (!$.isEmptyObject(memberInfo)) {
            if (!$.isEmptyObject(memberInfo.formercluboffice)) {
                $formerClubOffice.datagrid('loadData', memberInfo.formercluboffice);
            } else {
                $formerClubOffice.datagrid('loadData', []);
            }
        }
    });

    window.addEventListener("grid-row-deleteRow", function (event) {
        if (event.detail.success) {
            $formerClubOffice.datagrid('loadData', []);
        }
    });

    window.addEventListener("tree-row-selection", function (event) {
        $dataGrid.datagrid('loadData', []);
    });

    var gridHeight = ($('#member-info').height());
    var $formerClubOffice = $('#formerClubOffice-list');
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

    $formerClubOffice.datagrid({
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
            {field: 'formeOrganizationCategory', title: '社内组织类别', width: 110, align: 'left', editor: 'textbox'},
            {field: 'formeOrganizationName', title: '社内组织名称', width: 110, align: 'left', editor: 'textbox'},
            {field: 'formeOrganizationLevel', title: '社会组织级别', width: 120, align: 'left', editor: 'textbox'},
            {field: 'formeOrganizationJob', title: '社内职务名称', width: 120, align: 'left', editor: 'textbox'},
            {field: 'formeTheTime', title: '届次', width: 120, align: 'left', editor: 'textbox'},
            {field: 'formeStartTime', title: '开始时间', width: 120, align: 'left', editor: 'datebox'},
            {field: 'formeEndTime', title: '结束时间', width: 120, align: 'left', editor: 'datebox'}
        ]],
        onClickRow: function (index, row) {
            if (editIndex != index) {
                if (endEditing()) {
                    $formerClubOffice.datagrid('selectRow', index)
                        .datagrid('beginEdit', index);
                    editIndex = index;
                } else {
                    $formerClubOffice.datagrid('selectRow', editIndex);
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
        if ($formerClubOffice.datagrid('validateRow', editIndex)) {
            $formerClubOffice.datagrid('endEdit', editIndex);
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
            $formerClubOffice.datagrid('appendRow', {});
            editIndex = $formerClubOffice.datagrid('getRows').length - 1;
            $formerClubOffice.datagrid('selectRow', editIndex)
                .datagrid('beginEdit', editIndex);
        }
    }

    function removeit() {
        if (editIndex == undefined) {
            return;
        }
        $formerClubOffice.datagrid('cancelEdit', editIndex).datagrid('deleteRow', editIndex);
        editIndex = undefined;
    }

    function save() {
        if (memberInfo == null) {
            return
        }
        if (endEditing()) {
            memberInfo.formercluboffice = $formerClubOffice.datagrid('getRows');
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
