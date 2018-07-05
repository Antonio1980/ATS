import execjs


def get_element_position(query):
    """
    Allows to inject any JS code.
    :param query: JS code string.
    """
    context = execjs.compile("""
    function get_position(element) {
    return element.position();
    }
    """)
    context.call("get_position", execjs.eval(query))