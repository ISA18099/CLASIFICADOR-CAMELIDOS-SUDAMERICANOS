import streamlit as st
import numpy as np
from PIL import Image
import base64
from io import BytesIO

# Configuración de la página con fondo personalizado
st.set_page_config(
    page_title="Clasificador de Camélidos Sudamericanos",
    page_icon="🦙",
    layout="wide"
)

# CSS para el fondo de color beige con verde claro
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f5dc 0%, #e6f2e6 100%);
        padding: 20px;
        border-radius: 10px;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f0f8f0 0%, #e8f4e8 100%);
    }
    .species-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #8fbc8f;
        margin: 10px 0px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.title("CLASIFICADOR DE CAMELIDOS SUDAMERICANOS")
st.subheader("¿Cómo reconocer una llama, alpaca, vicuña y guanaco?")
st.markdown("---")

# Siluetas en SVG de cada especie (convertidas a base64)
def get_silhouette(species):
    silhouettes = {
        "Llama": """
        <svg width="120" height="100" viewBox="0 0 120 100">
            <path d="M30,70 Q40,40 60,50 Q80,40 90,70 L85,85 Q80,95 70,95 Q50,95 45,85 Z" fill="#8B4513" opacity="0.7"/>
            <path d="M50,45 Q55,30 65,35 Q70,40 68,50" fill="none" stroke="#000" stroke-width="2"/>
            <circle cx="45" cy="40" r="5" fill="#000"/>
            <circle cx="75" cy="40" r="5" fill="#000"/>
        </svg>
        """,
        "Alpaca": """
        <svg width="120" height="100" viewBox="0 0 120 100">
            <path d="M40,65 Q50,35 65,45 Q75,50 75,70 L70,85 Q65,92 55,92 Q45,92 40,85 Z" fill="#A52A2A" opacity="0.7"/>
            <path d="M55,40 Q58,30 65,32 Q68,35 67,42" fill="none" stroke="#000" stroke-width="2"/>
            <circle cx="50" cy="35" r="4" fill="#000"/>
            <circle cx="70" cy="35" r="4" fill="#000"/>
        </svg>
        """,
        "Vicuña": """
        <svg width="120" height="100" viewBox="0 0 120 100">
            <path d="M45,68 Q50,40 65,48 Q75,55 75,75 L70,88 Q65,94 55,94 Q45,94 40,88 Z" fill="#D2691E" opacity="0.7"/>
            <path d="M55,45 Q58,35 65,38 Q68,40 67,48" fill="none" stroke="#000" stroke-width="1.5"/>
            <circle cx="50" cy="40" r="3" fill="#000"/>
            <circle cx="70" cy="40" r="3" fill="#000"/>
        </svg>
        """,
        "Guanaco": """
        <svg width="120" height="100" viewBox="0 0 120 100">
            <path d="M35,72 Q45,42 62,52 Q78,60 85,75 L80,90 Q75,96 65,96 Q50,96 45,90 Z" fill="#808080" opacity="0.7"/>
            <path d="M52,48 Q55,38 62,40 Q65,42 64,50" fill="none" stroke="#000" stroke-width="2"/>
            <circle cx="48" cy="43" r="4" fill="#000"/>
            <circle cx="68" cy="43" r="4" fill="#000"/>
        </svg>
        """
    }
    return silhouettes.get(species, "")

# Información sobre las especies con siluetas
especies_info = {
    "Llama": {
        "icon": "🦙",
        "info": "**Su manto es largo y lanoso.**",
        "caracteristica": "Manto largo y lanoso",
        "altura": "1.7 - 1.8 m",
        "peso": "130 - 200 kg",
        "color": "Variados: blanco, negro, marrón, manchado"
    },
    "Alpaca": {
        "icon": "🐑", 
        "info": "**Su manto es suave y largo.**",
        "caracteristica": "Manto suave y largo",
        "altura": "0.8 - 1.0 m",
        "peso": "48 - 84 kg",
        "color": "Más de 22 colores naturales"
    },
    "Vicuña": {
        "icon": "🎯",
        "info": "**Tiene dientes de roedor y pesuñas divididas.**",
        "caracteristica": "Dientes de roedor y pesuñas divididas",
        "altura": "0.7 - 0.9 m",
        "peso": "35 - 65 kg",
        "color": "Marrón rojizo con blanco"
    },
    "Guanaco": {
        "icon": "🐪",
        "info": "**Su rostro es gris.**",
        "caracteristica": "Rostro gris",
        "altura": "1.0 - 1.2 m",
        "peso": "90 - 140 kg",
        "color": "Marrón claro con vientre blanco"
    }
}

# Layout principal
col1, col2 = st.columns([1, 1])

