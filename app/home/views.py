from . import home


@home.route('/')
def index():
    return "<h1 style='color:green'>home</h1"
