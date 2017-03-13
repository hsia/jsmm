/**
 * Created by S on 2017/2/22.
 */

// 其他职务
$(function () {

    var $grid = $("#socialDuties-list");
    var tabId = 'achievements';
    var gridTab = new GridTab(tabId, $grid);

    var columns = [
        {field: 'socialOrganizationCategory', title: '社会组织类别', width: 110, align: 'left', editor: 'textbox'},
        {field: 'socialOrganizationName', title: '社会组织名称', width: 110, align: 'left', editor: 'textbox'},
        {field: 'socialOrganizationLevel', title: '社会职务级别', width: 120, align: 'left', editor: 'textbox'},
        {field: 'socialOrganizationJob', title: '社会职务名称', width: 120, align: 'left', editor: 'textbox'},
        {field: 'socialTheTime', title: '届次', width: 120, align: 'left', editor: 'textbox'},
        {field: 'socialStartTime', title: '开始时间', width: 120, align: 'left', editor: 'datebox'},
        {field: 'socialEndTime', title: '结束时间', width: 120, align: 'left', editor: 'datebox'}
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
