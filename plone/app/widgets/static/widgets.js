(function($) {
  "use strict";

  $(document).ready(function() {

    var script1 = document.createElement('script');
    script1.setAttribute('type', 'text/javascript');
    script1.setAttribute('src', '/++resource++mockup/bower_components/requirejs/require.js');
    script1.onload = function() {
      var script2 = document.createElement('script');
      script2.setAttribute('type', 'text/javascript');
      script2.setAttribute('src', '/++resource++mockup/js/config.js');
      script2.onload = function() {
        requirejs.config({ baseUrl: '++resource++mockup/' });
        require(['mockup-bundles-widgets'], function(Widgets) {
          Widgets.scan('body');
        });
      };
      document.getElementsByTagName("head")[0].appendChild(script2);
    };
    document.getElementsByTagName("head")[0].appendChild(script1);

  });

}(jQuery));
