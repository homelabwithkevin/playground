def event(title, over, under):
    return f"""

    <div class="pt-4">
        <div class="box-border size-32 border-4 p-4">
            <div class="title">{title}</div>
            <button>Over: {over}</button>
            <button>Under: {under}</button>
        </div>
    </div>
    """

def events(items):
    item_html = ""
    for item in items:
        html = f"""
        <div class="box-border size-32 border-4 p-4">
            <div class='mb-2'>{item['title']}</div>
            <div class="grid grid-cols-2 gap-4">
                <div>Under</div>
                <div class='pl-4'>{item['under']}</div>
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div>Over</div>
                <div class='pl-4'>{item['over']}</div>
            </div>
        </div>
        """
        item_html += html

    return f"""
    <div class="pt-4 grid grid-cols-4 gap-4">
        {item_html}
    </div>
    """
