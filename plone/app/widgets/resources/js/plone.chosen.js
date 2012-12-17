jQuery(function($){

  function initChosen(context) {
    $('select.chosen', context).each(function(){
      var options = {};
      var el = $(this);
      options.allow_sortable = el.data('sortable') == 'true' ? true : false;

      var type = el.data('ajax') == 'true' ? 'ajax' : 'default';
      var type = el.data('date') == 'true' ? 'date' : 'default';

      if(type == 'ajax'){
        var url = el.data('ajax-url');
        el.ajaxChosen(options, {
          url: url,
          dataType: 'ajax'}, function (data) { return data; });
      }else if(type == 'date'){
        el.dateChosen(options);
      }else{
        el.chosen(options);
      }
    });
  }
  if ($.plone && $.plone.init) {
    $.plone.init.register(initChosen);
  } else {
    initChosen(document);
  }

});
