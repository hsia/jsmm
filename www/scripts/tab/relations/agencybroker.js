/**
 * Created by S on 2017/2/22.
 */

//介绍人
$(function () {

    var $grid = $("#agencyBroker-list");
    var tabId = 'agencybroker';
    var gridTab = new GridTab(tabId, $grid);

    var columns = [
        {field: 'agencyName', title: '姓名', width: 110, align: 'left', editor: 'textbox'},
        {field: 'agencyCompany', title: '单位', width: 110, align: 'left', editor: 'textbox'},
        {field: 'agencyJob', title: '职务', width: 120, align: 'left', editor: 'textbox'},
        {field: 'agencyRelationShip', title: '与本人关系', width: 120, align: 'left', editor: 'textbox'}
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