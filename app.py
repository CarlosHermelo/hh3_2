import os
from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Configura tu clave API de OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
# Lista para almacenar el historial de mensajes
historial = []

def obtener_respuesta(mensaje, historial):
    # Agregar el mensaje del usuario al historial
    historial.append({"role": "user", "content": mensaje})

    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=historial
        )
        # Obtener la respuesta del asistente y añadirla al historial
        mensaje_asistente = respuesta.choices[0].message['content']
        historial.append({"role": "assistant", "content": mensaje_asistente})
        return mensaje_asistente
    except Exception as e:
        return f"Hubo un error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        mensaje = request.form['mensaje']
        if mensaje.lower() == "salir":
            return render_template('index.html', historial=historial, terminado=True)

        respuesta = obtener_respuesta(mensaje, historial)
        return render_template('index.html', historial=historial)

    return render_template('index.html', historial=historial)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
