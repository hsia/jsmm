/**
 * Created by S on 2017/2/21.
 */

// 社会职务
$(function () {

    var $grid = $("#social-list");
    var tabId = 'social';
    var gridTab = new GridTab(tabId, $grid);

    var columns = [
        {
            field: 'socialOrgType',
            title: '社会组织类别',
            width: 60,
            align: 'left',
            editor: {
                type: 'combobox',
                options: {
                    valueField: 'value',
                    textField: 'text',
                    method: 'get',
                    url: 'static/data/socialOrgType.json',
                    prompt: '请选择'
                }
            }
        },
        {
            field: 'socialOrgName',
            title: '社会组织名称',
            width: 100,
            align: 'left',
            editor: {
                type: 'textbox',
                options: {}
            }
        },
        {
            field: 'socialPositionLevel',
            title: '社会职务级别',
            width: 60,
            align: 'left',
            editor: {
                type: 'combobox',
                options: {
                    valueField: 'value',
                    textField: 'text',
                    method: 'get',
                    url: 'static/data/socialPositionLevel.json',
                    prompt: '请选择'
                }
            }
        },
        {
            field: 'socialPositionName',
            title: '社会职务名称',
            width: 100,
            align: 'left',
            editor: {
                type: 'textbox',
                options: {}
            }
        },
        {
            field: 'socialPeriod',
            title: '届次',
            width: 30,
            align: 'left',
            editor: {type: 'textbox', options: {}}
        },
        {field: 'socialBeginDate', title: '开始时间', width: 60, align: 'left', editor: {type: 'datebox', options: {}}},
        {field: 'socialEndDate', title: '结束时间', width: 60, align: 'left', editor: {type: 'datebox', options: {}}},
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