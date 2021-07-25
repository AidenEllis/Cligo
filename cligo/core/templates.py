from cligo.core.renderer import render_template


def getCommandHelpTemplate(argsinfo, command_name):
    template = """{{ command }} usage:{% for argInfo in argsInfos.values() %}{% if argInfo.param_type == 'required' %} <{{ argInfo.name }}>{% else %} [{{ 
argInfo.name }}]{% endif %}{% endfor %}\n
Args:
{% for argInfo in argsInfos.values() -%}
{{ ' ' * command|length }} {{ argInfo.name }} {{ ' ' * argInfo.longest_name_len }} : type ({{ argInfo.type }}) {{ ' ' * 
argInfo.longest_type_len }} |  {{ argInfo.param_type }}  |  {{ 'default: ' if argInfo.default_value if 
argInfo.default_value }}{{ ' ' * 9 if not argInfo.default_value }}{{ argInfo.default_value if argInfo.default_value
}} {{ ' ' * argInfo.longest_default_value_len }} |  {{ 'keyword: ' if argInfo.keyword }}{{ argInfo.keyword if 
argInfo.keyword }}
{% endfor -%}"""

    argsinfo = argsinfo

    longest_name_len = 0
    longest_type_len = 0
    longest_default_value_len = 0

    for a in argsinfo.values():
        if a['default_value'] is True:
            a['default_value'] = 'True'

        elif a['default_value'] is False:
            a['default_value'] = 'False'

        elif a['default_value'] is None:
            a['default_value'] = 'None'

        if len(a['name']) > longest_name_len:
            longest_name_len = len(a['name'])

        if len(a['type']) > longest_type_len:
            longest_type_len = len(a['type'])

        if len(str(a['default_value'])) > longest_default_value_len:
            longest_default_value_len = len(str(a['default_value']))

    for k, v in argsinfo.items():
        a_ = longest_name_len - len(v['name'])
        argsinfo[k]['longest_name_len'] = a_

        b_ = longest_type_len - len(v['type'])
        argsinfo[k]['longest_type_len'] = b_
        c_ = longest_default_value_len - len(str(v['default_value']))
        argsinfo[k]['longest_default_value_len'] = c_

    context = {
        'command': command_name,
        'argsInfos': argsinfo
    }

    return render_template(template=template, context=context)
