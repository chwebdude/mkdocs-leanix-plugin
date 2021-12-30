## {{ fs.displayName }}

=== "Overview"    
    {{ fs.description | replace("\n", "\n\t") }}

    {% for tag in fs.tags %} <span style="background-color:{{ tag.bgColor }}; border-radius: 0.25em; display: inline-block; padding: .25em .4em; font-size: 75%">{{ tag.name }}</span> {% endfor %}

=== "Documents"
    {% for document in fs.documents %}
    * [{{ document.name }}]({{ document.url }})
    {% endfor %}

=== "Subscriptions"
{% for subs in fs.subscriptions %}
    * {{ get_user(subs.userId) }} {% for role in subs.linkedRoles %}<span style="background-color:grey; border-radius: 0.25em; display: inline-block; padding: .25em .4em; font-size: 75%; color: #fff">{{ role.name }}</span> {% endfor %}
{% endfor %}

    _Example_:

    ``` markdown
    1. Sed sagittis eleifend rutrum
    2. Donec vitae suscipit est
    3. Nulla tempor lobortis orci
    ```

    _Result_:

    1. Sed sagittis eleifend rutrum
    2. Donec vitae suscipit est
    3. Nulla tempor lobortis orci