LESSC = lessc
UGLIFYJS = uglifyjs
CSSMIN = cssmin
TARGETS = build/chosen.js build/chosen.ajax.js build/pickadate.js build/pickadate.css build/plone.init.js build/plone.chosen.js build/plone.pickadate.js build/chosen.css build/widgets.css


all:: clean $(TARGETS)

bootstrap:
	mkdir build -p
	cd ../../../../ && git submodule update --init --recursive

clean:
	rm -rf $(TARGETS)

build/chosen.js:
	$(UGLIFYJS) lib/ajax-chosen/dist/chosen/chosen/chosen.jquery.js > $@
build/chosen.ajax.js:
	cp lib/ajax-chosen/lib/ajax-chosen.min.js $@
build/pickadate.js:
	cp lib/pickadate/source/pickadate.legacy.js $@
build/pickadate.css:
	cp lib/pickadate/source/pickadate.css $@

build/plone.init.js:
	$(UGLIFYJS) js/plone.init.js > $@
build/plone.chosen.js:
	$(UGLIFYJS) js/plone.chosen.js > $@
build/plone.pickadate.js:
	cp js/plone.pickadate.js $@

build/chosen.css:
	$(CSSMIN) lib/ajax-chosen/dist/chosen/chosen/chosen.css > $@
build/widgets.css:
	$(CSSMIN) css/widgets.css > $@


.PHONY: all clean bootstrap
