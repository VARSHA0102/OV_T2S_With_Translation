from flask import Flask, render_template, request, send_file
from gtts import gTTS
from googletrans import Translator
import os

app = Flask(__name__)
translator = Translator()

# Home route to render the front-end form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle text input, translation, and generate speech
@app.route('/convert', methods=['POST'])
def convert_to_speech():
    text = request.form['text']
    input_lang = request.form['input_lang']
    output_lang = request.form['output_lang']

    if text:
        # Translate the text if the input language is different from the output language
        if input_lang != output_lang:
            translated = translator.translate(text, src=input_lang, dest=output_lang)
            translated_text = translated.text
        else:
            translated_text = text
        
        # Convert translated text to speech
        tts = gTTS(text=translated_text, lang=output_lang)
        audio_file = "output_audio.mp3"
        tts.save(audio_file)

        # Return the audio file to the user
        return send_file(audio_file, as_attachment=True)
    
    return 'No text provided', 400

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
