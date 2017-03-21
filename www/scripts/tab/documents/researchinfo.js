/**
 * Created by S on 2017/2/21.
 */

// 调研报告
$(function () {
    var tabId = 'researchReport';
    var $grid = $("#research-report");
    var docType = "researchReport";
    var gridTab = new GridTab(tabId, $grid, docType);
    var columns = [
        {
            field: 'fileUploadTime',
            title: '上传时间',
            width: 80,
            align: 'left',
            editor: {type: 'datetimebox', options: {}}
        }, {
            field: 'fileName',
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
                var path = "/document/" + row._id + "/" + row.fileName;
                return '<a href= ' + path + ' >下载</a>';
            }
        }
    ];
    var toolbar = [{
        text: '调研报告上传',
        iconCls: 'icon-import',
        handler: function () {
            gridTab.docUpload()
        }
    }, '-', {
        text: '文档删除',
        iconCls: 'icon-cancel',
        handler: function () {
            gridTab.docDelete()
        }
    }];
    gridTab.buildDocGrid(toolbar, columns);
    gridTab.registerListeners();
});