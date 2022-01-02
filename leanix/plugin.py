'''A MkDocs plugin to import data from LeanIX and render it as markdown'''
import logging
import re
import requests


from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

from jinja2 import Environment, PackageLoader


env = Environment(
    loader=PackageLoader(__package__, "templates")

)

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class LeanIXPlugin(BasePlugin):
    config_scheme = (
        ('api_token', config_options.Type(str, default='')),
        ('baseurl', config_options.Type(str, default='https://app.leanix.net')),
        ('workspaceid', config_options.Type(str, default='')),
        ('material', config_options.Type(bool, default=None)),

    )

    factsheet_regex = r'(```leanix-factsheet\s*\n)(?P<id>.*)(\n```)'
    rgba_regex = r'[rRgGbBaA]{3,4}\s*\(\s*(?P<red>\d{1,3})[,\s]*(?P<green>\d{1,3})[,\s]*(?P<blue>\d{1,3})[,\s]*.*\)'
    user_cache = {}

    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_config(self, config, **kwargs):
        # Check if is material theme
        if self.config['material'] is None:
            log.debug('Autodetermine if material theme is used')

            if 'material' in config['theme'].name:
                self.useMaterial = True
            else:
                self.useMaterial = False
        else:
            log.debug('Use explicit configuration')
            self.useMaterial = self.config['material']
        log.debug("Material theme is %s ", self.useMaterial)

        try:
            # or something else if you have a dedicated MTM instance - you will know it if that is the case and if you don't just use this one.
            auth_url = self.config['baseurl'] + '/services/mtm/v1/oauth2/token'

            response = requests.post(auth_url,
                                     auth=('apitoken',
                                           self.config['api_token']),
                                     data={'grant_type': 'client_credentials'})
            # this merely throws an error, if Webserver does not respond with a '200 OK'
            response.raise_for_status()
            access_token = response.json()['access_token']

            auth_header = 'Bearer ' + access_token
            self.header = {'Authorization': auth_header}
            log.debug("Authenticated against LeanIX")
            return config
        except:
            log.exception("Failed to authenticate against LeanIX - Verify that baseURL and token are correct\n\n")
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
        url = self.config['baseurl'] + "/services/mtm/v1/workspaces/" + \
            self.config['workspaceid'] + "/users/" + userid
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
            log.debug(f'Parse {background} as rgb(a) value with regex')
            red = int(match.group('red'))
            green = int(match.group('green'))
            blue = int(match.group('blue'))

        else:
            log.debug(f'Parse {background} as Hex value')
            # https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
            h = background.lstrip('#').lower()
            rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            red = rgb[0]
            green = rgb[1]
            blue = rgb[2]

        # Determine if white or black font should be used
        # https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color
        if (red * 0.299 + green * 0.587 + blue * 0.114) > 186:
            return "#000"
        return "#fff"

    def _factsheet(self, matchobj):
        log.debug("Quering factsheet" + matchobj.group('id'))
        url = self.config['baseurl'] + \
            "/services/pathfinder/v1/factSheets/" + matchobj.group('id')

        response = requests.get(url=url, headers=self.header)
        response.raise_for_status()

        factsheet = response.json()['data']

        template = env.get_template("factsheet_material.md")
        return template.render(fs=factsheet, get_user=self.get_user, get_font_color=self.get_font_color)

    def on_page_markdown(self, markdown, **kwargs):
        return re.sub(self.factsheet_regex, self._factsheet, markdown)
        # return markdown

    # def on_page_content(self, html, page, config, files):
    #     return html

    # def on_page_context(self, context, page, config, nav):
    #     return context

    # def on_post_page(self, output_content, page, config):
    #     return output_content
