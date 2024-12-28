def create_html(year, data, all_years, home=False):
    file_name = None
    if not home:
        file_name = f'{year}.html'
    else:
        file_name = f'index.html'

    header = f"""
    <html>
        <head>
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://unpkg.com/htmx.org@2.0.2"></script>
            <title>Jane Pictures of {year}</title>
        </head>
        <div class="flex justify-center mt-8 max-w-[400px] lg:max-w-full">
        <div class="grid grid-flow-rows max-w-[380px] lg:max-w-[1000px]">
    """

    home_html = f"""
        <div class="mb-3">
            <p>
                Welcome to Jane's Pictures.
            </p>
            <p>
                RIP October 2024
            </p>
            <p>
                <img src="{ cdn_url + '/' + '2023/xbgmzdilop.jpg'}" class="max-h-[600px]">
            </p>
        </div>
    """

    year_html = ""

    for y in all_years:
        y_name = y
        html_file = f'{y}.html'

        if y == 'home':
            html_file = 'index.html'

        year_html += f"""
        <div class="mb-3">
            <div>
                <a href={html_file} target="_blank">{y_name}</a>
            </div>
        </div>
        """

    if not home:
        images = ""
        for image in data:
            images += f"""
            <div class="mb-6">
                <div>
                    <img src="{ cdn_url + '/' + image['cdn_path']}" loading="lazy" class="max-h-[600px]">
                </div>
            </div>
            """

    end = f"""
    </html>
    """
    if not home:
        content = header + year_html + images + end
    else:
        content = header + year_html + home_html + end

    with open(file_name, 'w') as f:
        f.write(content)

    print(f'Wrote {file_name}')