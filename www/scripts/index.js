/**
 * Created by S on 2017/2/16.
 */
$(function(){

    function getData(){
			var rows = [];
            $.get('/members',function(data){
                for(var i=0;i<data.length;i++){
                    rows.push({
                        id:data[i]._id,
                        rev:data[i]._rev,
                        name:data[i].name,
                        age:data[i].age
                    });
                }
            });
			return rows;
		};
    var gridHeight = ($('#persons').height());
    var dg = $('#person-lists');
        dg.datagrid({
            iconCls: 'icon-ok',
            height: gridHeight,
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
                {field: 'id', hidden: true},
                {field: 'rev', checkbox: true},
                {field: 'name', title: '姓名', width: 110, align: 'left', sortable: true},
                {field: 'age', title: '年龄', width: 100, align: 'left', sortable: true},

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