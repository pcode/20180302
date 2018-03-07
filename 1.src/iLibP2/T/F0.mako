<%inherit file="/T/page_base.html"/>
<%block name="head_script">
    <script >
        //编辑用
        var vm = null;
        //搜索用
        var vm_s = null;
         //表格事件
        window.table_events = {
            //更新操作
            'click .updatebtn': function(e, value, row, index) {
                table_row_edit(e, value, row, index)
            },
            //删除操作
            'click .delbtn': function(e, value, row, index) {
               table_row_del(e,value,row,index);
            }
        };

        //处理ui事件
        function doaction(e){
            //获取事件命令对象
            var cmd = e.currentTarget.attributes['rel-cmd'].nodeValue;
            //处理显示搜索界面
            if(cmd=="search"){
                showDiv("#searchDiv",'640px','240px');
            }
            if(cmd=="dosearch"){
                refresh();
            }
            //处理新建
            if(cmd=="new"){
                vm.row.cmd="add";
                vm.row.funno = "";
                vm.row.funname = "";
                showDiv("#dataDiv","640px",'240px')
            }
            //实际执行的save操作
            if(cmd=="save"){
                $.post("/${fn}/ajax", vm.row, function (r) {refresh();}, "json");
            }
            //清理界面
            if(cmd=="clear"){
                layer.closeAll();
            }
            //显示导入
            if(cmd=="import"){
                showDiv("#importDiv","640px","240px");
            }
            //导出
            if(cmd=="export"){
                vm_s.row.cmd ='export';
                layer.load(0,{shade: [0.3,'#000']}); //0代表加载的风格，支持0-2
                $.post("/${fn}/ajax",vm_s.row,function(r){
                    if (r.result=="OK") {
                        window.location.href = r.filename;
                    }else {alert("导出数据失败,请稍后再试！");}
                    layer.closeAll();
                },'json')
            }
        }

        //刷新数据
        function refresh(){
            $("#the_data").bootstrapTable('refresh', {query:vm_s.row});
            layer.closeAll();
        }
        //表格查询参数适配
        function getParams(params){
            op = params;
            params =  vm_s.row;
            params.pageindex = op.offset / op.limit+1;
            params.pagesize = op.limit;
            return params;
        }
        //操作行render函数
        function table_formatter(value, row, index) {
                var fieldstr    =  '<a class="updatebtn">修改</a>';
                    fieldstr    += ' <a class="delbtn">删除</a>';
                return fieldstr
        }
        //操作行编辑
        function table_row_edit(e,value,row,index){
            row.the_id = row.id;
            row.cmd = 'edit';
            vm.row = row;
            showDiv("#dataDiv",'640px','240px')
        }
        //操作行删除
        function table_row_del(e, value, row, index){
            $.post("/F0011/ajax",{cmd:"del",id:value},function(r){ refresh();},"json")
        }
        //初始化用于编辑数据的vm
        function init_vm(){vm= new Vue({el:'#rowData',data:{row: {the_id  : '',cmd    : '',funno  : '',funname    : ''}}});}
        //初始化用于搜索的参数
        function init_vms(){vm_s= new Vue({el:'#searchform',data:{row: {funno   : '',funname: ''}}});}
        function init_table(){
            //初始化表格
            $('#the_data').bootstrapTable({
                    url             : "/${fn}/ajax",
                    queryParams     : getParams,
                    toolbar         : "#toolbar",
                    showColumns     : true,
                    striped         : true,
                    sidePagination  : "server",
                    pagination      : "true",
                    pageSize        : 20,
                    pageList        : [20, 50, 100, 500],
                    uniqueId        : "id"});
        }

        function init_btn_opt(){
            $(".optbtn").click(doaction);
        }
        function init_option_style(){
            $(".i-checks").iCheck({checkboxClass:"icheckbox_square-green",radioClass:"iradio_square-green"});
        }
        //绑定函数
        $(function(){
            init_vm();
            init_vms();
            init_table();
            init_btn_opt();
            init_option_style();
        });
    </script>
</%block>

<%block name="main_body">
<ol class="breadcrumb">
  <li><a href="#">首页</a></li><li><a href="#">系统</a></li><li class="active">系统功能</li>
</ol>
<!--查询结果-->
<div id="toolbar" class="btn-group">
    <button rel-cmd="search"    class="btn btn-primary optbtn"><span class="glyphicon glyphicon-search">    </span>查询</button>
    <button rel-cmd="new"       class="btn btn-primary optbtn"><span class="glyphicon glyphicon-plus" >     </span>新增</button>
    <button rel-cmd="import"    class="btn btn-primary optbtn"><span class="glyphicon glyphicon-import">    </span>导入</button>
    <button rel-cmd="export"    class="btn btn-primary optbtn"><span class="glyphicon glyphicon-export">    </span>导出</button>
</div>
<!--数据主体显示-->
<table id="the_data" style="margin-bottom: 15px;">
    <thead>
    <tr>
        <th data-field="funno"          data-title="功能编号"></th>
        <th data-field="funname"        data-title="功能名称"></th>
        <th data-field="funcatalog"     data-title="功能分类"></th>
        <th data-field="funclass"       data-title="功能类别"></th>
        <th data-field="displayname"    data-title="显示名称"></th>
        <th data-field="id"             data-title="操作" data-events='table_events'  data-formatter='table_formatter' ></th>
    </tr>
    </thead>
</table>
</%block>
<%block name ="include_module">
    <%include file="F0011_1.html"/>
    <%include file="F0011_2.html"/>
    <%include file="F0011_3.html"/>
</%block>
