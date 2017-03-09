$(function () {

    var gridHeight = $("#member-info").height();

    $.get('/tab/', function (data) {
        var tabData = data.docs;
        for (var i = 0; i < tabData.length; i++) {
            var obj = tabData[i];
            $('#all-tabs').tabs('add', {
                title: obj.gridTitle,
                content: '<table id=' + obj.tab_id + ' data-columns=' + JSON.stringify(obj.columns) + ' style="width:100%;height:100%;"></table>',
                closable: false,
                selected: false
            });
        }

        $('#all-tabs').tabs({
            onSelect: function (title, index) {

                var toolbar = [{
                    text: '添加记录',
                    iconCls: 'icon-add',
                    handler: function () {
                        append();
                    }
                }, '-', {
                    text: '移除记录',
                    iconCls: 'icon-remove',
                    handler: function () {
                        removeit();
                    }
                }, '-', {
                    text: '保存记录',
                    iconCls: 'icon-save',
                    handler: function () {
                        save();
                    }
                }];

                var tab = $('#all-tabs').tabs('getTab', index);
                var id = $('table', $(tab))[0].id;
                var columns = $('table', $(tab)).data('columns');
                var $dataGrid = $('#' + id);

                var $member = $('#member-list').datagrid('getSelected');

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
                if ($member != null) {
                    $.get('/members/tab/' + $member._id, function (data) {
                        if (data[id] != undefined) {
                            $dataGrid.datagrid('loadData', $member[id]);
                        }else{
                            $dataGrid.datagrid('loadData', []);
                        }
                    });
                }


                var memberInfo = null;
                window.addEventListener("grid-row-selection", function (event) {
                    memberInfo = event.detail;
                    if (!$.isEmptyObject(memberInfo)) {
                        $.get('/members/tab/' + memberInfo._id, function (data) {
                            if (data[id] != undefined) {
                                $dataGrid.datagrid('loadData', memberInfo[id]);
                            }else{
                                $dataGrid.datagrid('loadData', []);
                            }
                        });
                    }
                });

                var editIndex = undefined;

                function endEditing() {
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

                function append() {
                    if (memberInfo == null && $member == null) {
                        $.messager.alert('提示信息', '请选择一行社员信息!', 'error');
                        return;
                    }
                    if (endEditing()) {
                        $dataGrid.datagrid('appendRow', {});
                        editIndex = $dataGrid.datagrid('getRows').length - 1;
                        $dataGrid.datagrid('selectRow', editIndex)
                            .datagrid('beginEdit', editIndex);
                    }
                }

                function removeit() {
                    if (editIndex == undefined) {
                        return
                    }
                    $dataGrid.datagrid('cancelEdit', editIndex)
                        .datagrid('deleteRow', editIndex);
                    editIndex = undefined;
                }

                function save() {
                    if (memberInfo == null && $member == null) {
                        $.messager.alert('提示信息', '请选择一行社员信息!', 'error');
                        return;
                    }
                    if (endEditing()) {

                        var member_id='';
                        var data;
                        if(memberInfo != null){
                            memberInfo[id] = $dataGrid.datagrid('getRows');
                            member_id = memberInfo._id;
                            data=JSON.stringify(memberInfo)
                        }else{
                            $member[id] = $dataGrid.datagrid('getRows');
                            member_id = $member._id;
                            data=JSON.stringify($member)
                        }

                        $.ajax({
                            url: '/members/tab/' + member_id,
                            type: 'PUT',
                            data: data,
                            success: function (data) {
                                if (data.success) {
                                    $.messager.alert('提示', '数据保存成功!', 'info');
                                }
                            },
                            error: function (data) {
                                $.messager.alert('提示', '数据更新失败!', 'error');
                            }
                        });
                    }
                }
            }
        });
    });
});