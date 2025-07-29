import requests
from flask import Response

executed = False  # ← مؤشر يتم ضبطه إذا تم التحقق


def flask_run():
    global executed
    executed = True

    try:
        key = "EJMSF-F6KKZ-B6HTO-99SP1"
        verify_url = f"http://license.wekabi.com:5040/verify?key={key}"
        r = requests.get(verify_url, timeout=10)
        result = r.json()

        if result.get("status") != True:
            print("🔒 License is invalid or not activated. Rendering activation page...")

            # Fetch activation page HTML content directly
            activation_html = requests.get("http://license.wekabi.com:5040/activation", timeout=10).text
            return Response(activation_html, mimetype='text/html')

    except Exception as e:
        print("❌ Error while verifying license:", e)
        fallback_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>License Verification Error</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 50px;
                    background-color: #f4f4f4;
                }
                .card {
                    background: white;
                    max-width: 500px;
                    margin: auto;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #f0ad4e;
                    margin-bottom: 20px;
                }
                p {
                    color: #333;
                    line-height: 1.8;
                }
                .btn {
                    display: inline-block;
                    margin-top: 25px;
                    padding: 12px 25px;
                    background: #0275d8;
                    color: white;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: bold;
                    transition: background 0.3s;
                }
                .btn:hover {
                    background: #025aa5;
                }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>⚠️ License Verification Error</h1>
                <p>
                    We were unable to verify your license at this time.<br>
                    This could be due to a network issue or the verification server being temporarily unavailable.
                </p>
                <p>
                    Please check your internet connection and try again shortly.<br>
                    If the issue persists, contact our support team.
                </p>
                <a class="btn" href="mailto:support@wekabi.com">📧 Contact Support</a>
            </div>
        </body>
        </html>
        """
        return Response(fallback_html, mimetype='text/html')
