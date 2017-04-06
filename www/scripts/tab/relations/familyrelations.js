/**
 * Created by S on 2017/2/21.
 */
//社会关系
$(function () {

    var $grid = $("#familyRelation-list");
    var tabId = 'familyRelations';
    var gridTab = new GridTab(tabId, $grid);

    var columns = [
        {field: 'familyName', title: '姓名', width: 110, align: 'left', editor: 'textbox'},
        {
            field: 'familyRelation',
            title: '与本人的关系',
            width: 100,
            align: 'left',
            editor: {
                type: 'combobox',
                options: {
                    valueField: 'value',
                    textField: 'text',
                    method: 'get',
                    url: 'static/data/relationship.json',
                    prompt: '请选择'
                }
            }
        },
        {
            field: 'familyGender',
            title: '性别',
            width: 120,
            align: 'left',
            editor: {
                type: 'combobox',
                options: {
                    valueField: 'value',
                    textField: 'text',
                    method: 'get',
                    url: 'static/data/gender.json',
                    prompt: '请选择'
                }
            }
        },
        {field: 'familyBirthDay', title: '出生年月', width: 120, align: 'left', editor: 'datebox'},
        {field: 'familyCompany', title: '工作单位', width: 120, align: 'left', editor: 'textbox'},
        {field: 'familyJob', title: '职务', width: 120, align: 'left', editor: 'textbox'},
        {field: 'familyNationality', title: '国籍', width: 120, align: 'left', editor: 'textbox'},
        {
            field: 'familyPolitical ',
            title: '政治面貌',
            width: 120,
            align: 'left',
            editor: {
                type: 'combobox',
                options: {
                    valueField: 'value',
                    textField: 'text',
                    method: 'get',
                    url: 'static/data/party.json',
                    prompt: '请选择'
                }
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