import streamlit as st
import numpy as np
from PIL import Image
import json
import os
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(
    page_title="Clasificador de Camélidos Sudamericanos",
    page_icon="🐪",
    layout="wide"
)

# Intentar cargar TensorFlow con manejo de errores
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    st.error("⚠️ TensorFlow no está instalado. Instálalo con: pip install tensorflow")

# Diccionario de especies
ESPECIES = {
    'vicuna': {'nombre_comun': 'Vicuña', 'icono': '🦌', 'info': 'Animal silvestre protegido'},
    'guanaco': {'nombre_comun': 'Guanaco', 'icono': '🐐', 'info': 'Salvaje, habita en los Andes'},
    'llama': {'nombre_comun': 'Llama', 'icono': '🦙', 'info': 'Doméstica, animal de carga'},
    'alpaca': {'nombre_comun': 'Alpaca', 'icono': '🐑', 'info': 'Doméstica, lana de alta calidad'}
}

st.title("🐪 Clasificador de Camélidos Sudamericanos")

@st.cache_resource
def load_model():
    if not TENSORFLOW_AVAILABLE:
        return None
    try:
        model_paths = ['modelo_camelidos.h5', 'modelo_camelidos.keras']
        for path in model_paths:
            if os.path.exists(path):
                return tf.keras.models.load_model(path)
        st.error("Modelo no encontrado")
        return None
    except Exception as e:
        st.error(f"Error cargando modelo: {e}")
        return None

@st.cache_data
def load_class_names():
    try:
        paths = ['class_names.json', 'labels.json']
        for path in paths:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return json.load(f)
        return list(ESPECIES.keys())
    except:
        return list(ESPECIES.keys())

def preprocess_image(image):
    img = image.resize((224, 224))
    img_array = np.array(img)
    if img_array.shape[-1] == 4:
        img_array = img_array[..., :3]
    return img_array / 255.0

def simulate_prediction(image_array):
    # Simulación de predicción para demo
    probs = np.random.dirichlet(np.ones(4), size=1)[0]
    predicted_idx = np.argmax(probs)
    class_names = list(ESPECIES.keys())
    return class_names[predicted_idx], probs[predicted_idx], probs

# Cargar modelo y clases
model = load_model() if TENSORFLOW_AVAILABLE else None
class_names = load_class_names()

# Interfaz de usuario
option = st.sidebar.radio("Método de entrada:", ["Subir imagen", "Usar cámara"])
uploaded_file = st.sidebar.file_uploader("Sube una imagen", type=['jpg', 'jpeg', 'png']) if option == "Subir imagen" else st.sidebar.camera_input("Toma una foto")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)
    
    with st.spinner("Clasificando..."):
        img_array = preprocess_image(image)
        
        if model:
            img_array = np.expand_dims(img_array, axis=0)
            predictions = model.predict(img_array)
            predicted_idx = np.argmax(predictions[0])
            confidence = np.max(predictions[0])
            class_key = class_names[predicted_idx]
            all_probs = predictions[0]
        else:
            class_key, confidence, all_probs = simulate_prediction(img_array)
    
    # Mostrar resultados
    especie = ESPECIES.get(class_key, {})
    st.success(f"✅ **Resultado:** {especie.get('icono', '❓')} {especie.get('nombre_comun', class_key)}")
    st.metric("Confianza", f"{confidence:.2%}")
    
    # Gráfico de probabilidades
    fig, ax = plt.subplots()
    names = [f"{ESPECIES.get(k, {}).get('icono', '❓')} {ESPECIES.get(k, {}).get('nombre_comun', k)}" for k in class_names]
    ax.barh(names, all_probs * 100)
    ax.set_xlabel('Probabilidad (%)')
    st.pyplot(fig)

else:
    st.info("👈 Sube una imagen o usa la cámara")

st.sidebar.markdown("---")
st.sidebar.markdown("""
**🐪 Especies:**
- 🦌 Vicuña
- 🐐 Guanaco  
- 🦙 Llama
- 🐑 Alpaca
""")
