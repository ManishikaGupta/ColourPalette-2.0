import os
import requests
import numpy as np
from PIL import Image
import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tensorflow.keras.models import load_model

app = FastAPI(title="Skin Undertone Predictor API", description="API to predict skin undertones and return fashion color palettes.")

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model download configuration (matching original app.py)
MODEL_URL = "https://drive.google.com/uc?id=1X2bJ_TgEnT4K1VkWLW8c9H4MYmoAP9DM"
MODEL_PATH = "undertone_model.h5"

def download_model():
    if not os.path.exists(MODEL_PATH):
        print("⬇️ Downloading model from Google Drive...")
        with requests.get(MODEL_URL, stream=True) as r:
            r.raise_for_status()
            with open(MODEL_PATH, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("✅ Model downloaded successfully.")
    return MODEL_PATH

# Load model on startup
model_file = download_model()
model = load_model(model_file)
labels = ['cool', 'neutral', 'warm', 'olive']

# Preprocessing function (matching original app.py)
def preprocess(img):
    img = img.resize((224, 224))
    arr = np.array(img) / 255.0
    return np.expand_dims(arr, axis=0)

# Undertone color palettes (matching original app.py)
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

# Rich fashion and care recommendations based on skin undertones
fashion_recommendations = {
    "warm": {
        "clothing": [
            {"title": "Best Colors", "desc": "Earth tones such as mustard yellow, honey, burnt orange, terracotta, and warm coral look natural and glowing on you."},
            {"title": "Neutrals to Wear", "desc": "Choose warm camel, beige, sand, and rich chocolate brown instead of stark white or black."},
            {"title": "Colors to Avoid", "desc": "Icy shades, electric blue, and silver, which can make your skin look pale or washed out."}
        ],
        "makeup": [
            {"title": "Lips", "desc": "Look stunning in peach, copper, coral, warm terracottas, and tomato reds."},
            {"title": "Eyes", "desc": "Warm metallic shades like bronze, yellow gold, and copper eyeshadows complement your eyes best."},
            {"title": "Blush", "desc": "Soft peach, warm apricot, and bronze-toned blushes will enhance your natural warmth."}
        ],
        "jewelry": [
            {"title": "Metal Preference", "desc": "Yellow gold and copper accent your undertone beautifully, adding a rich glow."}
        ]
    },
    "cool": {
        "clothing": [
            {"title": "Best Colors", "desc": "Vibrant blues (cobalt, midnight, navy), emerald green, lavender, lilac, and berry reds complement you perfectly."},
            {"title": "Neutrals to Wear", "desc": "Opt for crisp white, charcoal grey, and cool taupe for a sleek, elegant look."},
            {"title": "Colors to Avoid", "desc": "Orange, tomato red, and mustard yellow, which can clash with your natural undertones."}
        ],
        "makeup": [
            {"title": "Lips", "desc": "Choose cool pink, plum, berry, ruby red, or magenta lipstick shades."},
            {"title": "Eyes", "desc": "Silver, cool lavender, grey, and ice blue shadows make your eyes pop."},
            {"title": "Blush", "desc": "Rosy pink, cool mauve, and light berry blushes highlight your cool tones."}
        ],
        "jewelry": [
            {"title": "Metal Preference", "desc": "Silver, white gold, and platinum look stunning on your skin, enhancing its cool brightness."}
        ]
    },
    "neutral": {
        "clothing": [
            {"title": "Best Colors", "desc": "You look great in a mix of tones: dusty pink, sage green, lagoon blue, mauve, and soft peach."},
            {"title": "Neutrals to Wear", "desc": "Off-white, greige, stone, coffee brown, and medium grey are perfect base colors."},
            {"title": "Colors to Avoid", "desc": "Super bright neon or overly saturated colors that can overwhelm your balanced tone."}
        ],
        "makeup": [
            {"title": "Lips", "desc": "Nudes, soft dusty pinks, mauve, and classic neutral red lipsticks suit you well."},
            {"title": "Eyes", "desc": "Neutral earth tones, taupe, soft brown, and champagne shimmer eyeshadows."},
            {"title": "Blush", "desc": "Dusty rose, soft peach, and neutral bronze shades."}
        ],
        "jewelry": [
            {"title": "Metal Preference", "desc": "You are versatile! Both yellow gold and silver/white gold complement your neutral undertone beautifully."}
        ]
    },
    "olive": {
        "clothing": [
            {"title": "Best Colors", "desc": "Teal, burgundy, deep plum, moss green, forest green, electric blue, and deep navy showcase your rich undertone."},
            {"title": "Neutrals to Wear", "desc": "Charcoal grey, true black, cool beige, and gunmetal give you a striking look."},
            {"title": "Colors to Avoid", "desc": "Very pale pastels, bright neon yellows, and warm orange, which can make your skin look sallow."}
        ],
        "makeup": [
            {"title": "Lips", "desc": "Berry, dark plum, brick red, and deep mauve colors look incredibly flattering on you."},
            {"title": "Eyes", "desc": "Emerald green, gold, warm brown, and copper eyeshadows bring out the depth of your eyes."},
            {"title": "Blush", "desc": "Warm rose, bronze, or terracotta blushes add the perfect touch of color."}
        ],
        "jewelry": [
            {"title": "Metal Preference", "desc": "Rose gold, yellow gold, and brass look rich and complement the green/golden hues of olive skin."}
        ]
    }
}

@app.post("/api/predict")
async def predict_endpoint(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # Preprocess
        processed_image = preprocess(image)
        
        # Predict
        preds = model.predict(processed_image)[0]
        idx = np.argmax(preds)
        confidence = float(preds[idx])
        predicted_label = labels[idx]
        
        return {
            "success": True,
            "undertone": predicted_label,
            "confidence": confidence,
            "palette": undertone_palette.get(predicted_label, {}),
            "recommendations": fashion_recommendations.get(predicted_label, {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# Serve frontend static assets if the build folder exists
frontend_build_path = "/Users/manishikagupta/Documents/ColourPalette-2.0-main/frontend/dist"

if os.path.exists(frontend_build_path):
    # Mount assets folder
    assets_path = os.path.join(frontend_build_path, "assets")
    if os.path.exists(assets_path):
        app.mount("/assets", StaticFiles(directory=assets_path), name="assets")
    
    # Mount image folders (preserving original images)
    for img_dir in ["index-img", "contests-img", "products-img"]:
        dir_path = os.path.join(frontend_build_path, img_dir)
        if os.path.exists(dir_path):
            app.mount(f"/{img_dir}", StaticFiles(directory=dir_path), name=img_dir)
            
    # Serve other top level static files directly
    @app.get("/favicon.svg")
    def serve_favicon():
        from fastapi.responses import FileResponse
        return FileResponse(os.path.join(frontend_build_path, "favicon.svg"))

    @app.get("/image.png")
    def serve_logo():
        from fastapi.responses import FileResponse
        return FileResponse(os.path.join(frontend_build_path, "image.png"))

@app.get("/")
def read_index():
    from fastapi.responses import FileResponse
    index_file = os.path.join(frontend_build_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "FastAPI is running. Please build the React frontend to serve it here."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
