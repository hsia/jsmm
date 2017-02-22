/**
 * Created by S on 2017/2/21.
 */

$(function () {
    var memberInfo = null;
    window.addEventListener("grid-row-selection", function (event) {
        memberInfo = event.detail;
        if (!$.isEmptyObject(memberInfo)) {
            if (!$.isEmptyObject(memberInfo.jobResumes)) {
                $jobResumes.datagrid('loadData', memberInfo.jobResumes);
            }else{
                $jobResumes.datagrid('loadData', []);
            }
        }
    });

    window.addEventListener("grid-row-deleteRow", function (event) {
        if (event.detail.success == true) {
            $jobResumes.datagrid('loadData', []);
        }
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
            {field: 'jobCompanyName', title: '单位名称', width: 110, align: 'left', editor: 'textbox'},
            {field: 'jobDep', title: '工作部门', width: 50, align: 'left', editor: 'textbox'},
            {field: 'jobDuties', title: '职务', width: 120, align: 'left', editor: 'textbox'},
            {field: 'jobTitle', title: '职称', width: 120, align: 'left', editor: 'textbox'},
            {field: 'jobAcademic', title: '学术职务', width: 120, align: 'left', editor: 'textbox'},
            {field: 'jobStartTime', title: '开始时间', width: 120, align: 'left', editor: 'datebox'},
            {field: 'jobEndTime', title: '结束时间', width: 120, align: 'left', editor: 'datebox'},
            {field: 'jobReterence', title: '证明人', width: 120, align: 'left', editor: 'textbox'}
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
        if (memberInfo == null) {
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
        console.log(editIndex);
        $jobResumes.datagrid('cancelEdit', editIndex).datagrid('deleteRow', editIndex);
        editIndex = undefined;
    }

    function save() {
        if (memberInfo == null) {
            return
        }
        if (endEditing()) {
            memberInfo.jobResumes = $jobResumes.datagrid('getRows');
            $.ajax({
                url: '/members/' + memberInfo._id,
                type: 'PUT',
                data: JSON.stringify(memberInfo),
                success: function (data) {
                    //删除成功以后，重新加载数据，并将choiceRows置为空。
                    $.messager.alert('提示', '数据保存成功!', 'info');
                },
                error: function (data) {
                    alert("success");
                    $.messager.alert('提示', '数据更新失败!', 'error');
                }
            });
        }
    }
});
