LESSC = lessc
UGLIFYJS = uglifyjs
CSSMIN = cssmin
TARGETS = build/widgets.css build/widgets.js build/widgets.png


all:: clean $(TARGETS)

build:
	mkdir build -p

clean:
	rm -rf $(TARGETS)
	rmdir build

build/widgets.js: build
	$(UGLIFYJS) lib/pickadate/source/pickadate.legacy.js > $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.core.js >> $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.plugin.ajax.js >> $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.plugin.arrow.js >> $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.plugin.autocomplete.js >> $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.plugin.clear.js >> $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.plugin.filter.js >> $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.plugin.focus.js >> $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.plugin.prompt.js >> $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.plugin.suggestions.js >> $@
	$(UGLIFYJS) lib/jquery-textext/src/js/textext.plugin.tags.js >> $@
	$(UGLIFYJS) lib/bootstrap/js/bootstrap-transition.js >> $@
	$(UGLIFYJS) lib/bootstrap/js/bootstrap-tab.js >> $@
	$(UGLIFYJS) js/patterns.js >> $@
	$(UGLIFYJS) js/pattern.calendar.js >> $@
	$(UGLIFYJS) js/pattern.autocomplete.js >> $@
	$(UGLIFYJS) js/pattern.tabs.js >> $@
	$(UGLIFYJS) js/plone.tabs.js >> $@

build/widgets.css: build
	$(CSSMIN) lib/pickadate/themes/pickadate.02.classic.css > $@
	$(CSSMIN) lib/jquery-textext/src/css/textext.core.css >> $@
	$(CSSMIN) lib/jquery-textext/src/css/textext.plugin.arrow.css >> $@
	$(CSSMIN) lib/jquery-textext/src/css/textext.plugin.autocomplete.css >> $@
	$(CSSMIN) lib/jquery-textext/src/css/textext.plugin.clear.css >> $@
	$(CSSMIN) lib/jquery-textext/src/css/textext.plugin.focus.css >> $@
	$(CSSMIN) lib/jquery-textext/src/css/textext.plugin.prompt.css >> $@
	$(CSSMIN) lib/jquery-textext/src/css/textext.plugin.tags.css >> $@
	$(LESSC) less/patterns.less | $(CSSMIN) >> $@
	sed -i 's@widgets.png@++resource++plone.app.widgets.png@g' $@

build/widgets.png: build
	cp less/widgets.png $@

.PHONY: all clean bootstrap
