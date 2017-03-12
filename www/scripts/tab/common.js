// var common_member_id = null;
// var common_document_id = null;
// var editIndex = undefined;
var selectedTabId = null; // 当前被选中的Tab的ID
var currentDocumentId = null; // 当前选中的文档ID

$(function () {
    $("#documents_tab").tabs({
        onSelect: function (title, index) {
            switch (index) {
                case 0:
                    common_document_id = null;
                    $("#department-report").datagrid("clearSelections");
                case 1:
                    common_document_id = null;
                    $("#department-info").datagrid("clearSelections");
                case 2:
                    common_document_id = null;
                    $("#speeches-text").datagrid("clearSelections");
            }
        }
    });
});

function buildGrid($dataGrid, toolbar, columns) {
    var gridHeight = $("#member-info").height();
    $dataGrid.datagrid({
        iconCls: 'icon-ok',
        height: gridHeight,
        rownumbers: true,
        nowrap: true,
        striped: true,
        fitColumns: true,
        loadMsg: '数据装载中......',
        allowSorts: true,
        remoteSort: true,
        multiSort: true,
        singleSelect: true,
        toolbar: toolbar,
        columns: [columns],
        onClickRow: function (index, row) {
            if (editIndex != index) {
                if (endEditing()) {
                    $dataGrid.datagrid('selectRow', index)
                        .datagrid('beginEdit', index);
                    editIndex = index;
                } else {
                    $dataGrid.datagrid('selectRow', editIndex);
                }
            }
        },
        onBeginEdit: function (index, row) {
            $(".combo").click(function () {
                $(this).prev().combobox("showPanel");
            });
        }
    });
}

function buildDocGrid($dataGrid, toolbar, columns) {
    var gridHeight = $("#member-info").height();
    $dataGrid.datagrid({
        iconCls: 'icon-ok',
        height: gridHeight,
        rownumbers: true,
        nowrap: true,
        striped: true,
        fitColumns: true,
        loadMsg: '数据装载中......',
        allowSorts: true,
        remoteSort: true,
        multiSort: true,
        singleSelect: true,
        toolbar: toolbar,
        columns: [columns],
        onSelect: function (rowIndex, rowData) {
            common_document_id = rowData._id;
        }
    });
}

function endEditing($dataGrid) {
    if (editIndex == undefined) {
        return true
    }
    if ($dataGrid.datagrid('validateRow', editIndex)) {
        $dataGrid.datagrid('endEdit', editIndex);
        editIndex = undefined;
        return true;
    } else {
        return false;
    }
}

function addRow($dataGrid) {
    if (common_member_id == null) {
        $.messager.alert('提示信息', '请选择一行社员信息!', 'error');
        return;
    }
    if (endEditing($dataGrid)) {
        $dataGrid.datagrid('appendRow', {});
        editIndex = $dataGrid.datagrid('getRows').length - 1;
        $dataGrid.datagrid('selectRow', editIndex)
            .datagrid('beginEdit', editIndex);
    }
}

function removeit($dataGrid) {
    if (editIndex == undefined) {
        return;
    }
    $dataGrid.datagrid('cancelEdit', editIndex).datagrid('deleteRow', editIndex);
    editIndex = undefined;
}

function save($dataGrid, obj) {
    if (common_member_id == null) {
        return
    }
    var memberInfo = {};
    $.get('/members/tab/' + common_member_id, function (data) {
        memberInfo = data;
        if (endEditing($dataGrid)) {
            memberInfo[obj] = $dataGrid.datagrid('getRows');
            $.ajax({
                url: '/members/' + memberInfo._id,
                type: 'PUT',
                data: JSON.stringify(memberInfo),
                success: function (data) {
                    //删除成功以后，重新加载数据，并将choiceRows置为空。
                    $.messager.alert('提示', '数据保存成功!', 'info');
                },
                error: function (data) {
                    alert("success");
                    $.messager.alert('提示', '数据更新失败!', 'error');
                }
            });
        }
    });
}

function docUpload($dataGrid, docType) {
    if (common_member_id == null) {
        $.messager.alert('提示信息', '请选择一行社员信息!', 'error');
        return;
    }
    $('#doc_upload_form').form('clear');
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
                    url: '/document/' + common_member_id + '/' + docType,
                    success: function (data) {
                        refreshDocGrid($dataGrid, docType);
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

function docDelete($dataGrid, docType) {
    if (common_document_id == null) {
        $.messager.alert('提示信息', '未选择文档！', 'info');
        return;
    }
    $.messager.confirm('删除提示', '确定删除文档?', function (r) {
        if (r) {
            $.ajax({
                url: '/document/' + common_document_id,
                type: 'DELETE',
                success: function (data) {
                    refreshDocGrid($dataGrid, docType);
                    $.messager.alert('提示信息', '删除文档成功！', 'info');
                },
                error: function (data) {
                    $.messager.alert('提示信息', '删除文档失败！', 'error');
                }
            });
        }
    });
}

function refreshDocGrid($dataGrid, docType) {
    $dataGrid.datagrid({
        loader: function (param, success) {
            $.get('/members/' + common_member_id, function (data) {
                success(data[docType]);
            })
        }
    });
}

function addSelectListener($dataGrid, obj) {
    window.addEventListener("grid-row-selection", function (event) {
        common_member_id = event.detail;
        $.get('/members/' + common_member_id, function (data) {
            if (!$.isEmptyObject(data)) {
                if (!$.isEmptyObject(data[obj])) {
                    $dataGrid.datagrid('loadData', data[obj]);
                } else {
                    $dataGrid.datagrid('loadData', []);
                }
            }
        });
    });
    window.addEventListener("grid-row-deleteRow", function (event) {
        if (event.detail.success == true) {
            $dataGrid.datagrid('loadData', []);
        }
    });
    window.addEventListener("tree-row-selection", function (event) {
        $dataGrid.datagrid('loadData', []);
    });
}