import fastapi_tags as ft


def test_atag_no_attrs_no_children():
    assert ft.A().render() == "<a></a>"


def test_atag_yes_attrs_no_children():
    tag = ft.A(href="/", cls="link").render()
    assert tag == '<a href="/" class="link"></a>'


def test_atag_yes_attrs_text_children():
    tag = ft.A("Link here", href="/", cls="link").render()
    assert tag == '<a href="/" class="link">Link here</a>'


def test_divtag_yes_attrs_a_child():
    html = ft.Div(ft.A("Link here", href="/", cls="link")).render()
    assert html == '<div><a href="/" class="link">Link here</a></div>'


def test_divtag_yes_attrs_multiple_a_children():
    html = ft.Div(
        ft.A("Link here", href="/", cls="link"),
        ft.A("Another link", href="/", cls="timid"),
    ).render()
    assert (
        html
        == '<div><a href="/" class="link">Link here</a><a href="/" class="timid">Another link</a></div>'
    )


def test_divtag_yes_attrs_nested_children():
    html = ft.Div(
        ft.P(
            "Links are here",
            ft.A("Link here", href="/", cls="link"),
            ft.A("Another link", href="/", cls="timid"),
        )
    ).render()
    assert (
        html
        == '<div><p>Links are here<a href="/" class="link">Link here</a><a href="/" class="timid">Another link</a></p></div>'
    )


def test_tag_types():
    assert issubclass(ft.A, ft.FTag)
    assert issubclass(ft.Div, ft.FTag)
    assert issubclass(ft.P, ft.FTag)


def test_subclassing():
    class AwesomeP(ft.P):
        def render(self) -> str:
            return f"<p{self.attrs}>AWESOME {self.children}!</p>"

    assert AwesomeP("library").render() == "<p>AWESOME library!</p>"


def test_subclassing_nested():
    class AwesomeP(ft.P):
        def render(self) -> str:
            return f"<p{self.attrs}>AWESOME {self.children}!</p>"

    html = ft.Div(AwesomeP("library")).render()
    assert html == "<div><p>AWESOME library!</p></div>"


def test_text_child_with_sibling_elements():
    html = ft.P("This is a", ft.Strong("cut off"), "sentence").render()
    assert html == "<p>This is a<strong>cut off</strong>sentence</p>"
