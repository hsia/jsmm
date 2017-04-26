/**
 * Created by S on 2017/2/21.
 */
// 学历学位
$(function () {
    var tabId = 'educationDegree';
    var $grid = $("#edudegree-list");
    var gridTab = new GridTab(tabId, $grid);
    var columns = [
        {
            field: 'eduSchoolName',
            title: '学校(单位)名称',
            width: 150,
            align: 'left',
            editor: {type: 'textbox', options: {}}
        },
        {
            field: 'eduStartingDate',
            title: '入学时间',
            width: 60,
            align: 'left',
            editor: {type: 'datebox', options: {}}
        },
        {
            field: 'eduGraduateDate',
            title: '毕业时间',
            width: 60,
            align: 'left',
            editor: {type: 'datebox', options: {}}
        },
        {
            field: 'eduMajor',
            title: '专业',
            width: 120,
            align: 'left',
            editor: {type: 'textbox', options: {}}
        },
        {
            field: 'eduEducation',
            title: '学历',
            width: 110,
            align: 'left',
            editor: {
                type: 'combobox',
                options: {
                    valueField: 'value',
                    textField: 'text',
                    method: 'get',
                    url: 'static/data/education.json',
                    prompt: '请选择'
                }
            }
        },
        {
            field: 'eduDegree',
            title: '学位',
            width: 110,
            align: 'left',
            editor: {
                type: 'combobox',
                options: {
                    valueField: 'value',
                    textField: 'text',
                    method: 'get',
                    url: 'static/data/degree.json',
                    prompt: '请选择'
                }
            }
        },
        {
            field: 'eduEducationType',
            title: '教育类别',
            width: 80,
            align: 'left',
            editor: {
                type: 'combobox',
                options: {
                    valueField: 'value',
                    textField: 'text',
                    method: 'get',
                    url: 'static/data/educationType.json',
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