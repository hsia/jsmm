/**
 * Created by S on 2017/2/22.
 */

$(function () {
    var memberInfo = null;
    window.addEventListener("grid-row-selection", function (event) {
        memberInfo = event.detail;
        if (!$.isEmptyObject(memberInfo)) {
            if (!$.isEmptyObject(memberInfo.agencybroker)) {
                $agencyBroker.datagrid('loadData', memberInfo.agencybroker);
            } else {
                $agencyBroker.datagrid('loadData', []);
            }
        }
    });

    window.addEventListener("grid-row-deleteRow", function (event) {
        if (event.detail.success) {
            $agencyBroker.datagrid('loadData', []);
        }
    });

    var gridHeight = ($('#member-info').height());
    var $agencyBroker = $('#agencyBroker-list');
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

    $agencyBroker.datagrid({
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
            {field: 'agencyName', title: '姓名', width: 110, align: 'left', editor: 'textbox'},
            {field: 'agencyCompany', title: '单位', width: 110, align: 'left', editor: 'textbox'},
            {field: 'agencyJob', title: '职务', width: 120, align: 'left', editor: 'textbox'},
            {field: 'agencyRelationShip', title: '与本人关系', width: 120, align: 'left', editor: 'textbox'}
        ]],
        onClickRow: function (index, row) {
            if (editIndex != index) {
                if (endEditing()) {
                    $agencyBroker.datagrid('selectRow', index)
                        .datagrid('beginEdit', index);
                    editIndex = index;
                } else {
                    $agencyBroker.datagrid('selectRow', editIndex);
                }
            }
        }
    });

    var editIndex = undefined;

    function endEditing() {
        if (editIndex == undefined) {
            return true
        }
        if ($agencyBroker.datagrid('validateRow', editIndex)) {
            $agencyBroker.datagrid('endEdit', editIndex);
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
            $agencyBroker.datagrid('appendRow', {});
            editIndex = $agencyBroker.datagrid('getRows').length - 1;
            $agencyBroker.datagrid('selectRow', editIndex)
                .datagrid('beginEdit', editIndex);
        }
    }

    function removeit() {
        if (editIndex == undefined) {
            return;
        }
        $agencyBroker.datagrid('cancelEdit', editIndex).datagrid('deleteRow', editIndex);
        editIndex = undefined;
    }

    function save() {
        if (memberInfo == null) {
            return
        }
        if (endEditing()) {
            memberInfo.agencybroker = $agencyBroker.datagrid('getRows');
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
