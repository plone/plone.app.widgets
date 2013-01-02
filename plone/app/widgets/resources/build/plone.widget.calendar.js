// plone integration for pickadate.
//
// Author: Rok Garbas
// Contact: rok@garbas.si
// Version: 1.0
// Depends:
//    ++resource++plone.app.jquery.js
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

var Calendar = function($el, options) { this.init($el, options); };
Calendar.prototype = {
  constructor: Calendar,
  init: function($el, options) {
    var self = this;
    self.$el = $el;
    self.prefix = 'calendar';
    self.options = $.extend(getOptions($el, this.prefix), options);
    self.$pickadate = $('<input />').hide().prependTo($el)
      .pickadate({
        format: 'yyyy-mm-dd',
        onSelect: function() {
          var date = self.pickadate.getDate().split('-');
          $.each(self.options.target.split(','), function(i, item) {
            $(item, self.$el).val(date[i]);
          });
        }
      });
    self.pickadate = self.$pickadate.data('pickadate');
    self.isOpen = false;
    self.$trigger = $(self.options.trigger, $el).show()
      .on('click', function(e) {
          e.stopPropagation();
          e.preventDefault();
          self.toggle();
        });
    $(self.options.target, $el).on('change', function() {
      var attrs = [];
      $.each(self.options.target.split(','), function(i, item) {
        attrs[i] = parseInt($(item, self.$el).val(), 10);
      });
      self.pickadate.setDate.apply(self.pickadate, attrs);
    });
    $.each(self.options.target.split(','), function(i, item) {
      $(item, self.$el).val();
    });
  },
  toggle: function() {
    if (this.isOpen) {
      this.close();
    } else {
      this.open();
    }
  },
  open: function() {
    if (!this.isOpen) {
      this.pickadate.open();
    }
  },
  close: function() {
    if (this.isOpen) {
      this.pickadate.close();
    }
  }
};


// jQuery integration
$.fn.ploneCalendar = function(options) {
  $(this).each(function() {
    var $el = $(this),
        dateName = $el.data('pattern'),
        data = $el.data(name);

    if (!data) {
      $el.data(dateName, data = new Calendar($el, options));
    }

    if (typeof options === 'string') {
      data[options]();
    }

  });
};


// pickadate initialization
function initialize(context) {
  $('[data-pattern~="calendar"]', context).ploneCalendar();
}


// plone.init.js integration (if exists)
if ($.plone && $.plone.init) {
  $.plone.init.register(initialize);
} else {
  initialize(document);
}

}(jQuery));
