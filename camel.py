import streamlit as st
import tensorflow as tf
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

# Intentar cargar todas las dependencias
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    st.warning("TensorFlow no está disponible - modo demostración")

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    st.warning("Matplotlib no está disponible")

# Diccionario de especies
ESPECIES = {
    'vicuna': {'nombre_comun': 'Vicuña', 'icono': '🦌', 'color': '#FF6B6B'},
    'guanaco': {'nombre_comun': 'Guanaco', 'icono': '🐐', 'color': '#4ECDC4'},
    'llama': {'nombre_comun': 'Llama', 'icono': '🦙', 'color': '#45B7D1'},
    'alpaca': {'nombre_comun': 'Alpaca', 'icono': '🐑', 'color': '#96CEB4'}
}

st.title("🐪 Clasificador de Camélidos Sudamericanos")

@st.cache_resource
def load_model():
    if not TENSORFLOW_AVAILABLE:
        return None
    try:
        model_paths = ['modelo_camelidos.h5', 'modelo_camelidos.keras', 'model.h5']
        for path in model_paths:
            if os.path.exists(path):
                return tf.keras.models.load_model(path)
        return None
    except Exception as e:
        st.error(f"Error cargando modelo: {e}")
        return None

@st.cache_data
def load_class_names():
    try:
        paths = ['class_names.json', 'labels.json', 'classes.json']
        for path in paths:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    classes = json.load(f)
                    if isinstance(classes, dict):
                        return list(classes.keys())
                    return classes
        return list(ESPECIES.keys())
    except:
        return list(ESPECIES.keys())

def preprocess_image(image):
    img = image.resize((224, 224))
    img_array = np.array(img)
    if len(img_array.shape) == 3 and img_array.shape[2] == 4:
        img_array = img_array[..., :3]
    return img_array / 255.0

def simulate_prediction():
    # Simulación para cuando no hay modelo
    probs = np.random.dirichlet(np.ones(4), size=1)[0]
    predicted_idx = np.argmax(probs)
    class_names = list(ESPECIES.keys())
    return class_names[predicted_idx], probs[predicted_idx], probs

# Cargar modelo y clases
model = load_model()
class_names = load_class_names()

# Interfaz de usuario
st.sidebar.header("📷 Subir imagen")
uploaded_file = st.sidebar.file_uploader(
    "Selecciona una imagen", 
    type=['jpg', 'jpeg', 'png'],
    help="Sube una imagen de vicuña, guanaco, llama o alpaca"
)

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagen subida", use_column_width=True)
        
        with st.spinner("🔍 Analizando imagen..."):
            img_array = preprocess_image(image)
            
            if model and TENSORFLOW_AVAILABLE:
                img_array = np.expand_dims(img_array, axis=0)
                predictions = model.predict(img_array, verbose=0)
                predicted_idx = np.argmax(predictions[0])
                confidence = np.max(predictions[0])
                class_key = class_names[predicted_idx] if predicted_idx < len(class_names) else list(ESPECIES.keys())[predicted_idx]
                all_probs = predictions[0]
            else:
                class_key, confidence, all_probs = simulate_prediction()
        
        # Mostrar resultados
        col1, col2 = st.columns(2)
        
        with col1:
            especie = ESPECIES.get(class_key, {})
            st.success(f"## {especie.get('icono', '❓')} {especie.get('nombre_comun', class_key)}")
            st.metric("Confianza", f"{confidence:.2%}")
            
            if not TENSORFLOW_AVAILABLE:
                st.warning("⚠️ Ejecutando en modo demostración")
        
        with col2:
            st.info("📊 Probabilidades:")
            for i, class_key in enumerate(ESPECIES.keys()):
                prob = all_probs[i] if i < len(all_probs) else 0
                especie = ESPECIES[class_key]
                progress = int(prob * 100)
                st.markdown(f"""
                {especie['icono']} **{especie['nombre_comun']}**: {prob:.2%}
                <div style="background: #ddd; border-radius: 5px; height: 20px;">
                    <div style="background: {especie['color']}; width: {progress}%; height: 100%; border-radius: 5px;"></div>
                </div>
                """, unsafe_allow_html=True)
        
        # Gráfico solo si matplotlib está disponible
        if MATPLOTLIB_AVAILABLE:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                names = [f"{ESPECIES[k]['icono']} {ESPECIES[k]['nombre_comun']}" for k in ESPECIES.keys()]
                colors = [ESPECIES[k]['color'] for k in ESPECIES.keys()]
                bars = ax.barh(names, all_probs[:4] * 100, color=colors)
                ax.set_xlabel('Probabilidad (%)')
                ax.set_title('Distribución de Probabilidades')
                st.pyplot(fig)
            except Exception as e:
                st.warning("No se pudo generar el gráfico")
        
    except Exception as e:
        st.error(f"Error procesando la imagen: {str(e)}")

else:
    st.info("👈 **Por favor, sube una imagen para comenzar**")
    st.markdown("""
    ### 🐪 Especies que puedes clasificar:
    - 🦌 **Vicuña**: Animal silvestre protegido
    - 🐐 **Guanaco**: Habita en zonas altas de los Andes  
    - 🦙 **Llama**: Animal doméstico de carga
    - 🐑 **Alpaca**: Criada por su lana de alta calidad
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
**📌 Requisitos:**
- Python 3.8+
- TensorFlow 2.x
- Streamlit

**🔄 Si ves errores:**
Verifica que todos los archivos estén en el repositorio
""")
