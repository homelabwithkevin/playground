def header(app_name):
    categories = [
        "New",
        "Sayings",
        "Mentions",
        "Tech",
    ]

    category_html = ""

    for category in categories:
        html = f"""
        <div>
            {category}
        </div>
        """
        category_html += html

    return f"""
    <div>
        {app_name}
    </div>
    <div class="grid grid-cols-4 gap-4 pt-4">
        {category_html}
    </div>
    """