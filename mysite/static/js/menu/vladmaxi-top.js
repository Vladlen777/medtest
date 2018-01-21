$(function(){
// Выравнивание верхней полосы меню
	var top_menu = $(".vladmaxi-top");
		top_menu.attr('width_prev', top_menu.width());

	$("#menu_btn").click(function() {
		var width_top_menu = top_menu.attr('width_prev');
		if ($("body").attr('data-menu-position') == 'closed')
			width_top_menu = top_menu.width() - 228;
		top_menu.width(width_top_menu);
	});
	$("body").click(function() {
		if ($("body").attr('data-menu-position') == 'open')
			if (top_menu.width() != top_menu.attr('width_prev')) {
				top_menu.width(top_menu.attr('width_prev'));
			}
	});
// Убрал фон навигатора по умолчанию
  $(".jPanelMenu-panel").css("background-color", "rgba(255,255,255,0)");
});