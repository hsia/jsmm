/**
 * Created by S on 2017/2/22.
 */

// 专利情况
$(function () {

    var data_grid = $("#patents-list");

    var columns = [
        {
            field: 'patentName',
            title: '获专利名称',
            width: 150,
            align: 'left',
            editor: {
                type: 'textbox',
                options: {}
            }
        },
        {
            field: 'patentDate',
            title: '获专利时间',
            width: 60,
            align: 'left',
            editor: {type: 'datebox', options: {}}
        },
        {
            field: 'patenNo',
            title: '专利号',
            width: 120,
            align: 'left',
            editor: {type: 'textbox', options: {}}
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
                save(data_grid, "patents");
            }
        }
    ];
    buildGrid(data_grid, toolbar, columns);
    addSelectListener(data_grid, "patents");
});