$(function () {

    var gridHeight = $('#membersinfo').height();
    var $dataGrid = $('#document-list');

    $dataGrid.datagrid({
        iconCls: 'icon-ok',
        height: gridHeight,
        rownumbers: true,
        pageSize: 10,
        nowrap: true,
        striped: true,
        fitColumns: true,
        loadMsg: '数据装载中......',
        pagination: true,
        allowSorts: true,
        multiSort: true,
        singleSelect: true,
        remoteSort: false,
        columns: [[
            {field: 'fileName', title: '文件名称', width: 110, sortable: true, align: 'left'},
            {field: 'type', title: '文件类型', width: 60, sortable: true, align: 'left', formatter: changeType},
            {field: 'name', title: '所属社员', width: 60, sortable: true, align: 'left'},
            {field: 'branch', title: '所属支社', width: 90, sortable: true, align: 'left'},
            {field: 'uploadTime', title: '创建时间', width: 80, sortable: true, align: 'left'},
            {field: 'clickDownload', title: '下载', width: 60, sortable: false, align: 'left', formatter: addLink},
        ]],
        loader: function (param, success) {
            var defaultUrl = '/documents';
            $.get(defaultUrl, function (data) {
                success(data)
            });
        },
        loadFilter: function (data) {
            if (typeof data.length == 'number' && typeof data.splice == 'function') {
                data = {
                    total: data.length,
                    rows: data
                }
            }
            var opts = $dataGrid.datagrid('options');
            var pager = $dataGrid.datagrid('getPager');
            pager.pagination({
                onSelectPage: function (pageNum, pageSize) {
                    opts.pageNumber = pageNum;
                    opts.pageSize = pageSize;
                    pager.pagination('refresh', {
                        pageNumber: pageNum,
                        pageSize: pageSize
                    });
                    $dataGrid.datagrid('loadData', data);
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
        onSelect: function (rowIndex, rowData) {
            memberInfo(rowData);
            var event = new CustomEvent("grid-row-selection", {
                detail: rowData
            });
            window.dispatchEvent(event);
        }
    });

    function changeType(value, row, index) {
        var result = '';
        switch (value) {
            case 'report':
                result = '部门报告';
                break;
            case 'info':
                result = '部门信息';
                break;
            case 'speech':
                result = '部门演讲稿';
                break;
        }

        return result;
    }

    function addLink(value, row, index) {
        return '<a href="">点击下载</a>';
    }

    //编辑数据
    function editInfo() {
        //1、先判断是否有选中的数据行
        var $member = $dataGrid.datagrid('getSelected');
        if ($member == null) {
            $.messager.alert('提示', '请选择需要编辑的数据!', 'error');
            return;
        }
        // 2、 发送异步请求，获得信息数据
        $.getJSON("/members/" + $member._id, function (data, status) {
            if (status) {
                $('#memberEdit-form').form('clear');
                $('#memberEdit-form').form('load', data);
                $('#memberEdit-dialog').dialog({
                    width: 800,
                    height: 630,
                    title: '编辑社员',
                    closed: false,
                    cache: false,
                    modal: true,
                    buttons: [{
                        iconCls: 'icon-ok',
                        text: '保存',
                        handler: function () {
                            $('#memberEdit-form').trigger('submit');
                        }
                    }, {
                        text: '取消',
                        handler: function () {
                            $('#memberEdit-dialog').dialog('close');
                        }
                    }]
                });
            } else {
                $.messager.alert('提示', '数据请求失败!', 'error');
            }
        })
    }

    //确认删除
    function confirmRemove() {
        //1、先判断是否有选中的数据行
        var member = $dataGrid.datagrid('getSelected');
        if (member == null) {
            $.messager.alert('提示', '请选择需要删除的数据!', 'error');
            return;
        }
        //2、将选中数据的_id放入到一个数组中
        var id = member._id;
        //3、提示删除确认
        $.messager.confirm('删除提示', '确定删除选中的数据?', function (r) {
            if (r) {
                //4、确认后，删除选中的数据
                removeItem(id)
            }
        });
    }

    //删除数据行
    function removeItem(id) {
        $.ajax({
            url: '/members/' + id,
            type: 'DELETE',
            success: function (data) {
                //删除成功以后，重新加载数据，并将choiceRows置为空。
                $dataGrid.datagrid('reload');

                $.messager.alert('提示', '数据删除成功!', 'info');
            },
            error: function (data) {
                $.messager.alert('提示', '数据删除失败!', 'error');
            }
        });
    }

});