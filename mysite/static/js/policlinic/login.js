$(function(){
	cMissingMessage = 'Поле необходимо заполнить';
	$('.insui-textbox').textbox({
		required:true,
		validType:'length[3,30]',
		missingMessage:cMissingMessage,
		invalidMessage:'Пожалуйста, введите текст от 3 до 30 символов'
	});
	function parserDate(s){
		if (!s) return new Date();
		var ss = (s.split('.'));
		var y = parseInt(ss[0],10);
		var m = parseInt(ss[1],10);
		var d = parseInt(ss[2],10);
		if (!isNaN(y) && !isNaN(m) && !isNaN(d)){
			return new Date(d,m-1,y);
		} else {
			return new Date();
		}
	};
	function formatterDate(date){
		var y = date.getFullYear();
		var m = date.getMonth()+1;
		var d = date.getDate();
		return (d<10?('0'+d):d)+'.'+(m<10?('0'+m):m)+'.'+y;
	};
	$('#birthday').datebox({
		required: true,
		missingMessage: cMissingMessage,
		currentText: 'Сегодня',
		closeText: 'Закрыть',
		formatter: formatterDate,
		parser: parserDate
	});
	c = $('#birthday').datebox('calendar');
	c.calendar({
		weeks: ['П','В','С','Ч','П','С','В'],
		months: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 
					'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
	});
	$('.login-form').form({
		onSubmit: function(param){
			return $(this).form('validate');
		},
		success: function(data){
			document.location.href = "/policlinic/doctor/"+data+"/";
		}
	});
});