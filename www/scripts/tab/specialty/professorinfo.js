/**
 * Created by S on 2017/2/22.
 */

// 专家情况
$(function () {

    var data_grid = $("#professor-list");

    var columns = [
        {
            field: 'professorName',
            title: '专家名称',
            width: 60,
            align: 'left',
            editor: {
                type: 'textbox',
                options: {}
            }
        },
        {
            field: 'approvalDate',
            title: '批准时间',
            width: 60,
            align: 'left',
            editor: {type: 'datebox', options: {}}
        },
        {
            field: 'approvalCompanyLevel',
            title: '批准单位级别',
            width: 80,
            align: 'left',
            editor: {type: 'textbox', options: {}}
        },
        {
            field: 'approvalCompanyName',
            title: '批准单位名称',
            width: 100,
            align: 'left',
            editor: {type: 'textbox', options: {}}
        },
        {
            field: 'govSubsidiesType',
            title: '政府津贴类别',
            width: 80,
            align: 'left',
            editor: {
                type: 'textbox',
                options: {}
            }
        },
        {
            field: 'subsidiesDate',
            title: '享受津贴时间',
            width: 60,
            align: 'left',
            editor: {
                type: 'datebox',
                options: {}
            }
        }
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
                save(data_grid, "professor");
            }
        }
    ];
    buildGrid(data_grid, toolbar, columns);
    addSelectListener(data_grid, "professor");
});