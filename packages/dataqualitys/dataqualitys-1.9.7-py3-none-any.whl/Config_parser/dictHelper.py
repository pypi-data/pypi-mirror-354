def get_nested(config, path, default=None):
    keys = path.split(".")
    for key in keys:
        if isinstance(config, dict):
            config = config.get(key, default)
        else:
            return default
    return config









   # $env:AWS_ACCESS_KEY_ID = "AKIAQFLZDNPQ5FSZEAEA"
   # $env:AWS_SECRET_ACCESS_KEY = "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"
