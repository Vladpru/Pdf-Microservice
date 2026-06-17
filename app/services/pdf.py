from pathlib import Path
from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from app.schemas.payload import EntityPayload

_templates_dir = Path(__file__).parent.parent / "templates"
_static_dir = Path(__file__).parent.parent.parent / "static"

_jinja_env = Environment(loader=FileSystemLoader(str(_templates_dir)))


def render_pdf(payload: EntityPayload) -> bytes:
    template_name = f"{payload.entity_type}.html"
    template = _jinja_env.get_template(template_name)

    html_content = template.render(
        **payload.model_dump(),
        static_url=_static_dir.as_uri(),
        export_date=datetime.now(timezone.utc).strftime("%B %d, %Y"),
    )

    css = CSS(filename=str(_static_dir / "styles.css"))
    return HTML(string=html_content, base_url=str(_static_dir)).write_pdf(stylesheets=[css])
