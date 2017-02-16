/**
 * Created by S on 2017/2/16.
 */
$(function () {
    var gridHeight = ($('#persons').height());
    var dg = $('#person-lists');

    dg.datagrid({
        iconCls: 'icon-ok',
        height: gridHeight,
        rownumbers: true,
        pageSize: 10,
        nowrap: true,
        striped: true,
        loadMsg: '数据装载中......',
        pagination: true,
        //idField: 'id',
        allowSorts: true,
        remoteSort: true,
        multiSort: true,
        //fitColumn: true,
        columns: [[
            {field: '_id', hidden: true},
            {field: '_rev', hidden: true},
            {field: 'name', title: '姓名', width: 110, align: 'left'},
            {field: 'age', title: '年龄', width: 100, align: 'left'}
        ]],
        loader:function (param,success) {
           var defaultUrl = '/members';
           $.get(defaultUrl, function (data) {
                success(data)
           });
        },
        loadFilter: function(data){
            if (typeof data.length == 'number' && typeof data.splice == 'function') {
            data = {
                total: data.length,
                rows: data
            }
        }
        var opts = dg.datagrid('options');
        var pager = dg.datagrid('getPager');
        pager.pagination({
            onSelectPage: function (pageNum, pageSize) {
                opts.pageNumber = pageNum;
                opts.pageSize = pageSize;
                pager.pagination('refresh', {
                    pageNumber: pageNum,
                    pageSize: pageSize
                });
                dg.datagrid('loadData', data);
            }
        });
        if (!data.originalRows) {
            data.originalRows = (data.rows);
        }
        var start = (opts.pageNumber - 1) * parseInt(opts.pageSize);
        var end = start + parseInt(opts.pageSize);
        data.rows = (data.originalRows.slice(start, end));
        return data;
        },
        onCheck: function (index, row) {
            choiceRows = dg.datagrid("getChecked");
            buttonStatus(choiceRows);
        },
        onUncheck: function (index, row) {
            choiceRows = dg.datagrid("getChecked");
            buttonStatus(choiceRows);
        },
        onCheckAll: function (rows) {
            choiceRows = dg.datagrid("getChecked");
            buttonStatus(choiceRows);
        },
        onUncheckAll: function (rows) {
            choiceRows = null;
            buttonStatus(choiceRows);
        }
    });

    function getDataStatus(value, row, index) {
        return utils.changeDataStatus(row.dataStatus);
    }

    function getDataTime(value, row, index) {
        return row.dataTime.substr(0, 8);
    }

});