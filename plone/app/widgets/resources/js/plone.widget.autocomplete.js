// plone integration for textext.
//
// Author: Rok Garbas
// Contact: rok@garbas.si
// Version: 1.0
// Depends:
//    ++resource++plone.app.jquery.js
//    ++resource++plone.app.widgets/textext.js
//
// Description:
//
// License:
//
// Copyright (C) 2010 Plone Foundation
//
// This program is free software; you can redistribute it and/or modify it
// under the terms of the GNU General Public License as published by the Free
// Software Foundation; either version 2 of the License.
//
// This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
// FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
// more details.
//
// You should have received a copy of the GNU General Public License along with
// this program; if not, write to the Free Software Foundation, Inc., 51
// Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
//

/*jshint bitwise:true, curly:true, eqeqeq:true, immed:true, latedef:true,
  newcap:true, noarg:true, noempty:true, nonew:true, plusplus:true,
  undef:true, strict:true, trailing:true, browser:true, evil:true */
/*global jQuery:false */


(function($, undefined) {
"use strict";

// utility to read options
function getOptions($el, prefix, options) {
  options = options || {};

  if (!$.nodeName($el[0], 'body')) {
    options = getOptions($el.parent(), prefix, options);
  }

  if($el.length) {
    $.each($el[0].attributes, function(index, attr) {
      if (attr.name.substr(0, ('data-'+prefix).length) === 'data-'+prefix) {
        options[attr.name.substr(('data-'+prefix).length+1)] = attr.value;
      }
    });
  }

  return options;
}

var Autocomplete = function($el, options) { this.init($el, options); };
Autocomplete.prototype = {
  constructor: Autocomplete,
  init: function($el, options) {
    var self = this;
    self.$el = $el;
    self.prefix = 'autocomplete';
    self.options = $.extend(getOptions($el, this.prefix), options);
    self.$el.css('height', '22px');
    self.$el.textext({
      plugins: self.options.plugins
    });
    self.$el.css('height', 'auto');
  }
};


// jQuery integration
$.fn.ploneAutocomplete= function(options) {
  $(this).each(function() {
    var $el = $(this),
        dateName = $el.data('pattern'),
        data = $el.data(name);

    if (!data) {
      $el.data(dateName, data = new Autocomplete($el, options));
    }

    if (typeof options === 'string') {
      data[options]();
    }

  });
};


// autocomplete initialization
function initialize(context) {
  $('[data-pattern~="autocomplete"]', context).ploneAutocomplete();
}


// plone.init.js integration (if exists)
if ($.plone && $.plone.init) {
  $.plone.init.register(initialize);
} else {
  initialize(document);
}

}(jQuery));
