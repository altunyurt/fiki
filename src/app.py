from flask import Flask, abort, make_response, render_template, redirect
from functools import cache
import frontmatter
import mistune
import typing as t

from core.config import config


app = Flask(__name__, template_folder="templates")
app.config.from_object(config)


class FikiRenderer(mistune.HTMLRenderer):
    def image(self, text: str, url: str, title: t.Optional[str] = None) -> str:
        img = super().image(text, url, title)

        # Wraps the <img> tag in an <a> tag pointing to the source
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{img}</a>'


# Create the markdown instance using your custom renderer
markdown = mistune.create_markdown(renderer=FikiRenderer())


@cache
def read_page(path, lang):
    data = frontmatter.load(path)
    return {
        "title": data["title"],
        "preview": data["preview"],
        "filename": path.parts[-1],
        "lang": lang,
        "content": data.content,
    }


@cache
def render_md(content: str):
    return markdown(content)


@app.get("/")
def get_index():
    return redirect("/en")


@app.get("/<string:lang>/<string:page>")
@app.get("/<string:lang>", defaults={"page": "index.md"})
def get_page(lang, page):

    safe_path = (config.PAGES_ROOT / lang / page).resolve()

    if not safe_path.is_relative_to(config.PAGES_ROOT):
        abort(403)  # Forbidden: Attempted to break out of the folder

    if not safe_path.is_file() or safe_path.suffix != ".md":
        abort(404)

    cdata = read_page(safe_path, lang)
    return render_template("page.jinja", content=render_md(cdata["content"]))


@cache
def make_listing(lang):
    results = []
    safe_path = (config.PAGES_ROOT / lang).resolve()
    for file in sorted(safe_path.glob("*.md")):
        cdata = read_page(file, lang)
        results.append(cdata)
    return results


@app.get("/robots.txt")
def robots():
    resp = make_response(
        """
# Allow all bots to see the site structure
User-agent: *
Allow: /
Allow: /llms.txt
""",
        200,
    )
    resp.mimetype = "text/plain"
    return resp


@app.get("/llms.txt")
def llms():
    with open("/llms.txt", "r") as f:
        resp = make_response(f.read(), 200)
        resp.mimetype = "text/plain"
    return resp


if __name__ == "__main__":
    host = "127.0.0.1" if config.DEVELOPMENT else "unix:///tmp/app.sock"
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    print(app.url_map)
    app.run(host=host, port=8081, debug=True)
