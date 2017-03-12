var GridTab = function(tabId, $grid) {
    this.memberId = null;
    this.tabId = tabId;
    this.$grid = $grid;
    this.editIndex = null;
};

GridTab.prototype.endEditing = function() {
    if (!this.editIndex) {
        return true;
    }
    if (this.$grid.datagrid('validateRow', this.editIndex)) {
        this.$grid.datagrid('endEdit', this.editIndex);
        this.editIndex = null;
        return true;
    } else {
        return false;
    }
};

GridTab.prototype.addRow = function() {
    if (!this.memberId) {
        $.messager.alert('提示信息', '请选择一行社员信息!', 'error');
        return;
    }
    if (this.endEditing()) {
        this.$grid.datagrid('appendRow', {});
        this.editIndex = this.$grid.datagrid('getRows').length - 1;
        this.$grid.datagrid('selectRow', this.editIndex)
            .datagrid('beginEdit', this.editIndex);
    }
};

GridTab.prototype.removeRow = function() {
    if (this.editIndex) {
        this.$grid.datagrid('cancelEdit', this.editIndex)
            .datagrid('deleteRow', this.editIndex);
        this.editIndex = null;
    }
};

GridTab.prototype.saveRow = function() {
    var memberInfo = {};
    var that = this;
    if (!this.memberId) {
        return;
    }
    $.get('/members/tab/' + this.memberId, function (data) {
        memberInfo = data;
        if (that.endEditing(that.$grid)) {
            memberInfo[that.tabId] = that.$grid.datagrid('getRows');
            $.ajax({
                url: '/members/' + memberInfo._id,
                type: 'PUT',
                data: JSON.stringify(memberInfo),
                success: function (data) {
                    //删除成功以后，重新加载数据，并将choiceRows置为空。
                    $.messager.alert('提示', '数据保存成功!', 'info');
                },
                error: function (data) {
                    $.messager.alert('提示', '数据更新失败!', 'error');
                }
            });
        }
    });
};

GridTab.prototype.buildGrid = function(columns, toolbar) {
    var height = $("#member-info").height();
    var that = this;
    this.$grid.datagrid({
        iconCls: 'icon-ok',
        height: height,
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
        columns: columns,
        onClickRow: function(index, row) {
            if (that.editIndex != index) {
                if (that.endEditing()) {
                    that.$grid.datagrid('selectRow', index)
                        .datagrid('beginEdit', index);
                    that.editIndex = index;
                } else {
                    that.$grid.datagrid('selectRow', that.editIndex);
                }
            }
        },
        onBeginEdit: function(index, row) {
            $(".combo").click(function () {
                $(this).prev().combobox("showPanel");
            });
        },
        onSelect: function(title, index) {
            selectedTabId = that.tabId;
            that.reloadGrid();
        }
    });
};

GridTab.prototype.reloadGrid(clear) = function() {
    var that = this;
    if (clear) {
        this.$grid.datagrid('loadData', []);
    }
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

GridTab.prototype.registerListeners = function() {
    var that = this;
    window.addEventListener("grid-row-selection", function (event) {
        that.memberId = event.detail;
        if (selectedTabId == that.tabId) { // 仅更新在前端显示的Tab内容
            that.reloadGrid();
        }
    });
    window.addEventListener("grid-row-deleteRow", function (event) {
        if (event.detail.success == true) {
            that.reloadGrid(true);
        }
    });
    window.addEventListener("tree-row-selection", function (event) {
        that.reloadGrid(true);
    });
}
