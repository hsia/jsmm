/**
 * Created by S on 2017/2/21.
 */

// 参政议政履职情况
$(function () {

    var $grid = $("#politics-resume");
    var tabId = 'politicsResume';
    var gridTab = new GridTab(tabId, $grid);

    var columns = [
        {
            field: 'resumeDate',
            title: '日期',
            width: 60,
            align: 'left',
            editor: {type: 'datebox', options: {}}
        },
        {
            field: 'resumeEvent',
            title: '事件',
            width: 160,
            align: 'left',
            editor: {type: 'textbox', options: {}}
        },
        {
            field: 'resumeTime',
            title: '时间',
            width: 80,
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
