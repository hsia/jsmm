/**
 * Created by S on 2017/2/22.
 */

// 业务专长
$(function () {

    var data_grid = $("#specializedskill-list");

    var columns = [
        {
            field: 'specializedType',
            title: '专业分类',
            width: 100,
            align: 'left',
            editor: {
                type: 'textbox',
                options: {}
            }
        },
        {
            field: 'specializedName',
            title: '专业名称',
            width: 100,
            align: 'left',
            editor: {type: 'textbox', options: {}}
        },
        {
            field: 'specializedDetailName',
            title: '专业详细名称',
            width: 150,
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
                save(data_grid, "specializedskill");
            }
        }
    ];
    buildGrid(data_grid, toolbar, columns);
    addSelectListener(data_grid, "specializedskill");
});