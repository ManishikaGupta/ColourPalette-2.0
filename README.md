# ColourPalette-2.0
Deployed Link:
https://huggingface.co/spaces/manishika/skin-undertone

APP INTERFACE:
<img width="1440" height="900" alt="Screenshot 2025-07-10 at 10 14 34 PM" src="https://github.com/user-attachments/assets/5317c904-33ef-4615-8fb5-18c27f66d9aa" />

COOL UNDERTONE:
<img width="1440" height="900" alt="Screenshot 2025-07-10 at 10 15 15 PM" src="https://github.com/user-attachments/assets/37377e15-9dc8-4108-9e1d-c7cda5e0e7ff" />

OLIVE UNDERTONE:
<img width="1440" height="900" alt="Screenshot 2025-07-10 at 10 16 17 PM" src="https://github.com/user-attachments/assets/eefb4f03-8ee9-410e-85b8-75a0bd3c9a0f" />

🎯 Project Overview
This project implements a computer vision solution for skin undertone classification using advanced deep learning techniques. By leveraging transfer learning with MobileNetV2, we achieve high accuracy while maintaining computational efficiency.
Key Features
Transfer Learning: Utilizes pre-trained MobileNetV2 for feature extraction
Data Augmentation: Comprehensive augmentation pipeline to prevent overfitting
Two-Stage Training: Initial training with frozen base model, followed by fine-tuning
Balanced Classification: Handles four distinct undertone classes effectively

🏗️ Architecture
Model Structure
MobileNetV2 (Pre-trained, ImageNet weights)
    ↓
GlobalAveragePooling2D
    ↓
Dropout(0.5)
    ↓
Dense(128, activation='relu')
    ↓
Dense(4, activation='softmax')
