from __future__ import unicode_literals

from flask import current_app
from flask_pluginengine import render_plugin_template, current_plugin
from wtforms import StringField, BooleanField

from indico.cli.core import cli_command, cli_group
from indico.core import signals
from indico.util.i18n import force_locale, get_current_locale, IndicoLocale, make_bound_gettext, make_bound_ngettext
from indico.util.i18n import gettext as core_gettext
from indico.core.plugins import IndicoPlugin, IndicoPluginBlueprint
from indico.web.forms.base import IndicoForm
from indico.web.rh import RH
from indico.web.views import WPDecorated, WPJinjaMixin

gettext = _ = make_bound_gettext('example')
ngettext = make_bound_ngettext('example')


class WPTestView(WPJinjaMixin, WPDecorated):
    """Base WP for Public view on DutyStation."""

    template_prefix = 'example:/'

    def _get_body(self, params):
        return self._get_page_content(params)


class SettingsForm(IndicoForm):
    dummy_message = StringField('Dummy Message')
    show_message = BooleanField('Show Message')


class ExamplePlugin(IndicoPlugin):
    """Example Plugin

    An example plugin that demonstrates the capabilities of the new Indico plugin system.
    """

    configurable = True
    settings_form = SettingsForm
    default_settings = {'dummy_message': '',
                        'show_message': False}

    def init(self):
        super(ExamplePlugin, self).init()
        self.inject_bundle('main.js')
        self.inject_bundle('main.css')
        self.inject_bundle('test.js', WPTestView)
        self.connect(signals.plugin.shell_context, self._extend_shell_context)
        self.connect(signals.plugin.cli, self._add_cli)

    def get_blueprints(self):
        return blueprint

    def _add_cli(self, sender):
        @cli_command()
        def example():
            """Example command from example plugin"""
            with current_app.test_request_context():
                with force_locale('es_ES'):
                    print(_('example plugin says hi'), current_plugin)
                    if self.settings.get('show_message'):
                        print(self.settings.get('dummy_message'))

        @cli_group(invoke_without_command=True)
        def examples():
            """Example group from example plugin"""
            print('root', current_plugin)

        @examples.command()
        def a():
            print('a', current_plugin)

        @examples.command()
        def b():
            print('b', current_plugin)

        yield example
        yield examples

    def _extend_shell_context(self, sender, add_to_context, add_to_context_multi, **kwargs):
        add_to_context('bar', name='foo', doc='foobar from example plugin', color='magenta!')
        from flask import render_template, render_template_string
        add_to_context(render_template, color='magenta!')
        add_to_context(render_template_string, color='magenta!')


blueprint = IndicoPluginBlueprint('example', __name__)


class WPExample(WPDecorated):

    def _get_body(self, params):
        locale = get_current_locale()
        params['language'] = IndicoLocale.parse('en').languages[locale.language]
        params['python_msg_core_i18n'] = core_gettext('Hello world!')
        params['python_msg_plugin_i18n'] = _('Hello world!')
        return render_plugin_template('example:example.html', **params)


class RHExample(RH):
    def _process(self):
        return WPExample(self, foo=u'bar').display()


class RHTest(RH):
    def _process(self):
        return WPTestView.render_template('test.html')


blueprint.add_url_rule('/example', 'example', view_func=RHExample)
blueprint.add_url_rule('/example/x', 'example', view_func=RHExample)
blueprint.add_url_rule('/test', 'test', view_func=RHTest)
