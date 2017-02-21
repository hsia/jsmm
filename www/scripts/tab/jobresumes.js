/**
 * Created by S on 2017/2/21.
 */

$(function () {
    var gridHeight = ($('#member-info').height());

    var toolbar = [
        {
            text: '添加',
            iconCls: 'icon-add',
            handler: function () {
                addRow();
            }
        }
    ];

    $('#job-resumes').datagrid({
        iconCls: 'icon-ok',
        height: gridHeight,
        rownumbers: true,
        pageSize: 10,
        nowrap: true,
        striped: true,
        fitColumns: true,
        loadMsg: '数据装载中......',
        pagination: true,
        allowSorts: true,
        remoteSort: true,
        multiSort: true,
        singleSelect: true,
        toolbar: toolbar,
        columns: [[
            {field: 'name', title: '单位名称', width: 110, align: 'left', editor: 'text'},
            {field: 'gender', title: '工作部门', width: 50, align: 'left'},
            {field: 'birthday', title: '职务', width: 120, align: 'left'},
            {field: 'nation', title: '职称', width: 120, align: 'left'},
            {field: 'idCard', title: '学术职务', width: 120, align: 'left'},
            {field: 'branch', title: '开始时间', width: 120, align: 'left'},
            {field: 'organ', title: '结束时间', width: 120, align: 'left'},
            {field: 'branchTime', title: '证明人', width: 120, align: 'left'}
        ]]
    });

    function addRow() {
        var editIndex = undefined;
        editIndex = $('#dg').datagrid('getRows').length - 1;
        $('#dg').datagrid('selectRow', editIndex).datagrid('beginEdit', editIndex);
    }

});