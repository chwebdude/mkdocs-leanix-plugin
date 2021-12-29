# mkdocs-leanix-plugin

This is a plugin for MkDocs to display data from LeanIX.

## Setup

Install the plugin using pip:

`pip install mkdocs-leanix-plugin`

Activate the plugin in `mkdocs.yml`:
```yaml
plugins:
  - leanix  
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [MkDocs documentation][mkdocs-plugins].

## Config

* `api_token` - The API token
* `baseurl` - Base URL of your LeanIX instance. Can be `https://yourorganization.leanix.net`

## Usage

## See Also

More information about templates [here][mkdocs-template].

More information about blocks [here][mkdocs-block].

[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[mkdocs-template]: https://www.mkdocs.org/user-guide/custom-themes/#template-variables
[mkdocs-block]: https://www.mkdocs.org/user-guide/styling-your-docs/#overriding-template-blocks
