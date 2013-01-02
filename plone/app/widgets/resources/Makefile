LESSC = lessc
UGLIFYJS = cat
CSSMIN = cssmin
TARGETS = build/pickadate.js build/pickadate.css build/textext.js build/textext.css build/plone.init.js build/plone.widget.autocomplete.js build/plone.widget.calendar.js build/widgets.css build/img


all:: clean $(TARGETS)

bootstrap:
	mkdir build -p
	cd ../../../../ && git submodule update --init --recursive

clean:
	rm -rf $(TARGETS)

build/pickadate.js:
	$(UGLIFYJS) lib/pickadate/source/pickadate.legacy.js > $@
build/pickadate.css:
	$(CSSMIN) lib/pickadate/source/pickadate.css > $@
build/textext.js:
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.core.js > $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.plugin.ajax.js >> $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.plugin.arrow.js >> $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.plugin.autocomplete.js >> $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.plugin.clear.js >> $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.plugin.filter.js >> $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.plugin.focus.js >> $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.plugin.prompt.js >> $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.plugin.suggestions.js >> $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.plugin.tags.js >> $@
build/textext.css:
	$(CSSMIN) lib/jquery-textext/src/css/textext.core.css > $@
	$(CSSMIN) lib/jquery-textext/src/css/textext.core.css >> $@
	$(CSSMIN) lib/jquery-textext/src/css/textext.plugin.arrow.css >> $@
	$(CSSMIN) lib/jquery-textext/src/css/textext.plugin.autocomplete.css >> $@
	$(CSSMIN) lib/jquery-textext/src/css/textext.plugin.clear.css >> $@
	$(CSSMIN) lib/jquery-textext/src/css/textext.plugin.focus.css >> $@
	$(CSSMIN) lib/jquery-textext/src/css/textext.plugin.prompt.css >> $@
	$(CSSMIN) lib/jquery-textext/src/css/textext.plugin.tags.css >> $@

build/plone.init.js:
	$(UGLIFYJS) js/plone.init.js > $@
build/plone.widget.autocomplete.js:
	cp js/plone.widget.autocomplete.js $@
build/plone.widget.calendar.js:
	$(UGLIFYJS) js/plone.widget.calendar.js > $@

build/widgets.css:
	$(CSSMIN) css/widgets.css > $@

build/img:
	mkdir build/img -p
	cp lib/jquery-textext/src/css/arrow.png build/img/textext-arrow.png
	cp lib/jquery-textext/src/css/close.png build/img/textext-close.png


.PHONY: all clean bootstrap
