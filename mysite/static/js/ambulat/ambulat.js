$(function(){
	dgan = $('#gambcard');
	tambcard = $('#tambcard');
	sambcard = $('#sambcard');
	amb_url = '/ambulat/load/';
	panet = $('#panet');
	netresize = $('#netresize');
	pamain = $('#pamain');
	isRefresh = 0;
	cLoadMsg = 'Обробка, почекайте будь ласка...'

	formInit();

	function formInit() {
		sambcard.show();
		defResizable();
		setReadOnly();
	};
	function defResizable() {
		pamain.resizable({minWidth:820, handles:'e'});
		netresize.resizable({minHeight:250, handles:'s'});
		panet.panel({border:false});
	};
	function setReadOnly() {
		$('[t_amb]').textbox({readonly:true});
	};	
	dgan.datagrid({
		rownumbers: true,
		singleSelect: true,
		pagination:true,
		remoteSort: false,
		sortName: 'receptiondate',
		sortOrder: 'desc',
		loadMsg: cLoadMsg,		
		columns:[[
			{field:'ambid',hidden:'true'},
			{field:'doctorfullname',title:'ПІБ лікаря',width:200,halign:'center'},
			{field:'receptiondate',title:'Дата прийому',width:94,align:'center',halign:'center',sortable:'true',sorter:dateSort},
			{field:'cabinetno',title:'Кабінет',width:60,halign:'center'},
			{field:'recepttimestart',title:'Час<br />прийому з',width:64,align:'center',halign:'center'},
			{field:'recepttimeend',title:'Час<br />прийому по',width:64,align:'center',halign:'center'},
			{field:'patientfullname',title:'ПІБ пацієнта',width:200,halign:'center'},
			{field:'cardno',title:'№ амбул.<br />карти',width:60,halign:'center'}
		]],
		onLoadSuccess: function(data){
			dgan.datagrid('selectRow', 0);
		},
		onClickRow: function(index, row){
			//refreshAgreements();
		},
		onBeforeSortColumn: function(sort,order){
			//agentAgreenmentClear();
		}
	});
	pager = dgan.datagrid({
		url: amb_url + '?ambcard=1',
		method: 'get'		
	}).datagrid('getPager');
    pager.pagination({
		beforePageText:"Сторінка",
		afterPageText:"з {pages}",
		displayMsg:"Показано від {from} по {to} з {total} элементів",
		buttons:[{
			iconCls:'icon-search',
			handler:function(){
				alert('search');
			}
		},{
			iconCls:'icon-add',
			handler:function(){
				alert('add');
			}
		},{
			iconCls:'icon-edit',
			handler:function(){
				alert('edit');
			}
		},{
			iconCls:'icon-print',
			handler:function(){
				repUrl = '/ambulat/rep_ambulat/';
				params = 'Toolbar=1,Location=0,Directories=0,Status=0,Menubar=0,Scrollbars=1,Resizable=1,Width=550,Height=400';
				window.open(repUrl, 'Отчет', params);				
			}
		}]
	});	
	dgan.datagrid('enableFilter', [
	{field:'doctorfullname', type:'textbox', options:{onChange:function(value){onSetFilter(dgan, 'doctorfullname', value)}}},
	{field:'receptiondate', type:'textbox', options:{onChange:function(value){onSetFilter(dgan, 'receptiondate', value)}}},
	{field:'cabinetno', type:'textbox', options:{onChange:function(value){onSetFilter(dgan,'cabinetno', value)}}},
	{field:'recepttimestart', type:'textbox', options:{onChange:function(value){onSetFilter(dgan, 'recepttimestart', value)}}},
	{field:'recepttimeend', type:'textbox', options:{onChange:function(value){onSetFilter(dgan, 'recepttimeend', value)}}},
	{field:'patientfullname', type:'textbox', options:{onChange:function(value){onSetFilter(dgan, 'patientfullname', value)}}},
	{field:'cardno', type:'textbox', options:{onChange:function(value){onSetFilter(dgan, 'cardno', value)}}}
	]);
	function onSetFilter(dg, afield, avalue){
        if (avalue == ''){
            dg.datagrid('removeFilterRule', afield);
        } else {
			op_value = 'contains';
            dg.datagrid('addFilterRule', {
                field: afield,
                op: op_value,
                value: avalue
            });
        }
        dg.datagrid('doFilter');
	};
    function parserDate(s){
        if (!s) return ''
        var ss = (s.split('-'));
        var y = parseInt(ss[0],10);
        var m = parseInt(ss[1],10);
        var d = parseInt(ss[2],10);
		return (d<10?('0'+d):d)+'.'+(m<10?('0'+m):m)+'.'+y;
    };
	tambcard.tabs({
		onSelect:function(title,index){
			if (index == 1) {
				row = dgan.datagrid('getSelected');
				if (row != null) {
					$('[t_amb]').each(function(idx, element){
						fieldname = $(element).attr('t_amb');
						ElementValue = row[fieldname];
						if (fieldname == 'birthday') 
							ElementValue = parserDate(ElementValue);
						$(element).textbox('setValue', ElementValue);
					})
				} else {
					$('[t_amb]').textbox('clear');
				}
			}
		}
	});
	function dateSort(a,b){
		if (a == null) a = '01.01.1900';
		if (b == null) b = '01.01.1900';	
		a = a.split('.');
		b = b.split('.');
		if (a[2] == b[2]){
			if (a[1] == b[1]){
				return (a[0]>b[0]?1:-1);
			} else {
				return (a[1]>b[1]?1:-1);
			}
		} else {
			return (a[2]>b[2]?1:-1);
		}
	};
	netresize.resizable({
		onStartResize: function(e){
			panet.panel('close');
		},
		onStopResize: function(e){
			if (panet.height() != netresize.height()) {
				panet.panel('resize');
				tambcard.tabs('resize');
			}
			panet.panel('open');
		}
	});
	pamain.resizable({
		onStopResize: function(e){
			if (pamain.width() != netresize.width()){
				tambcard.tabs('resize');
			};
		}
	});
});