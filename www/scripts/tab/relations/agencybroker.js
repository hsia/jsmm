/**
 * Created by S on 2017/2/22.
 */

//介绍人
$(function () {

    var data_grid = $("#agencyBroker-list");

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
                save(data_grid, "agencybroker");
            }
        }
    ];
    buildGrid(data_grid, toolbar, columns);
    addSelectListener(data_grid, "agencybroker");
});