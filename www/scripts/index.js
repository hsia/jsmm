/**
 * Created by S on 2017/2/16.
 */
$(function(){
    var dg = $('#person-lists');

        dg.datagrid({
            iconCls: 'icon-ok',
            height: 325,
            rownumbers: true,
            pageSize: 20,
//        pageList: [10, 20, 30, 40, 50],
            nowrap: true,
            striped: true,
            //url: '/system/accountsPage',
            loadMsg: '数据装载中......',
            pagination: true,
            //idField: 'id',
            allowSorts: true,
            remoteSort: true,
            multiSort: true,
            //fitColumn: true,
            columns: [[
                {field: 'identification', hidden: true},
                {field: 'ck', checkbox: true},
                {field: 'buyerType', title: '购买方类型编码', width: 110, align: 'left', sortable: true},
                {field: 'buyerTypeName', title: '购买方类型', width: 100, align: 'left', sortable: true},
                {field: 'dataTime', title: '时间', width: 110, align: 'left', sortable: true},
                {field: 'noAgreeContent', title: '驳回内容', width: 120, align: 'left', sortable: true},
                {field: 'mineUploadName', title: '创建人', width: 80, align: 'left', sortable: true},
                {field: 'organName', title: '所属单位', width: 100, align: 'left', sortable: true},
            ]],
//        loader: function (param, success, error) {
//            var defaultUrl = '/bangDan/page';
//            var jsonResult = JSON.stringify(param);
//            $.post(defaultUrl, jsonResult, function (data) {
//                if (data.success) {
//                    utils.fastJson.format(data);
//                    success(data.data)
//                } else {
//                    utils.modal.message('create', error);
//                }
//            }, 'json');
//        },
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

})