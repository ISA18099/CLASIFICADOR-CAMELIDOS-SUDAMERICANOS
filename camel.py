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

# Diccionario de especies (FALTANTE EN EL CÓDIGO ORIGINAL)
ESPECIES = {
    'vicuna': {
        'nombre_comun': 'Vicuña',
        'icono': '🦌',
        'info': 'Animal silvestre protegido, fibra muy valiosa. Habita en los altos Andes.',
        'cientifico': 'Vicugna vicugna'
    },
    'guanaco': {
        'nombre_comun': 'Guanaco', 
        'icono': '🐐',
        'info': 'Salvaje, habita en zonas altas de los Andes. Parentesco cercano con la llama.',
        'cientifico': 'Lama guanicoe'
    },
    'llama': {
        'nombre_comun': 'Llama',
        'icono': '🦙',
        'info': 'Doméstica, usada como animal de carga. Importante en la cultura andina.',
        'cientifico': 'Lama glama'
    },
    'alpaca': {
        'nombre_comun': 'Alpaca',
        'icono': '🐑',
        'info': 'Doméstica, criada por su lana de alta calidad. Fibra muy suave y cálida.',
        'cientifico': 'Vicugna pacos'
    }
}

# Título de la app
st.title("🐪 Clasificador de Camélidos Sudamericanos")
st.markdown("Clasifica imágenes de **vicuñas, guanacos, llamas y alpacas** usando Redes Neuronales Convolucionales (CNN)")

# Cargar modelo y etiquetas
@st.cache_resource
def load_model():
    """Carga el modelo preentrenado"""
    try:
        # Buscar el modelo en diferentes ubicaciones
        possible_paths = [
            'modelo_camelidos.h5',
            '/content/modelo_camelidos.h5',
            './models/modelo_camelidos.h5',
            'modelo_camelidos.keras'
        ]
        
        for model_path in possible_paths:
            if os.path.exists(model_path):
                model = tf.keras.models.load_model(model_path)
                return model
        
        st.error("Model file not found. Please make sure 'modelo_camelidos.h5' is in the correct directory.")
        return None
    except Exception as e:
        st.error(f"Error cargando el modelo: {e}")
        return None

@st.cache_data
def load_class_names():
    """Carga los nombres de las clases"""
    # Buscar el archivo en diferentes ubicaciones
    possible_paths = [
        'class_names.json',
        '/content/class_names.json',
        './models/class_names.json',
        'labels.json'
    ]
    
    for class_names_path in possible_paths:
        if os.path.exists(class_names_path):
            try:
                with open(class_names_path, 'r') as f:
                    class_names = json.load(f)
                
                # Asegurar que class_names sea una lista
                if isinstance(class_names, dict):
                    # Si es diccionario, extraer las keys
                    class_names = list(class_names.keys())
                return class_names
            except Exception as e:
                st.error(f"Error reading {class_names_path}: {e}")
                continue
    
    st.error("Class names file not found. Using default classes.")
    return ['vicuna', 'guanaco', 'llama', 'alpaca']  # Default fallback

# Sidebar
st.sidebar.header("Configuración")
st.sidebar.info("Sube una imagen o usa la cámara para clasificar camélidos")

# Opción de upload o cámara
option = st.sidebar.radio(
    "Selecciona el método de entrada:",
    ["Subir imagen", "Usar cámara"]
)

# Function to preprocesar image
def preprocess_image(image):
    """Preprocesa la imagen para el modelo"""
    img = image.resize((224, 224))
    img_array = np.array(img)
    
    # Convertir a RGB si tiene canal alpha
    if img_array.shape[-1] == 4:
        img_array = img_array[..., :3]
    
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Function to predict image
def predict_image(model, image_array, class_names):
    """Realiza la predicción"""
    try:
        predictions = model.predict(image_array)
        predicted_class = np.argmax(predictions[0])
        confidence = np.max(predictions[0])

        # Obtener el nombre de la clase predicha
        predicted_class_name = class_names[predicted_class] if predicted_class < len(class_names) else "Desconocido"
        
        # Mapear a nombre en español con icono
        species_name = ESPECIES.get(predicted_class_name, {}).get('nombre_comun', predicted_class_name)
        icono = ESPECIES.get(predicted_class_name, {}).get('icono', '❓')
        
        return f"{icono} {species_name}", confidence, predictions[0], predicted_class_name
        
    except Exception as e:
        st.error(f"Error en la predicción: {e}")
        return "Error", 0.0, np.zeros(len(class_names)), "Error"

