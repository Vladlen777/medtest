$(function(){
  var url = '/lisa/calculator/rule/?id=';
  var cc = $('#scheme');
  var cr = $('#rule');
	cr.combobox({
		valueField: 'ID',
		textField: 'NAME',
		method: 'GET',
		editable: false
	});
    function rule_refresh(url){
/*		$.get(url, function(jdata){
//			$("#test1").text(jdata);
			$('#rule').combobox({
				data: JSON.parse(jdata)
			});
			$('#rule').combobox('setValue', '1');
		});*/
/*		$('#rule').combobox('options').method = 'GET';
		$('#rule').combobox('reload', url);*/
		/*$('#rule').combobox({
			valueField: 'ID',
			textField: 'NAME',
			method: 'GET',
			url: url, //'@Url.Action(url,"WidgetFeatures")'
			editable: false
		});*/
		cr.combobox('reload', url);
//		first = cr.combobox('getData')[0]['ID'];
		cr.combobox('setValue', '1');
		ClearDetail();
    };
	cc.combobox({
		onSelect: function(rec){
//			var json_data = '[{"ID":1,"NAME":"Java"},{"ID":2,"NAME":"C#"},{"ID":3,"NAME":"Ruby","selected":true},{"ID":4,"NAME":"Perl"}]';
			rule_refresh(url + rec.value);
			return;
		}
	});
	cc.combobox('textbox').bind('keydown', function(e){
		if (e.keyCode == 13) { //Key <Enter>
			var opts = cc.combobox('options');
			var data = cc.combobox('getData');
			var curvalue = cc.combobox('getValue');
			for(var i=0; i<data.length; i++){
				var item = data[i];
				if (item[opts.valueField] == curvalue){
//					alert(item[opts.valueField]);
					rule_refresh(url + curvalue);
					return;
				}
			}
		}
	});

	function SaveDetail(row){
		row.amount = parseFloat($('#eta').numberbox('getValue'));
		row.riskamount = parseFloat($('#etra').numberbox('getValue'));
		row.countpayment = $('#cntpays').numberbox('getValue');
	};
	dg = $('#dg');
	$('#btngroup').bind('click', function(){
		$('#detail').show();
		dg.datagrid({
			url:'/lisa/calculator/addgroup/?scheme='+cc.combobox('getValue'),
			method: 'get',
			singleSelect:true,
			rownumbers:true,
			nowrap:false,
			columns:[[
				{field:'grouprisk',title:'Группа<br />моя',align:'center',width:125},
				{field:'riskname',title:'Риск',width:100},
				{field:'amount',title:'Взнос',width:80,align:'right',formatter:formatPrice},
				{field:'riskamount',title:'Сумма',width:80,align:'right',formatter:formatPrice},
				{field:'countpayment',title:'Количество взносов',width:100,hidden:'true'}
			]],
			onLoadSuccess: function(data){
			/*	dg.datagrid('selectAll');
				var rows = dg.datagrid('getSelections');
				var ids = {};
				for(var i=0; i<rows.length; i++){
					ids.push(rows[i].itemid);
				}
				alert(ids.join('\n'));*/
				dg.datagrid('selectRow', 0);
				var row = dg.datagrid('getSelected');
				if (row != null){RefreshDetail(row)};
			},
			onBeforeSelect: onBeforeSelect
		});
		function formatPrice(val,row,index){
			return val.toFixed(2);
		};
		function RefreshDetail(row){
			$('#eta').numberbox('setValue', row.amount);
			$('#etra').numberbox('setValue', row.riskamount);
			$('#cntpays').numberbox('setValue', row.countpayment);
		};
		function onBeforeSelect(index,row){
			var selected = dg.datagrid('getSelected');
			if (selected && selected != row){
				SaveDetail(selected);
				selected_index = dg.datagrid('getRowIndex', selected);
				dg.datagrid('refreshRow', selected_index);
				RefreshDetail(row);
			}
		};
	});
	$('#eta,#etra').numberbox({
		min:0,
		recision:2,
		groupSeparator:' '
	});
	$('#cntpays').numberbox({
		min:0,
		precision:0
	});
	cc.combobox('clear');
	$('#detail').hide();
	function ClearDetail(){
		dg.datagrid('loadData', {"total":0,"rows":[]});
		$('#detail').hide();
	};
	$('#btnclear').bind('click', function(){
		$('#ff').form('clear');
		ClearDetail();
	});
	$('#btnsubmit').bind('click', function(){
/*		var ids = [];
		$('#dg').datagrid('selectRow', 0);
		var rows = $('#dg').datagrid('getData');
		alert(rows.length);
		for(var i=0; i<rows.length; i++){
			ids.push(rows[i].itemid);
		}
		alert(ids.join('\n'));*/
		$('#ff').submit();
/*		$.ajax({
			type: "POST",
			url: "/lisa/calculator/calc2/",
			data: "name=John&location=Boston",
			beforeSend: function(request) {
				return request.setRequestHeader('X-CSRF-Token', $("input[name='csrfmiddlewaretoken']").val());
			},
			success: function(msg){
				alert( "Прибыли данные: " + msg );
			},
			error: function(XMLHttpRequest, textStatus, errorThrown){
				alert(errorThrown);
			}
		});*/
	});
	$('#ff').form({
		url:'/lisa/calculator/calc/',
		onSubmit: function(param){
			// do some check
			// return false to prevent submit;
			var json_data = '{"ID":1,"NAME":"Java"},{"ID":2,"NAME":"C#"}';
/*			for(var i=0; i<data.length; i++){
				var item = data[i];
				alert(item);
			}
			var cells = {};
			for (ix = 0; ix < 9; ix++)
			{
				cells[ix] = ix+',';
			};*/
			var rows = dg.datagrid('getRows');
			var columns = dg.datagrid('getColumnFields');
			var selected = dg.datagrid('getSelected');
			SaveDetail(selected);
			selected_index = dg.datagrid('getRowIndex', selected);
			dg.datagrid('refreshRow', selected_index);		
			param.p1 = rows[selected_index][columns[3]];
		},
		success: function(data){
			alert(data);
/*			var data = eval('(' + data + ')');  // change the JSON string to javascript object
			if (data.success){
				alert(data.message)
			}*/
		}
	});
	$('#tt').tabs({
		onSelect:function(title,index){
			if (index == 1) {
				$('#rule2').empty();
				$('#rule2').append('<iframe scrolling="yes" frameborder="0"  src="http://127.0.0.1:8000/lisapdf/" style="width:100%;height:100%;">');
			}	
		}
	});
});