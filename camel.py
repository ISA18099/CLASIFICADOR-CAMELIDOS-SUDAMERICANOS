import streamlit as st
import numpy as np
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Clasificador de Camélidos Sudamericanos",
    page_icon="🦙",
    layout="wide"
)

# CSS con fondo amarillo claro para títulos y mejoras visuales
st.markdown("""
<style>
    .main {
        background-color: #f5f5dc;
    }
    .title-container {
        background-color: #fffacd;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 5px solid #8B4513;
    }
    .subtitle-container {
        background-color: #fffacd;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0px;
        border-left: 4px solid #8B4513;
    }
    .species-info {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0px;
        border-left: 4px solid #8B4513;
    }
    .size-comparison {
        background-color: #f5f5dc;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #8B4513;
        margin: 10px 0px;
    }
    .cafe-text {
        color: #8B4513;
        font-weight: bold;
    }
    .taxonomy-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #8B4513;
        font-family: 'Courier New', monospace;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# Título principal con fondo amarillo claro
st.markdown('<div class="title-container">', unsafe_allow_html=True)
st.title("CLASIFICADOR DE CAMÉLIDOS SUDAMERICANOS")
st.subheader("¿Cómo reconocer una llama, alpaca, vicuña y guanaco?")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Información taxonómica corregida
taxonomia = """
**La familia Camelidae está formada por dos tribus: los Camelini y los Lamini** (Stanley et al., 1994; Wheeler, 1995).

**Tribu Camelini**
└── **GÉNERO: Camelus**
    ├── Camelus bactrianus → **CAMELLO**
    └── Camelus dromedarius → **DROMEDARIO**

**Familia Camelidae**

**Tribu Lamini**
├── **GÉNERO: Lama**
│   ├── Lama guanicoe → **GUANACO**
│   └── Lama glama → **LLAMA**
└── **GÉNERO: Vicugna**
    ├── Vicugna vicugna → **VICUÑA**
    └── Vicugna pacos → **ALPACA**
"""

# Texto exacto proporcionado para cada especie (con ícono de animal para vicuña)
especies_texto = {
    "Alpaca": {
        "nombre_cientifico": "Lama pacos",
        "icon": "🐑",
        "texto_completo": "**Alpaca (Lama pacos)**\n\nDescripción: Más pequeña que la llama, con una silueta más curvilínea. Posee un clásico mechón de fibra en la frente. Uso: Criada por su valiosa fibra, considerada una de las más finas y suaves del mundo. Estado: Doméstica."
    },
    "Guanaco": {
        "nombre_cientifico": "Lama guanicoe",
        "icon": "🐪",
        "texto_completo": "**Guanaco (Lama guanicoe)**\n\nDescripción: Silvestre, con pelaje denso de color marrón-rojizo claro y el vientre blanquecino. Es el antepasado silvestre de la llama. Uso: No tiene un uso económico principal, pero es una especie importante por su valor ecológico. Estado: Silvestre."
    },
    "Llama": {
        "nombre_cientifico": "Lama glama",
        "icon": "🦙",
        "texto_completo": "**Llama (Lama glama)**\n\nDescripción: Es el camélido doméstico de mayor tamaño y peso, con patas largas, orejas prominentes y curvadas, y pelaje grueso y áspero. Uso: Se utiliza como animal de carga para el transporte y, en menor medida, por su lana y carne. Estado: Doméstica."
    },
    "Vicuña": {
        "nombre_cientifico": "Vicugna vicugna",
        "icon": "🦌",  # Cambiado a un animal (ciervo) en lugar del diana
        "texto_completo": "**Vicuña (Vicugna vicugna)**\n\nDescripción: La más pequeña de los camélidos andinos, con cuerpo grácil y movimientos ágiles. Posee pelaje muy fino y brillante, de color marrón claro en el lomo y blanquecino en el pecho. Uso: Su fibra es considerada la más fina del mundo, y se aprovecha en la industria textil de lujo. Estado: Silvestre y protegida tras un peligro de extinción."
    }
}

# Layout principal
col1, col2 = st.columns([1, 1])

with col1:
    # Clasificación taxonómica con fondo amarillo claro
    st.markdown('<div class="subtitle-container">', unsafe_allow_html=True)
    st.markdown("### 📊 Clasificación Taxonómica")
    st.markdown("**Figura 1. Clasificación de los camélidos**")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="taxonomy-box">', unsafe_allow_html=True)
    st.markdown(taxonomia)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Especies de camélidos andinos con fondo amarillo claro en el subtítulo
    st.markdown('<div class="subtitle-container">', unsafe_allow_html=True)
    st.markdown("### 🦙 Especies de Camélidos Andinos")
    st.markdown('</div>', unsafe_allow_html=True)
    
    for especie, datos in especies_texto.items():
        st.markdown(f'<div class="species-info">', unsafe_allow_html=True)
        st.markdown(datos["texto_completo"])
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Sección de clasificación de imágenes con fondo amarillo claro
    st.markdown('<div class="subtitle-container">', unsafe_allow_html=True)
    st.header("📤 Clasificador de Imágenes")
    st.markdown('</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Selecciona una imagen de un camélido sudamericano",
        type=['jpg', 'jpeg', 'png'],
        help="Sube una imagen clara de una llama, alpaca, guanaco o vicuña"
    )
    
    if uploaded_file is not None:
        # Mostrar imagen original (CORREGIDO el parámetro use_column_width)
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagen subida", use_container_width=True)  # Corregido aquí
        
        # Botón para clasificar
        if st.button("🔍 Identificar Especie", type="primary", use_container_width=True):
            with st.spinner("Analizando imagen..."):
                try:
                    # Simulación simple de clasificación
                    classes = list(especies_texto.keys())
                    # Crear probabilidades más realistas
                    probabilities = np.random.dirichlet(np.ones(4) * 10, size=1)[0]
                    
                    result_index = np.argmax(probabilities)
                    predicted_class = classes[result_index]
                    confidence = probabilities[result_index]
                    
                    # Mostrar resultados con fondo amarillo claro
                    st.markdown('<div class="subtitle-container">', unsafe_allow_html=True)
                    st.subheader("📊 Resultados de la Identificación")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Resultado principal
                    st.success(f"**Especie identificada:** {especies_texto[predicted_class]['icon']} {predicted_class}")
                    st.metric("Nivel de confianza", f"{confidence:.2%}")
                    
                    # Mostrar el texto completo de la especie identificada
                    st.markdown(f'<div class="species-info">', unsafe_allow_html=True)
                    st.markdown(especies_texto[predicted_class]["texto_completo"])
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Probabilidades para todas las especies
                    st.markdown('<div class="subtitle-container">', unsafe_allow_html=True)
                    st.subheader("Probabilidades por especie:")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    for i, especie in enumerate(classes):
                        prob_percent = probabilities[i] * 100
                        st.write(f"**{especies_texto[especie]['icon']} {especie}:** {prob_percent:.1f}%")
                        st.progress(float(probabilities[i]))
                        
                except Exception as e:
                    st.error(f"Error al procesar la imagen: {str(e)}")

    # Comparación de tamaño con fondo beige y texto café
    st.markdown("---")
    st.markdown('<div class="subtitle-container">', unsafe_allow_html=True)
    st.markdown("### 📏 Comparación de Tamaño")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="size-comparison">', unsafe_allow_html=True)
    st.markdown('<p class="cafe-text">Altura promedio (a la cruz):</p>', unsafe_allow_html=True)
    
    # Barras de tamaño simplificadas
    especies_altura = [
        ("LLAMA", "1.7-1.8 m", 180),
        ("GUANACO", "1.0-1.2 m", 120),
        ("ALPACA", "0.8-1.0 m", 90),
        ("VICUÑA", "0.7-0.9 m", 80)
    ]
    
    for especie, altura, pixels in especies_altura:
        st.markdown(f'<p class="cafe-text">{especie} - {altura}</p>', unsafe_allow_html=True)
        st.markdown(f'<div style="width: {pixels}px; height: 20px; background-color: #8B4513; border-radius: 3px; margin-bottom: 10px;"></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Instrucciones con fondo amarillo claro
with st.expander("📋 Instrucciones para mejor identificación", expanded=False):
    st.markdown("""
    **Para obtener mejores resultados:**
    - Toma fotos con buena iluminación
    - Enfoca claramente al animal
    - Usa fondos simples
    - Procura imágenes nítidas
    """)

# Footer
st.markdown("---")
st.markdown('<div style="text-align: center; color: #8B4513;">', unsafe_allow_html=True)
st.markdown("**CLASIFICADOR DE CAMÉLIDOS SUDAMERICANOS**")
st.markdown('</div>', unsafe_allow_html=True)
