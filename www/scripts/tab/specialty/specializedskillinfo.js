/**
 * Created by S on 2017/2/22.
 */

// 业务专长
$(function () {

    var $grid = $("#specializedskill-list");
    var tabId = 'specializedskill';
    var gridTab = new GridTab(tabId, $grid);

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
                gridTab.addRow();
            }
        }, '-', {
            text: '移除记录',
            iconCls: 'icon-remove',
            handler: function () {
                gridTab.removeRow();
            }
        }, '-', {
            text: '保存记录',
            iconCls: 'icon-save',
            handler: function () {
                gridTab.saveRow();
            }
        }
    ];
    gridTab.buildGrid(toolbar, columns);
    gridTab.registerListeners();
});