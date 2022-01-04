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
* `base_url` - Base URL of your LeanIX instance. Can be `https://yourorganization.leanix.net`
* `material` [optional] - Set this to `true` if the material design template should be used. This requires the `pymdownx.tabbed` extension to be enabled

Alternatively to the `api_token` in the `mkdocs.yml` a environment variable called `LEANIX_API_TOKEN` can be set. This is likely the way in CI/CD scenarios.

Workspace information (name and id) is retrived from the JWT token.

### Sample

```yaml
plugins
  - leanix:
      api_token: asdfsa23kjlsadflkjsalkjf3 # or LEANIX_API_TOKEN environment variable
      base_url: https://yourcompany.leanix.net/
      workspace_name: test
```

## Usage

Simply create a code block of the type `leanix-factsheet` and insert the GUID of the factsheet to be shown:

### Sample

````markdown
```leanix-factsheet
d3bdeca8-8f79-4ee9-af4b-e390accf9f3d
```
````

### Customization

Own templates can be used. Add the path to the template after the factsheet GUID. The template must be inside the docs directory.

````markdown
```leanix-factsheet
d3bdeca8-8f79-4ee9-af4b-e390accf9f3d
templates/custom_factsheet.jinja2
```
````

Get some inspiration of the [packed templates](gh-templates). A factsheet object will be provided as `fs` and can be printed out with `{{ fs }}`. Two helper functions are provided:

* `get_user(userid)` - Gets friendly username from LeanIX and creates a Markdown mailto-link.
* `get_font_color(backgroundColor)` - Gets a black or white CSS color from a provided CSS background color. Can be used to ensure enough contrast between text and background color.

## Screenshots

### Overview

![Overview](https://raw.githubusercontent.com/chwebdude/mkdocs-leanix-plugin/master/docs/img/Overview.png)

### Documents

![Documents](https://raw.githubusercontent.com/chwebdude/mkdocs-leanix-plugin/master/docs/img/Documents.png)

### Subscriptions

![Subscriptions](https://raw.githubusercontent.com/chwebdude/mkdocs-leanix-plugin/master/docs/img/Subscriptions.png)

### Lifecycle

![Lifecycle](https://raw.githubusercontent.com/chwebdude/mkdocs-leanix-plugin/master/docs/img/Lifecycle.png)

[mkdocs]: https://www.mkdocs.org/
[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[mkdocs-block]: https://www.mkdocs.org/user-guide/styling-your-docs/#overriding-template-blocks
[leanix]: https://www.leanix.net/
[gh-templates]: https://github.com/chwebdude/mkdocs-leanix-plugin/tree/master/leanix/templates
