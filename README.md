# 🩻 Med AI - Intelligent Pulmonary Diagnostic System
> **AI-Powered X-Ray Analysis with Real-Time Hardware Feedback & Automated Telemedicine Workflow.**

---

## 🌎 <a name="english"></a>

### 🎓 Academic Background & Intellectual Property
The core AI architecture, neural network weights (`.weights.h5`), and diagnostic methodology were originally developed as part of a patented research project at **[University]**. 
**My Contribution:** I designed and implemented the entire end-to-end software ecosystem, including the Desktop GUI, multi-threaded processing, automated medical reporting, and IoT hardware integration via Serial communication.

### 🛠️ Technical Key Features
* **Deep Learning Integration:** Utilizes Keras/TensorFlow CNNs to classify X-Ray images (Normal vs. Disease).
* **Asynchronous UX:** Multi-threaded architecture ensures a fluid UI with animated scanning (GIF) while the AI processes data in the background.
* **Telemedicine Module:** Automated SMTP integration to dispatch AI-generated PDF reports directly to patient emails.
* **Hardware Interface (IoT):** Real-time physical feedback via Arduino-controlled LED indicators (Serial COM auto-discovery).
* **Clinical Reporting:** Dynamic PDF generation using ReportLab, featuring institutional watermarks and branding.

### 🔧 Tech Stack
`Python` | `TensorFlow/Keras` | `Tkinter` | `Arduino/C++` | `ReportLab` | `SMTPlib`

### How to Run
> To run this project locally, follow these steps:

1. **Clone the Repository / Clonar o Repositório:**
git clone https://github.com/Cyber-ViPs/Smart-Pulmonary-Diagnosis
cd Med_AI

2. **Create a Virtual Environment**
python -m venv .venv
source .venv/Scripts/activate  # Windows: .\.venv\Scripts\activate

3. **Install Dependencies**
pip install -r requirements.txt

4. **Project Structure**
Ensure your folders are organized as follows (The system will validate this on startup):

       models/my_trained_model.weights.h5

       data/training, data/test, data/production

       assets/ (Icons and GIFs)

5.📥 Download Model Weights: Due to GitHub's file size limitations, the pre-trained weights are hosted externally. Please download the my_trained_model.weights.h5 file from the link below and place it inside the models/ folder before running the application: https://drive.google.com/drive/folders/1Y7dCnpdKpDZJUnXr88myRxrK-O4Oa5FK?usp=drive_link




6. **Execute the Application**
python main.py

**Environment Setup**
**Email Integration Setup:**
To use the automated reporting feature, you must set up your Gmail "App Password". For security reasons, credentials are not hardcoded. Please set the following environment variables or update the start_send_email method with your own credentials:

    MED_AI_EMAIL: Your gmail address.

    MED_AI_PASSWORD: Your 16-digit Google App Password.


**Note on Model Accuracy:** 
The included my_trained_model.weights.h5 file is provided for demonstration purposes only, with a recorded accuracy of 86%. For production-grade precision, users are encouraged to use the provided AI.ipynb notebook to retrain the model on a larger dataset using local hardware or Google Colab.

Credits

    - (Cyber-ViPs)
    

---

## 🇧🇷 Versão em Português <a name="portugues"></a>

### 🚀 Visão Geral
Este sistema integra Inteligência Artificial avançada com uma interface desktop robusta para auxiliar no diagnóstico pulmonar. O projeto foca na experiência do usuário e na automação do fluxo de trabalho clínico.

### ✨ Funcionalidades Principais
* **Análise de IA:** Classificação automática de Raio-X.
* **Interface Fluida:** Uso de Threads para evitar travamentos durante o processamento da rede neural.
* **Envio de Laudos:** Sistema integrado para enviar o PDF gerado diretamente para o e-mail do cliente/médico.
* **Feedback Físico:** Conexão com Arduino para acender LEDs de alerta conforme o diagnóstico.

---
