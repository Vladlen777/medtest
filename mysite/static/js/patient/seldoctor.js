$(function(){
	dgpl = $('#gpersonnel');
	tpersonnel = $('#tpersonnel');
	trecord = $('#trecord');
	pers_url = '/ambulat/patient/';
	papers = $('#papers');
	plresize = $('#plresize');
	pamain = $('#pamain');
    dgcm = $('#gcurriculum');
	breg = $('#btnregistry');
	freg = $('#fregistry');
	cLoadMsg = 'Обробка, почекайте будь ласка...';
	FCurId = 0;

	formInit();

	function formInit() {
		trecord.show();
		defResizable();		
	};
	function defResizable() {
		pamain.resizable({minWidth:510, handles:'e'});
		plresize.resizable({minHeight:250, handles:'s'});
		papers.panel({border:false});
	};
	dgpl.datagrid({
		rownumbers: true,
		singleSelect: true,
		pagination:true,
		remoteSort: false,
		sortName: 'personnelfullname',
		loadMsg: cLoadMsg,		
		columns:[[
			{field:'id',hidden:'true'},
			{field:'personnelfullname',title:'ПІБ фахівця',width:220,halign:'center',sortable:'true'},
			{field:'specialityname',title:'Спеціальність',width:140,halign:'center'},
			{field:'cabinetno',title:'Кабінет',width:60,halign:'center'}
		]],
		onLoadSuccess: function(data){			
			dgpl.datagrid('selectRow', 0);
		}
	});
	pager = dgpl.datagrid({
		url: pers_url + 'load/?person=1',
		method: 'get'
	}).datagrid('getPager');
    pager.pagination({
		beforePageText:"Сторінка",
		afterPageText:"з {pages}",
		displayMsg:"від {from} по {to} з {total}"
	});
	dgpl.datagrid('enableFilter', [
	{field:'personnelfullname', type:'textbox', options:{onChange:function(value){onSetFilter(dgpl, 'personnelfullname', value)}}},
	{field:'specialityname', type:'textbox', options:{onChange:function(value){onSetFilter(dgpl, 'specialityname', value)}}},
	{field:'cabinetno', type:'textbox', options:{onChange:function(value){onSetFilter(dgpl, 'cabinetno', value)}}}
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
	plresize.resizable({
		onStartResize: function(e){
			papers.panel('close');
		},
		onStopResize: function(e){
			if (papers.height() != plresize.height()) {
				papers.panel('resize');
				tpersonnel.tabs('resize');
			}
			papers.panel('open');
		}
	});
	pamain.resizable({
		onStopResize: function(e){
			if (pamain.width() != plresize.width()){
				tpersonnel.tabs('resize');
			};
		}
	});
	dgcm.datagrid({
		method: 'get',
		rownumbers: true,
		singleSelect: true,
		loadMsg: cLoadMsg,	
		columns:[[
			{field:'curriculumdate',title:'Дата',width:100,align:'center',halign:'center'},
			{field:'weekday',title:'День тижня',width:160,halign:'center'},
			{field:'receptiontime',title:'Час прийому',width:100,align:'center',halign:'center'}
		]],
		onLoadSuccess: function(data){			
			dgcm.datagrid('selectRow', FCurId);
		},
		rowStyler: function(index,row){
			if (row != null) {
				if (row.ambid > 0)
					return 'background-color:#b4eeb4;';
			}	
		}
	});
	tpersonnel.tabs({
		onSelect:function(title,index){
			if (index == 1) {
				row = dgpl.datagrid('getSelected');
				if (row != null) {
					$('span.doctorinfo').html('<b> '+row.specialityname+': '
					                                +row.personnelfullname+', кабінет '
													+row.cabinetno+'</b>');
					dgcm.datagrid('reload', pers_url + 'load/?dpersonid=' + row.id);
				} else {
					$('span.doctorinfo').html('');					
					dgcm.datagrid('loadData', {"total":0,"rows":[],"footer":[]});
				}
			}
		}
	});
	breg.bind('click', function(){
		freg.submit();
	});
	freg.form({
		url: '/ambulat/patient/save/',
		onSubmit: function(param){
			param.patient_id = breg.attr('t_pid');
			row = dgpl.datagrid('getSelected');
			if (row != null) {
				param.personnel_id = row.id;
				param.cabinetno = row.cabinetno;
			};
			row = dgcm.datagrid('getSelected');
			RegistryPatient = 0;
			if (row != null) {
				param.receptiondate = row.curriculumdate;
				param.recepttimestart = row.receptiontime;
				RegistryPatient = row.ambid;
				if (RegistryPatient > 0)
					$.messager.alert('Помилка', 'Запис на прийом на час "'+
				                     row.receptiontime+'" неможлива. Виберіть інший час.', 'error');
			};
			return (RegistryPatient == 0);
		},
		success: function(jdata){
			row = dgcm.datagrid('getSelected');
			FCurId = row.id;
			$.messager.alert('Реєстрація', 'Ви записані на прийом до лікаря<br />'+
			                 $('span.doctorinfo').html()+
							 ' на '+row.curriculumdate+
							 ' час '+row.receptiontime, 'info');
			dgcm.datagrid('reload');
			//document.location.href = "/patient/";
		}
	});
});