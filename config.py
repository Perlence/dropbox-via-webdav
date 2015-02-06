def _setup():
    import json
    from os import path
    from warnings import warn

    def relopen(name, *args, **kwargs):
        return open(path.join(path.dirname(__file__), name), *args, **kwargs)

    with relopen('default.json') as default:
        config = json.load(default)
    try:
        with relopen('config.json') as config_fp:
            config.update(json.load(config_fp))
    except IOError:
        warn('user config is missing')

    return config

globals().update(_setup())
del _setup
