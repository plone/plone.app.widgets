(function($) {
  "use strict";

  $(document).ready(function() {

    var script1 = document.createElement('script');
    script1.setAttribute('type', 'text/javascript');
    script1.setAttribute('src', '/++resource++mockup/bower_components/requirejs/require.js');
    script1.onload = function() {
      console.log('script1 loaded');
      var script2 = document.createElement('script');
      script2.setAttribute('type', 'text/javascript');
      script2.setAttribute('src', '/++resource++mockup/js/config.js');
      script2.onload = function() {
        console.log('script2 loaded');
        requirejs.config({ baseUrl: '++resource++mockup/' });
        require(['mockup-bundles-widgets'], function(Widgets) {
          console.log('widgets loading');
          Widgets.scan('body');
          console.log('widgets loaded');
        });
      };
      document.getElementsByTagName("head")[0].appendChild(script2);
    };
    document.getElementsByTagName("head")[0].appendChild(script1);

  });

}(jQuery));
