//报告
$(function () {

    var memberInfo = null;
    var getRow = '';
    var getCurrentPage = '';
    var currentRowData = null;

    window.addEventListener("grid-row-selection", function (event) {
        memberInfo = event.detail;
        getRow = memberInfo.sbRow;
        getCurrentPage = memberInfo.sbCurrentPage;
        loadD();
    });

    function loadD() {
        if (memberInfo != null) {
            if (memberInfo.departmentReport != null) {
                $dataGrid.datagrid('loadData', memberInfo.departmentReport);
            } else {
                $dataGrid.datagrid('loadData', []);
            }
        }
    }

    window.addEventListener("grid-row-deleteRow", function (event) {
        if (event.detail.success) {
            $dataGrid.datagrid('loadData', []);
        }
    });

    var $dataGrid = $("#docWord-list");
    var gridHeight = $("#member-info").height();
    var toolbar = [{
        text: '各部门的报告上传',
        iconCls: 'icon-import',
        handler: function () {
            if (memberInfo == null) {
                $.messager.alert('提示信息', '请选择一行社员信息!', 'error');
                return;
            }
            $('#doc_upload_form').form('clear');
            $('#doc_id').val(memberInfo._id);
            $('#doc_type').val('departmentReport');
            $('#member_doc').dialog({
                width: 300,
                height: 200,
                title: '文档上传',
                closed: false,
                cache: false,
                modal: true,
                buttons: [{
                    iconCls: 'icon-import',
                    text: '导入',
                    handler: function () {
                        $('#doc_upload_form').form('submit', {
                            url: '/doc/upload/',
                            success: function (data) {
                                $dataGrid.datagrid({
                                    loader: function (param, success) {
                                        $.get('/members/' + memberInfo._id, function (data) {
                                            var result = JSON.parse(data);
                                            success(result.departmentReport);
                                        })
                                    }
                                });
                                $('#member_doc').dialog('close');
                                $.messager.alert('提示信息', '文档上传成功！', 'info');
                            }
                        });
                    }
                }, {
                    iconCls: 'icon-cancel',
                    text: '取消',
                    handler: function () {
                        $('#doc_upload_form').form('clear');
                        $('#member_doc').dialog('close');
                    }
                }]
            })
        }
    }, '-', {
        text: '文档删除',
        iconCls: 'icon-cancel',
        handler: function () {
            var obj = {};
            obj.id = memberInfo._id;
            obj.file_url = currentRowData.file_url;
            obj.doc_type = 'departmentReport';
            obj.rowData = currentRowData;
            $.post('/members/del/', JSON.stringify(obj), function () {
                $.messager.alert('提示信息', '删除文档成功！', 'info');
                loadD();
                $('#member-list').datagrid('gotoPage', getCurrentPage).datagrid('reload').datagrid('selectRow', getRow);
            })
        }
    }];

    $('#department-report').click(function () {
        window.addEventListener("grid-row-selection", function (event) {
            memberInfo = event.detail;
            getRow = memberInfo.sbRow;
            getCurrentPage = memberInfo.sbCurrentPage;
            loadD();
        });
        $dataGrid.datagrid({
            iconCls: 'icon-ok',
            height: gridHeight,
            rownumbers: true,
            pageSize: 10,
            nowrap: true,
            striped: true,
            fitColumns: true,
            loadMsg: '数据装载中......',
            // pagination: true,
            allowSorts: true,
            remoteSort: true,
            multiSort: true,
            singleSelect: true,
            toolbar: toolbar,
            columns: [[
                {
                    field: 'depReportTime',
                    title: '上传时间',
                    width: 80,
                    align: 'left',
                    editor: {type: 'datetimebox', options: {}}
                }, {
                    field: 'depReportName',
                    title: '文件名称',
                    width: 160,
                    align: 'left',
                    editor: {type: 'textbox', options: {}}
                }, {
                    field: 'clickDownload',
                    title: '操作',
                    width: 60,
                    sortable: false,
                    align: 'left',
                    formatter: function (value, row, index) {
                        var path = "/members/download/" + row.file_url;
                        return '<a href= ' + path + ' >下载</a>';
                    }
                }
            ]],
            onSelect: function (rowIndex, rowData) {
                currentRowData = rowData;
            }
        });
        loadD();
        if (getCurrentPage != '' && getRow != '') {
            $('#member-list').datagrid('gotoPage', getCurrentPage).datagrid('reload').datagrid('selectRow', getRow);
        }else{
            $('#member-list').datagrid('reload');
        }
    });
});