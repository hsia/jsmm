$(function () {

    var gridHeight = $('#membersinfo').height();
    var $dataGrid = $('#document-list');

    var toolbar = [{
        text: '高级查询',
        iconCls: 'icon-search',
        handler: function () {
            documentsSearch();
        }
    }];

    $dataGrid.datagrid({
        iconCls: 'icon-ok',
        height: gridHeight,
        rownumbers: true,
        pageSize: 20,
        nowrap: true,
        striped: true,
        fitColumns: true,
        loadMsg: '数据装载中......',
        pagination: true,
        allowSorts: true,
        multiSort: false,
        singleSelect: true,
        remoteSort: true,
        toolbar: toolbar,
        columns: [[
            {field: 'fileName', title: '文件名称', width: 110, sortable: false, align: 'left'},
            {
                field: 'docType',
                title: '文件类型',
                width: 60,
                sortable: false,
                align: 'left',
                formatter: changeType
            },
            {field: 'name', title: '社员姓名', width: 60, sortable: false, align: 'left'},
            {field: 'branch', title: '所属支社', width: 90, sortable: false, align: 'left'},
            {field: 'fileUploadTime', title: '创建时间', width: 80, sortable: true, align: 'left'},
            {
                field: 'clickDownload',
                title: '操作',
                width: 60,
                sortable: false,
                align: 'left',
                formatter: function (value, row, index) {
                    var path = "/document/" + row._id + "/" + row.fileName;
                    return '<a href= ' + path + '>下载</a>';
                }
            }
        ]]
    });

    var organName = null;
    window.addEventListener("tree-row-selection", function (event) {
        organName = event.detail;
        if (organName != null) {
            $dataGrid.datagrid({
                loader: function (param, success) {
                    param.branch = organName;
                    $.post('/documents', JSON.stringify(param), function (data) {
                        success(data)
                    }, 'json');
                }
            });
        } else {
            return false;
        }
    });

    window.addEventListener("organ-tree-operation", function (event) {
        $dataGrid.datagrid({
            loader: function (param, success) {
                param.branch = '';
                $.post('/documents', JSON.stringify(param), function (data) {
                    success(data)
                }, 'json');
            }
        });
    });

    $('#tabsAll').tabs({
        border: false,
        onSelect: function (title, index) {
            $("#tb-form").form('clear');
            var node = $('#organTree').tree('getSelected');
            console.log(title + "," + index);
            if (index == 1) {
                $dataGrid.datagrid({
                    loader: function (param, success) {
                        if (node != null) {
                            param.branch = node.id;
                        }
                        var defaultUrl = '/documents';
                        $.post(defaultUrl, JSON.stringify(param), function (data) {
                            success(data)
                        }, 'json');
                    }
                })
            }
        }
    });

    function changeType(value, row, index) {
        var result = '';
        switch (value) {
            case 'researchReport':
                result = '调研报告';
                break;
            case 'politicsInfo':
                result = '参政议政信息';
                break;
            case 'unitedTheory':
                result = '统战理论';
                break;
            case 'propaganda':
                result = '宣传稿';
                break;
        }

        return result;
    }

    $("#document-search-form").submit(function (event) {
        var formData = $(this).serializeArray();
        var documentInfo = {};
        $.each(formData, function (index, element) {
            documentInfo[element.name] = element.value;
        });
        documentInfo.branch = (branch == null ? '' : branch);
        if (documentInfo.startDate != '' && documentInfo.endDate == '') {
            var mydate = new Date();
            currYear = mydate.getFullYear();
            currMonth = mydate.getMonth() + 1;
            currDay = mydate.getDate();
            documentInfo.endDate = currYear + "-" + ((currMonth < 10) ? ("0" + currMonth) : currMonth) + "-" + ((currDay < 10) ? ("0" + currDay) : currDay);
        } else if (documentInfo.startDate == '' && documentInfo.endDate != '') {
            documentInfo.startDate = '1970-01-01';
        } else {

        }
        $('#document-search').dialog('close');
        $('#document-search-form').form('clear');
        $dataGrid.datagrid({
            loader: function (param, success) {
                param.documentInfo = documentInfo;
                param.branch = (organName == null ? '' : organName);
                var defaultUrl = '/documents';
                $.post(defaultUrl, JSON.stringify(param), function (data) {
                    success(data)
                }, 'json');
            }
        })
    });

    function documentsSearch() {

        $('#docTypeD').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/documenttype.json',
            method: 'get'
        })
        $('#document-search').dialog({
            width: 600,
            height: 300,
            title: '社员查询',
            closed: false,
            cache: false,
            modal: true,
            buttons: [{
                iconCls: 'icon-ok',
                text: '查询',
                handler: function () {
                    $('#document-search-form').trigger('submit');
                }
            }, {
                iconCls: 'icon-cancel',
                text: '取消',
                handler: function () {
                    $('#document-search-form').form('clear');
                    $('#document-search').dialog('close');
                }
            }]
        });
    }
});
