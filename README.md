# Audio Accuracy Checker

A Django web application that analyzes audio files against DOCX scripts to check accuracy, identify missing words, wrong pronunciations, and provide detailed reports.

## Features

- **Speech-to-Text**: Uses OpenAI's Whisper AI for high-accuracy audio transcription
- **Script Analysis**: Extracts text from DOCX files for comparison
- **Word-by-Word Comparison**: Detailed analysis showing exactly where errors occur
- **Accuracy Scoring**: Overall accuracy percentage and detailed statistics
- **Error Classification**: Identifies missing words, wrong words, and extra words
- **Export Results**: Download detailed CSV reports
- **Modern UI**: Beautiful, responsive interface with Bootstrap 5
- **Real-time Processing**: Background processing with status updates

## Technology Stack

- **Backend**: Django 5.0
- **AI/ML**: OpenAI Whisper (speech-to-text)
- **Text Processing**: python-docx, fuzzywuzzy
- **Frontend**: Bootstrap 5, Font Awesome
- **Database**: SQLite (can be changed to PostgreSQL/MySQL for production)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd audio_detection
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Usage

### Basic Workflow

1. **Upload Files**: Go to the home page and upload your DOCX script and audio file
2. **Start Analysis**: Click "Start Analysis" to begin processing
3. **Monitor Progress**: The system will show processing status in real-time
4. **View Results**: Once complete, view detailed word-by-word analysis
5. **Export Data**: Download CSV reports for further analysis

### Supported File Formats

- **Scripts**: DOCX, DOC
- **Audio**: WAV, MP3, M4A, FLAC

### Analysis Features

- **Accuracy Score**: Overall percentage of correctly spoken words
- **Word Statistics**: Total, correct, missing, and wrong word counts
- **Error Types**:
  - **Missing**: Words in script but not in audio
  - **Wrong**: Words spoken differently than in script
  - **Extra**: Words in audio but not in script
  - **Correct**: Words matching the script exactly

## AI Models Used

### Whisper AI
- **Model**: OpenAI Whisper (base model by default)
- **Accuracy**: Industry-leading speech recognition
- **Languages**: Multi-language support
- **Processing**: Local processing (no internet required after model download)

### Text Comparison
- **Algorithm**: Fuzzy string matching with Levenshtein distance
- **Threshold**: 80% similarity for word matching
- **Features**: Handles pronunciation variations and minor errors

## Project Structure

```
audio_detection/
├── audio_detection/          # Main project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── audio_checker/           # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Form definitions
│   ├── services.py          # Core analysis logic
│   ├── admin.py             # Admin interface
│   ├── urls.py              # App URL patterns
│   └── templates/           # HTML templates
├── static/                  # Static files (CSS, JS)
├── media/                   # Uploaded files
├── requirements.txt         # Python dependencies
├── manage.py               # Django management script
└── README.md               # This file
```

## Configuration

### Environment Variables

Create a `.env` file in the project root for production settings:

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Whisper Model Configuration

You can change the Whisper model size in `audio_checker/services.py`:

```python
# Available models: 'tiny', 'base', 'small', 'medium', 'large'
analyzer = AudioAnalyzer(model_size='base')
```

- **tiny**: Fastest, least accurate
- **base**: Good balance (default)
- **small**: Better accuracy
- **medium**: High accuracy
- **large**: Best accuracy, slowest

## Performance Considerations

- **Audio Length**: Longer files take more time to process
- **Model Size**: Larger models are more accurate but slower
- **File Size**: Large audio files may require more memory
- **Concurrent Users**: Background processing prevents blocking

## Troubleshooting

### Common Issues

1. **Whisper model download fails**
   - Check internet connection
   - Ensure sufficient disk space
   - Try using a smaller model

2. **Audio file not supported**
   - Convert to WAV, MP3, M4A, or FLAC format
   - Check file corruption

3. **Script file issues**
   - Ensure DOCX format
   - Check file permissions
   - Verify file is not corrupted

4. **Memory errors**
   - Use smaller Whisper model
   - Process shorter audio files
   - Increase system memory

### Error Logs

Check Django logs for detailed error information:
```bash
python manage.py runserver --verbosity=2
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review Django and Whisper documentation

## Acknowledgments

- OpenAI for the Whisper speech recognition model
- Django community for the excellent web framework
- Bootstrap team for the responsive UI framework 