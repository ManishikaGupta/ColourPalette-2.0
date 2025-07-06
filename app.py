import streamlit as st
import gdown
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

# Load the trained model
@st.cache_resource
def load_model_from_drive():
    file_id = "1X2bJ_TgEnT4K1VkWLW8c9H4MYmoAP9DM"  # ✅ Replace with your own file ID
    url = f"https://drive.google.com/uc?id={file_id}"
    output_path = "model.h5"

    if not os.path.exists(output_path):
        gdown.download(url, output_path, quiet=False)

    model = tf.keras.models.load_model(output_path)
    return model

model = load_model_from_drive()

labels = ['cool', 'neutral', 'warm', 'olive']

# Preprocessing function
def preprocess(img):
    img = img.convert("RGB")  # Ensures 3 channels (RGB)
    img = img.resize((224, 224))
    arr = np.array(img) / 255.0
    return np.expand_dims(arr, axis=0)

# Color palettes
undertone_palette = {
    "warm": {
        "mustard yellow": "#FFDB58", "burnt orange": "#CC5500", "terracotta": "#E2725B",
        "warm red": "#C72C48", "coral": "#FF7F50", "peach": "#FFE5B4", "deep berry": "#8A1538",
        "caramel": "#AF6E4D", "chestnut": "#954535", "amber": "#FFBF00", "sunflower yellow": "#FFC512",
        "honey": "#FFC30B", "copper": "#B87333", "rust": "#B7410E", "bronze": "#CD7F32", "turquoise": "#40E0D0",
        "olive green": "#808000", "avocado": "#568203", "creamy off-white": "#FAF3E0", "camel": "#C19A6B",
        "beige": "#F5F5DC", "sand": "#C2B280", "chocolate brown": "#381819"
    },
    "cool": {
        "cobalt blue": "#0047AB", "midnight blue": "#191970", "emerald green": "#50C878",
        "jade": "#00A86B", "lavender": "#E6E6FA", "lilac": "#C8A2C8", "ice blue": "#AFDBF5",
        "powder blue": "#B0E0E6", "mint": "#98FF98", "ice pink": "#FFDDE6", "rose": "#FF007F",
        "blush": "#DE5D83", "ruby": "#E0115F", "cranberry": "#950714", "navy": "#000080",
        "periwinkle": "#CCCCFF", "steel blue": "#4682B4", "crisp white": "#F8F8FF",
        "charcoal grey": "#36454F", "cool taupe": "#D8B4A6", "pearl grey": "#C0C0C0", "silver": "#C0C0C0"
    },
    "neutral": {
        "dusty pink": "#DCAE96", "rosewood": "#65000B", "jade": "#00A86B", "sage green": "#9DC183",
        "lagoon blue": "#4CB7A5", "light peach": "#FFE0B5", "mauve": "#E0B0FF", "warm taupe": "#D2B1A3",
        "medium green": "#3EB489", "slate blue": "#6A5ACD", "muted teal": "#367588", "stone": "#867E76",
        "greige": "#BEB6AA", "off-white": "#F8F8F0", "soft black": "#2E2E2E", "coffee brown": "#4B3621",
        "medium grey": "#BEBEBE", "mink": "#A27B5C", "sandstone": "#786D5F"
    },
    "olive": {
        "teal": "#008080", "burgundy": "#800020", "plum": "#8E4585", "cool grey": "#8C92AC",
        "moss green": "#8A9A5B", "forest green": "#228B22", "light mint": "#AAF0D1", "aqua": "#00FFFF",
        "seafoam": "#9FE2BF", "jade green": "#00A86B", "periwinkle": "#CCCCFF", "lavender grey": "#C4C3D0",
        "charcoal": "#36454F", "true black": "#000000", "gunmetal": "#2a3439", "fuchsia": "#FF00FF",
        "raspberry": "#E30B5C", "icy plum": "#D8A1C4", "electric blue": "#7DF9FF", "deep navy": "#000F89",
        "stone grey": "#928E85", "soft white": "#FCFBF4", "cool beige": "#D8CAB8", "blue-grey": "#7393B3"
    }
}

# Function to display color blocks
def display_color_blocks(palette_dict):
    html_blocks = ""
    for color_name, hex_value in palette_dict.items():
        block = f"""
        <div style='
            display:inline-block;
            width:80px;
            height:80px;
            margin:5px;
            background-color:{hex_value};
            border-radius:10px;
            border:1px solid #333;
            text-align:center;
            color:white;
            font-size:10px;
            padding-top:60px;
            box-shadow:1px 1px 5px rgba(0,0,0,0.3);
        '>{color_name}</div>
        """
        html_blocks += block
    st.markdown(html_blocks, unsafe_allow_html=True)

# Streamlit UI
st.title("🎨 Skin Undertone Predictor with Color Palette")

uploaded = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Uploaded Image", use_container_width=True)
    
    x = preprocess(img)
    preds = model.predict(x)[0]
    idx = np.argmax(preds)
    conf = preds[idx]
    predicted_label = labels[idx]

    st.markdown(f"### 🎯 Predicted Undertone: **{predicted_label.title()}** ({conf*100:.1f}% confidence)")
    
    # Palette
    st.markdown("### 👗 Suggested Colors:")
    display_color_blocks(undertone_palette[predicted_label])