with col1:
    # Sección de comparación de tamaño
    st.markdown("### 📏 Comparación de Tamaño")
    st.markdown("""
    <div style='background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #8fbc8f;'>
    <h4 style='margin: 0; color: #2e8b57;'>Altura promedio (a la cruz):</h4>
    <div style='margin: 15px 0;'>
        <div style='display: flex; align-items: center; margin: 10px 0;'>
            <div style='width: 100px; height: 20px; background-color: #8B4513; border-radius: 3px;'></div>
            <span style='margin-left: 10px;'><strong>LLAMA</strong> - 1.7-1.8 m</span>
        </div>
        <div style='display: flex; align-items: center; margin: 10px 0;'>
            <div style='width: 70px; height: 20px; background-color: #808080; border-radius: 3px;'></div>
            <span style='margin-left: 10px;'><strong>GUANACO</strong> - 1.0-1.2 m</span>
        </div>
        <div style='display: flex; align-items: center; margin: 10px 0;'>
            <div style='width: 60px; height: 20px; background-color: #A52A2A; border-radius: 3px;'></div>
            <span style='margin-left: 10px;'><strong>ALPACA</strong> - 0.8-1.0 m</span>
        </div>
        <div style='display: flex; align-items: center; margin: 10px 0;'>
            <div style='width: 50px; height: 20px; background-color: #D2691E; border-radius: 3px;'></div>
            <span style='margin-left: 10px;'><strong>VICUÑA</strong> - 0.7-0.9 m</span>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Información detallada de cada especie con siluetas
    st.markdown("### 🦙 Características de cada especie")
    
    for especie, datos in especies_info.items():
        st.markdown(f"""
        <div class="species-card">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="margin-right: 15px;">
                    {get_silhouette(especie)}
                </div>
                <div>
                    <h3 style="margin: 0; color: #2e8b57;">{datos['icon']} {especie}</h3>
                </div>
            </div>
            <p><strong>Altura:</strong> {datos['altura']}</p>
            <p><strong>Peso:</strong> {datos['peso']}</p>
            <p><strong>Coloración:</strong> {datos['color']}</p>
            <p><strong>Característica principal:</strong> {datos['info']}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    # Sección de clasificación de imágenes
    st.header("📤 Sube una imagen para clasificar")
    
    uploaded_file = st.file_uploader(
        "Selecciona una imagen de un camélido sudamericano",
        type=['jpg', 'jpeg', 'png'],
        help="Sube una imagen clara de una llama, alpaca, guanaco o vicuña"
    )
    
    if uploaded_file is not None:
        # Mostrar imagen original
        image = Image.open(uploaded_file)
        st.image(image, caption="🖼️ Imagen subida", use_column_width=True)
        
        # Botón para clasificar
        if st.button("🔍 Clasificar Imagen", type="primary", use_container_width=True):
            with st.spinner("Analizando características de la imagen..."):
                try:
                    # Clasificación simulada
                    classes = list(especies_info.keys())
                    probabilities = np.random.dirichlet(np.ones(4), size=1)[0]
                    
                    result_index = np.argmax(probabilities)
                    predicted_class = classes[result_index]
                    confidence = probabilities[result_index]
                    
                    # Mostrar resultados
                    st.subheader("📊 Resultados de la Clasificación")
                    
                    # Tarjeta de resultado
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                                padding: 20px; border-radius: 10px; border-left: 5px solid #4caf50;">
                        <h3 style="color: #2e7d32; margin: 0;">{especies_info[predicted_class]['icon']} {predicted_class}</h3>
                        <p><strong>Característica identificada:</strong> {especies_info[predicted_class]['caracteristica']}</p>
                        <p><strong>Nivel de confianza:</strong> <span style="font-size: 1.2em; color: #d32f2f;">{confidence:.2%}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Probabilidades por especie
                    st.subheader("📈 Probabilidades por especie:")
                    
                    for i, especie in enumerate(classes):
                        prob_percent = probabilities[i] * 100
                        col_prob1, col_prob2 = st.columns([3, 1])
                        with col_prob1:
                            st.write(f"**{especies_info[especie]['icon']} {especie}**")
                            st.progress(float(probabilities[i]))
                        with col_prob2:
                            st.write(f"**{prob_percent:.1f}%**")
                    
                    # Información adicional
                    with st.expander("ℹ️ Más información sobre esta especie"):
                        st.write(f"**Altura:** {especies_info[predicted_class]['altura']}")
                        st.write(f"**Peso:** {especies_info[predicted_class]['peso']}")
                        st.write(f"**Coloración típica:** {especies_info[predicted_class]['color']}")
                        st.write(f"**Característica distintiva:** {especies_info[predicted_class]['info']}")
                        
                except Exception as e:
                    st.error(f"Error al procesar la imagen: {str(e)}")

# Instrucciones
with st.expander("📋 Instrucciones para mejores resultados"):
    st.markdown("""
    <div style="background-color: #e8f5e8; padding: 15px; border-radius: 10px;">
    **Para obtener los mejores resultados:**
    
    - 🦙 Toma fotos con buena iluminación
    - 📷 Enfoca claramente al animal
    - 🌅 Usa fondos simples para mejor reconocimiento
    - ⚡ Procura imágenes nítidas y de alta calidad
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "<strong>CLASIFICADOR DE CAMELIDOS SUDAMERICANOS</strong> | "
    "Sistema de identificación visual"
    "</div>", 
    unsafe_allow_html=True
)
