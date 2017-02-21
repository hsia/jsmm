$(function () {
    //学位学历
    var $edudegreeList = $("#professional-list");
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
    $edudegreeList.datagrid({
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
            {field: 'schoolName', title: '学校(单位)名称', width: 150, align: 'left', editor: {type:'textbox', options:{required:true}}},
            {field: 'startingDate', title: '入学时间', width: 60, align: 'left', editor: {type:'datebox', options:{required:true}}},
            {field: 'graduateDate', title: '毕业时间', width: 60, align: 'left', editor: {type:'datebox', options:{required:true}}},
            {field: 'major', title: '专业', width: 120, align: 'left', editor: {type:'textbox', options:{required:true}}},
            {field: 'education', title: '学历', width: 110, align: 'left', editor: {type:'combobox', options:{valueField:'value',textField:'text',method:'get', url:'data/education.json',required:true,prompt:'请选择'}}},
            {field: 'degree', title: '学位', width: 110, align: 'left', editor: {type:'combobox', options:{valueField:'value',textField:'text',method:'get', url:'data/degree.json',required:true,prompt:'请选择'}}},
            {field: 'educationType', title: '教育类别', width: 80, align: 'left', editor: {type:'combobox', options:{valueField:'value',textField:'text',method:'get', url:'data/educationType.json',required:true,prompt:'请选择',panelHeight:'auto'}}},
        ]],
        onClickRow: function (index, row) {
            if (editIndex != index) {
                if (endEditing()) {
                    $edudegreeList.datagrid('selectRow', index)
                        .datagrid('beginEdit', index);
                    editIndex = index;
                } else {
                    $edudegreeList.datagrid('selectRow', editIndex);
                }
            }
        }
    });

    var editIndex = undefined;

    function endEditing() {
        if (editIndex == undefined) {
            return true
        }
        if ($edudegreeList.datagrid('validateRow', editIndex)) {
            $edudegreeList.datagrid('endEdit', editIndex);
            editIndex = undefined;
            return true;
        } else {
            return false;
        }
    }

    function onClickRow(index) {
        if (editIndex != index) {
            if (endEditing()) {
                $edudegreeList.datagrid('selectRow', index)
                    .datagrid('beginEdit', index);
                editIndex = index;
            } else {
                $edudegreeList.datagrid('selectRow', editIndex);
            }
        }
    }

    function append() {
        if (endEditing()) {
            $edudegreeList.datagrid('appendRow', {});
            editIndex = $edudegreeList.datagrid('getRows').length - 1;
            $edudegreeList.datagrid('selectRow', editIndex)
                .datagrid('beginEdit', editIndex);
        }
    }

    function removeit() {
        if (editIndex == undefined) {
            return
        }
        $edudegreeList.datagrid('cancelEdit', editIndex)
            .datagrid('deleteRow', editIndex);
        editIndex = undefined;
    }

    function accept() {
        if (endEditing()) {
            console.log($edudegreeList.datagrid('getRows'));
        }
    }


})