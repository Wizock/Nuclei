from flask import Response, redirect, render_template, url_for

from ...extension_globals.database import db
from .main import video_compression_blueprint
from .models import video_media


@video_compression_blueprint.route(
    "/video/<int:id>/<string:name>", methods=["GET", "POST"]
)
def view_video(id: int, name: str) -> Response:
    try:
        video_query = video_media.query.filter_by(id=id, name=name).first()
        return render_template("video_player.html", video_query=video_query)
    except AttributeError:
        if not video_query:
            return redirect(url_for("index_endpoint.index_design")), 400
        else:
            return render_template(
                "video_player.html", video_query=ValueError("Video not found")
            )


@video_compression_blueprint.route(
    "/delete/<int:id>/<string:name>", methods=["GET", "POST"]
)
def delete_video(id: int, name: str) -> Response:
    try:
        video_query: video_media = video_media.query.filter_by(id=id, name=name).first()
        db.session.delete(video_query)
        db.session.commit()
        return redirect(url_for("index_endpoint.index_design")), 200
    except AttributeError:
        if not video_query:
            return redirect(url_for("index_endpoint.index_design")), 400
        else:
            return render_template(
                "video_player.html", video_query=ValueError("Video not found")
            )
