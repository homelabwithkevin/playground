def header(app_name, slogan):
    categories = [
        '<a href="/about" class="text-blue-400 hover:text-blue-300">About</a>'
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
        {app_name} | {slogan}
    </div>
    <div class="grid grid-cols-4 gap-4 pt-4">
        {category_html}
    </div>
    """