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
    <div class="bg-slate-700 p-6 items-center justify-center rounded-xl">
    <div>
        <!-- Main Card -->
        <div class="card-gradient rounded-xl p-6 space-y-5">
            <!-- Header with Avatar and Chance Badge -->
            <div class="flex items-start justify-between gap-4">
                <div class="flex-1">
                    <h2 class="question-text text-white text-lg">{item['title']}</h2>
                </div>
            </div>
            
            <!-- Vote Buttons -->
            <div class="grid grid-cols-2 gap-3 pt-2">
                <button class="button-yes w-full bg-green-600 hover:bg-green-300 rounded-lg py-3 px-4 font-semibold text-white text-sm transition-all active:scale-95 cursor-pointer">
                    <span class="flex items-center justify-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                        </svg>
                        Yes
                    </span>
                </button>
                <button class="button-no w-full bg-red-700 hover:bg-red-400 rounded-lg py-3 px-4 font-semibold text-white text-sm transition-all active:scale-95 cursor-pointer">
                    <span class="flex items-center justify-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                        No
                    </span>
                </button>
            </div>
        </div>
    </div>
    </div>
        """
        item_html += html

    return f"""
    <div class="pt-4 grid grid-cols-4 gap-4">
        {item_html}
    </div>
    """
