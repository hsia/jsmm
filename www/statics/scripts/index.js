/**
 * Created by S on 2017/2/16.
 */
$(function () {
    $("#logout").click(function () {
        $.messager.confirm('确定', '注销当前用户？', function (r) {
            if (r) {
                window.location.href = '/logout';
            }
        });
    })

    //绑定新建支社回车提交
    $('#organNew').textbox('textbox').keydown(function (e) {
        if (e.keyCode == 13) {
            $('#organ-add-form').trigger('submit');
        }
    });
    //绑定编辑支社回车提交
    $('#organEdit').textbox('textbox').keydown(function (e) {
        if (e.keyCode == 13) {
            $('#organ-edit-form').trigger('submit');
        }
    });

    function addPageFillData() {
        $('#gender').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/gender.json',
            method: 'get'
        })
        $('#nation').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/peoples.json',
            method: 'get'
        })
        $('#health').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/health.json',
            method: 'get'
        })
        $('#marriage').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/marriage.json',
            method: 'get'
        })
        $('#idType').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/idType.json',
            method: 'get'
        })
        $('#retire').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/retire.json',
            method: 'get'
        })
        $('#sector').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/sector.json',
            method: 'get'
        })
        $('#lost').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/retire.json',
            method: 'get'
        })
        $('#stratum').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/retire.json',
            method: 'get'
        })
        $('#highestEducation').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/highestEducation.json',
            method: 'get'
        })
        $('#newBranch').combotree({
            url: '/organ',
            method: 'get'
        });
    }

    function editPageFillDataE() {
        $('#genderE').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/gender.json',
            method: 'get'
        })
        $('#nationE').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/peoples.json',
            method: 'get'
        })
        $('#healthE').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/health.json',
            method: 'get'
        })
        $('#marriageE').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/marriage.json',
            method: 'get'
        })
        $('#idTypeE').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/idType.json',
            method: 'get'
        })
        $('#retireE').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/retire.json',
            method: 'get'
        })
        $('#sectorE').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/sector.json',
            method: 'get'
        })
        $('#lostE').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/retire.json',
            method: 'get'
        })
        $('#stratumE').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/retire.json',
            method: 'get'
        })
        $('#highestEducationE').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/highestEducation.json',
            method: 'get'
        })
        $('#editBranchE').combotree({
            url: '/organ',
            method: 'get'
        });
    }

    function searchPageFillData() {
        $('#genderS').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/gender.json',
            method: 'get'
        })
        $('#sectorS').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/sector.json',
            method: 'get'
        })
        $('#highestEducationS').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/highestEducation.json',
            method: 'get'
        })
        $('#lostS').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/retire.json',
            method: 'get'
        })
        $('#stratumS').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/retire.json',
            method: 'get'
        })
        $('#socialPositionLevelS').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/socialPositionLevel.json',
            method: 'get'
        })
        $('#formeOrganizationLevelS').combobox({
            valueField: 'value',
            textField: 'text',
            url: 'static/data/formeOrganizationLevel.json',
            method: 'get'
        })
    }

    //添加组织机构数的点击后触发自定义监听事件
    branch = null;
    $('#organTree').tree({
        loader: function (param, success) {
            $.get('/organ', function (data) {
                success(data);
            });
        },
        onClick: function (node) {
            branch = node.text;
            var event = new CustomEvent("tree-row-selection", {
                detail: node.text
            });
            //获得当前tab
            var tab = $('#tabsAll').tabs('getSelected');
            var index = $('#tabsAll').tabs('getTabIndex', tab);
            // console.log(index)
            if (index == 1) {
                window.dispatchEvent(event);
            }
            //清空页签内容
            // window.dispatchEvent(eventDelete);
            // buildMemberDetails({});
            var getCurrentRows = $memberList.datagrid('options').pageSize;
            $memberList.datagrid('load', {'branch': node.text, 'page': 1, 'rows': getCurrentRows, 'flag': 'search'})
        }
    });

    //下拉框、时间框点击的时候自动下拉
    $(".combo").click(function () {
        $(this).prev().combobox("showPanel");
    });

    var getRow = '';
    var getCurrentPage = '';
    var gridHeight = ($('#members').height());
    var $memberList = $('#member-list');
    var $documentList = $('#document-list');

    //保存社员数据
    $("#member-form").submit(function (event) {
        event.preventDefault();
        var formData = $(this).serializeArray();
        var memberInfo = {};
        $.each(formData, function (index, element) {
            memberInfo[element.name] = element.value;
        });
        if (memberInfo.name == "" || memberInfo.gender == '' || memberInfo.birthday == '' || memberInfo.nativePlace == '') {
            return false;
        }
        $.post('/members/', JSON.stringify(memberInfo), function (data) {
            if (data.success == "true") {
                $('#member-dialog').dialog('close');
                $('#member-form').form('clear');
                $memberList.datagrid('reload');
                //清空页签内容
                window.dispatchEvent(eventDelete);
                // $.messager.alert('提示信息', '添加社员成功！', 'info');
            }
        })
    });

    $("#memberEdit-form").submit(function (event) {
        event.preventDefault();

        getCurrentPage = $memberList.datagrid('options').pageNumber;
        var formData = $(this).serializeArray();
        var memberInfo = {};
        $.each(formData, function (index, element) {
            memberInfo[element.name] = element.value;
        });
        if (memberInfo.name == "" || memberInfo.gender == '' || memberInfo.birthday == '' || memberInfo.nativePlace == '') {
            return false;
        }
        $.ajax({
            url: '/members/' + memberInfo._id,
            type: 'PUT',
            data: JSON.stringify(memberInfo),
            success: function (data) {
                $('#memberEdit-dialog').dialog('close');
                //删除成功以后，重新加载数据，并将choiceRows置为空。
                // console.log(getRow);
                $memberList.datagrid('gotoPage', getCurrentPage).datagrid('reload');
                //清空页签内容
                // window.dispatchEvent(eventDelete);
                // $memberList.datagrid('selectRow', getRow);
                // $.messager.alert('提示', '数据更新成功!', 'info');
            },
            error: function (data) {
                $.messager.alert('提示', '数据更新失败!', 'error');
            }
        });
    });

    var toolbar = [{
        text: '添加',
        iconCls: 'icon-add',
        handler: function () {
            addPageFillData();
            $('#member-dialog').dialog({
                width: 800,
                height: 630,
                title: '添加社员',
                closed: false,
                cache: false,
                resizable: true,
                modal: true,
                buttons: [{
                    iconCls: 'icon-save',
                    text: '保存',
                    handler: function () {
                        $('#member-form').trigger('submit');
                    }
                }, {
                    iconCls: 'icon-cancel',
                    text: '取消',
                    handler: function () {
                        $('#member-form').form('clear');
                        $('#member-dialog').dialog('close');
                    }
                }]
            });
            $('#memberAddName').next('span').find('input').focus();
        }
    }, '-', {
        text: '编辑',
        iconCls: 'icon-edit',
        handler: function () {
            editPageFillDataE();
            //后台查询需要编辑的数据的详细信息，并将返回的数据放入到memeberEdit-form中
            editInfo();
        }
    }, '-', {
        text: '删除',
        iconCls: 'icon-cancel',
        handler: function () {
            confirmRemove();
        }
    }, '-', {
        text: '高级查询',
        iconCls: 'icon-search',
        handler: function () {
            searchPageFillData();
            memberSearch();
        }
    }, '-', {
        text: '社员导入',
        iconCls: 'icon-import',
        handler: function () {
            $('#member_upload_form').form('clear');
            $('#member_upload').dialog({
                width: 300,
                height: 200,
                title: '导入社员',
                closed: false,
                cache: false,
                modal: true,
                buttons: [{
                    iconCls: 'icon-import',
                    text: '导入',
                    handler: function () {
                        uploadName = $("#memeberUploadName").filebox('getValue')
                        if (uploadName == '') {
                            $.messager.alert('提示信息', "请选择需要导入的社员信息文件！");
                            return false;
                        }
                        $('#member_upload').dialog('close');
                        $.messager.progress({
                            title: 'Please waiting',
                            msg: 'Loading data...'
                        });
                        $('#member_upload_form').form('submit', {
                            success: function (data) {
                                var member = JSON.parse(data);
                                $memberList.datagrid('reload');
                                if (member.success == false && ('name' in member.msg[0])) {
                                    var error_members = "<b>以下社员导入失败(姓名和出生日期重复):</b><br/>";
                                    member.msg.forEach(function (obj) {
                                        error_members += obj.name + "【" + obj.birthday + "】<br/>"
                                    });
                                    // $memberList.datagrid('reload');
                                    $.messager.progress('close');
                                    $.messager.alert('提示信息', error_members);
                                } else if (member.success == false && ('content' in member.msg[0])) {
                                    var error_members = "<b>以下导入文件内容错误，请检查:</b><br/>";
                                    member.msg.forEach(function (obj) {
                                        error_members += obj.content + "<br/>"
                                    });
                                    // $memberList.datagrid('reload');
                                    $.messager.progress('close');
                                    $.messager.alert('提示信息', error_members);
                                } else if (member.success == false && ('filename' in member.msg[0])) {
                                    var error_members = "<b>以下导入文件类型错误，只能导入Excel:</b><br/>";
                                    member.msg.forEach(function (obj) {
                                        error_members += obj.filename + "<br/>"
                                    });
                                    // $memberList.datagrid('reload');
                                    $.messager.progress('close');
                                    $.messager.alert('提示信息', error_members);
                                } else if (member.success == false && ('filecontent' in member.msg[0])) {
                                    var error_members = "<b>以下Excel文件内容不符合要求(年龄和生日不能为空)，请检查！</b><br/>";
                                    member.msg.forEach(function (obj) {
                                        error_members += obj.filecontent + "<br/>"
                                    });
                                    // $memberList.datagrid('reload');
                                    $.messager.progress('close');
                                    $.messager.alert('提示信息', error_members);
                                } else {
                                    // $memberList.datagrid('reload');
                                    $.messager.progress('close');
                                    // $.messager.alert('提示信息', '导入社员成功！', 'info');
                                }
                            }
                        });
                    }
                }, {
                    iconCls: 'icon-cancel',
                    text: '取消',
                    handler: function () {
                        $('#member_upload_form').form('clear');
                        $('#member_upload').dialog('close');
                    }
                }]
            })
            // $('#tab_title').next('span').find('input').focus();
        }
    }
        // , '-', {
        //     text: '提醒',
        //     iconCls: 'icon-clock',
        //     handler: function () {
        //         reminderBirthday();
        //     }
        //
        // }
        , '-', {
            text: '社员导出',
            iconCls: 'save-excel',
            handler: function () {
                exportMembersExcel();
            }
        }, '-', {
            text: '新建自定义tab',
            iconCls: 'icon-add',
            handler: function () {
                client_add_tab();
            }
        }, '-', {
            text: '编辑自定义tab',
            iconCls: 'icon-add',
            handler: function () {
                client_edit_tab();
            }
        }];

    var defaultUrl = '/members2/';

    $memberList.datagrid({
        iconCls: 'icon-ok',
        height: gridHeight,
        rownumbers: true,
        pageSize: 10,
        nowrap: true,
        striped: true,
        fitColumns: true,
        loadMsg: '数据装载中......',
        pagination: true,
        allowSorts: true,
        multiSort: false,
        singleSelect: true,
        toolbar: toolbar,
        remoteSort: false,
        // url: defaultUrl,
        // method: 'GET',
        columns: [[
            {field: '_id', hidden: true},
            {field: '_rev', hidden: true},
            {
                field: 'name', title: '姓名', width: 110, sortable: true, align: 'left',
                sorter: function (a, b) {
                    return makePy(a)[0] > makePy(b)[0] ? 1 : -1
                }
            },
            {field: 'gender', title: '性别', width: 50, sortable: true, align: 'left',},
            {field: 'birthday', title: '出生日期', width: 120, sortable: true, align: 'left'},
            {field: 'nation', title: '民族', width: 120, sortable: true, align: 'left'},
            {field: 'idCard', title: '身份证号', width: 120, sortable: true, align: 'left'},
            {field: 'branch', title: '所属支社', width: 120, sortable: true, align: 'left'},
            {field: 'organ', title: '所属基层组织', width: 120, sortable: true, align: 'left'},
            {field: 'branchTime', title: '入社时间', width: 120, sortable: true, align: 'left'}
        ]],
        loader: function (param, success) {
            $.get(defaultUrl, param, function (data) {
                success(data);
            });
            //清空选中社员信息
            window.dispatchEvent(new CustomEvent("grid-dg-refresh", {
                detail: {success: true}
            }));
            //清空页签内容
            window.dispatchEvent(new CustomEvent("grid-row-deleteRow", {
                detail: {success: true}
            }));
            //清空社员详情内容
            buildMemberDetails({});
        },
        loadFilter: function (data) {
            //清空选中社员信息
            window.dispatchEvent(new CustomEvent("grid-dg-refresh", {
                detail: {success: true}
            }));
            //清空页签内容
            window.dispatchEvent(new CustomEvent("grid-row-deleteRow", {
                detail: {success: true}
            }));
            //清空社员详情内容
            buildMemberDetails({});
            if (typeof data.length == 'number' && typeof data.splice == 'function') {
                data = {
                    total: data.length,
                    rows: data
                }
            }
            var opts = $memberList.datagrid('options');
            var pager = $memberList.datagrid('getPager');
            pager.pagination({
                onSelectPage: function (pageNum, pageSize) {
                    opts.pageNumber = pageNum;
                    opts.pageSize = pageSize;
                    pager.pagination('refresh', {
                        pageNumber: pageNum,
                        pageSize: pageSize
                    });
                    $memberList.datagrid('loadData', data);
                }
            });
            if (!data.originalRows) {
                data.originalRows = (data.rows);
            }
            var start = (opts.pageNumber - 1) * parseInt(opts.pageSize);
            var end = start + parseInt(opts.pageSize);
            data.rows = (data.originalRows.slice(start, end));
            return data;
        },
        onSelect: function (rowIndex, rowData) {
            getRow = rowIndex;
            var memberId = rowData._id;
            $.get('/members/' + memberId).done(function (data) {
                if (!$.isEmptyObject(data)) {
                    buildMemberDetails(data);
                    $("#create_file").change(function () {
                        $('#member_image_upload').form('submit', {
                            success: function (data) {
                                var result = eval('(' + data + ')');
                                $('#member_image').attr('src', 'static/image/' + result.fileName);
                                $('#upload').val('');
                            }
                        });
                    });
                    var event = new CustomEvent("grid-row-selection", {
                        detail: data
                    });
                    window.dispatchEvent(event);
                }
            });
        }
    });

    function refreshDocumentListEvent() {
        var event = new CustomEvent("organ-tree-operation", {});
        window.dispatchEvent(event);
    }

    //自定义event，用来清空页签中的数据
    var eventDelete = new CustomEvent("grid-row-deleteRow", {
        detail: {success: true}
    });

    function pinyinSort(py1, py2) {
        pyjx1 = makePy(py1)[0];
        pyjx2 = makePy(py2)[0];
        console.log(pyjx1 + ' > ' + pyjx2 + ' = ' + pyjx1 > pyjx2);
    }


    //社员信息详情
    function buildMemberDetails(rowData) {
        var html = `
<div class="member-detail">
    <div class="member-picture">
        <img id="member_image" src="${rowData.picture || 'static/image/deaulf.jpg'}" style="width:100%;">
        <form id="member_image_upload" action='/image/upload/' enctype="multipart/form-data" method='post'>
            <input id="create_file" type="file" name="picture" accept="image/*" style="width:100%">
            <input id="create_file" type="hidden" name="picture_id" value="${rowData._id}">
        </form>      
    </div>
    
    <div class="member-column">
        <div class="member-item"><span class="member-item-title">外文姓名: </span>${rowData.foreignName || ""}</div>
        <div class="member-item"><span class="member-item-title">曾用名: </span>${rowData.usedName || ""}</div>
        <div class="member-item"><span class="member-item-title">籍贯: </span>${rowData.nativePlace || ""}</div>
        <div class="member-item"><span class="member-item-title">出生地: </span>${rowData.birthPlace || ""}</div>
        <div class="member-item"><span class="member-item-title">健康状态: </span>${rowData.health || ""}</div>
        <div class="member-item"><span class="member-item-title">婚姻状况: </span>${rowData.marriage || ""}</div>
        <div class="member-item"><span class="member-item-title">有效证件类别: </span>${rowData.idType || ""}</div>
        <div class="member-item"><span class="member-item-title">证件号码: </span>${rowData.idNo || ""}</div>
        <div class="member-item"><span class="member-item-title">移动电话: </span>${rowData.mobile || ""}</div>
        <div class="member-item"><span class="member-item-title">界别: </span>${rowData.sector || ""}</div>
        <div class="member-item"><span class="member-item-title">职务级别: </span>${rowData.jobLevel || ""}</div>
    </div>
    <div class="member-column">
        <div class="member-item"><span class="member-item-title">党派交叉: </span>${rowData.partyCross || ""}</div>
        <div class="member-item"><span class="member-item-title">单位名称: </span>${rowData.companyName || ""}</div>
        <div class="member-item"><span class="member-item-title">参加工作时间: </span>${rowData.jobTime || ""}</div>
        <div class="member-item"><span class="member-item-title">工作部门: </span>${rowData.department || ""}</div>
        <div class="member-item"><span class="member-item-title">办理退休手续: </span>${rowData.retire || ""}</div>
        <div class="member-item"><span class="member-item-title">职务: </span>${rowData.duty || ""}</div>
        <div class="member-item"><span class="member-item-title">职称: </span>${rowData.jobTitle || ""}</div>
        <div class="member-item"><span class="member-item-title">学术职务: </span>${rowData.academic || ""}</div>
        <div class="member-item"><span class="member-item-title">电子邮箱: </span>${rowData.email || ""}</div>
        <div class="member-item"><span class="member-item-title">是否失联: </span>${rowData.lost || ""}</div>
        <div class="member-item"><span class="member-item-title">职称级别: </span>${rowData.titleLevel || ""}</div>
    </div>
    <div class="member-column">
        <div class="member-item"><span class="member-item-title">家庭地址: </span>${rowData.homeAddress || ""}</div>
        <div class="member-item"><span class="member-item-title">家庭地址邮编: </span>${rowData.homePost || ""}</div>
        <div class="member-item"><span class="member-item-title">家庭电话: </span>${rowData.homeTel || ""}</div>
        <div class="member-item"><span class="member-item-title">公司地址: </span>${rowData.companyAddress || ""}</div>
        <div class="member-item"><span class="member-item-title">公司邮编: </span>${rowData.companyPost || ""}</div>
        <div class="member-item"><span class="member-item-title">单位电话: </span>${rowData.companyTel || ""}</div>
        <div class="member-item"><span class="member-item-title">通信地址: </span>${rowData.commAddress || ""}</div>
        <div class="member-item"><span class="member-item-title">通信地址邮编: </span>${rowData.commPost || ""}</div>
        <div class="member-item"><span class="member-item-title">爱好: </span>${rowData.hobby || ""}</div>
        <div class="member-item"><span class="member-item-title">新阶层: </span>${rowData.stratum || ""}</div>
        <div class="member-item"><span class="member-item-title">最高学历: </span>${rowData.highestEducation || ""}</div>
    </div>
</div>
`;
        $('#member-info').html(html);
    }

    //编辑数据
    function editInfo() {
        //1、先判断是否有选中的数据行
        var $member = $memberList.datagrid('getSelected');
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
                    resizable: true,
                    modal: true,
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
                $('#memberEditName').next('span').find('input').focus();
            } else {
                $.messager.alert('提示', '数据请求失败!', 'error');
            }
        })
    }

    //确认删除
    function confirmRemove() {
        //1、先判断是否有选中的数据行
        var member = $memberList.datagrid('getSelected');
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
                $memberList.datagrid('reload');

                // window.dispatchEvent(eventDelete);

                // buildMemberDetails({});

                // $.messager.alert('提示', '数据删除成功!', 'info');
            },
            error: function (data) {
                $.messager.alert('提示', '数据删除失败!', 'error');
            }
        });
    }

    $("#member-search-form").submit(function (event) {
        event.preventDefault();
        var formData = $(this).serializeArray();
        var memberInfo = {};
        $.each(formData, function (index, element) {
            memberInfo[element.name] = element.value;
        });

        var $start_age = $('#start_age').val();
        var $end_age = $('#end_age').val();
        if ($start_age != '' && $end_age != '') {
            memberInfo['startAge'] = moment().subtract($start_age, 'y').format("YYYY-MM-DD");
            memberInfo['endAge'] = moment().subtract($end_age, 'y').format("YYYY-MM-DD");
        }
        memberInfo.branch = (branch == null ? '' : branch);
        var getCurrentRows = $memberList.datagrid('options').pageSize;

        memberInfo.page = 1;
        memberInfo.rows = getCurrentRows;
        memberInfo.flag = 'search'
        // $.post('/members/search/', JSON.stringify(memberInfo), function (data) {
        //     $('#member-search').dialog('close');
        //
        //     $memberList.datagrid('loadData', data.docs);
        //
        // })

        $memberList.datagrid('load', memberInfo)
        //清空页签内容
        // window.dispatchEvent(eventDelete);
        // buildMemberDetails({});
        $('#member-search').dialog('close');
    });

    function memberSearch() {
        $('#member-search-form').form('clear');
        $('#member-search').dialog({
            width: 600,
            height: 450,
            title: '社员查询',
            closed: false,
            cache: false,
            modal: true,
            buttons: [{
                iconCls: 'icon-ok',
                text: '查询',
                handler: function () {
                    $('#member-search-form').trigger('submit');
                }
            }, {
                iconCls: 'icon-cancel',
                text: '取消',
                handler: function () {
                    $('#member-search-form').form('clear');
                    $('#member-search').dialog('close');
                }
            }]
        });
        $('#memberSearchName').next('span').find('input').focus();
    }

    //添加tab页
    function client_add_tab() {
        var gridHeight = ($("#member-info").height()) + 77;
        $("#tab_title").textbox('setValue', '');
        $('#client_add_tab_table').datagrid('loadData', []);
        $('#client_add_tab').dialog({
            title: '新建自定义tab',
            closed: false,
            cache: false,
            modal: true,
            height: gridHeight
        })
    }

    choiceNode = '';
    //编辑tab页
    function client_edit_tab() {
        $('#client_edit_tab_table').datagrid('loadData', []);
        var gridHeight = ($("#member-info").height()) + 77;
        $('#tab_edit_title').combotree({
            url: '/tabcombtree/',
            method: 'get',
            onSelect: function (node) {
                choiceNode = node;
                console.log(node.id + ':' + node.text)
                $('#client_edit_tab_table').datagrid({
                    loader: function (param, success) {
                        var defaultUrl = '/tabcombtree/' + node.id;
                        $.get(defaultUrl, function (data) {
                            success(data.columns)
                        }, 'json');
                    },
                })
            }
        })
        $('#client_edit_tab').dialog({
            title: '编辑自定义tab',
            closed: false,
            cache: false,
            modal: true,
            height: gridHeight
        })
    }

