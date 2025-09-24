import streamlit as st
import numpy as np
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Clasificador de Camélidos Sudamericanos",
    page_icon="🦙",
    layout="wide"
)

# Título principal
st.title("# COMO DIFERENCIAR A UNA:")
st.subheader("LLAMA, ALPACA, VICUÑA Y GUANACO.")
st.markdown("---")

# Información sobre las especies
especies_info = {
    "Llama": {
        "icon": "## Llama",
        "info": "**Su manto es largo y lanoso.**",
        "caracteristica": "Manto largo y lanoso"
    },
    "Alpaca": {
        "icon": "## Alpaca", 
        "info": "**Su manto es suave y largo.**",
        "caracteristica": "Manto suave y largo"
    },
    "Vicuña": {
        "icon": "## Vicuña",
        "info": "**Tiene dientes de roedor y pesuñas divididas.**",
        "caracteristica": "Dientes de roedor y pesuñas divididas"
    },
    "Guanaco": {
        "icon": "## Guanaco",
        "info": "**Su rostro es gris.**",
        "caracteristica": "Rostro gris"
    }
}

# Sidebar con información
st.sidebar.header("📚 Información de las Especies")
st.sidebar.markdown("### Características distintivas:")
for especie, datos in especies_info.items():
    st.sidebar.markdown(datos["icon"])
    st.sidebar.info(datos["info"])
    st.sidebar.markdown("---")

# Función para preprocesar la imagen
def preprocess_image(image):
    image = image.resize((224, 224))
    image_array = np.array(image)
    # Si la imagen tiene canal alpha (RGBA), convertir a RGB
    if len(image_array.shape) > 2 and image_array.shape[-1] == 4:
        image_array = image_array[:, :, :3]
    image_array = image_array / 255.0
    return image_array

# Función de clasificación simulada
def classify_image(image):
    # Simular análisis de características visuales
    processed_image = preprocess_image(image)
    
    # Simular probabilidades
    simulated_probs = np.random.dirichlet(np.ones(4), size=1)[0]
    
    return simulated_probs

# Interfaz principal
st.header("📤 Sube una imagen para clasificar")

uploaded_file = st.file_uploader(
    "Selecciona una imagen de un camélido sudamericano",
    type=['jpg', 'jpeg', 'png'],
    help="Sube una imagen clara de una llama, alpaca, guanaco o vicuña"
)

col1, col2 = st.columns([1, 1])

with col1:
    if uploaded_file is not None:
        # Mostrar imagen original
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagen subida", use_column_width=True)
        
        # Botón para clasificar
        if st.button("🔍 Clasificar Imagen", type="primary"):
            with st.spinner("Analizando características de la imagen..."):
                try:
                    # Clasificación simulada
                    classes = ["Llama", "Alpaca", "Guanaco", "Vicuña"]
                    probabilities = classify_image(image)
                    
                    result_index = np.argmax(probabilities)
                    predicted_class = classes[result_index]
                    confidence = probabilities[result_index]
                    
                    # Mostrar resultados
                    with col2:
                        st.subheader("📊 Resultados de la Clasificación")
                        
                        # Mostrar la especie predicha
                        st.markdown(f"## {predicted_class}")
                        st.success(f"**Característica identificada:** {especies_info[predicted_class]['caracteristica']}")
                        st.metric("Nivel de confianza", f"{confidence:.2%}")
                        
                        # Mostrar probabilidades en forma de tabla (sin matplotlib)
                        st.subheader("Probabilidades por especie:")
                        
                        # Crear una barra de progreso visual para cada especie
                        for i, especie in enumerate(classes):
                            prob_percent = probabilities[i] * 100
                            st.write(f"**{especie}:** {prob_percent:.1f}%")
                            st.progress(float(probabilities[i]))
                        
                        # Información adicional de la especie
                        st.info(f"**Información:** {especies_info[predicted_class]['info']}")
                        
                except Exception as e:
                    st.error(f"Error al procesar la imagen: {str(e)}")

# Sección de características
st.markdown("---")
st.header("Características distintivas de cada especie:")

for especie, datos in especies_info.items():
    st.markdown(datos["icon"])
    st.info(datos["info"])
    st.markdown("---")

# Instrucciones
with st.expander("📋 Instrucciones para mejores resultados"):
    st.markdown("""
    **Para obtener los mejores resultados:**
    
    - Toma fotos con buena iluminación
    - Enfoca claramente al animal
    - Usa fondos simples para mejor reconocimiento
    - Procura imágenes nítidas y de alta calidad
    """)

# Footer
st.markdown("---")
st.markdown("**Clasificador de Camélidos Sudamericanos** | Demo de funcionalidad")
