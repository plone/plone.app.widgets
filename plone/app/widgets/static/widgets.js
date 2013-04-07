
(function($) {
  "use strict";

  $(document).ready(function() {

    var script = document.createElement('script');
    script.setAttribute('type', 'text/javascript');
    script.setAttribute('src', '++resource++mockup/jam/require.js');
    //requirejs.onreadystatechange = function() {
    //  if (requirejs.readyState == "loaded") {
    //    window.require(['++resource++mockup/js/bundles/widgets.js']);
    //  }
    //};
    script.onload = function() {
      requirejs.config({ baseUrl: '++resource++mockup/' });
      window.require(['js/bundles/widgets'], function(Widgets) {
        Widgets.scan('body');
      });
    };
    document.getElementsByTagName("head")[0].appendChild(script);

  });

}(jQuery));