// function reminderBirthday() {
//     $('#reminder_dialog').dialog({
//         title: '提醒',
//         closed: false,
//         cache: false,
//         modal: true,
//         height: 200,
//         width: 200
//     })
// }
//
// $('#reminder_birthday').click(function () {
//     var now = moment().format("M-D");
//     var end = moment().add(7, 'd').format("M-D");
//     $.get('/members/?startTime=' + now + '&endTime=' + end, function (data) {
//         $memberList.datagrid('loadData', data);
//         $('#reminder_dialog').dialog("close")
//     });
// });
//
// $('#reminder_retire').click(function () {
//    var now = moment().format("YYYY-MM-DD");
//     $.get('/members/reminder/' + now,function (data) {
//         $memberList.datagrid('loadData', data.docs);
//         $('#reminder_dialog').dialog("close")
//     })
// });

    $('#retire_time_div').click(function () {
        var now = moment().format("YYYY-MM-DD");
        $('#retire_time_input').textbox("setValue", now);
    });

    function exportMembersExcel() {
        $('#members_export_excel').dialog({
            title: '社员导出',
            closed: false,
            cache: false,
            modal: true,
            height: 150,
            width: 200
        })
    }

    $('#memberInfo_export').click(function () {
        var member = $memberList.datagrid('getSelected');
        if (member == null) {
            $.messager.alert('提示', '请选择需要导出的社员!', 'error');
            return;
        }
        window.location.href = '/member/export/' + member._id;
        $('#members_export_excel').dialog('close');
    });

    $('#memberInfo_cus_export').click(function () {
        var member = $memberList.datagrid('getSelected');
        if (member == null) {
            $.messager.alert('提示', '请选择需要导出的社员!', 'error');
            return;
        }
        window.location.href = '/member/export/' + member._id + '?cus = cus';
        $('#members_export_excel').dialog('close');
    });

    $('#members_export').click(function () {
        var formData = $("#member-search-form").serializeArray();
        var memberInfo = {};
        $.each(formData, function (index, element) {
            memberInfo[element.name] = element.value;
        });

        var $start_age = $('#start_age').val();
        var $end_age = $('#end_age').val();
        if ($start_age != '' && $end_age != '') {
            memberInfo['startAge'] = moment().subtract($start_age, 'y').format("YYYY-MM-DD");
            memberInfo['endAge'] = moment().subtract($end_age, 'y').format("YYYY-MM-DD");
        }
        memberInfo.branch = (branch == null ? '' : branch);

        window.location.href = '/member/information/' + JSON.stringify(memberInfo)
        $('#members_export_excel').dialog('close');
    });

