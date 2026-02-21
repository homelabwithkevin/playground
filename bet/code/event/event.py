def generate_bar_chart(votes):
    yes_count = votes.get('yes', 0)
    no_count = votes.get('no', 0)
    total = yes_count + no_count

    if total == 0:
        yes_percent = 50
        no_percent = 50
    else:
        yes_percent = (yes_count / total) * 100
        no_percent = (no_count / total) * 100

    return f"""
        <div class="w-full bg-gray-700 rounded-lg h-8 flex overflow-hidden">
            <div class="bg-green-600 flex items-center justify-center text-white font-semibold text-sm leading-none" style="width: {yes_percent}%">
                {yes_percent:.0f}%
            </div>
            <div class="bg-red-700 flex items-center justify-center text-white font-semibold text-sm leading-none" style="width: {no_percent}%">
                {no_percent:.0f}%
            </div>
        </div>
    """


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


def generate_event_card(item):
    """Generate HTML for a single event card."""
    return f"""
    <div class="bg-slate-700 p-6 items-center justify-center rounded-xl" id="event-{item['index']}">
    <div>
        <!-- Main Card -->
        <div class="card-gradient rounded-xl p-6 space-y-5">
            <!-- Header with Avatar and Chance Badge -->
            <div class="flex items-start justify-between gap-4">
                <div class="flex-1">
                    <h2 class="question-text text-white text-lg">{item['title']} | {item['index']}</h2>
                </div>
            </div>

            <!-- Vote Buttons -->
            <div class="grid grid-cols-2 gap-3 pt-2">
                <button hx-post="/event/{item['index']}?vote=yes" hx-target="#event-{item['index']}" hx-swap="outerHTML" class="button-yes w-full bg-green-600 hover:bg-green-300 rounded-lg py-3 px-4 font-semibold text-white text-sm transition-all active:scale-95 cursor-pointer">
                    <span class="flex items-center justify-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                        </svg>
                        Yes ({item['votes'].get('yes', 0)})
                    </span>
                </button>
                <button hx-post="/event/{item['index']}?vote=no" hx-target="#event-{item['index']}" hx-swap="outerHTML" class="button-no w-full bg-red-700 hover:bg-red-400 rounded-lg py-3 px-4 font-semibold text-white text-sm transition-all active:scale-95 cursor-pointer">
                    <span class="flex items-center justify-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                        No ({item['votes'].get('no', 0)})
                    </span>
                </button>
            </div>

            <!-- Vote Distribution Bar Chart -->
            <div class="pt-4">
                {generate_bar_chart(item['votes'])}
            </div>
        </div>
    </div>
    </div>
    """


def events(items):
    item_html = ""
    for item in items:
        html = generate_event_card(item)
        item_html += html

    return f"""
    <div class="pt-4 grid grid-cols-4 gap-4">
        {item_html}
    </div>
    """
