/**
 * Created by S on 2017/2/21.
 */

$(function () {
    var memberInfo = null;
    window.addEventListener("grid-row-selection", function (event) {
        memberInfo = event.detail;
        if (!$.isEmptyObject(memberInfo)) {
            if (!$.isEmptyObject(memberInfo.familyRelations)) {
                $familyList.datagrid('loadData', memberInfo.familyRelations);
            } else {
                $familyList.datagrid('loadData', []);
            }
        }
    });

    window.addEventListener("grid-row-deleteRow", function (event) {
        if (event.detail.success) {
            $familyList.datagrid('loadData', []);
        }
    });

    var gridHeight = ($('#member-info').height());
    var $familyList = $('#familyRelation-list');
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

    $familyList.datagrid({
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
            {field: 'familyName', title: '姓名', width: 110, align: 'left', editor: 'textbox'},
            {
                field: 'familyRelation',
                title: '与本人的关系',
                width: 100,
                align: 'left',
                editor: {
                    type: 'combobox',
                    options: {
                        valueField: 'value',
                        textField: 'text',
                        method: 'get',
                        url: 'data/relationship.json',
                        prompt: '请选择'
                    }
                }
            },
            {
                field: 'familyGender',
                title: '性别',
                width: 120,
                align: 'left',
                editor: {
                    type: 'combobox',
                    options: {
                        valueField: 'value',
                        textField: 'text',
                        method: 'get',
                        url: 'data/gender.json',
                        prompt: '请选择'
                    }
                }
            },
            {field: 'familyBirthDay', title: '出生年月', width: 120, align: 'left', editor: 'datebox'},
            {field: 'familyCompany', title: '工作单位', width: 120, align: 'left', editor: 'textbox'},
            {field: 'familyJob', title: '职务', width: 120, align: 'left', editor: 'textbox'},
            {field: 'familyNationality', title: '国籍', width: 120, align: 'left', editor: 'textbox'},
            {
                field: 'familyPolitical ',
                title: '政治面貌',
                width: 120,
                align: 'left',
                editor: {
                    type: 'combobox',
                    options: {
                        valueField: 'value',
                        textField: 'text',
                        method: 'get',
                        url: 'data/party.json',
                        prompt: '请选择'
                    }
                }
            }
        ]],
        onClickRow: function (index, row) {
            if (editIndex != index) {
                if (endEditing()) {
                    $familyList.datagrid('selectRow', index)
                        .datagrid('beginEdit', index);
                    editIndex = index;
                } else {
                    $familyList.datagrid('selectRow', editIndex);
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
        if ($familyList.datagrid('validateRow', editIndex)) {
            $familyList.datagrid('endEdit', editIndex);
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
            $familyList.datagrid('appendRow', {});
            editIndex = $familyList.datagrid('getRows').length - 1;
            $familyList.datagrid('selectRow', editIndex)
                .datagrid('beginEdit', editIndex);
        }
    }

    function removeit() {
        if (editIndex == undefined) {
            return;
        }
        $familyList.datagrid('cancelEdit', editIndex).datagrid('deleteRow', editIndex);
        editIndex = undefined;
    }

    function save() {
        if (memberInfo == null) {
            return
        }
        if (endEditing()) {
            memberInfo.familyRelations = $familyList.datagrid('getRows');
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