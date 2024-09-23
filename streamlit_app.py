import streamlit as st
import requests
from PIL import Image
import io
import google.generativeai as genai

# UI configurations
st.set_page_config(page_title="JDM-DESIGN", page_icon="🖌️", layout="wide")

# Access the Hugging Face API token from Streamlit secrets
API_TOKEN = st.secrets["hf_api_token"]
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Function to query the Hugging Face API for image generation
def query_huggingface_api(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

# Load the Gemini model for text generation using API key
api_key = st.secrets["google_api_key"]
genai.configure(api_key=api_key)  # Configure the API key

# Title
st.title("🎨 JDM-DESIGN - Estudio de Arte Textual a Imagen")

def configure_sidebar() -> None:
    with st.sidebar:
        st.markdown("# 🤖 Mejora tu Idea")
        st.info("**¡Hola! Comienza aquí ↓**", icon="👋🏾")
        
        # User input for prompt
        user_input = st.text_area("Describe lo que quieres:", height=150)
        
        # Button for generating the response
        submitted = st.button("Generar Respuesta", type="primary")
        
        return submitted, user_input

def main_page(submitted: bool, user_input: str) -> None:
    if submitted and user_input:
        default_message = (
            "A partir del siguiente mensaje, mejora la descripción incluyendo detalles específicos "
            "como colores, estilos y otros elementos creativos que desees:"
        )
        input_text = f"{default_message} {user_input}"
        
        # Generate text with Gemini
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(input_text)
            improved_prompt = response.text
            
            st.session_state.generated_prompt = improved_prompt  # Save prompt for later use

        except Exception as e:
            st.error(f"Error al generar la respuesta: {e}")

    if 'generated_prompt' in st.session_state:
        st.header("🎨 Generación de Imágenes")
        st.write(f"Prompt mejorado: '{st.session_state.generated_prompt}'")
        
        if st.button("Generar Imagen"):
            with st.spinner("🖌️ Transformando tus palabras en arte...\n⚙️ Modelo iniciado\n🙆‍♀️ Estírate mientras tanto..."):
                try:
                    image_bytes = query_huggingface_api({"inputs": st.session_state.generated_prompt})
                    image = Image.open(io.BytesIO(image_bytes))
                    st.image(image, caption=f"Imagen generada para el prompt: '{st.session_state.generated_prompt}'", use_column_width=True)
                except Exception as e:
                    st.error(f"Error al generar la imagen: {e}")
    else:
        st.warning("Genera una respuesta para habilitar la generación de imágenes.")

def main():
    submitted, user_input = configure_sidebar()
    main_page(submitted, user_input)

if __name__ == "__main__":
    main()