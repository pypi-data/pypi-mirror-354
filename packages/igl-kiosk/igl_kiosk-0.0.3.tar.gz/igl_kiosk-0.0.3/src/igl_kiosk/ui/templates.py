"""
HTML templates for the web display application.
"""


def get_welcome_html():
    """Get the welcome page HTML."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fullscreen Web Display</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                text-align: center;
            }
            .container {
                max-width: 800px;
                padding: 40px;
            }
            h1 {
                font-size: 3em;
                margin-bottom: 30px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .info {
                font-size: 1.2em;
                line-height: 1.6;
                margin-bottom: 30px;
            }
            .command-example {
                background: rgba(0,0,0,0.3);
                padding: 20px;
                border-radius: 10px;
                font-family: monospace;
                font-size: 1.1em;
                margin: 20px 0;
            }
            .shortcuts {
                margin-top: 40px;
                font-size: 1em;
                opacity: 0.8;
            }
            .status {
                position: fixed;
                top: 20px;
                right: 20px;
                background: rgba(0,0,0,0.5);
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌐 Fullscreen Web Display</h1>
            <div class="info">
                Ready to display websites injected via external commands!<br>
                <small>Pages load in background and display when fully loaded</small>
            </div>
            <div class="command-example">
                Command file: web_display_commands.json<br>
                Format: {"url": "https://example.com"}
            </div>
            <div class="shortcuts">
                <strong>Keyboard Shortcuts:</strong><br>
                ESC - Exit • F11 - Toggle Fullscreen • Ctrl+R - Reload
            </div>
        </div>
        <div class="status" id="status">Ready</div>
    </body>
    </html>
    """


def get_loading_status_script(message):
    """Get JavaScript to update loading status."""
    return f"""
    (function() {{
        var statusDiv = document.getElementById('status');
        if (statusDiv) {{
            statusDiv.textContent = '{message}';
            statusDiv.style.background = 'rgba(255, 165, 0, 0.8)';
        }}
    }})();
    """
