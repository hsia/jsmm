/**
 * Created by S on 2017/2/21.
 */

// 工作履历
$(function () {

    var data_grid = $("#job-resumes");

    var columns = [
        {field: 'jobCompanyName', title: '单位名称', width: 110, align: 'left', editor: 'textbox'},
        {field: 'jobDep', title: '工作部门', width: 50, align: 'left', editor: 'textbox'},
        {field: 'jobDuties', title: '职务', width: 120, align: 'left', editor: 'textbox'},
        {field: 'jobTitle', title: '职称', width: 120, align: 'left', editor: 'textbox'},
        {field: 'jobAcademic', title: '学术职务', width: 120, align: 'left', editor: 'textbox'},
        {field: 'jobStartTime', title: '开始时间', width: 120, align: 'left', editor: 'datebox'},
        {field: 'jobEndTime', title: '结束时间', width: 120, align: 'left', editor: 'datebox'},
        {field: 'jobReterence', title: '证明人', width: 120, align: 'left', editor: 'textbox'}
    ];
    var toolbar = [
        {
            text: '添加记录',
            iconCls: 'icon-add',
            handler: function () {
                addRow(data_grid);
            }
        }, '-', {
            text: '移除记录',
            iconCls: 'icon-remove',
            handler: function () {
                removeit(data_grid);
            }
        }, '-', {
            text: '保存记录',
            iconCls: 'icon-save',
            handler: function () {
                save(data_grid, "jobResumes");
            }
        }
    ];
    buildGrid(data_grid, toolbar, columns);
    addSelectListener(data_grid, "jobResumes");
});
