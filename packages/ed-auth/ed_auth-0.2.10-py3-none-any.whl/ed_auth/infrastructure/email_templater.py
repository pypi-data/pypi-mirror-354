from jinja2 import Environment, FileSystemLoader

from ed_auth.application.contracts.infrastructure.abc_email_templater import \
    ABCEmailTemplater


class EmailTemplater(ABCEmailTemplater):
    def __init__(self) -> None:
        self._file_names: dict[str, str] = {
            "login": "login.html",
        }
        self._template_env = Environment(
            loader=FileSystemLoader("./email_templates"))

    def login(self, first_name: str, otp: str) -> str:
        template = self._load_template("login")
        return template.render(first_name=first_name, otp=otp)

    def _load_template(self, template_key: str):
        file_name = self._file_names.get(template_key)
        if not file_name:
            raise ValueError(f"Template key '{template_key}' not found.")
        return self._template_env.get_template(file_name)
