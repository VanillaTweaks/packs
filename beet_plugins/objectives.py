import json
import re
from functools import cache

from beet import Context
from mecha import AstObjective, Mecha, Visitor, rule

# TODO: from minecraft_text_components import TextComponent
TextComponent = object

NAME = r"[a-z0-9]+(?:_[a-z0-9]+)*"
RESOURCE_LOCATION = rf"({NAME})(:{NAME}(?:/{NAME})*)?"
OBJECTIVE_NAME = r"([-+._0-9A-Za-z]+)"
OBJECTIVE_CRITERION = r"([._:A-Z_a-z])"
OBJECTIVE_DISPLAY = r"(.+)"
OBJECTIVE_KEY = re.compile(
    rf"^{RESOURCE_LOCATION}( |\.){OBJECTIVE_NAME}"
    rf"(?: {OBJECTIVE_CRITERION}(?: {OBJECTIVE_DISPLAY}))$"
)


class ObjectiveData:
    resource_location: str
    name: str
    criterion: str = "dummy"
    display: TextComponent | None = None

    def __init__(self, ctx: Context, value: str):
        match = OBJECTIVE_KEY.match(value)
        if match is None:
            raise ValueError(
                "The following `config.yaml` objective value does not match the pattern"
                ' `rf"^{RESOURCE_LOCATION}( |\\.){OBJECTIVE_NAME}(?: '
                f'{{OBJECTIVE_CRITERION}}(?: {{OBJECTIVE_DISPLAY}}))$"`:\n{repr(value)}'
            )

        namespace, colon_and_path, separator, name, criterion, display = match.groups()

        if namespace == "vt":
            namespace = "vanillatweaks"
        elif namespace == "pack":
            namespace = ctx.project_id

        resource_location = namespace + colon_and_path

        namespaced = separator == "."
        if namespaced:
            name = resource_location.replace(":", ".").replace("/", ".") + "." + name

        self.resource_location = resource_location
        self.name = name
        if criterion:
            self.criterion = criterion
        if display:
            self.display = json.loads(display)

    def __hash__(self):
        return hash(self.name)


# A mapping from the name of each objective defined in the `config.yaml` files of both
#  `lib` and the pack to that objective's data.
config_objectives: dict[str, ObjectiveData] = {}
# All objectives used in the pack to that objective's data.
used_objectives = set[ObjectiveData]()


class ObjectiveVisitor(Visitor):
    @rule(AstObjective)
    @cache
    def objective(self, node: AstObjective):
        objective_name = node.value

        if objective_name in config_objectives:
            used_objectives.add(config_objectives[objective_name])


def beet_default(ctx: Context):
    mech = ctx.inject(Mecha)

    config_objective_values = frozenset[str](
        *ctx.meta["pack_config"]["objectives"], *ctx.meta["lib_config"]["objectives"]
    )

    for value in config_objective_values:
        objective = ObjectiveData(ctx, value)
        config_objectives[objective.name] = objective

    ctx.meta["objectives"] = used_objectives

    objective_visitor = ObjectiveVisitor()
    mech.steps.insert(0, objective_visitor)

    _, data = ctx.packs
    data.mount(
        "data/vanillatweaks/modules/datapacks",
        "../../../lib/datapacks/objectives.bolt",
    )
