$(function () {

    var gridHeight = $('#membersinfo').height();
    var $dataGrid = $('#document-list');


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
        toolbar: '#tb',
        columns: [[
            {field: 'fileName', title: '文件名称', width: 110, sortable: false, align: 'left'},
            {
                field: 'type',
                title: '文件类型',
                width: 60,
                sortable: false,
                align: 'left',
                formatter: changeType
            },
            {field: 'name', title: '所属社员', width: 60, sortable: false, align: 'left'},
            {field: 'branch', title: '所属支社', width: 90, sortable: true, align: 'left'},
            {field: 'uploadTime', title: '创建时间', width: 80, sortable: false, align: 'left'},
            {
                field: 'clickDownload',
                title: '操作',
                width: 60,
                sortable: false,
                align: 'left',
                formatter: function (value, row, index) {
                    var path="/members/download/"+row.file_url;
                    return '<a href= '+path+' >下载</a>';
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
                    param.organName = organName;
                    $.post('/documents/', JSON.stringify(param), function (data) {
                        success(data)
                    }, 'json');
                }
            });
        } else {
            return false;
        }
    });

    $('#tabsAll').tabs({
        border: false,
        onSelect: function (title, index) {
            $("#tb-form").form('clear');
            console.log(title + "," + index);
            if (index == 1 && organName == null) {
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
            case 'report':
                result = '部门报告';
                break;
            case 'info':
                result = '部门信息';
                break;
            case 'speech':
                result = '演讲稿';
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

    //查询
    $('#searchButton').click(function (event) {
        event.preventDefault();
        var formData = $('#tb-form').serializeArray();
        var searchInfo = {};
        $.each(formData, function (index, element) {
            console.log(element)
            searchInfo[element.name] = element.value;
        });
        // $.ajax({
        //     url: '/documentSearch/',
        //     type: 'POST',
        //     data: JSON.stringify(searchInfo),
        //     success: function (data) {
        //         //删除成功以后，重新加载数据，并将choiceRows置为空。
        //         $dataGrid.datagrid('reload');
        //     },
        //     error: function (data) {
        //         $.messager.alert('提示', '数据查询失败!', 'error');
        //     }
        // });

        $dataGrid.datagrid({
            loader: function (param, success) {
                param.searchInfo = searchInfo;
                param.searchInfo.branch = (organName == null ? '' : organName);
                var defaultUrl = '/documentSearch';
                $.post(defaultUrl, JSON.stringify(param), function (data) {
                    success(data)
                }, 'json');
            }
        })
    })
})
;