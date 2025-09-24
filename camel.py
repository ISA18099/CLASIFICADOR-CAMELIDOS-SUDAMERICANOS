import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import matplotlib.pyplot as plt

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

# Información sobre las especies con los íconos exactos de tu imagen
st.sidebar.header("📚 Información de las Especies")
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

# Mostrar información en sidebar exactamente como en tu imagen
st.sidebar.markdown("### Características distintivas:")
for especie, datos in especies_info.items():
    st.sidebar.markdown(datos["icon"])
    st.sidebar.info(datos["info"])
    st.sidebar.markdown("---")

# Cargar modelo
@st.cache_resource
def load_model():
    # Reemplaza esto con la carga real de tu modelo
    # model = tf.keras.models.load_model('modelo_camelidos.h5')
    # return model
    return None

model = load_model()

# Función para preprocesar la imagen
def preprocess_image(image):
    image = image.resize((224, 224))
    image_array = np.array(image)
    image_array = image_array / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

# Función para hacer la predicción
def predict_image(model, image):
    processed_image = preprocess_image(image)
    prediction = model.predict(processed_image)
    return prediction

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
            with st.spinner("Analizando imagen..."):
                try:
                    # Simulación de resultado (eliminar cuando tengas el modelo real)
                    classes = ["Llama", "Alpaca", "Guanaco", "Vicuña"]
                    simulated_prediction = np.random.dirichlet(np.ones(4), size=1)[0]
                    result_index = np.argmax(simulated_prediction)
                    predicted_class = classes[result_index]
                    confidence = simulated_prediction[result_index]
                    
                    # Mostrar resultados
                    with col2:
                        st.subheader("📊 Resultados de la Clasificación")
                        
                        # Mostrar la especie predicha con el formato de tu imagen
                        st.markdown(f"## {predicted_class}")
                        st.success(f"**Característica identificada:** {especies_info[predicted_class]['caracteristica']}")
                        st.metric("Nivel de confianza", f"{confidence:.2%}")
                        
                        # Gráfico de barras de probabilidades
                        fig, ax = plt.subplots(figsize=(10, 6))
                        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
                        bars = ax.bar(classes, simulated_prediction * 100, color=colors)
                        ax.set_ylabel('Probabilidad (%)')
                        ax.set_title('Distribución de Probabilidades por Especie')
                        
                        # Añadir valores en las barras
                        for bar, value in zip(bars, simulated_prediction * 100):
                            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                                   f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
                        
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        st.pyplot(fig)
                        
                        # Información adicional de la especie
                        st.info(f"**Información adicional:** {especies_info[predicted_class]['info']}")
                        
                except Exception as e:
                    st.error(f"Error al procesar la imagen: {str(e)}")

# Sección de instrucciones
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
st.markdown(
    "**Clasificador de Camélidos Sudamericanos** | "
    "**Soporte:** contacto@ejemplo.com"
)

# Mostrar las características como en tu imagen
st.markdown("---")
st.header("Características distintivas de cada especie:")

for especie, datos in especies_info.items():
    st.markdown(datos["icon"])
    st.info(datos["info"])
    st.markdown("---")
