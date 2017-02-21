$(function () {
    var memberInfo = null;
    window.addEventListener("grid-row-selection", function (event) {
        // console.log(event.detail);
        memberInfo = event.detail;
    });

    //学位学历
    var $professionalList = $("#professional-list");
    var professionalGridHeight = $("#member-info").height();
    var professionalToolbar = [{
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
    $professionalList.datagrid({
        iconCls: 'icon-ok',
        height: professionalGridHeight,
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
        toolbar: professionalToolbar,
        columns: [[
            {
                field: 'proProjectName',
                title: '项目名称',
                width: 120,
                align: 'left',
                editor: {type: 'textbox', options: {required: true}}
            },
            {
                field: 'proProjectType',
                title: '项目类型',
                width: 90,
                align: 'left',
                editor: {
                    type: 'combobox',
                    options: {
                        valueField: 'value',
                        textField: 'text',
                        method: 'get',
                        url: 'data/projectType.json',
                        required: true,
                        prompt: '请选择'
                    }
                }
            },
            {
                field: 'proProjectCompany',
                title: '项目下达单位',
                width: 120,
                align: 'left',
                editor: {type: 'textbox', options: {required: true}}
            },
            {
                field: 'proRolesInProject',
                title: '项目中所任角色',
                width: 60,
                align: 'left',
                editor: {
                    type: 'combobox',
                    options: {
                        valueField: 'value',
                        textField: 'text',
                        method: 'get',
                        url: 'data/roleInProject.json',
                        required: true,
                        prompt: '请选择'
                    }
                }
            },
            {
                field: 'proStartDate',
                title: '开始时间',
                width: 60,
                align: 'left',
                editor: {type: 'datebox', options: {required: true}}
            },
            {field: 'porEndDate', title: '结束时间', width: 60, align: 'left', editor: {type: 'datebox', options: {}}},
        ]],
        onClickRow: function (index, row) {
            if (editIndex != index) {
                if (endEditing()) {
                    $professionalList.datagrid('selectRow', index)
                        .datagrid('beginEdit', index);
                    editIndex = index;
                } else {
                    $professionalList.datagrid('selectRow', editIndex);
                }
            }
        }
    });

    var editIndex = undefined;

    function endEditing() {
        if (editIndex == undefined) {
            return true
        }
        if ($professionalList.datagrid('validateRow', editIndex)) {
            $professionalList.datagrid('endEdit', editIndex);
            editIndex = undefined;
            return true;
        } else {
            return false;
        }
    }

    function onClickRow(index) {
        if (editIndex != index) {
            if (endEditing()) {
                $professionalList.datagrid('selectRow', index)
                    .datagrid('beginEdit', index);
                editIndex = index;
            } else {
                $professionalList.datagrid('selectRow', editIndex);
            }
        }
    }

    function append() {
        if (memberInfo == null) {
            $.messager.alert('提示信息', '请选择一行社员信息!', 'error');
            return;
        }
        if (endEditing()) {
            $professionalList.datagrid('appendRow', {});
            editIndex = $professionalList.datagrid('getRows').length - 1;
            $professionalList.datagrid('selectRow', editIndex)
                .datagrid('beginEdit', editIndex);
        }
    }

    function removeit() {
        if (editIndex == undefined) {
            return
        }
        $professionalList.datagrid('cancelEdit', editIndex)
            .datagrid('deleteRow', editIndex);
        editIndex = undefined;
    }

    function accept() {
        if(memberInfo==null){
            return
        }
        if (endEditing()) {
            console.log($professionalList.datagrid('getRows'));
            memberInfo.professionalSkill = $professionalList.datagrid('getRows');
            $.ajax({
                url: '/members/' + memberInfo._id,
                type: 'PUT',
                data: JSON.stringify(memberInfo),
                success: function (data) {
                    $.messager.alert('提示', '数据保存成功!', 'info');
                },
                error: function (data) {
                    alert("success");
                    $.messager.alert('提示', '数据更新失败!', 'error');
                }
            });
        }
    }


})