from django import forms
from .models import AudioAnalysis

class AudioAnalysisForm(forms.ModelForm):
    class Meta:
        model = AudioAnalysis
        fields = ['title', 'script_file', 'audio_file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter analysis title'
            }),
            'script_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.docx,.doc'
            }),
            'audio_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.wav,.mp3,.m4a,.flac'
            })
        }
    
    def clean_script_file(self):
        script_file = self.cleaned_data.get('script_file')
        if script_file:
            if not script_file.name.endswith(('.docx', '.doc')):
                raise forms.ValidationError("Please upload a valid DOCX or DOC file.")
        return script_file
    
    def clean_audio_file(self):
        audio_file = self.cleaned_data.get('audio_file')
        if audio_file:
            if not audio_file.name.endswith(('.wav', '.mp3', '.m4a', '.flac')):
                raise forms.ValidationError("Please upload a valid audio file (WAV, MP3, M4A, FLAC).")
        return audio_file 