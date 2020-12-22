from eme.entities import load_settings

_gamecf = load_settings('core/content/config.ini')


def get_settings():
    return _gamecf


def getcfg(opts, default=None, cast=None):
    return _gamecf.get(opts, default, cast)
