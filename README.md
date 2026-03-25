# 🩻 Med AI - Intelligent Pulmonary Diagnostic System
> **AI-Powered X-Ray Analysis with Real-Time Hardware Feedback & Automated Telemedicine Workflow.**

---

## 🌎 English Version <a name="english"></a>

### 🎓 Academic Background & Intellectual Property
The core AI architecture, neural network weights (`.weights.h5`), and diagnostic methodology were originally developed as part of a patented research project at **[University Name]**. 
**My Contribution:** I designed and implemented the entire end-to-end software ecosystem, including the Desktop GUI, multi-threaded processing, automated medical reporting, and IoT hardware integration via Serial communication.

### 🛠️ Technical Key Features
* **Deep Learning Integration:** Utilizes Keras/TensorFlow CNNs to classify X-Ray images (Normal vs. Disease).
* **Asynchronous UX:** Multi-threaded architecture ensures a fluid UI with animated scanning (GIF) while the AI processes data in the background.
* **Telemedicine Module:** Automated SMTP integration to dispatch AI-generated PDF reports directly to patient emails.
* **Hardware Interface (IoT):** Real-time physical feedback via Arduino-controlled LED indicators (Serial COM auto-discovery).
* **Clinical Reporting:** Dynamic PDF generation using ReportLab, featuring institutional watermarks and branding.

### 🔧 Tech Stack
`Python` | `TensorFlow/Keras` | `Tkinter` | `Arduino/C++` | `ReportLab` | `SMTPlib`

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
