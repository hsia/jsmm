$(function () {

    $.get('/tab/', function (data) {
        var tabData = data.docs;
        for (var i = 0; i < tabData.length; i++) {
            var obj = tabData[i];
            $('#custom_tab').tabs('add', {
                title: obj.gridTitle,
                content: '<table id=' + obj.tab_id + ' data-columns=' + JSON.stringify(obj.columns) + ' style="width:100%;height:100%;"></table>',
                closable: false,
                selected: false
            });
        }

        $('#custom_tab').tabs({
            onSelect: function (title, index) {

                var tab = $('#custom_tab').tabs('getTab', index);
                var id = $('table', $(tab))[0].id;
                var columns = $('table', $(tab)).data('columns');
                var $dataGrid = $('#' + id);

                var toolbar = [{
                    text: '添加记录',
                    iconCls: 'icon-add',
                    handler: function () {
                        addRow($dataGrid);
                    }
                }, '-', {
                    text: '移除记录',
                    iconCls: 'icon-remove',
                    handler: function () {
                        removeit($dataGrid);
                    }
                }, '-', {
                    text: '保存记录',
                    iconCls: 'icon-save',
                    handler: function () {
                        save($dataGrid,id);
                    }
                }];

                buildGrid($dataGrid, toolbar, columns);
                addSelectListener($dataGrid, id);
            }
        });
    });
});