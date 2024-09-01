def form_message(sub=None):
    return f"""
    <form hx-post="/Prod/post" hx-target="#result" hx-on::after-request="this.reset()" hx-indicator="#spinner">
        <div class="col-span-full">
            <div class="mt-4 p-4">
                <input id="user_id" value="{sub}" class="hidden">
                <p class="mt-3 text-sm leading-6 text-gray-600">Write a message</p>
                <textarea id="message" name="message" rows="3" class="block w-full rounded-md border-0 p-4 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"></textarea>
            </div>
        </div>

        <div class="mt-6 flex items-center justify-end gap-x-6">
            <button type="submit" hx-target="#result" hx-swap="#blank" class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Save</button>
        </div>
    </form>

    <div id="result"></div>
    <div id="blank"></div>
    <div id="spinner" class="htmx-indicator">Submitting...</div>
    """
