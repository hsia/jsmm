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
        multiSort: true,
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
            {field: 'name', title: '所属社员', width: 60, sortable: false, align: 'left'},
            {field: 'branch', title: '所属支社', width: 90, sortable: false, align: 'left'},
            {field: 'fileUploadTime', title: '创建时间', width: 80, sortable: false, align: 'left'},
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
            console.log(title + "," + index);
            if (index == 1) {
                $dataGrid.datagrid({
                    loader: function (param, success) {
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
                    toolbar: '#tb',
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