// $('#reminder_retire').click(function () {
//     var now = moment().format("YYYY-MM-DD");
//     $.get('/members/reminder/' + now, function (data) {
//         $memberList.datagrid('loadData', data.docs);
//         $('#reminder_dialog').dialog("close")
//     })
// });

//新建支社
    $('#newOrgan').click(function () {
        $('#organ-add').dialog({
            width: 300,
            height: 150,
            title: '新建支社',
            closed: false,
            cache: false,
            modal: true,
            buttons: [{
                iconCls: 'icon-ok',
                text: '确定',
                handler: function () {
                    $('#organ-add-form').trigger('submit');
                }
            }, {
                iconCls: 'icon-cancel',
                text: '取消',
                handler: function () {
                    $('#organ-add-form').form('clear');
                    $('#organ-add').dialog('close');
                }
            }]
        });
        $('#organNew').next('span').find('input').focus();

    });

    $("#organ-add-form").submit(function (event) {
        event.preventDefault();
        var formData = $(this).serializeArray();
        if (formData[0].value == '') {
            // $.messager.alert('提示', '请输入组织机构名称!', 'info');
            return false;
        }

        $.ajax({
            url: '/organ/' + formData[0].value,
            type: 'PUT',
            success: function (data) {
                //删除成功以后，重新加载数据，并将choiceRows置为空。
                if (data.success) {
                    $('#organ-add').dialog('close');
                    $('#organ-add-form').form('clear');

                    $('#organTree').tree('loadData', data.content);
                    // $.messager.alert('提示', '新建支社成功!', 'info');
                    //重新加载会员列表/文档列表
                    var getCurrentRows = $memberList.datagrid('options').pageSize;
                    $memberList.datagrid('load', {
                        'page': 1,
                        'rows': getCurrentRows,
                    })
                    //清空页签内容
                    // window.dispatchEvent(eventDelete);
                    refreshDocumentListEvent();
                } else {
                    $.messager.alert('提示', data.content, 'warning');
                }
            },
            error: function (data) {
                $.messager.alert('提示', '新建支社失败!', 'error');
            }
        });
    });

