from typing import Dict, List, Literal


class Prompt:
    def __init__(
        self,
        template: str,
        input_variables: List[str],
        output_type: Literal["text", "json"],
        output_field: str,
    ):
        self.template = template
        self.input_variables = input_variables
        self.output_type = output_type
        self.output_field = output_field

    def render(self, input_parameters: Dict[str, str]) -> str:
        for key, _ in input_parameters.items():
            if key not in self.input_variables:
                raise ValueError(f"Invalid input variable: {key}")
        return self.template.format(**input_parameters)
