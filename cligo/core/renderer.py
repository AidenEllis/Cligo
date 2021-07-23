from jinja2 import Environment, BaseLoader, StrictUndefined, Undefined


__all__ = ['render_template']

policies = {"forbid": StrictUndefined, "allow": Undefined}


def render_template(template: str, context: dict, undefined="allow") -> str:
    template = Environment(
        loader=BaseLoader(), undefined=policies[undefined]
    ).from_string(template)
    return template.render(context)
