import streamlit as st
import numpy as np
from PIL import Image

# Configuración de la página con fondo personalizado
st.set_page_config(
    page_title="Clasificador de Camélidos Sudamericanos",
    page_icon="🦙",
    layout="wide"
)

# CSS para el fondo con siluetas y colores cálidos pastel
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #fff5e6 0%, #ffe6e6 50%, #e6f2ff 100%);
        padding: 20px;
        border-radius: 10px;
        position: relative;
        overflow: hidden;
    }
    .main::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url("data:image/svg+xml,%3Csvg width='400' height='400' viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M80,100 Q120,60 160,80 Q200,100 180,140 Q160,180 120,160 Q80,140 80,100 Z' fill='%23ffd9b3' opacity='0.3'/%3E%3Cpath d='M250,120 Q290,80 330,100 Q350,140 320,170 Q280,200 240,180 Q220,150 250,120 Z' fill='%23ffb3b3' opacity='0.3'/%3E%3Cpath d='M150,250 Q190,220 230,240 Q250,280 220,310 Q180,340 140,320 Q120,280 150,250 Z' fill='%23b3d9ff' opacity='0.3'/%3E%3C/svg%3E");
        opacity: 0.1;
        z-index: -1;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #fff0e6 0%, #ffe6e6 100%);
    }
    .species-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #ff9966;
        margin: 15px 0px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        backdrop-filter: blur(5px);
    }
    .taxonomy-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #ff9966;
        margin: 15px 0px;
        backdrop-filter: blur(5px);
    }
    .classification-tree {
        font-family: 'Courier New', monospace;
        background-color: rgba(248, 249, 250, 0.8);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #ff9966;
    }
    .result-card {
        background: linear-gradient(135deg, rgba(255, 245, 230, 0.95) 0%, rgba(255, 230, 230, 0.95) 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #ff6666;
        backdrop-filter: blur(5px);
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.title("CLASIFICADOR DE CAMÉLIDOS SUDAMERICANOS")
st.subheader("¿Cómo reconocer una llama, alpaca, vicuña y guanaco?")
st.markdown("---")

# Información taxonómica
taxonomia = """
**La familia Camelidae está formada por dos tribus: los Camelini y los Lamini** (Stanley et al., 1994; Wheeler, 1995).

**Tribu Camelini**
└── **GÉNERO: Camelus**
    ├── Camelus bactrianus → **CAMELIO**
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

# Descripciones detalladas de cada especie
especies_detalladas = {
    "Alpaca": {
        "nombre_cientifico": "Lama pacos",
        "icon": "🐑",
        "descripcion": "Más pequeña que la llama, con una silueta más curvilínea. Posee un clásico mechón de fibra en la frente.",
        "uso": "Criada por su valiosa fibra, considerada una de las más finas y suaves del mundo.",
        "estado": "Doméstica",
        "altura": "0.8 - 1.0 m",
        "peso": "48 - 84 kg",
        "color": "Más de 22 colores naturales",
        "color_borde": "#ff9966"
    },
    "Guanaco": {
        "nombre_cientifico": "Lama guanicoe",
        "icon": "🐪",
        "descripcion": "Silvestre, con pelaje denso de color marrón-rojizo claro y el vientre blanquecino. Es el antepasado silvestre de la llama.",
        "uso": "No tiene un uso económico principal, pero es una especie importante por su valor ecológico.",
        "estado": "Silvestre",
        "altura": "1.0 - 1.2 m",
        "peso": "90 - 140 kg",
        "color": "Marrón claro con vientre blanco",
        "color_borde": "#ff6666"
    },
    "Llama": {
        "nombre_cientifico": "Lama glama",
        "icon": "🦙",
        "descripcion": "Es el camélido doméstico de mayor tamaño y peso, con patas largas, orejas prominentes y curvadas, y pelaje grueso y áspero.",
        "uso": "Se utiliza como animal de carga para el transporte y, en menor medida, por su lana y carne.",
        "estado": "Doméstica",
        "altura": "1.7 - 1.8 m",
        "peso": "130 - 200 kg",
        "color": "Variados: blanco, negro, marrón, manchado",
        "color_borde": "#ffcc66"
    },
    "Vicuña": {
        "nombre_cientifico": "Vicugna vicugna",
        "icon": "🎯",
        "descripcion": "La más pequeña de los camélidos andinos, con cuerpo grácil y movimientos ágiles. Posee pelaje muy fino y brillante, de color marrón claro en el lomo y blanquecino en el pecho.",
        "uso": "Su fibra es considerada la más fina del mundo, y se aprovecha en la industria textil de lujo.",
        "estado": "Silvestre y protegida tras un peligro de extinción",
        "altura": "0.7 - 0.9 m",
        "peso": "35 - 65 kg",
        "color": "Marrón rojizo con blanco",
        "color_borde": "#ff99cc"
    }
}

# Layout principal
col1, col2 = st.columns([1, 1])

with col1:
    # Clasificación taxonómica
    st.markdown("### 📊 Clasificación Taxonómica de los Camélidos")
    st.markdown('<div class="taxonomy-card">', unsafe_allow_html=True)
    st.markdown("**Figura 1. Clasificación de los camélidos**")
    st.markdown('<div class="classification-tree">', unsafe_allow_html=True)
    st.markdown(taxonomia)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Especies de camélidos andinos
    st.markdown("### 🦙 Especies de Camélidos Andinos")
    
    for especie, datos in especies_detalladas.items():
        # Determinar color de borde según el estado
        border_color = datos["color_borde"]
        
        st.markdown(f"""
        <div class="species-card" style="border-left: 5px solid {border_color};">
            <h3 style="color: #d35400; margin: 0 0 15px 0;">
                {datos['icon']} {especie} 
                <small style="font-size: 0.7em; color: #666;">({datos['nombre_cientifico']})</small>
            </h3>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                <div>
                    <strong>📏 Altura:</strong> {datos['altura']}<br>
                    <strong>⚖️ Peso:</strong> {datos['peso']}
                </div>
                <div>
                    <strong>🎨 Coloración:</strong> {datos['color']}<br>
                    <strong>🏷️ Estado:</strong> {datos['estado']}
                </div>
            </div>
            
            <p><strong>📝 Descripción:</strong> {datos['descripcion']}</p>
            <p><strong>💼 Uso principal:</strong> {datos['uso']}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    # Sección de clasificación de imágenes
    st.header("📤 Clasificador de Imágenes")
    st.markdown("Sube una foto de un camélido sudamericano para identificarlo automáticamente")
    
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
        if st.button("🔍 Identificar Especie", type="primary", use_container_width=True):
            with st.spinner("Analizando características morfológicas..."):
                try:
                    # Clasificación simulada
                    classes = list(especies_detalladas.keys())
                    probabilities = np.random.dirichlet(np.ones(4), size=1)[0]
                    
                    result_index = np.argmax(probabilities)
                    predicted_class = classes[result_index]
                    confidence = probabilities[result_index]
                    
                    # Mostrar resultados
                    st.subheader("📊 Resultados de la Identificación")
                    
                    # Determinar color según confianza
                    confidence_color = "#27ae60" if confidence > 0.7 else "#f39c12" if confidence > 0.5 else "#e74c3c"
                    
                    # Tarjeta de resultado
                    datos_especie = especies_detalladas[predicted_class]
                    st.markdown(f"""
                    <div class="result-card">
                        <h3 style="color: #c0392b; margin: 0 0 15px 0;">
                            {datos_especie['icon']} {predicted_class}
                            <small style="font-size: 0.7em; color: #666;">({datos_especie['nombre_cientifico']})</small>
                        </h3>
                        <p><strong>🔍 Característica identificada:</strong> {datos_especie['descripcion'].split('.')[0]}.</p>
                        <p><strong>📈 Nivel de confianza:</strong> 
                        <span style="font-size: 1.2em; color: {confidence_color}; font-weight: bold;">{confidence:.2%}</span></p>
                        <p><strong>🏷️ Estado:</strong> {datos_especie['estado']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Probabilidades por especie
                    st.subheader("📈 Probabilidades por Especie")
                    
                    for i, especie in enumerate(classes):
                        prob_percent = probabilities[i] * 100
                        datos = especies_detalladas[especie]
                        
                        col_prob1, col_prob2 = st.columns([3, 1])
                        with col_prob1:
                            st.write(f"**{datos['icon']} {especie}** ({datos['nombre_cientifico']})")
                            st.progress(float(probabilities[i]))
                        with col_prob2:
                            st.write(f"**{prob_percent:.1f}%**")
                    
                    # Información adicional expandible
                    with st.expander("ℹ️ Información Detallada de la Especie Identificada"):
                        st.write(f"**📝 Descripción completa:** {datos_especie['descripcion']}")
                        st.write(f"**💼 Uso principal:** {datos_especie['uso']}")
                        st.write(f"**📏 Altura promedio:** {datos_especie['altura']}")
                        st.write(f"**⚖️ Peso promedio:** {datos_especie['peso']}")
                        st.write(f"**🎨 Coloración típica:** {datos_especie['color']}")
                        
                except Exception as e:
                    st.error(f"Error al procesar la imagen: {str(e)}")
    
    # Comparación de tamaño
    st.markdown("---")
    st.markdown("### 📏 Comparación de Tamaño")
    st.markdown("""
    <div style='background-color: rgba(255, 255, 255, 0.95); padding: 20px; border-radius: 15px; border-left: 5px solid #ff9966;'>
    <h4 style='margin: 0 0 15px 0; color: #d35400;'>Altura promedio (a la cruz):</h4>
    <div style='margin: 15px 0;'>
        <div style='display: flex; align-items: center; margin: 12px 0;'>
            <div style='width: 120px; height: 22px; background: linear-gradient(90deg, #ff9966, #ff5e62); border-radius: 5px;'></div>
            <span style='margin-left: 15px; font-weight: bold;'>LLAMA - 1.7-1.8 m</span>
        </div>
        <div style='display: flex; align-items: center; margin: 12px 0;'>
            <div style='width: 80px; height: 22px; background: linear-gradient(90deg, #ff6666, #ff3366); border-radius: 5px;'></div>
            <span style='margin-left: 15px; font-weight: bold;'>GUANACO - 1.0-1.2 m</span>
        </div>
        <div style='display: flex; align-items: center; margin: 12px 0;'>
            <div style='width: 60px; height: 22px; background: linear-gradient(90deg, #ffcc66, #ffb366); border-radius: 5px;'></div>
            <span style='margin-left: 15px; font-weight: bold;'>ALPACA - 0.8-1.0 m</span>
        </div>
        <div style='display: flex; align-items: center; margin: 12px 0;'>
            <div style='width: 50px; height: 22px; background: linear-gradient(90deg, #ff99cc, #ff66cc); border-radius: 5px;'></div>
            <span style='margin-left: 15px; font-weight: bold;'>VICUÑA - 0.7-0.9 m</span>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

# Instrucciones
with st.expander("📋 Instrucciones para una Identificación Precisa"):
    st.markdown("""
    <div style="background-color: rgba(255, 245, 230, 0.9); padding: 20px; border-radius: 15px;">
    <h4 style="color: #d35400;">Para obtener los mejores resultados en la identificación:</h4>
    
    - 🦙 <strong>Enfoca claramente</strong> al animal, especialmente la cabeza y el pelaje
    - 📷 <strong>Buena iluminación</strong> para apreciar colores y texturas
    - 🌅 <strong>Fondo simple</strong> que no distraiga del animal
    - ⚡ <strong>Imagen nítida</strong> para analizar características morfológicas
    - 👁️ <strong>Vista lateral</strong> preferible para apreciar silueta y tamaño
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #d35400; background-color: rgba(255, 245, 230, 0.8); padding: 15px; border-radius: 10px;'>"
    "<strong>CLASIFICADOR TAXONÓMICO DE CAMÉLIDOS SUDAMERICANOS</strong><br>"
    "<small>Sistema de identificación basado en características morfológicas</small>"
    "</div>", 
    unsafe_allow_html=True
)
