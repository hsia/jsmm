/**
 * Created by S on 2017/2/22.
 */

// 专利情况
$(function () {

    var $grid = $("#patents-list");
    var tabId = 'patents';
    var gridTab = new GridTab(tabId, $grid);

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
                gridTab.addRow();
            }
        }/*, '-', {
            text: '上移记录',
            iconCls: 'icon-move-up',
            handler: function () {
                gridTab.moveUp();
            }
        }, '-', {
            text: '下移记录',
            iconCls: 'icon-move-down',
            handler: function () {
                gridTab.moveDown();
            }
         }*/, '-', {
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