//编辑支社
    $('#editOrgan').click(function () {
        var node = $('#organTree').tree('getSelected');
        if (node == null) {
            $.messager.alert('提示', '请选择需要编辑的数据!', 'error');
            return;
        } else if (node.text == '北京市' || node.text == '朝阳区') {
            $.messager.alert('提示', '该数据不能修改，请选择支社数据进行修改!', 'warning');
            return;
        } else {
            $('#organ-edit-form').form('load', {organName: node.text})
        }

        $('#organ-edit').dialog({
            width: 300,
            height: 150,
            title: '编辑支社',
            closed: false,
            cache: false,
            modal: true,
            buttons: [{
                iconCls: 'icon-ok',
                text: '确定',
                handler: function () {
                    $('#organ-edit-form').trigger('submit');
                }
            }, {
                iconCls: 'icon-cancel',
                text: '取消',
                handler: function () {
                    $('#organ-edit-form').form('clear');
                    $('#organ-edit').dialog('close');
                }
            }]
        });
        $('#organEdit').next('span').find('input').focus();
    })

    $("#organ-edit-form").submit(function (event) {
        event.preventDefault();
        var node = $('#organTree').tree('getSelected');
        var formData = $(this).serializeArray();
        if (formData[0].value == '') {
            // $.messager.alert('提示', '请输入组织机构名称!', 'info');
            return false;
        }

        $.ajax({
            url: '/organ/update/' + node.id + '/' + formData[0].value,
            type: 'PUT',
            success: function (data) {
                if (data.success) {
                    $('#organ-edit').dialog('close');
                    $('#organ-edit-form').form('clear');
                    //修改成功以后，重新加载数据，并将choiceRows置为空。
                    $('#organTree').tree('loadData', data.content);
                    //重新加载会员列表/文档列表
                    var getCurrentRows = $memberList.datagrid('options').pageSize;
                    $memberList.datagrid('load', {
                        'page': 1,
                        'rows': getCurrentRows,
                    })
                    //清空页签内容
                    // window.dispatchEvent(eventDelete);
                    refreshDocumentListEvent();

                    // $.messager.alert('提示', '修改支社成功!', 'info');
                } else {
                    $.messager.alert('提示', data.content, 'warning');
                }

            },
            error: function (data) {
                $.messager.alert('提示', '修改支社失败!', 'error');
            }
        });
    });

