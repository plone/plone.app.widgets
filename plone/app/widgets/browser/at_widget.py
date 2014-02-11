from Products.Five import BrowserView


class PatternsWidgetMacros(BrowserView):

    @property
    def macros(self):
        return self.index.macros
