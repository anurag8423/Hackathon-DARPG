from django.shortcuts import render
from pedalboard import *
import noisereduce as nr
from django.http import JsonResponse,HttpResponse
from pedalboard.io import AudioFile
from django.conf import settings
import os
import uuid
from openai import OpenAI

def home(request):
    return render(request,'home.html')


def transcribe_audio(audio_file_path):
    # Initialize OpenAI client
    client = OpenAI(api_key="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")

    # Get the directory path of the textDocuments folder within the media folder
    media_dir = os.path.join(settings.MEDIA_ROOT, 'textDocuments')

    # Ensure the textDocuments directory exists, create it if not
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)

    # Extract the filename without extension
    audio_filename = os.path.splitext(os.path.basename(audio_file_path))[0]

    # Generate the path for the text file
    text_file_path = os.path.join(media_dir, f"{audio_filename}.txt")

    # Read the audio file
    with open(audio_file_path, "rb") as audio_file:
        # Perform audio transcription
        translation = client.audio.translations.create(
            model="whisper-1", 
            file=audio_file
        )

        # Write the transcription text to the file
        with open(text_file_path, "w") as text_file:
            text_file.write(translation.text)

        # Print the path where the file is saved
        print("Transcription saved to:", text_file_path)

def enhance_audio(file_path):
    sr = 44100
    # Load audio file
    with AudioFile(file_path).resampled_to(sr) as f:
        audio = f.read(f.frames)

    # Reduce noise
    reduced_noise = nr.reduce_noise(y=audio, sr=sr, stationary=True, prop_decrease=0.75)

    # Create pedalboard with desired effects
    board = Pedalboard([
        NoiseGate(threshold_db=-30, ratio=1.5, release_ms=250),
        Compressor(threshold_db=-16, ratio=2.5),
        LowShelfFilter(cutoff_frequency_hz=400, gain_db=10, q=1),
        Gain(gain_db=10)
    ])

    # Apply effects to the audio
    effected = board(reduced_noise, sr)

    # Write the processed audio back to the same file
    with AudioFile(file_path, 'w', sr, effected.shape[0]) as f:
        f.write(effected)
    transcribe_audio(file_path)



def upload_audio(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        # Ensure the "audios" folder exists within the "media" directory
        audio_folder = os.path.join(settings.MEDIA_ROOT, 'audios')
        os.makedirs(audio_folder, exist_ok=True)  # Ensure directory exists
        # Save the audio file in the "audios" folder
        file_path = os.path.join(audio_folder, audio_file.name)
        with open(file_path, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)
        enhance_audio(file_path)
        text_filename = os.path.splitext(audio_file.name)[0] + '.txt'
        text_filepath = os.path.join(settings.MEDIA_ROOT, 'textDocuments', text_filename)

        response_data = {'fileAvailable': True, 'filepath': text_filepath}
        
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'No audio file provided'}, status=400)

def download_file(request):
    file_path = request.GET.get('file')
    if file_path:
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=' + file_name
            return response
    else:
        return HttpResponse("File path not provided", status=400)
    
def upload(request):
    context={'fileAvailable': False, 'filepath': None,'buffer':False}
    if request.method=='POST':
        audio=request.FILES.get('audio')
        save_path = os.path.join(settings.MEDIA_ROOT, 'audios')  # Path to the "audios" folder
        
        # Create the directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)
        
        # Generate a unique filename for the audio file
        unique_filename = str(uuid.uuid4()) + os.path.splitext(audio.name)[1]
        
        # Save the file to the specified path
        file_path = os.path.join(save_path, unique_filename)
        with open(file_path, 'wb') as destination:
            for chunk in audio.chunks():
                destination.write(chunk)
        enhance_audio(file_path)
        audio_base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Construct the file path for the corresponding text file
        text_file_path = os.path.join(settings.MEDIA_ROOT, 'textDocuments', audio_base_name + '.txt')
        
        # Update context with file path information
        context['fileAvailable'] = True
        context['filepath'] = text_file_path
        context['buffer']=True

    return render(request,'upload.html',context)
    
