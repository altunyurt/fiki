from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
STATIC_ROOT = PROJECT_ROOT.joinpath("static/").resolve()
SITEMAPS_ROOT = STATIC_ROOT.joinpath("sitemaps/").resolve()
TEMPLATES_ROOT = PROJECT_ROOT.joinpath("templates").resolve()
PAGES_ROOT = PROJECT_ROOT.joinpath("pages").resolve()



