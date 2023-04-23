import shutil

from pathlib import Path
from jinja2 import Environment, FileSystemLoader


ROOT_PATH = Path(__file__).parent.absolute()

TEMPLATES_ROOT = ROOT_PATH / 'templates'
OUTPUT_ROOT = ROOT_PATH / 'site'

ENV = Environment(loader=FileSystemLoader(searchpath=TEMPLATES_ROOT))


if TEMPLATES_ROOT.exists():
    shutil.rmtree(TEMPLATES_ROOT)

shutil.copytree(OUTPUT_ROOT, OUTPUT_ROOT)


for path in TEMPLATES_ROOT.rglob("*.html"):
    template = ENV.get_template(path.relative_to(TEMPLATES_ROOT).as_posix())
    rendered_html = template.render()

    output_path = OUTPUT_ROOT / path.name
    output_path.write_text(rendered_html)


for path in OUTPUT_ROOT.rglob("_*.*"):
    if path.is_file():
        path.unlink()
