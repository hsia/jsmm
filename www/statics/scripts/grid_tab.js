var GridTab = function (tabId, $grid) {
    this.member = null;
    this.memberId = null;
    console.log(this.memberId)
    this.tabId = tabId;
    this.$grid = $grid;
    this.editIndex = undefined;
    this.documentId = null;
};

GridTab.prototype.endEditing = function () {
    if (this.editIndex == undefined) {
        return true;
    }
    if (this.$grid.datagrid('validateRow', this.editIndex)) {
        this.$grid.datagrid('endEdit', this.editIndex);
        this.editIndex = undefined;
        return true;
    } else {
        return false;
    }
};

GridTab.prototype.addRow = function () {
    console.log(this.memberId)
    if (!this.memberId) {
        $.messager.alert('提示信息', '请选择一行社员信息!', 'error');
        return;
    }
    if (this.endEditing()) {
        var row = this.$grid.datagrid('getSelected');
        if (row != null) {
            this.editIndex = this.$grid.datagrid('getRowIndex', row);
            console.log('this.editIndex:' + this.editIndex)
            console.log(this)
            this.$grid.datagrid('insertRow', {
                index: this.editIndex,	// index start with 0
                row: {}
            });
            this.$grid.datagrid('selectRow', this.editIndex).datagrid('beginEdit', this.editIndex);
        } else {
            this.$grid.datagrid('appendRow', {});
            this.editIndex = this.$grid.datagrid('getRows').length - 1;
            this.$grid.datagrid('selectRow', this.editIndex).datagrid('beginEdit', this.editIndex);
        }
    }
};

//上移记录
GridTab.prototype.moveUp = function () {
    if (this.editIndex == undefined) {
        return
    }

    this.$grid.datagrid('endEdit', this.editIndex)
    var row = this.$grid.datagrid('getSelected');
    var index = this.$grid.datagrid('getRowIndex', row);
    mySort(index, 'up', this.$grid);
};

//下移记录
GridTab.prototype.moveDown = function () {
    if (this.editIndex == undefined) {
        return
    }
    this.$grid.datagrid('endEdit', this.editIndex)
    var row = this.$grid.datagrid('getSelected');
    var index = this.$grid.datagrid('getRowIndex', row);
    mySort(index, 'down', this.$grid);
};


GridTab.prototype.removeRow = function () {
    if (this.editIndex == undefined || this.editIndex < 0) {
        return
    }
    this.$grid.datagrid('cancelEdit', this.editIndex)
        .datagrid('deleteRow', this.editIndex);

    rows = this.$grid.datagrid('getRows')

    if (this.editIndex >= rows.length) {
        this.editIndex = (rows.length - 1);
        this.$grid.datagrid('selectRow', this.editIndex);
    } else {
        this.$grid.datagrid('selectRow', this.editIndex);
    }
};

GridTab.prototype.saveRow = function () {
    var memberInfo = {};
    var that = this;
    if (!this.memberId) {
        return;
    }
    $.get('/members/tab/' + this.memberId, function (data) {
        memberInfo = data;
        if (that.endEditing()) {
            memberInfo[that.tabId] = that.$grid.datagrid('getRows');
            $.ajax({
                url: '/members/' + memberInfo._id,
                type: 'PUT',
                data: JSON.stringify(memberInfo),
                success: function (data) {
                    if (data.success == "false") {
                        $.messager.alert('提示', data.content, 'error');
                    } else {
                        //删除成功以后，重新加载数据，并将choiceRows置为空。
                        $.messager.alert('提示', '数据保存成功!', 'info');
                    }
                },
                error: function (data) {
                    $.messager.alert('提示', '数据更新失败!', 'error');
                }
            });
        }
    });
};

