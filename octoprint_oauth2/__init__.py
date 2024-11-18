"""
This initialize plugin for authorization using framework OAuth 2.0
for application OctoPrint
"""
import logging
from octoprint import plugin
from octoprint_oauth2.oauth_user_manager import OAuthBasedUserManager


class OAuth2Plugin(plugin.StartupPlugin, plugin.TemplatePlugin,
                   plugin.SettingsPlugin, plugin.AssetPlugin):
    """
    Class for OAuth2 plugin for application OctoPrint
    """

    # Template plugin mixin
    def get_template_configs(self):
        """
        Plugin sets used templates
        """
        self._logger.info("OAuth 2.0 get template configs")
        return [{"type": "navbar", "template": "oauth2_login.jinja2",
                 "custom_bindings": False, "replaces": "login"}]

    # Asset plugin mixin
    def get_assets(self):
        """
        Plugin sets assets
        """
        self._logger.info("OAuth 2.0 get assets")
        return {"js": ["js/oauth2.js"]}

    def get_settings_defaults(self):
        config =dict(
                access_token_query_key = "token",
                endpoint1 = {
                    "client_id": 0,
                    "client_secret": "12345"
                    },
                login_path = "http://login/",
                token_headers = {
                    "Accept": "application/json"
                    },
                token_path = "http://token/",
                user_info_path = "http://userinfo",
                username_key = "profile"
                )
        self._logger.info(f"Config is of type: {dir(config)}")
        return config


    def get_settings_restricted_paths(self):
        """
        Plugin set restricted paths of config.yaml
        """
        return {"admin": [["plugins", "oauth2"]]}

    def on_after_startup(self):
        self._logger.info("Oauth2 Loaded and ready")


def user_factory_hook(components, settings, *args, **kwargs):
    """
    User factory hook, to initialize OAuthBasedUserManager, which controls login users
    """
    logging.getLogger("octoprint.plugins." + __name__).info(
        "OAuth 2.0 hooking OAuthBasedUserManager")
    return OAuthBasedUserManager(components, settings)


__plugin_name__ = "OAuth"
__plugin_pythoncompat__ = ">=3,<4"
__plugin_implementation__ = OAuth2Plugin()
__plugin_hooks__ = {
    "octoprint.access.users.factory": user_factory_hook
}