$(function(){
	dgpl = $('#gpersonnel');
	tpersonnel = $('#tpersonnel');
	trecord = $('#trecord');
	pers_url = '/ambulat/personnel/';
	papers = $('#papers');
	plresize = $('#plresize');
	pamain = $('#pamain');
	pabutton = $('#pabutton');
	cspec = $('#spec');
	bsave = $('#btnsave');
	bcancel = $('#btncancel');
	fsave = $('#fsave');
	fdel = $('#fdel');
	dgcm = $('#gcurriculum');
	cLoadMsg = 'Обробка, почекайте будь ласка...';
	FPersonId = 0;
	FRowIndex = 0;
	FInsertMode = false;
	editIndex = undefined;

	formInit();

	function formInit() {
		trecord.show();
		defResizable();		
		setReadOnlyMode(true);
		pabutton.hide();
		bsave.linkbutton({iconCls:'icon-save', iconAlign:'left'});
		bcancel.linkbutton({iconCls:'icon-cancel', iconAlign:'left'});
	};
	function defResizable() {
		pamain.resizable({minWidth:520, handles:'e'});
		plresize.resizable({minHeight:250, handles:'s'});
		papers.panel({border:false});
	};
	function setReadOnlyMode(readonly) {
		$('[t_amb]').textbox({readonly:readonly});
		cspec.combobox({readonly:readonly});
		dgcm.datagrid({readonly:readonly});
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
			dgpl.datagrid('selectRow', FRowIndex);
		},
		onClickRow: function(index, row){
			FRowIndex = index;
		}
	});
	function setNewTitleForRecordTab(title) {
		tab = tpersonnel.tabs('getSelected');
		tpersonnel.tabs('update', {
			tab: tab,
			options: {title: title}
		});
	};
	function setControls(title) {
		tpersonnel.tabs('select', 'Запис');
		setNewTitleForRecordTab(title);
		pabutton.show();
		setReadOnlyMode(false);
		tpersonnel.tabs('disableTab', 0);
	};
	pager = dgpl.datagrid({
		url: pers_url + 'load/?person=1',
		method: 'get'
	}).datagrid('getPager');
    pager.pagination({
		beforePageText:"Сторінка",
		afterPageText:"з {pages}",
		displayMsg:"від {from} по {to} з {total}",
		buttons:[{
			iconCls:'icon-add',
			buttonText:'Додати',
			handler:function(){
				FInsertMode = true;
				FPersonId = 0;
				FRowIndex = 0;
				setControls('Додати');
				$('[t_amb]').textbox('clear');
				cspec.combobox('clear');
				dgcm.datagrid('reload', pers_url + 'load/?newperson=0');
				FInsertMode = false;
			}
		},{
			iconCls:'icon-edit',
			handler:function(){
				FPersonId = 0;
				row = dgpl.datagrid('getSelected');
				if (row != null) {
					FPersonId = row.id;
					setControls('Змінити');
					cspec.combobox('setValue', row.speciality_id);
				}
			}
		},{
			iconCls:'icon-delete',
			handler:function(){
				FPersonId = 0;
				$.messager.confirm('Confirm','Ви упевнені, що хочете видалити запис?',function(r){
					if (r){
						row = dgpl.datagrid('getSelected');
						if (row != null) {
							FPersonId = row.id;
							fdel.submit();
						}
					}
				});
			}
		}]
	});
	fdel.form({
		url: pers_url + 'del/',
		onSubmit: function(param){
			param.personid = FPersonId;
			return true;
		},
		success: function(jdata){
			dgpl.datagrid('reload');
		},
		onLoadError: function(){
			alert('Ошибка!');
		}
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
	tpersonnel.tabs({
		onSelect:function(title,index){
			if (index == 1 && !FInsertMode) {
				row = dgpl.datagrid('getSelected');
				if (row != null) {
					$('[t_amb]').each(function(idx, element){
						fieldname = $(element).attr('t_amb');
						$(element).textbox('setValue', row[fieldname]);
					});
					cspec.combobox('setValue', row.speciality_id);
					dgcm.datagrid('reload', pers_url + 'load/?personid=' + row.id);
				} else {
					$('[t_amb]').textbox('clear');
					cspec.combobox('clear');
					dgcm.datagrid('loadData', {"total":0,"rows":[],"footer":[]});
				}
			}
		}
	});
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
	function repairControls() {
		setNewTitleForRecordTab('Запис');
		pabutton.hide();				
		setReadOnlyMode(true);
		tpersonnel.tabs('enableTab', 0);
		tpersonnel.tabs('select', 'Персонал');
	};
	bsave.bind('click', function(){
		fsave.submit();
	});
	bcancel.bind('click', function(){
		repairControls();
	});
	fsave.form({
		url: pers_url + 'save/',
		onSubmit: function(param){
			param.id = "{'id':" + String(FPersonId) + "}";
			dgcm.datagrid('acceptChanges');
			param.curriculum = '';
			rows = dgcm.datagrid('getRows');
			if (rows.length > 0)
				param.curriculum = GetParamCurriculum(rows);
			return ValidateForm();
		},
		success: function(jdata){
			repairControls();
			dgpl.datagrid('reload');
		},
		onLoadError: function(){
			alert('Помилка!');
		}
	});
	dgcm.datagrid({
		method: 'get',
		rownumbers: true,
		singleSelect: true,
		loadMsg: cLoadMsg,	
		onClickCell: onClickCell,
		columns:[[
			{field:'id',hidden:'true'},
			{field:'weekdaynum',hidden:'true'},
			{field:'curriculumdate',title:'Дата',width:100,align:'center',halign:'center'},
			{field:'weekday',title:'День тижня',width:160,halign:'center'},
			{field:'recepttimestart',title:'Час<br />прийому з',width:70,
				align:'center',halign:'center',editor:{type:'timespinner',options:{min:'08:00'}}},
			{field:'recepttimeend',title:'Час<br />прийому по',width:70,
				align:'center',halign:'center',editor:{type:'timespinner',options:{min:'08:00'}}}
		]],
		onLoadSuccess: function(data){			
			dgcm.datagrid('selectRow', 0);
		}
	});
	function endEditing(){
		opts = dgcm.datagrid('options');
		if (opts.readonly == true) {return false}
		if (editIndex == undefined){return true}
		if (dgcm.datagrid('validateRow', editIndex)){
			dgcm.datagrid('endEdit', editIndex);
			editIndex = undefined;
			return true;
		} else {
			return false;
		}
	};
	function onClickCell(index, field){
		if (editIndex != index){
			if (endEditing()){
				dgcm.datagrid('selectRow', index)
					.datagrid('beginEdit', index);
				var ed = dgcm.datagrid('getEditor', {index:index,field:field});
				if (ed){
					($(ed.target).data('textbox') ? $(ed.target).textbox('textbox') : $(ed.target)).focus();
				}
				editIndex = index;
			} else {
				setTimeout(function(){
					dgcm.datagrid('selectRow', index);
				},0);
			}
		}
	};
    function NullToNoneStr(val){
        if (!val || val == null) return 'None'; else return "'"+val+"'";
    };
	function GetParamCurriculum(rows){
		result = '';
		if (rows.length > 0){
			for(i = 0; i < rows.length; i++){
				row = rows[i];
				if (result != '')
					result = result + ',';
				result = result + i.toString()
					+":{'weekday': " + row['weekdaynum']
					+ ",'recepttimestart': " + NullToNoneStr(row['recepttimestart'])
					+ ",'recepttimeend': " + NullToNoneStr(row['recepttimeend'])
					+ "}";
			}
			result = "{" + result + "}";
		}
		return result;
	};
	function ValidateForm(){
		sMessage = '';
		if (cspec.combobox('getValue') == '')
			sMessage = 'Выберіть спеціальність';
		FIO = $('[t_amb]').get().reverse();
		$(FIO).each(function(idx, element){
			if ($(element).textbox('getValue').trim() == '') {
				fieldname = $(element).attr('t_amb');
				if (fieldname == 'lastname')
					sMessage = 'Заповните прізвище';				
				if (fieldname == 'firstname')
					sMessage = "Заповните им'я";
				if (fieldname == 'middlename')
					sMessage = 'Заповните по батькові';
				if (fieldname == 'cabinetno')
					sMessage = 'Заповните кабінет';
			}
		});
		if (sMessage != '')
			$.messager.alert('Помилка', sMessage, 'error');
		return (sMessage == '');
	}
});