//合并支社
    $('#mergeOrgan').click(function () {

        // $('#mergeBranch').combotree({
        //     url: '/organ',
        //     method: 'get',
        //     required: true
        // });

        // $('#mergeBranch').combotree('reload')
        $('#mergeBranch').combotree({
            url: '/organ',
            method: 'get'
        });
        $('#mergeBranch').textbox('textbox').focus()
        var node = $('#organTree').tree('getSelected');
        if (node == null) {
            $.messager.alert('提示', '请选择需要合并的支社!', 'error');
            return;
        } else if (node.text == '北京市' || node.text == '朝阳区') {
            $.messager.alert('提示', '该数据不能合并，请选择支社数据进行合并!', 'warning');
            return;
        }
        $('#organ-merge').dialog({
            width: 300,
            height: 150,
            title: '合并支社',
            closed: false,
            cache: false,
            modal: true,
            buttons: [{
                iconCls: 'icon-ok',
                text: '确定',
                handler: function () {
                    $.messager.confirm('合并提示', '合并后原有支社的所有人员自动转到目标支社，确定吗？', function (r) {
                        if (r) {
                            $('#organ-merge-form').trigger('submit');
                        }
                    });
                }
            }, {
                iconCls: 'icon-cancel',
                text: '取消',
                handler: function () {
                    $('#organ-merge-form').form('clear');
                    $('#organ-merge').dialog('close');
                }
            }]
        });
        $('#mergeBranch').next('span').find('input').focus();
    })

    $("#organ-merge-form").submit(function (event) {
        event.preventDefault();
        var node = $('#organTree').tree('getSelected');
        var formData = $(this).serializeArray();
        if (formData[0].value == '') {
            // $.messager.alert('提示', '请输入组织机构名称!', 'info');
            return false;
        }
        if (node.id == formData[0].value) {
            $.messager.alert('提示', '选择的目标支社和原支社相同，请选择不同的支社!', 'warning');
            return false;
        }

        $('#organ-merge').dialog('close');
        $('#organ-merge-form').form('clear');
        $.ajax({
            url: '/organ/merge/' + node.id + '/' + formData[0].value,
            type: 'PUT',
            success: function (data) {
                //删除成功以后，重新加载数据，并将choiceRows置为空。
                $('#organTree').tree('loadData', data);
                //重新加载会员列表/文档列表
                var getCurrentRows = $memberList.datagrid('options').pageSize;
                $memberList.datagrid('load', {
                    'page': 1,
                    'rows': getCurrentRows,
                })
                //清空页签内容
                // window.dispatchEvent(eventDelete);
                refreshDocumentListEvent();

                // $.messager.alert('提示', '支社合并成功!', 'info');
            },
            error: function (data) {
                $.messager.alert('提示', '修改合并失败!', 'error');
            }
        });
    });

