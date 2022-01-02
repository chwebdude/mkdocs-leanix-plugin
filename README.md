# MkDocs LeanIX Plugin

This is a plugin for [MkDocs](mkdocs) to display data from [LeanIX](leanix).

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

## Configuration

* `api_token` - The API token
* `baseurl` - Base URL of your LeanIX instance. Can be `https://yourorganization.leanix.net`
* `workspaceid` - ID of your workspace. This is a GUID and is used do get user information
* `material` [optional] - Set this to `true` if the material design template should be used. This requires the `pymdownx.tabbed` extension to be enabled

## Usage

Simply create a code block of the type `leanix-factsheet` and insert the GUID of the factsheet to be shown:

### Sample

````markdown
```leanix-factsheet
d3bdeca8-8f79-4ee9-af4b-e390accf9f3d
```
````
#### Overview

![Overview](https://raw.githubusercontent.com/chwebdude/mkdocs-leanix-plugin/master/docs/img/Overview.png)

#### Documents

![Documents](https://raw.githubusercontent.com/chwebdude/mkdocs-leanix-plugin/master/docs/img/Documents.png)

#### Subscriptions

![Subscriptions](https://raw.githubusercontent.com/chwebdude/mkdocs-leanix-plugin/master/docs/img/Subscriptions.png)

#### Lifecycle

![Lifecycle](https://raw.githubusercontent.com/chwebdude/mkdocs-leanix-plugin/master/docs/img/Lifecycle.png)

[mkdocs]: https://www.mkdocs.org/
[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[mkdocs-block]: https://www.mkdocs.org/user-guide/styling-your-docs/#overriding-template-blocks
[leanix]: https://www.leanix.net/
