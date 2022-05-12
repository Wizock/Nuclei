from ..views import compression_service_blueprint

@compression_service_blueprint.route('/video_compression/')
def video_compression_index():
    return 'Video compression index'