# Load model and classes
model = load_model()
class_names = load_class_names()

if model is not None and class_names is not None:
    # Image input
    if option == "Subir imagen":
        uploaded_file = st.sidebar.file_uploader(
            "Sube una imagen",
            type=['jpg', 'jpeg', 'png', 'bmp']
        )
    else:
        uploaded_file = st.sidebar.camera_input("Toma una foto")

    if uploaded_file is not None:
        # Display image
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Imagen subida", use_column_width=True)

            # Preprocess and predict
            with st.spinner("Clasificando..."):
                img_array = preprocess_image(image)
                species, confidence, all_predictions, predicted_key = predict_image(model, img_array, class_names)

            # Display results
            col1, col2 = st.columns(2)

            with col1:
                st.success("✅ **Resultado de la clasificación:**")
                
                # Mostrar resultado con estilo
                st.markdown(f"""
                <div style='text-align: center; padding: 20px; background-color: #f0f8ff; border-radius: 10px;'>
                    <h2>{species}</h2>
                    <h3>Confianza: {confidence:.2%}</h3>
                </div>
                """, unsafe_allow_html=True)

                # Bar chart of probabilities
                fig, ax = plt.subplots(figsize=(10, 6))
                
                # Crear nombres para el gráfico con iconos
                display_names = []
                for class_name in class_names:
                    icon = ESPECIES.get(class_name, {}).get('icono', '❓')
                    name = ESPECIES.get(class_name, {}).get('nombre_comun', class_name)
                    display_names.append(f"{icon} {name}")
                
                colors = ['#ff9999' if i == np.argmax(all_predictions) else '#66b3ff' for i in range(len(all_predictions))]
                
                bars = ax.barh(display_names, all_predictions * 100, color=colors)
                ax.set_xlabel('Probabilidad (%)')
                ax.set_title('Distribución de Probabilidades')
                ax.set_xlim(0, 100)
                
                # Añadir valores en las barras
                for i, (bar, prob) in enumerate(zip(bars, all_predictions)):
                    width = bar.get_width()
                    ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                           f'{prob:.1%}', ha='left', va='center')
                
                st.pyplot(fig)

            with col2:
                st.info("📊 **Detalles de la predicción:**")
                
                # Tabla de probabilidades
                for i, (class_name, prob) in enumerate(zip(class_names, all_predictions)):
                    icon = ESPECIES.get(class_name, {}).get('icono', '❓')
                    name = ESPECIES.get(class_name, {}).get('nombre_comun', class_name)
                    
                    # Resaltar la predicción principal
                    if i == np.argmax(all_predictions):
                        st.markdown(f"**{icon} {name}: {prob:.2%} ✅**")
                    else:
                        st.markdown(f"{icon} {name}: {prob:.2%}")

                # Información adicional sobre la especie predicha
                if predicted_key in ESPECIES:
                    especie_info = ESPECIES[predicted_key]
                    st.markdown("---")
                    st.markdown(f"**📖 Sobre la {especie_info['nombre_comun']}:**")
                    st.markdown(f"**Nombre científico:** {especie_info['cientifico']}")
                    st.info(especie_info['info'])

        except Exception as e:
            st.error(f"Error procesando la imagen: {e}")

    else:
        st.info("👈 Por favor, sube una imagen o usa la cámara para comenzar")

else:
    if model is None:
        st.error("No se pudo cargar el modelo. Verifica que el archivo 'modelo_camelidos.h5' exista.")
    if class_names is None:
        st.error("No se pudo cargar el archivo de nombres de clase.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
## **📁 Cómo usar:**
1. Sube una imagen o usa la cámara
2. Espera a que el modelo clasifique
3. Revisa los resultados y probabilidades

## **🐪 Especies soportadas:**
- 🦌 Vicuña (Vicugna vicugna)
- 🐐 Guanaco (Lama guanicoe)  
- 🦙 Llama (Lama glama)
- 🐑 Alpaca (Vicugna pacos)

## **⚙️ Requisitos:**
- Python 3.8+
- TensorFlow 2.x
- Streamlit
""")

# Información adicional en el footer principal
st.markdown("---")
st.caption("Desarrollado con ❤️ usando TensorFlow y Streamlit | Clasificador de Camélidos Sudamericanos")
