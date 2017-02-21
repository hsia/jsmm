$(function () {
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
            {field: 'projectName', title: '项目名称', width: 150, align: 'left', editor: {type:'textbox', options:{required:true}}},
            {field: 'projectType', title: '项目类型', width: 60, align: 'left', editor: {type:'datebox', options:{required:true}}},
            {field: 'projectCompany', title: '项目下达单位', width: 60, align: 'left', editor: {type:'datebox', options:{required:true}}},
            {field: 'rolesInProject', title: '项目中所任角色', width: 120, align: 'left', editor: {type:'textbox', options:{required:true}}},
            {field: 'startDate', title: '开始时间', width: 110, align: 'left', editor: {type:'combobox', options:{valueField:'value',textField:'text',method:'get', url:'data/education.json',required:true,prompt:'请选择'}}},
            {field: 'endDate', title: '结束时间', width: 110, align: 'left', editor: {type:'combobox', options:{valueField:'value',textField:'text',method:'get', url:'data/degree.json',required:true,prompt:'请选择'}}},
            {field: 'educationType', title: '教育类别', width: 80, align: 'left', editor: {type:'combobox', options:{valueField:'value',textField:'text',method:'get', url:'data/educationType.json',required:true,prompt:'请选择',panelHeight:'auto'}}},
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
        if (endEditing()) {
            console.log($professionalList.datagrid('getRows'));
        }
    }


})