//删除支社
    $('#deleteOrgan').click(function () {
        //1、先判断是否有选中的数据行
        var node = $('#organTree').tree('getSelected');
        if (node == null) {
            $.messager.alert('提示', '请选择需要删除的数据!', 'error');
            return;
        } else if (node.text == '北京市' || node.text == '朝阳区') {
            $.messager.alert('提示', '该数据不能删除，请选择支社数据进行删除!', 'warning');
            return;
        }
        //2、将选中数据的_id放入到一个数组中
        var id = node.id;
        //3、提示删除确认
        $.messager.confirm('删除提示', '确定删除选中的数据?', function (r) {
            if (r) {
                //4、确认后，删除选中的数据
                removeOrgan(id)
            }
        });
    })

//删除数据行
    function removeOrgan(id) {
        $.ajax({
            url: '/organ/' + id,
            type: 'DELETE',
            success: function (data) {
                if (data.success) {
                    //删除成功以后，重新加载数据。
                    $('#organTree').tree('loadData', data.content);
                    //重新加载会员列表/文档列表
                    var getCurrentRows = $memberList.datagrid('options').pageSize;
                    $memberList.datagrid('load', {
                        'page': 1,
                        'rows': getCurrentRows,
                    })
                    refreshDocumentListEvent();
                    // $.messager.alert('提示', '支社删除成功!', 'info');
                } else {
                    $.messager.alert('提示', data.content, 'warning');
                }

            },
            error: function (data) {
                $.messager.alert('提示', '支社删除失败!', 'error');
            }
        });
    }

