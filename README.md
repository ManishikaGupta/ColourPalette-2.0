# ColourPalette-2.0

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?logo=tensorflow)](https://www.tensorflow.org/)
[![Keras](https://img.shields.io/badge/Keras-API-red?logo=keras)](https://keras.io/)
[![MobileNetV2](https://img.shields.io/badge/MobileNetV2-TransferLearning-green)](#)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b?logo=streamlit)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ModelEval-blueviolet?logo=scikitlearn)](https://scikit-learn.org/)
[![NumPy](https://img.shields.io/badge/NumPy-Array%20Ops-purple?logo=numpy)](https://numpy.org/)
[![Pillow](https://img.shields.io/badge/Pillow-Image%20Handling-yellowgreen)](https://python-pillow.org/)

### DEMO VIDEO

https://github.com/user-attachments/assets/96866718-6f47-4473-a6c2-cf364ce385fc

### Deployed Link:

https://huggingface.co/spaces/manishika/skin-undertone

## 🎯 Project Overview
This project implements a computer vision solution for skin undertone classification using advanced deep learning techniques. By leveraging transfer learning with MobileNetV2, we achieve high accuracy while maintaining computational efficiency.

### Key Features
Transfer Learning: Utilizes pre-trained MobileNetV2 for feature extraction
Data Augmentation: Comprehensive augmentation pipeline to prevent overfitting
Two-Stage Training: Initial training with frozen base model, followed by fine-tuning
Balanced Classification: Handles four distinct undertone classes effectively

## 🏗️ Model Architecture & Performance
Base Model: MobileNetV2 (pre-trained on ImageNet)

Fine-Tuning: Custom classification head; final layers unfrozen with a low learning rate

Evaluation Dataset: 1,489 images

Accuracy: 87%
