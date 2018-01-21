$(function(){
	dgpl = $('#gpersonnel');
	tpersonnel = $('#tpersonnel');
	pers_url = '/policlinic/doctor/';
	papers = $('#papers');
	plresize = $('#plresize');
	pamain = $('#pamain');
    dgcm = $('#gcurriculum');
	breg = $('#btnregistry');
	freg = $('#fregistry');
	cLoadMsg = 'Обработка, подождите пожалуйста...';
	FCurId = 0;

	formInit();

	function formInit() {
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
			{field:'personnelfullname',title:'ФИО специалиста',width:220,halign:'center',sortable:'true'},
			{field:'specialityname',title:'Специальность',width:140,halign:'center'},
			{field:'cabinetno',title:'Кабинет',width:60,halign:'center'}
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
		beforePageText:"Страница",
		afterPageText:"из {pages}",
		displayMsg:"с {from} по {to} из {total}"
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
			{field:'weekday',title:'День недели',width:160,halign:'center'},
			{field:'receptiontime',title:'Время приема',width:100,align:'center',halign:'center'}
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
					                                +row.personnelfullname+', кабинет '
													+row.cabinetno+'</b>');
					dgcm.datagrid('reload', pers_url + 'load/?personid=' + row.id);
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
		url: '/policlinic/ambcard/save/',
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
					$.messager.alert('Ошибка', 'Запись на прием на время "'+
				                     row.receptiontime+'" невозможна. Выберите другое время.', 'error');
			};
			return (RegistryPatient == 0);
		},
		success: function(jdata){
			row = dgcm.datagrid('getSelected');
			FCurId = row.id;
			$.messager.alert('Регистрация', 'Вы записаны на прием к врачу<br />'+
			                 $('span.doctorinfo').html()+
							 ' на '+row.curriculumdate+
							 ' время '+row.receptiontime, 'info');
			dgcm.datagrid('reload');
			//document.location.href = "/policlinic/";
		}
	});
});