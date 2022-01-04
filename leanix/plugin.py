'''A MkDocs plugin to import data from LeanIX and render it as markdown'''
import logging
import os
import re
import requests
import jwt

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.exceptions import PluginError

from jinja2.environment import Template
from jinja2 import Environment, PackageLoader

env = Environment(
    loader=PackageLoader(__package__, "templates")
)

log = logging.getLogger(__name__)


class LeanIXPlugin(BasePlugin):
    """
    Plugin to fetch LeanIX Data and render it as markdown in MkDocs.
    """
    config_scheme = (
        ('api_token', config_options.Type(str, default=None)),
        ('base_url', config_options.Type(str, default='https://app.leanix.net')),
        ('material', config_options.Type(bool, default=None)),

    )

    factsheet_regex = r'(```leanix-factsheet\s*\n)(?P<id>\S*)\n((?P<template>\S*)\n)?(```)'
    rgba_regex = r'[rRgGbBaA]{3,4}\s*\(\s*(?P<red>\d{1,3})[,\s]*(?P<green>\d{1,3})[,\s]*(?P<blue>\d{1,3})[,\s]*.*\)'
    user_cache = {}
    use_material = False
    header = {}
    docs_dir = ''
    workspace_id = ''
    workspace_name = ''

    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_config(self, config, **kwargs):
        """
        Executed on plugin configuration from MkDocs
        """
        self.docs_dir = os.path.realpath(
            config['docs_dir'])  # save for template directory checking

        # Check if is material theme
        if self.config['material'] is None:
            log.debug('Autodetermine if material theme is used')
            if 'material' in config['theme'].name:
                self.use_material = True
            else:
                self.use_material = False
        else:
            log.debug('Use explicit configuration')
            self.use_material = self.config['material']
        log.debug("Material theme is %s ", self.use_material)

        # Check if api token is provided trough config or environment variable
        if self.config['api_token'] is None:
            envvar = os.environ.get('LEANIX_API_TOKEN')
            if envvar is None:
                raise PluginError(
                    "Could not find a LeanIX API Token in config or environment variable")
            self.config['api_token'] = envvar

        try:
            # or something else if you have a dedicated MTM instance - you will know it if that is the case and if you don't just use this one.
            auth_url = self.config['base_url'] + '/services/mtm/v1/oauth2/token'

            response = requests.post(auth_url,
                                     auth=('apitoken',
                                           self.config['api_token']),
                                     data={'grant_type': 'client_credentials'})
            # this merely throws an error, if Webserver does not respond with a '200 OK'
            response.raise_for_status()
            access_token = response.json()['access_token']

            auth_header = 'Bearer ' + access_token
            self.header = {'Authorization': auth_header}

            # Get workspace information from token
            token = jwt.decode(access_token, options={
                               "verify_signature": False})
            
            self.workspace_id = token['principal']['permission']['workspaceId']
            self.workspace_name = token['principal']['permission']['workspaceName']

            log.debug("Authenticated against LeanIX")
            log.info("Usering workspace %s with id %s",
                     self.workspace_name, self.workspace_id)
            return config
        except:
            log.exception(
                "Failed to authenticate against LeanIX - Verify that base_url and token are correct\n\n")
            raise

    def get_user(self, userid):
        """Gets a markdown mailto link for a user from the LeanIX user id.

        Args:
            userid (str): LeanIX User ID

        Returns:
            str: User displayname with mailto link.
        """
        if userid in self.user_cache:
            log.debug("Get cached user with ID %s", userid)
            return self.user_cache[userid]

        log.debug("Get User with ID %s", userid)
        url = self.config['base_url'] + "/services/mtm/v1/workspaces/" + \
            self.workspace_id + "/users/" + userid

        response = requests.get(url=url, headers=self.header)
        response.raise_for_status()
        user = response.json()['data']
        display_name = user['displayName']
        email = user['email']

        log.debug('Got %s', email)
        # Save user information in cache
        self.user_cache[userid] = f'[{display_name}](mailto:{email})'
        return self.user_cache[userid]

    def get_font_color(self, background):
        """Gets black or white color code depending of provided background color.

        Args:
            background (str): CSS color definition

        Returns:
            str: Black (#fff) or White (#000)
        """
        # Check if is rgba
        match = re.match(self.rgba_regex, background)
        if match:
            log.debug("Parse %s as rgb(a) value with regex", background)
            red = int(match.group('red'))
            green = int(match.group('green'))
            blue = int(match.group('blue'))

        else:
            log.debug("Parse %s as Hex value", background)
            # https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
            hue = background.lstrip('#').lower()
            rgb = tuple(int(hue[i:i+2], 16) for i in (0, 2, 4))
            red = rgb[0]
            green = rgb[1]
            blue = rgb[2]

        # Determine if white or black font should be used
        # https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color
        if (red * 0.299 + green * 0.587 + blue * 0.114) > 186:
            return "#000"
        return "#fff"

    def _factsheet(self, matchobj):
        # Load Template
        log.debug("Load template")
        if matchobj.group('template'):
            template_path = os.path.realpath(os.path.join(self.docs_dir, matchobj.group(
                'template')))  # Combine paths -> template must be inside of docs directory
            log.debug("Load specified template at %s", template_path)
            if not os.path.exists(template_path):  # Check if template exists
                log.error("The defined template '%s' must be stored inside of '%s'",
                          template_path, self.docs_dir)
                raise PluginError(
                    f"The defined template '{template_path}' could not be found. It must be stored inside of '{self.docs_dir}'")
            with open(template_path, "r") as template_file:
                template = Template(template_file.read())

        else:
            if self.config['material']:
                log.debug("Loading default material template")
                template = env.get_template("factsheet_material.jinja2")
            else:
                log.debug("Loading default template")
                template = env.get_template("factsheet.jinja2")

        # Load LeanIX Data
        log.debug("Quering factsheet %s", matchobj.group('id'))
        url = self.config['base_url'] + \
            "/services/pathfinder/v1/factSheets/" + matchobj.group('id')

        response = requests.get(url=url, headers=self.header)
        response.raise_for_status()

        factsheet = response.json()['data']

        return template.render(fs=factsheet, get_user=self.get_user, get_font_color=self.get_font_color, worskpace_id=self.workspace_id, workspace_name=self.workspace_name, base_url=self.config['base_url'])

    def on_page_markdown(self, markdown, **kwargs):
        """
        Called when markdown is generated in MkDocs
        """
        return re.sub(self.factsheet_regex, self._factsheet, markdown)
