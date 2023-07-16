from itertools import chain


def chain_buttons(data):
    button_slug = data.get("ButtonSlug", [])
    button_url = data.get("ButtonUrl", [])
    return chain(button_slug, button_url)


def sort_buttons(data):
    if next(chain_buttons(data), None) is None:
        return []
    max_order = max(button.get("order", 0) for button in chain_buttons(data))
    return sorted(
        chain_buttons(data),
        key=lambda button: (
            button.get("order", 0) or max_order + 1,
            button.get("cover_text", ""),
        ),
    )
