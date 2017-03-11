/**
 * Created by S on 2017/2/21.
 */

// 技术成果
$(function () {

    var data_grid = $("#achievements-list");

    var columns = [
        {field: 'achievementsName', title: '成果名称', width: 110, align: 'left', editor: 'textbox'},
        {
            field: 'achievementsLevel',
            title: '成果水平',
            width: 110,
            align: 'left',
            editor: {
                type: 'combobox',
                options: {
                    valueField: 'value',
                    textField: 'text',
                    method: 'get',
                    url: 'data/resultsLevel.json',
                    prompt: '请选择',
                    panelHeight: 'auto'
                }
            }
        },
        {field: 'identificationUnit', title: '鉴定单位', width: 120, align: 'left', editor: 'textbox'},
        {field: 'achievementsRemark', title: '备注', width: 120, align: 'left', editor: 'textbox'}
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
                save(data_grid, "achievements");
            }
        }
    ];
    buildGrid(data_grid, toolbar, columns);
    addSelectListener(data_grid, "achievements");
});