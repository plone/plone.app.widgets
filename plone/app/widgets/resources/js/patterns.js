// Patterns 
//
// Author: Rok Garbas
// Contact: rok@garbas.si
// Version: 1.0
// Dependencies:
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
/*global jQuery:false, console:false */

(function($, undefined) {
"use strict";

var error = jQuery.error,
    _registry = [];

// Get options from element's data attributes
// Collect options from parent tree of elements
function getOptions($el, prefix, options) {
  options = options || {};

  // get options from parent element first, stop if element tag name is 'body'
  if (!$.nodeName($el[0], 'body')) {
    options = getOptions($el.parent(), prefix, options);
  }

  // collect all options from element
  if($el.length) {
    $.each($el[0].attributes, function(index, attr) {
      if (attr.name.substr(0, ('data-'+prefix).length) === 'data-'+prefix) {
        if (attr.value === 'true') {
          options[$.camelCase(attr.name.substr(('data-'+prefix).length+1))] = true;
        } else if (attr.value === 'false') {
          options[$.camelCase(attr.name.substr(('data-'+prefix).length+1))] = false;
        } else {
          options[$.camelCase(attr.name.substr(('data-'+prefix).length+1))] = attr.value;
        }
      }
    });
  }

  return options;
}

// Initialize patterns over some context/dom element.
// Patterns already initialized won't be initialized again.
function initializePatterns(context) {
  $.each(_registry, function(i, Pattern) {
    $('[data-pattern="' + Pattern.prototype.name + '"]').each(function() {
      if ($(this).data('_pattern') === undefined) {
        $(this).data('_pattern', new Pattern($(this),
            getOptions($(this), Pattern.prototype.name)));
      }
    });
  });
}

// Register pattern
function registerPattern(Pattern) {
  if (!Pattern.prototype.name) {
    error('Pattern you try to register has no name.');
    return;
  }
  if (Pattern.prototype.jqueryPlugin) {
    $.fn[Pattern.prototype.jqueryPlugin] = function(method, options) {
      $(this).each(function() {
        var $el = $(this),
            pattern = $el.data('_pattern');
        if (typeof method === "object") {
          options = method;
          method = undefined;
        }
        if (!pattern) {
          $el.data('_pattern',
            new Pattern($el, getOptions($el, Pattern.prototype.name, options)));
        } else if (method && pattern[method]) {
          pattern[method].apply(pattern, [options]);
        }

      });
      return this;
    };
    $.fn[Pattern.prototype.jqueryPlugin].Constructor = Pattern.constructor;
  }
  _registry.push(Pattern);
}

// Base Pattern
var BasePattern = function($el, options) {
  this.$el = $el.addClass('pattern-' + this.name);
  this.options = options;
  if (this.init) {
    this.init();
  }
};
BasePattern.prototype = { constructor: BasePattern };
BasePattern.extend = function(NewPattern) {
  var Base = this;
  var Constructor;

  if (NewPattern && NewPattern.hasOwnProperty('constructor')) {
    Constructor = NewPattern.constructor;
  } else {
    Constructor = function() { Base.apply(this, arguments); };
  }

  var Surrogate = function() { this.constructor = Constructor; };
  Surrogate.prototype = Base.prototype;
  Constructor.prototype = new Surrogate();

  $.extend(true, Constructor.prototype, NewPattern);

  Constructor.__super__ = Base.prototype;
  return Constructor;
};

// Initial initialization of patterns
$(document).ready(function() {
  initializePatterns($(document));
});

// Public API
window.Patterns = {
  _registry: _registry,
  initialize: initializePatterns,
  register: registerPattern,
  getOptions: getOptions,
  Base: BasePattern
};


}(window.jQuery));