//修改密码
    $('#mod-passwd').click(function () {
        console.log($('#usernamehide').html())
        $("#userNameId").textbox('setValue', $('#usernamehide').html());
        $('#userNameId').textbox('textbox').attr('readonly', true);
        $('#password-modified').dialog({
            width: 300,
            height: 230,
            title: '修改密码',
            closed: false,
            cache: false,
            modal: true,
            buttons: [{
                iconCls: 'icon-ok',
                text: '确定',
                handler: function () {
                    passwordModified();
                }
            }, {
                iconCls: 'icon-cancel',
                text: '取消',
                handler: function () {
                    $('#password-form').form('clear');
                    $('#password-modified').dialog('close');
                }
            }]
        });
    });

    function passwordModified() {
        var formData = $("#password-form").serializeArray();
        var userInfo = {};
        $.each(formData, function (index, element) {
            userInfo[element.name] = element.value;
        });

        if (userInfo.username == "" || userInfo.oldPassword == '' || userInfo.newPassword == '' || userInfo.newPasswordSecond == '') {
            return false;
        }

        $.post("/user/", JSON.stringify(userInfo), function (data) {
            if (data.success) {
                $('#password-modified').dialog('close');
                $.messager.alert('提示', '修改密码成功,请重新登录！', 'info', function () {
                    window.location.href = '/logout'
                });
                $('#password-form').form('clear');
            } else if (!data.success) {
                $.messager.alert('提示', data.content, 'error');
            } else {
                $.messager.alert('提示', "修改密码失败", 'error');
            }
        })
    }

})
;