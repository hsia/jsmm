/**
 * Created by S on 2017/2/21.
 */

// 发言稿
$(function () {

    var data_grid = $("#speeches-text");
    var docType = "speechesText";

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
        text: '信息上传',
        iconCls: 'icon-import',
        handler: function () {
            docUpload(data_grid, docType)
        }
    }, '-', {
        text: '文档删除',
        iconCls: 'icon-cancel',
        handler: function () {
            docDelete(data_grid, docType)
        }
    }];
    buildDocGrid(data_grid, toolbar, columns);
    addSelectListener(data_grid, docType);
});