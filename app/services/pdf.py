from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
import markdown as md
from jinja2 import Environment, FileSystemLoader
from app.schemas.payload import EntityPayload

_templates_dir = Path(__file__).parent.parent / "templates"
_static_dir = Path(__file__).parent.parent.parent / "static"
_assets_dir = Path(__file__).parent.parent / "assets"

_jinja_env = Environment(loader=FileSystemLoader(str(_templates_dir)))
_md = md.Markdown(extensions=["extra"])


def _md_to_html(text: Optional[str]) -> str:
    if not text:
        return ""
    _md.reset()
    return _md.convert(text)


def render_pdf(payload: EntityPayload) -> bytes:
    from weasyprint import HTML, CSS

    template_name = f"{payload.entity_type}.html"
    template = _jinja_env.get_template(template_name)

    data = payload.model_dump()
    data["description"] = _md_to_html(data.get("description"))
    if data.get("ai_summary"):
        data["ai_summary"] = _md_to_html(data["ai_summary"])
    if data.get("comments"):
        for comment in data["comments"]:
            comment["body"] = _md_to_html(comment.get("body"))

    html_content = template.render(
        **data,
        static_url=_static_dir.as_uri(),
        assets_url=_assets_dir.as_uri(),
        export_date=datetime.now(timezone.utc).strftime("%B %d, %Y"),
    )

    css = CSS(filename=str(_static_dir / "styles.css"))
    pdf_bytes = HTML(string=html_content, base_url=str(_static_dir)).write_pdf(
        stylesheets=[css]
    )
    return pdf_bytes or b""
