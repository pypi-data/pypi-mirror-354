# sopel-safety

A Sopel plugin providing alerts about malicious URLs.

_This is a continuation of Sopel's [built-in `safety` plugin][old-builtin]._

[old-builtin]: https://github.com/sopel-irc/sopel/blob/1c6aeb93a269a3997a9d55ec102a9ed77e393402/sopel/builtins/safety.py
[//]: # (`old-builtin` is also used in NEWS!)

## Installing

Releases are hosted on PyPI, so after installing Sopel, all you need is `pip`:

```shell
$ pip install sopel-safety
```

## Configuring

The easiest way to configure `sopel-safety` is via Sopel's configuration
wizard—simply run `sopel-plugins configure safety` and enter the values for
which it prompts you.

### Migrating from `sopel.builtins.safety`

Sopel's old built-in `safety` plugin had a setting called `enabled_by_default`,
which was deprecated in favor of a `default_mode` setting. This plugin doesn't
include any logic to handle the `enabled_by_default` value, and Sopel's logs
will warn about that setting if present in the config file.

**If you used to use the built-in `safety` plugin, you should delete
`enabled_by_default` from your config file and set `default_mode` to one of the
choices described below.**

**You can also safely delete the `malwaredomains.txt` file if it exists in your
Sopel bot's homedir.** Newer versions of `safety` (both the built-in plugin and
this continuation package) use `unsafedomains.txt` instead.

### Available options

* `default_mode` — Which operating mode to use in channels without a mode set.\
  Available options are 'off', 'local', 'local strict', 'on', and 'strict'.
* `known_good` — A list of "known good" domains or regexes to consider trusted.
* `vt_api_key` — Optional VirusTotal API key.\
  Providing this can improve malicious URL detection. Without it, this plugin
  will check against the domain blocklist only.
* `domain_blocklist_url` — Optional URL of an alternate domain blocklist.\
  This plugin uses [StevenBlack's unified hosts file][SBfile] by default, which
  aggregates known domains across adware and malware categories. This option can
  be used to specify [a different variant from the same repository][SBvars], or
  another compatible file maintained elsewhere.

[SBfile]: https://github.com/StevenBlack/hosts/blob/master/hosts
[SBvars]: https://github.com/StevenBlack/hosts#list-of-all-hosts-file-variants
