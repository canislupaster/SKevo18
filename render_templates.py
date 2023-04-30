import shutil
import json

from pathlib import Path
from jinja2 import Environment, FileSystemLoader


ROOT_PATH = Path(__file__).parent.absolute()

TEMPLATES_ROOT = ROOT_PATH / 'templates'
I18N_ROOT = ROOT_PATH / 'i18n'
OUTPUT_ROOT = ROOT_PATH / 'site'

ENV = Environment(loader=FileSystemLoader(searchpath=TEMPLATES_ROOT), keep_trailing_newline=True)



def main():
    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)


    for locale_path in I18N_ROOT.glob('*.json'):
        locale = locale_path.stem

        output_root = OUTPUT_ROOT / locale
        output_root.mkdir(parents=True, exist_ok=True)
        shutil.copytree(TEMPLATES_ROOT, output_root)


        for path in TEMPLATES_ROOT.rglob("*.html"):
            template = ENV.get_template(path.relative_to(TEMPLATES_ROOT).as_posix())
            rendered_html = template.render({'t': json.loads(locale_path.read_bytes()) })

            output_path = output_root / path.relative_to(TEMPLATES_ROOT)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(rendered_html.lstrip().encode('utf-8'))


    for path in OUTPUT_ROOT.rglob("_*.*"):
        path.unlink()



if __name__ == '__main__':
    main()
