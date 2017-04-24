/**
 * Created by S on 2017/2/22.
 */

// 工作获奖
$(function () {

    var $grid = $("#award-list");
    var tabId = 'award';
    var gridTab = new GridTab(tabId, $grid);

    var columns = [
        {
            field: 'awardProjectName',
            title: '获奖项目名称',
            width: 150,
            align: 'left',
            editor: {
                type: 'textbox',
                options: {}
            }
        },
        {
            field: 'awardDate',
            title: '获奖时间',
            width: 60,
            align: 'left',
            editor: {type: 'datebox', options: {}}
        },
        {
            field: 'awardNameAndLevel',
            title: '获奖级别',
            width: 120,
            align: 'left',
            editor: {type: 'textbox', options: {}}
        },
        {
            field: 'awardRoleInProject',
            title: '项目中角色',
            width: 50,
            align: 'left',
            editor: {type: 'textbox', options: {}}
        },
        {
            field: 'awardCompany',
            title: '授予单位',
            width: 100,
            align: 'left',
            editor: {
                type: 'textbox',
                options: {}
            }
        },
        {
            field: 'awardMemo',
            title: '备注',
            width: 150,
            align: 'left',
            editor: {
                type: 'textbox',
                options: {}
            }
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