import streamlit as st
import numpy as np
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Clasificador de Camélidos Sudamericanos",
    page_icon="🦙",
    layout="wide"
)

# CSS con colores suaves y diseño moderno
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .title-container {
        background: linear-gradient(135deg, #fff9c4 0%, #ffecb3 100%);
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: none;
    }
    .subtitle-container {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border: none;
    }
    .species-card-alpaca {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0px;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2);
        border-left: 5px solid #4caf50;
    }
    .species-card-guanaco {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0px;
        box-shadow: 0 4px 12px rgba(33, 150, 243, 0.2);
        border-left: 5px solid #2196f3;
    }
    .species-card-llama {
        background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0px;
        box-shadow: 0 4px 12px rgba(233, 30, 99, 0.2);
        border-left: 5px solid #e91e63;
    }
    .species-card-vicuna {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0px;
        box-shadow: 0 4px 12px rgba(255, 152, 0, 0.2);
        border-left: 5px solid #ff9800;
    }
    .species-title-alpaca {
        color: #2e7d32;
        font-size: 1.4em;
        font-weight: 700;
        margin-bottom: 15px;
        text-align: center;
    }
    .species-title-guanaco {
        color: #1565c0;
        font-size: 1.4em;
        font-weight: 700;
        margin-bottom: 15px;
        text-align: center;
    }
    .species-title-llama {
        color: #c2185b;
        font-size: 1.4em;
        font-weight: 700;
        margin-bottom: 15px;
        text-align: center;
    }
    .species-title-vicuna {
        color: #ef6c00;
        font-size: 1.4em;
        font-weight: 700;
        margin-bottom: 15px;
        text-align: center;
    }
    .species-content {
        color: #5d4037;
        line-height: 1.6;
        font-size: 1em;
    }
    .species-content strong {
        color: #455a64;
    }
    .upload-container {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .result-container {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .size-comparison {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    .progress-bar {
        background: linear-gradient(90deg, #81c784, #4caf50);
        border-radius: 10px;
    }
    .stButton button {
        background: linear-gradient(135deg, #4fc3f7 0%, #29b6f6 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 25px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(41, 182, 246, 0.3);
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #29b6f6 0%, #039be5 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(41, 182, 246, 0.4);
    }
    .species-icon {
        font-size: 24px;
        margin-right: 10px;
    }
    .taxonomy-box {
        background: linear-gradient(135deg, #f5f5f5 0%, #eeeeee 100%);
        padding: 20px;
        border-radius: 15px;
        font-family: 'Courier New', monospace;
        line-height: 1.6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .species-grid {
        background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%);
        padding: 25px;
        border-radius: 20px;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Título principal con diseño atractivo
st.markdown('<div class="title-container">', unsafe_allow_html=True)
st.markdown('<h1 style="color: #5d4037; margin-bottom: 10px;">🦙 CLASIFICADOR DE CAMÉLIDOS SUDAMERICANOS</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="color: #7e57c2; font-weight: 300;">Descubre y reconoce las especies de camélidos andinos</h3>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Información taxonómica
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

# Texto exacto proporcionado para cada especie
especies_texto = {
    "Alpaca": {
        "nombre_cientifico": "Lama pacos",
        "icon": "🐑",
        "texto_completo": "**Alpaca (Lama pacos)**\n\n**Descripción:** Más pequeña que la llama, con una silueta más curvilínea. Posee un clásico mechón de fibra en la frente.\n\n**Uso:** Criada por su valiosa fibra, considerada una de las más finas y suaves del mundo.\n\n**Estado:** Doméstica.",
        "color_clase": "alpaca"
    },
    "Guanaco": {
        "nombre_cientifico": "Lama guanicoe",
        "icon": "🦌",
        "texto_completo": "**Guanaco (Lama guanicoe)**\n\n**Descripción:** Silvestre, con pelaje denso de color marrón-rojizo claro y el vientre blanquecino. Es el antepasado silvestre de la llama.\n\n**Uso:** No tiene un uso económico principal, pero es una especie importante por su valor ecológico.\n\n**Estado:** Silvestre.",
        "color_clase": "guanaco"
    },
    "Llama": {
        "nombre_cientifico": "Lama glama",
        "icon": "🦙",
        "texto_completo": "**Llama (Lama glama)**\n\n**Descripción:** Es el camélido doméstico de mayor tamaño y peso, con patas largas, orejas prominentes y curvadas, y pelaje grueso y áspero.\n\n**Uso:** Se utiliza como animal de carga para el transporte y, en menor medida, por su lana y carne.\n\n**Estado:** Doméstica.",
        "color_clase": "llama"
    },
    "Vicuña": {
        "nombre_cientifico": "Vicugna vicugna",
        "icon": "🐾",
        "texto_completo": "**Vicuña (Vicugna vicugna)**\n\n**Descripción:** La más pequeña de los camélidos andinos, con cuerpo grácil y movimientos ágiles. Posee pelaje muy fino y brillante, de color marrón claro en el lomo y blanquecino en el pecho.\n\n**Uso:** Su fibra es considerada la más fina del mundo, y se aprovecha en la industria textil de lujo.\n\n**Estado:** Silvestre y protegida tras un peligro de extinción.",
        "color_clase": "vicuna"
    }
}

# Layout principal - columna izquierda más pequeña (1/4)
col1, col2 = st.columns([1, 3])

with col1:
    # Clasificación taxonómica
    st.markdown('<div class="subtitle-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #1565c0; margin: 0;">📊 Clasificación Taxonómica</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #1565c0; margin: 5px 0 0 0; font-size: 0.9em;">Figura 1. Clasificación de los camélidos</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="taxonomy-box">', unsafe_allow_html=True)
    st.markdown(taxonomia)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Comparación de tamaño
    st.markdown('<div class="size-comparison">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: #5d4037; margin-bottom: 15px;">📏 Comparación de Tamaño</h4>', unsafe_allow_html=True)
    st.markdown('<p style="color: #5d4037; font-weight: 600;">Altura promedio (a la cruz):</p>', unsafe_allow_html=True)
    
    especies_altura = [
        ("🦙 LLAMA", "1.7-1.8 m", 100),
        ("🦌 GUANACO", "1.0-1.2 m", 70),
        ("🐑 ALPACA", "0.8-1.0 m", 55),
        ("🐾 VICUÑA", "0.7-0.9 m", 45)
    ]
    
    for especie, altura, width in especies_altura:
        st.markdown(f'<p style="color: #5d4037; margin: 10px 0 5px 0;">{especie} - {altura}</p>', unsafe_allow_html=True)
        st.markdown(f'<div style="width: {width}%; height: 12px; background: linear-gradient(90deg, #81c784, #4caf50); border-radius: 6px; margin-bottom: 15px;"></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Sección principal de clasificación de imágenes
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #7b1fa2; text-align: center; margin-bottom: 20px;">📸 Clasificador de Imágenes</h2>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Selecciona una imagen de un camélido sudamericano",
        type=['jpg', 'jpeg', 'png'],
        help="Sube una imagen clara de una llama, alpaca, guanaco o vicuña"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        # Mostrar imagen original en grande
        image = Image.open(uploaded_file)
        col_img, col_btn = st.columns([3, 1])
        
        with col_img:
            st.image(image, caption="🖼️ Imagen cargada para análisis", use_container_width=True)
        
        with col_btn:
            if st.button("🔍 Analizar Imagen", type="primary", use_container_width=True):
                with st.spinner("🔬 Analizando características morfológicas..."):
                    try:
                        # Simulación de clasificación
                        classes = list(especies_texto.keys())
                        probabilities = np.random.dirichlet(np.ones(4) * 15, size=1)[0]
                        
                        result_index = np.argmax(probabilities)
                        predicted_class = classes[result_index]
                        confidence = probabilities[result_index]
                        
                        # Mostrar resultados
                        st.markdown('<div class="result-container">', unsafe_allow_html=True)
                        st.markdown('<h3 style="color: #2e7d32; text-align: center;">🎯 Resultados del Análisis</h3>', unsafe_allow_html=True)
                        
                        # Tarjeta de resultado principal
                        st.success(f"**Especie identificada:** {especies_texto[predicted_class]['icon']} **{predicted_class}**")
                        st.metric("Nivel de confianza", f"{confidence:.2%}")
                        
                        # Información de la especie identificada
                        color_clase = especies_texto[predicted_class]['color_clase']
                        st.markdown(f'<div class="species-card-{color_clase}">', unsafe_allow_html=True)
                        st.markdown(f'<div class="species-title-{color_clase}">{especies_texto[predicted_class]["icon"]} {predicted_class}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="species-content">{especies_texto[predicted_class]["texto_completo"]}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Probabilidades detalladas
                        st.markdown('<div style="background: white; padding: 20px; border-radius: 15px; margin-top: 20px;">', unsafe_allow_html=True)
                        st.markdown('<h4 style="color: #5d4037;">📈 Probabilidades por especie:</h4>', unsafe_allow_html=True)
                        
                        for i, especie in enumerate(classes):
                            prob_percent = probabilities[i] * 100
                            col_prob1, col_prob2, col_prob3 = st.columns([1, 3, 1])
                            with col_prob1:
                                st.markdown(f'<div class="species-icon">{especies_texto[especie]["icon"]}</div>', unsafe_allow_html=True)
                            with col_prob2:
                                st.write(f"**{especie}**")
                                st.progress(float(probabilities[i]))
                            with col_prob3:
                                st.write(f"**{prob_percent:.1f}%**")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"❌ Error al procesar la imagen: {str(e)}")

# Información de especies en la parte inferior CON FONDO COLORIDO
st.markdown("---")
st.markdown('<div class="species-grid">', unsafe_allow_html=True)
st.markdown('<div class="subtitle-container">', unsafe_allow_html=True)
st.markdown('<h3 style="color: #1565c0; margin: 0;">🦙 Especies de Camélidos Andinos</h3>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Grid de 2x2 para las especies con colores diferentes
cols = st.columns(2)
for i, (especie, datos) in enumerate(especies_texto.items()):
    with cols[i % 2]:
        color_clase = datos['color_clase']
        st.markdown(f'<div class="species-card-{color_clase}">', unsafe_allow_html=True)
        st.markdown(f'<div class="species-title-{color_clase}">{datos["icon"]} {especie}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="species-content">{datos["texto_completo"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer atractivo
st.markdown("---")
st.markdown('<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #f5f5f5 0%, #eeeeee 100%); border-radius: 15px;">', unsafe_allow_html=True)
st.markdown('<h4 style="color: #5d4037; margin: 0;">🦙 CLASIFICADOR DE CAMÉLIDOS SUDAMERICANOS</h4>', unsafe_allow_html=True)
st.markdown('<p style="color: #666; margin: 5px 0 0 0;">Sistema inteligente de identificación visual</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