GridTab.prototype.docUpload = function () {
    if (this.memberId == null) {
        $.messager.alert('提示信息', '请选择一行社员信息!', 'error');
        return;
    }
    console.log(this.memberId);
    var that = this;
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
                $('#member_doc').dialog('close');
                $.messager.progress({
                    title: 'Please waiting',
                    msg: 'Loading data...'
                });
                $('#doc_upload_form').form('submit', {
                    url: '/document/' + that.memberId + '/' + that.tabId,
                    success: function (data) {
                        that.reloadGridRemote();
                        $.messager.progress('close');
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
};

GridTab.prototype.docDelete = function () {
    if (this.documentId == null) {
        $.messager.alert('提示信息', '未选择文档！', 'info');
        return;
    }
    var that = this;
    $.messager.confirm('删除提示', '确定删除文档?', function (r) {
        if (r) {
            $.ajax({
                url: '/document/' + that.documentId,
                type: 'DELETE',
                success: function (data) {
                    that.reloadGridRemote();
                    $.messager.alert('提示信息', '删除文档成功！', 'info');
                },
                error: function (data) {
                    $.messager.alert('提示信息', '删除文档失败！', 'error');
                }
            });
        }
    });
};

GridTab.prototype.buildGrid = function (toolbar, columns) {
    var height = $("#member-info").height();
    var that = this;
    console.log(this)
    this.$grid.datagrid({
        iconCls: 'icon-ok',
        height: height * 0.89,
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
            if (that.editIndex != index) {
                if (that.endEditing()) {
                    that.$grid.datagrid('selectRow', index).datagrid('beginEdit', index);
                    that.editIndex = index;
                } else {
                    that.$grid.datagrid('selectRow', that.editIndex);
                }
            }
        },
        onBeginEdit: function (index, row) {
            $(".combo").click(function () {
                $(this).prev().combobox("showPanel");
            });
        }
    });
};

GridTab.prototype.buildDocGrid = function (toolbar, columns) {
    var gridHeight = $("#member-info").height();
    var that = this;
    this.$grid.datagrid({
        iconCls: 'icon-ok',
        height: gridHeight * 0.89,
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
            that.documentId = rowData._id;
        }
    });
};

GridTab.prototype.reloadGrid = function (clear) {
    if (clear) {
        this.$grid.datagrid('loadData', []);
        return;
    }
    if (!$.isEmptyObject(this.member)) {
        if (!$.isEmptyObject(this.member[this.tabId])) {
            this.$grid.datagrid('loadData', this.member[this.tabId]);
        } else {
            this.$grid.datagrid('loadData', []);
        }
    }
};

GridTab.prototype.reloadGridRemote = function () {
    var that = this;
    $.get('/members/' + this.memberId, function (data) {
        if (!$.isEmptyObject(data)) {
            if (!$.isEmptyObject(data[that.tabId])) {
                that.$grid.datagrid('loadData', data[that.tabId]);
            } else {
                that.$grid.datagrid('loadData', []);
            }
        }
    });
};

GridTab.prototype.registerListeners = function () {
    var that = this;
    window.addEventListener("grid-row-selection", function (event) {
        that.member = event.detail;
        that.memberId = that.member._id;
        that.reloadGrid();
    });
    window.addEventListener("grid-dg-refresh", function (event) {
        that.member = null;
        that.memberId = null;
        that.reloadGrid();
    });
    window.addEventListener("grid-row-deleteRow", function (event) {
        if (event.detail.success == true) {
            that.reloadGrid(true);
        }
    });
    window.addEventListener("tree-row-selection", function (event) {
        that.reloadGrid(true);
    });
    console.log(that)
};

function mySort(index, type, $grid) {
    if ("up" == type) {
        if (index != 0) {
            var toup = $grid.datagrid('getData').rows[index];
            var todown = $grid.datagrid('getData').rows[index - 1];
            $grid.datagrid('getData').rows[index] = todown;
            $grid.datagrid('getData').rows[index - 1] = toup;
            $grid.datagrid('refreshRow', index);
            $grid.datagrid('refreshRow', index - 1);
            $grid.datagrid('selectRow', index - 1);
        }
    } else if ("down" == type) {
        var rows = $grid.datagrid('getRows').length;
        if (index != rows - 1) {
            var todown = $grid.datagrid('getData').rows[index];
            var toup = $grid.datagrid('getData').rows[index + 1];
            $grid.datagrid('getData').rows[index + 1] = todown;
            $grid.datagrid('getData').rows[index] = toup;
            $grid.datagrid('refreshRow', index);
            $grid.datagrid('refreshRow', index + 1);
            $grid.datagrid('selectRow', index + 1);
        }
        $grid
    }

}
