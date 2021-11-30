$('#table').bootstrapTable({
    columns: [{
        field: 'id',
        title: 'ID',
        formatter:idForm,
        width:'25%'
    }, {
        field: 'name',
        title: '名字',
        width:'25%',
        formatter:nameForm,
    }, {
        field: 'price',
        title: '价格',
        width:'25%',
        formatter:priceForm
    }, {
        field:'id',
        title: '操作',
        width:'25%',
        formatter:doSome
    },],
    data:[]
});
//input输入框
function priceForm(value,row,index){
    return ['<input type="text" id="1plan'+row.id+'" data='+value+' value='+value+' onblur="addTarget('+row.id+',1)">'].join("")
}
//下拉列表
function nameForm(value,row,index){
    return `
            <select id="sele`+ row.id +`" onchange="selectchange(`+ row.id +`)" class="ss">
                <option value="1">item1</option>
                <option value="2">item2</option>
                <option value="3">item3</option>
                <option value="4">item4</option>
            </select>
        `
}

function add(){
    var count = $('#table').bootstrapTable('getData').length;

    
    $('#table').bootstrapTable('insertRow',{index:count,row: {
        id:count+1,
        name:'',
        price:'2'
    }});
}
//id:这条数据的id  type :1,2,3:代表的是第几个目标值
function addTarget(id,type){
    var writevalue=$("#"+type+"plan"+id).val(); //获取改变后的输入框的值
    var oldvalue = $("#"+type+"plan"+id).attr("data"); //获取输入框原本的值
    
    if(!(writevalue==oldvalue)){//通过判断输入框的值是否改变，是否写入jsontarget改变的json数据
        oldvalue=writevalue;
        $("#"+type+"plan"+id).attr("data",oldvalue);
        writeJson(id,type,writevalue);
    }

}

//修改指定单元格值
function writeJson(id,type,writevalue){
    var counts = $('#table').bootstrapTable('getData');

    for(var i = 0;i<counts.length;i++){
        if(counts[i].id == id){
            $('#table').bootstrapTable('updateCell',{
                index:i,
                field:'price',
                value:writevalue
            })
        }
    }
}

BootstrapTable.prototype.insertRow = function (params) {
    if (!params.hasOwnProperty('index') || !params.hasOwnProperty('row')) {
        return;
    }
    this.options.data.splice(params.index, 0, params.row);
    this.initSearch();
    this.initPagination();
    this.initSort();
    this.initBody(true);
};

function reloadSlect(){
    //将表内数据遍历，在数据修改导致重置后，遍历和表内数据，
    //重新修改option的selected属性
    var counts = $('#table').bootstrapTable('getData');

    counts.forEach(function(item){

        var options = $("#sele"+ item.id + " option");
        var name = item.name;
        for(var j = 0;j<options.length;j++){
            options.eq(j).removeAttr("selected");
            if(options.eq(j).val() == name){
                options.eq(j).attr("selected","selected");
            }
        }
    })

}
