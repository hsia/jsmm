/**
 * Created by S on 2017/2/22.
 */

// 论文著作
$(function () {

    var data_grid = $("#paper-list");

    var columns = [
        {
            field: 'paperPublications',
            title: '论文/著作',
            width: 60,
            align: 'left',
            editor: {
                type: 'combobox',
                options: {
                    valueField: 'value',
                    textField: 'text',
                    method: 'get',
                    url: 'data/publicationsType.json',
                    panelHeight: 'auto',
                    prompt: '请选择'
                }
            }
        },
        {
            field: 'paperName',
            title: '作品名称',
            width: 120,
            align: 'left',
            editor: {type: 'textbox', options: {}}
        },
        {
            field: 'paperPress',
            title: '刊物/出版社',
            width: 120,
            align: 'left',
            editor: {type: 'textbox', options: {}}
        },
        {
            field: 'paperAuthorSort',
            title: '第几作者',
            width: 50,
            align: 'left',
            editor: {type: 'textbox', options: {}}
        },
        {
            field: 'paperPressDate',
            title: '发行时间',
            width: 60,
            align: 'left',
            editor: {
                type: 'datebox',
                options: {}
            }
        },
        {
            field: 'paperRoleDetail',
            title: '角色说明',
            width: 110,
            align: 'left',
            editor: {
                type: 'combobox',
                options: {
                    valueField: 'value',
                    textField: 'text',
                    method: 'get',
                    url: 'data/rolesInPublications.json',
                    prompt: '请选择',
                    panelHeight: 'auto'
                }
            }
        }
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
                save(data_grid, "paper");
            }
        }
    ];
    buildGrid(data_grid, toolbar, columns);
    addSelectListener(data_grid, "paper");
});