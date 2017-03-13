/**
 * Created by S on 2017/2/22.
 */

// 社内职务
$(function () {

    var $grid = $("#formerClubOffice-list");
    var tabId = 'formercluboffice';
    var gridTab = new GridTab(tabId, $grid);

    var columns = [
        {field: 'formeOrganizationCategory', title: '社内组织类别', width: 110, align: 'left', editor: 'textbox'},
        {field: 'formeOrganizationName', title: '社内组织名称', width: 110, align: 'left', editor: 'textbox'},
        {field: 'formeOrganizationLevel', title: '社会组织级别', width: 120, align: 'left', editor: 'textbox'},
        {field: 'formeOrganizationJob', title: '社内职务名称', width: 120, align: 'left', editor: 'textbox'},
        {field: 'formeTheTime', title: '届次', width: 120, align: 'left', editor: 'textbox'},
        {field: 'formeStartTime', title: '开始时间', width: 120, align: 'left', editor: 'datebox'},
        {field: 'formeEndTime', title: '结束时间', width: 120, align: 'left', editor: 'datebox'}
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
