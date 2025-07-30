# Fullscreen Web Display

A PyQt6-based fullscreen web browser that can receive URLs via external commands, perfect for kiosk displays, digital signage, or presentation systems.

## Features

- **Fullscreen Display**: Runs in fullscreen mode by default
- **External URL Injection**: Load websites by updating a JSON command file
- **Background Loading**: Pages load in the background and display when fully loaded
- **Keyboard Shortcuts**: ESC to exit, F11 to toggle fullscreen, Ctrl+R to reload
- **Error Handling**: Graceful handling of loading failures
- **Clean Architecture**: Well-organized, modular codebase

## Installation

### From Source

1. Clone the repository:

```bash
git clone https://github.com/yourusername/fullscreen-web-display.git
cd fullscreen-web-display
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install the package:

```bash
pip install -e .
```

### Using pip (if published)

```bash
pip install fullscreen-web-display
```

## Usage

### Running the Application

```bash
# If installed via pip
fullscreen-web-display

# Or run directly
python -m fullscreen_web_display.main
```

### Displaying Websites

The application monitors a JSON file called `web_display_commands.json` in the current directory. To display a website:

1. Create or edit the `web_display_commands.json` file:

```json
{
  "url": "https://example.com"
}
```

2. The application will automatically detect the change and load the website in the background
3. Once fully loaded, it will switch to display the new page

### Keyboard Shortcuts

- **ESC**: Exit the application
- **F11**: Toggle fullscreen mode
- **Ctrl+R**: Reload the current page

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

The project follows PEP 8 guidelines. Use tools like `black` or `autopep8` for formatting:

```bash
black src/
```

### Adding Features

1. Fork the repository
2. Create a feature branch
3. Add your changes in reasonable commits
4. Add tests for new functionality
5. Submit a pull request

## Requirements

- Python 3.8+
- PyQt6 >= 6.4.0
- PyQt6-WebEngine >= 6.4.0

## Use Cases

- **Digital Signage**: Display rotating web content on screens
- **Kiosk Systems**: Show specific web applications in fullscreen
- **Presentation Systems**: Display web-based presentations
- **Monitoring Dashboards**: Show real-time web dashboards
- **Remote Display Control**: Control what's displayed from external scripts

## Troubleshooting

### Common Issues

1. **PyQt6 Installation**: Make sure you have PyQt6 and PyQt6-WebEngine installed
2. **File Permissions**: Ensure the application can create and monitor the JSON file
3. **Network Issues**: Check internet connectivity if pages fail to load

### Debug Mode

Set the environment variable `DEBUG=1` to enable verbose logging:

```bash
DEBUG=1 fullscreen-web-display
```

## License

This project is currently copyrighted by me but contributions are very welcome.
I just have to find the right open source license.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Changelog

### v1.0.0

- Initial release
- Fullscreen web display functionality
- External URL injection via JSON file
- Background loading
- Keyboard shortcuts
- Modular architecture