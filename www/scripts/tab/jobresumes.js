/**
 * Created by S on 2017/2/21.
 */

$(function () {

    var postData = null;

    window.addEventListener("grid-row-selection", function (event) {
        postData = event.detail;
    });
    var gridHeight = ($('#member-info').height());
    var $jobResumes = $('#job-resumes');
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

    $jobResumes.datagrid({
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
            {field: 'jobName', title: '单位名称', width: 110, align: 'left', editor: 'textbox'},
            {field: 'gender', title: '工作部门', width: 50, align: 'left', editor: 'textbox'},
            {field: 'birthday', title: '职务', width: 120, align: 'left', editor: 'textbox'},
            {field: 'nation', title: '职称', width: 120, align: 'left', editor: 'textbox'},
            {field: 'idCard', title: '学术职务', width: 120, align: 'left', editor: 'textbox'},
            {field: 'branch', title: '开始时间', width: 120, align: 'left', editor: 'datebox'},
            {field: 'organ', title: '结束时间', width: 120, align: 'left', editor: 'datebox'},
            {field: 'branchTime', title: '证明人', width: 120, align: 'left', editor: 'textbox'}
        ]],
        onClickRow: function (index, row) {
            if (editIndex != index) {
                if (endEditing()) {
                    $jobResumes.datagrid('selectRow', index)
                        .datagrid('beginEdit', index);
                    editIndex = index;
                } else {
                    $jobResumes.datagrid('selectRow', editIndex);
                }
            }
        }
    });

    var editIndex = undefined;

    function endEditing() {
        if (editIndex == undefined) {
            return true
        }
        if ($jobResumes.datagrid('validateRow', editIndex)) {
            $jobResumes.datagrid('endEdit', editIndex);
            editIndex = undefined;
            return true;
        } else {
            return false;
        }
    }

    function addRow() {
        if (postData == null) {
            $.messager.alert('提示信息', '请选择一行社员信息!', 'error');
            return;
        }
        if (endEditing()) {
            $jobResumes.datagrid('appendRow', {});
            editIndex = $jobResumes.datagrid('getRows').length - 1;
            $jobResumes.datagrid('selectRow', editIndex)
                .datagrid('beginEdit', editIndex);
        }
    }

    function removeit() {
        if (editIndex == undefined) {
            return;
        }
        $jobResumes.datagrid('cancelEdit', editIndex).datagrid('deleteRow', editIndex);
        editIndex = undefined;
    }

    function save() {
        if (postData == null) {
            return;
        }
        $jobResumes.datagrid('acceptChanges');
        postData.job = $jobResumes.datagrid('getRows');
        $.ajax({
            url: '/members/' + postData._id,
            type: 'PUT',
            data: JSON.stringify(postData),
            success: function (data) {
                if (data.success == "true") {
                    $.messager.alert('提示信息', '社员工作履历添加成功！', 'info');
                }
            }
        });
    }

});