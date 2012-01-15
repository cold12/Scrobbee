#!/usr/bin/env python

"""A Jinja Handler and tool.  This code is in the public domain.

Usage:
@cherrypy.expose
@cherrypy.tools.jinja(filename='index.html')
def controller(**kwargs):
    return {

    } # This dict is the template context     

"""
# Gotten from https://gist.github.com/1316124

import cherrypy
import jinja2
from jinja2.environment import Environment, Template

class JinjaHandler(cherrypy.dispatch.LateParamPageHandler):
    """Callable which sets response.body."""

    def __init__(self, env, template_name, next_handler):
        self.env = env
        self.template_name = template_name
        self.next_handler = next_handler

    def __call__(self):
        context = {}
        try:
            r = self.next_handler()
            context.update(r)
        except ValueError, e:
            cherrypy.log('%s (handler for "%s" returned "%s")\n' % (
                e, self.template_name, repr(r)), traceback=True)

        context.update({
            'request': cherrypy.request,
            'app_url': cherrypy.request.app.script_name,
        })

        cherrypy.request.template = tmpl = self.env.get_template(self.template_name)
        output = tmpl.render(**context)

        return output


class JinjaLoader(object):
    """A CherryPy 3 Tool for loading Jinja templates."""

    def __init__(self, views_dir):
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(views_dir))

    def __call__(self, filename):
        cherrypy.request.handler = JinjaHandler(self.env, filename, cherrypy.request.handler)

    def add_filter(self, func):
        """Decorator which adds the given function to jinja's filters."""
        self.env.filters[func.__name__] = func
        return func

    def add_global(self, func):
        """Decorator which adds the given function to jinja's globals."""
        self.env.globals[func.__name__] = func
        return func