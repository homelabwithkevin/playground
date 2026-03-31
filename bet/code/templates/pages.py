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


def about(app_name, slogan):
    """Generate the about page with satirical content."""
    return f"""
    <html>
        <head>
            <title>About {app_name}</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        </head>
        <body class="bg-slate-900">
            <div class="flex justify-center pt-4 px-2 sm:px-0">
                <div class="w-full max-w-4xl">
                    <a href="/" class="text-blue-400 hover:text-blue-300 mb-4 inline-block">← Back to home</a>
                    <div class="bg-slate-700 p-8 rounded-xl text-white space-y-6">
                        <h1 class="text-4xl font-bold">About {app_name}</h1>

                        <div class="space-y-4">
                            <h2 class="text-2xl font-semibold text-blue-400">Our Mission</h2>
                            <p>We believe that the best way to make important life decisions is to gamble on them with your friends. Why have productive conversations when you can have <span class="italic">betting rounds</span>?</p>
                            <p>Our platform is designed with one core principle in mind: <span class="font-bold">democratizing disagreement through quantifiable loss</span>.</p>
                        </div>

                        <div class="space-y-4">
                            <h2 class="text-2xl font-semibold text-blue-400">How We Operate</h2>
                            <p>We've streamlined the ancient art of wagering down to its purest form:</p>
                            <ol class="list-decimal list-inside space-y-2 ml-2">
                                <li>Create a bet about something that matters (or doesn't)</li>
                                <li>Convince others they're wrong</li>
                                <li>Watch votes accumulate in real-time like a stock ticker for bad decisions</li>
                                <li>Feel a sense of accomplishment regardless of the outcome</li>
                            </ol>
                        </div>

                        <div class="space-y-4">
                            <h2 class="text-2xl font-semibold text-blue-400">Why Bets?</h2>
                            <p>Traditional polling is boring. Surveys are slow. Asking people directly what they think requires effort and listening skills.</p>
                            <p>But bets? Bets cut right to the chase. They tell us not just what people think, but what they're <span class="font-bold">willing to stake on it</span>. It's the same principle as the stock market, except with lower stakes and higher confidence in incorrect predictions.</p>
                        </div>

                        <div class="space-y-4">
                            <h2 class="text-2xl font-semibold text-blue-400">Our Track Record</h2>
                            <p>We've successfully enabled thousands of people to document their poor judgment. Our users report a 99.7% satisfaction rate with how clearly they can see in hindsight that they were wrong.</p>
                        </div>

                        <div class="space-y-4">
                            <h2 class="text-2xl font-semibold text-blue-400">Data & Privacy</h2>
                            <p>We store your betting history in a database somewhere. We take your privacy very seriously—so seriously that we don't know where your data is either. What we do know is that it's probably fine.</p>
                            <p><span class="text-gray-400 text-sm">(All votes are recorded. Forever. There is no forgetting.</span>)</p>
                        </div>

                        <div class="space-y-4">
                            <h2 class="text-2xl font-semibold text-blue-400">Contact Us</h2>
                            <p>Have questions? Feature requests? Complaints about your poor decision-making? Unfortunately, we can't help with the last one. That's on you.</p>
                        </div>

                        <div class="mt-8 pt-6 border-t border-slate-600 text-center text-sm text-gray-400">
                            <p>{app_name}: <span class="italic">"{slogan}"</span></p>
                            <p class="mt-2">Making Bets Since We Could Afford the AWS Bill</p>
                        </div>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """