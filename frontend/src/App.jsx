import { useState, useRef, useEffect } from 'react';
import { 
  Camera, 
  Upload, 
  RefreshCw, 
  Check, 
  Sparkles, 
  Shirt, 
  Heart 
} from 'lucide-react';
import './App.css';

// Change this to your deployed Render backend URL after deploying it!
const RENDER_BACKEND_URL = "https://your-backend-app.onrender.com";

// Auto-detect backend URL based on host (falls back to local API port 8000 during dev, or RENDER_BACKEND_URL in prod)
const BACKEND_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://127.0.0.1:8000'
  : RENDER_BACKEND_URL;


function App() {
  const [activeTab, setActiveTab] = useState('upload'); // 'upload' or 'camera' inside analyzer
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  
  // Camera state
  const [cameraStream, setCameraStream] = useState(null);
  const [cameraError, setCameraError] = useState(null);
  const videoElementRef = useRef(null);
  const videoRef = (node) => {
    videoElementRef.current = node;
    if (node && cameraStream && node.srcObject !== cameraStream) {
      node.srcObject = cameraStream;
    }
  };

  // Prediction State
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  
  // UI States
  const [copiedColor, setCopiedColor] = useState(null);
  const [recTab, setRecTab] = useState('clothing'); // 'clothing', 'makeup', 'jewelry'
  const fileInputRef = useRef(null);

  // Handle stream cleanup
  const stopCamera = () => {
    if (cameraStream) {
      cameraStream.getTracks().forEach(track => track.stop());
      setCameraStream(null);
    }
  };

  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, [cameraStream]);

  // Start webcam
  const startCamera = async () => {
    setCameraError(null);
    setSelectedFile(null);
    setPreviewUrl(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 480 } } 
      });
      setCameraStream(stream);
    } catch (err) {
      console.error("Camera access error:", err);
      setCameraError("Unable to access camera. Please ensure permissions are granted.");
    }
  };

  // Switch analyzer input tabs
  const handleTabChange = (tab) => {
    setActiveTab(tab);
    setError(null);
    if (tab === 'camera') {
      startCamera();
    } else {
      stopCamera();
      setPreviewUrl(null);
      setSelectedFile(null);
    }
  };

  // File Upload Handlers
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      processSelectedFile(file);
    }
  };

  const processSelectedFile = (file) => {
    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    setError(null);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      processSelectedFile(file);
    }
  };

  // Capture Photo from Camera
  const capturePhoto = () => {
    if (videoElementRef.current && cameraStream) {
      const video = videoElementRef.current;
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      const ctx = canvas.getContext('2d');
      // Mirror horizontal translation for intuitive selfie look
      ctx.translate(canvas.width, 0);
      ctx.scale(-1, 1);
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      
      canvas.toBlob((blob) => {
        const file = new File([blob], "selfie.jpg", { type: "image/jpeg" });
        setSelectedFile(file);
        const url = URL.createObjectURL(blob);
        setPreviewUrl(url);
        stopCamera();
      }, 'image/jpeg', 0.95);
    }
  };

  // Reset Analyzer
  const resetAnalyzer = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    if (activeTab === 'camera') {
      startCamera();
    }
  };

  // Call prediction backend API
  const analyzeUndertone = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch(`${BACKEND_URL}/api/predict`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server returned error status: ${response.status}`);
      }

      const data = await response.json();
      if (data.success) {
        setResult(data);
      } else {
        throw new Error(data.detail || "Analysis failed.");
      }
    } catch (err) {
      console.error("API Call error:", err);
      setError("Failed to process prediction. Please ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  // Copy Color Hex code
  const copyColorToClipboard = (hex, name) => {
    navigator.clipboard.writeText(hex);
    setCopiedColor({ name, hex });
    setTimeout(() => {
      setCopiedColor(null);
    }, 2000);
  };

  return (
    <>
      {/* Header Navigation Bar - Muted Layout */}
      <header>
        <div className="logo-container" onClick={() => window.location.reload()}>
          <img src="image.png" alt="Logo" style={{width: '32px', height: 'auto'}} />
          <span className="logo-text" style={{fontSize: '32px'}}>Aura</span>
        </div>
      </header>

      {/* Main Content Area */}
      <main>
        {/* Hero Welcome banner */}
        <section className="hero-section">
          <h3 className="hero-subtitle">Elevate Your Personal Style</h3>
          <h1 className="hero-title">Discover Your Perfect Color Palette</h1>
          <p className="hero-description">
            Upload a selfie or click a picture in real-time. Aura analyzes your skin undertone to generate a curated palette of styling, clothing, and makeup recommendations tailored to you.
          </p>
        </section>

        {/* Core app layout */}
        <section className="app-container" style={{margin: '10px auto 50px'}}>
          
          {/* Card 1: Input Center (Webcam / Upload) */}
          <div className="card">
            <div className="tabs">
              <button 
                className={`tab-btn ${activeTab === 'upload' ? 'active' : ''}`}
                onClick={() => handleTabChange('upload')}
              >
                Upload Photo
              </button>
              <button 
                className={`tab-btn ${activeTab === 'camera' ? 'active' : ''}`}
                onClick={() => handleTabChange('camera')}
              >
                Take Selfie
              </button>
            </div>

            {/* Upload Tab */}
            {activeTab === 'upload' && !previewUrl && (
              <div 
                className="upload-area"
                onClick={() => fileInputRef.current?.click()}
                onDragOver={handleDragOver}
                onDrop={handleDrop}
              >
                <Upload size={44} className="upload-icon" />
                <p className="upload-text">Drag and drop your picture here</p>
                <p className="upload-subtext">Supports JPG, JPEG, and PNG format files</p>
                <input 
                  type="file" 
                  ref={fileInputRef} 
                  onChange={handleFileChange} 
                  accept="image/*"
                  style={{ display: 'none' }}
                />
              </div>
            )}

            {/* Camera Tab (Active stream) */}
            {activeTab === 'camera' && cameraStream && !previewUrl && (
              <div className="camera-area">
                <video 
                  ref={videoRef} 
                  autoPlay 
                  playsInline 
                  muted 
                  className="camera-preview"
                  style={{ transform: 'scaleX(-1)' }} 
                />
                <div className="camera-controls">
                  <button className="btn" onClick={capturePhoto}>
                    <Camera size={18} /> Capture Photo
                  </button>
                </div>
              </div>
            )}

            {/* Camera Permission Error */}
            {activeTab === 'camera' && cameraError && !previewUrl && (
              <div className="camera-area" style={{ backgroundColor: '#1a191b' }}>
                <div className="camera-placeholder">
                  <Camera size={40} style={{ color: '#ef4444' }} />
                  <p style={{ color: '#fff', fontSize: '14px' }}>{cameraError}</p>
                  <button className="btn btn-secondary" onClick={startCamera} style={{ color: 'white', backgroundColor: 'var(--primary)', border: 'none' }}>
                    Retry Camera
                  </button>
                </div>
              </div>
            )}

            {/* Captured / Uploaded Image Preview */}
            {previewUrl && (
              <div>
                <div className="preview-container">
                  <img src={previewUrl} className="preview-img" alt="Selfie preview" />
                  <button className="btn-overlay-close" onClick={resetAnalyzer} title="Reset picture">
                    ✕
                  </button>
                </div>

                {!result && (
                  <button className="btn" onClick={analyzeUndertone} disabled={loading}>
                    {loading ? (
                      <>
                        <RefreshCw size={18} className="animate-spin" /> Analyzing Skin Tone...
                      </>
                    ) : (
                      <>
                        <Sparkles size={18} /> Run AI Analysis
                      </>
                    )}
                  </button>
                )}

                {result && (
                  <button className="btn btn-secondary" onClick={resetAnalyzer}>
                    <RefreshCw size={16} /> Scan Another Photo
                  </button>
                )}
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div style={{ color: '#f84258', marginTop: '16px', fontSize: '13px', fontWeight: '600', textAlign: 'center' }}>
                ⚠️ {error}
              </div>
            )}
          </div>

          {/* Card 2: Predictions and Color Palette */}
          <div className="card results-card">
            {!result ? (
              <div className="results-placeholder">
                <div className="spinner" style={{ animation: 'none', borderColor: 'var(--border)', borderLeftColor: 'var(--border)' }}>
                  <Sparkles size={24} style={{ color: 'var(--text-muted)', margin: '10px' }} />
                </div>
                <h3 className="results-placeholder-title">Awaiting Analysis</h3>
                <p style={{ fontSize: '13px', maxWidth: '300px', margin: '0 auto' }}>
                  Upload a photo or take a selfie to see your predicted skin undertone and fashion suggestions.
                </p>
              </div>
            ) : (
              <div>
                {/* Result undertone header */}
                <div className="results-header">
                  <span className="results-badge">Detected Profile</span>
                  <h2 className="undertone-name">{result.undertone} undertone</h2>
                  
                  <div className="confidence-bar-container">
                    <div className="confidence-label">
                      <span>Confidence</span>
                      <span>{(result.confidence * 100).toFixed(1)}%</span>
                    </div>
                    <div className="confidence-bar">
                      <div 
                        className="confidence-fill" 
                        style={{ width: `${result.confidence * 100}%` }}
                      />
                    </div>
                  </div>
                </div>

                {/* Color Swatches Palette */}
                <div className="palette-section">
                  <h3 className="section-title">Your Curated Color Swatches</h3>
                  <div className="color-grid">
                    {Object.entries(result.palette).map(([colorName, hexVal]) => (
                      <div 
                        className="color-swatch-container" 
                        key={colorName}
                        onClick={() => copyColorToClipboard(hexVal, colorName)}
                        title={`Click to copy: ${colorName} (${hexVal})`}
                      >
                        <div 
                          className="color-swatch" 
                          style={{ backgroundColor: hexVal }}
                        />
                        <span className="color-name">{colorName}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Recommendations Tabs */}
                <div className="recommendations-section">
                  <h3 className="section-title">Fashion & Styling advice</h3>
                  
                  <div className="rec-tabs">
                    <button 
                      className={`rec-tab ${recTab === 'clothing' ? 'active' : ''}`}
                      onClick={() => setRecTab('clothing')}
                    >
                      <Shirt size={13} style={{verticalAlign: 'text-bottom', marginRight: '4px'}} /> Clothing
                    </button>
                    <button 
                      className={`rec-tab ${recTab === 'makeup' ? 'active' : ''}`}
                      onClick={() => setRecTab('makeup')}
                    >
                      <Heart size={13} style={{verticalAlign: 'text-bottom', marginRight: '4px'}} /> Makeup
                    </button>
                    <button 
                      className={`rec-tab ${recTab === 'jewelry' ? 'active' : ''}`}
                      onClick={() => setRecTab('jewelry')}
                    >
                      <Sparkles size={13} style={{verticalAlign: 'text-bottom', marginRight: '4px'}} /> Jewelry
                    </button>
                  </div>

                  <div className="rec-content">
                    {result.recommendations[recTab] && result.recommendations[recTab].map((item, index) => (
                      <div className="rec-item" key={index}>
                        <h4 className="rec-item-title">{item.title}</h4>
                        <p className="rec-item-desc">{item.desc}</p>
                      </div>
                    ))}
                  </div>
                </div>

              </div>
            )}
          </div>
        </section>
      </main>

      {/* Copy color code clipboard notification toast */}
      {copiedColor && (
        <div className="alert-toast">
          <Check size={16} style={{ color: '#10b981' }} />
          <span>Copied {copiedColor.name} ({copiedColor.hex})!</span>
        </div>
      )}

      {/* Elegant Footer */}
      <footer>
        <div className="footer-logo">Aura</div>
        <p className="footer-text">Skin Undertone & Color Palette Analyzer • Designed for Fashion and Care</p>
        <div className="footer-links">
          <a href="#" onClick={(e) => {e.preventDefault(); alert("Aura Undertone classification uses a pre-trained MobileNetV2 network. Accuracy is ~87%.");}}>Model Details</a>
          <a href="#" onClick={(e) => {e.preventDefault(); alert("Take/upload a photo in soft, natural lighting without makeup to get the most accurate undertone prediction.");}}>Styling Help</a>
        </div>
        <div className="copyright">© 2026 Aura Fashion Inc. All rights reserved.</div>
      </footer>
    </>
  );
}

export default App;
