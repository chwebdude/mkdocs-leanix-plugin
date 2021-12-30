## {{ fs.displayName }}

=== "Overview"    
    {{ fs.description | replace("\n", "\n\t") }}

    {% for tag in fs.tags %} <span style="background-color:{{ tag.bgColor }}; border-radius: 0.25em; display: inline-block; padding: .25em .4em; font-size: 75%; color:{{ get_font_color(tag.bgColor) }}">{{ tag.name }}</span> {% endfor %}

{% if fs.documents %}
=== "Documents"
    {% for document in fs.documents %}
    * [{{ document.name }}]({{ document.url }})
    {% endfor %}
{% endif %}

{% if fs.subscriptions %}
=== "Subscriptions"
    {% for subs in fs.subscriptions %}
    * {{ get_user(subs.userId) }} {% for role in subs.linkedRoles %}<span style="background-color:grey; border-radius: 0.25em; display: inline-block; padding: .25em .4em; font-size: 75%; color: #fff">{{ role.name }}</span> {% endfor %}
    {% endfor %}
{% endif %}