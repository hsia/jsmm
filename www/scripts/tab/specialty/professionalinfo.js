/**
 * Created by S on 2017/2/22.
 */

//专业技术
$(function () {

    var $grid = $("#professional-list");
    var tabId = 'professionalSkill';
    var gridTab = new GridTab(tabId, $grid);

    var columns = [
            {
                field: 'proProjectName',
                title: '项目名称',
                width: 120,
                align: 'left',
                editor: {type: 'textbox', options: {}}
            },
        {
            field: 'proProjectType',
            title: '项目类型',
            width: 90,
            align: 'left',
            editor: {
                type: 'combobox',
                options: {
                    valueField: 'value',
                    textField: 'text',
                    method: 'get',
                    url: 'static/data/projectType.json',
                    prompt: '请选择'
                }
            }
        },
        {
            field: 'proProjectCompany',
            title: '项目下达单位',
            width: 120,
            align: 'left',
            editor: {type: 'textbox', options: {}}
        },
        {
            field: 'proRolesInProject',
            title: '项目中所任角色',
            width: 60,
            align: 'left',
            editor: {
                type: 'combobox',
                options: {
                    valueField: 'value',
                    textField: 'text',
                    method: 'get',
                    url: 'static/data/roleInProject.json',
                    prompt: '请选择'
                }
            }
        },
        {
            field: 'proStartDate',
            title: '开始时间',
            width: 60,
            align: 'left',
            editor: {type: 'datebox', options: {}}
        },
        {field: 'porEndDate', title: '结束时间', width: 60, align: 'left', editor: {type: 'datebox', options: {}}},
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