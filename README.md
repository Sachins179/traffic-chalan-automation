# 🚦 Traffic Chalan Automation System

An end-to-end **AI-powered traffic violation detection and e-chalan automation system** that analyzes traffic images, identifies violations, detects and reads vehicle number plates, retrieves vehicle-owner information, calculates applicable fines, generates PDF e-chalans, and provides a WhatsApp notification link.





\

---

## 📌 Overview

Manual traffic-violation processing can involve multiple steps, including identifying the violation, reading the vehicle number plate, retrieving vehicle information, calculating fines, preparing documentation, and notifying the vehicle owner.

The **Traffic Chalan Automation System** integrates these steps into a single automated pipeline.

### Workflow

1. 🖼️ Upload or provide a traffic image
2. 🤖 Detect one or more traffic violations using a Vision LLM
3. 💰 Retrieve applicable fines from PostgreSQL
4. 🚘 Detect the vehicle number plate using computer vision
5. 🔤 Read the number plate using Vision LLM-based OCR
6. 👤 Identify the vehicle owner using database lookup and fuzzy matching
7. 📄 Generate a professional PDF e-chalan
8. 📱 Generate a WhatsApp notification link for manual sending

The system supports **multiple violations in a single image**, such as *No Helmet + Triple Riding*.

---

## ✨ Key Features

* **Multi-Violation Detection**
  Detects multiple traffic violations from a single image.

* **AI-Powered Vision Analysis**
  Uses Groq Vision LLM for violation classification and number-plate OCR.

* **Three-Layer Number Plate Detection**
  Combines Canny edge detection, Haar Cascade classification, and full-image fallback.

* **OCR Error Tolerance**
  Uses fuzzy string matching to handle common OCR character errors such as `R ↔ K` and `0 ↔ O`.

* **Automated Fine Calculation**
  Retrieves violation-specific fines from PostgreSQL and calculates the total amount.

* **Vehicle Owner Lookup**
  Searches vehicle records and performs fuzzy matching when OCR results are imperfect.

* **PDF E-Chalan Generation**
  Automatically generates a structured, professional PDF document using ReportLab.

* **WhatsApp Notification**
  Creates a `wa.me` link containing the relevant notification information for manual sending.

* **Streamlit Web Interface**
  Provides a simple interface for uploading images and viewing analysis results.

* **CLI Support**
  Allows the complete pipeline to be executed directly from the terminal.

* **Structured Logging**
  Maintains console and file-based logs for debugging and traceability.

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────────┐
                    │    Traffic Image        │
                    └────────────┬────────────┘
                                 │
                                 ▼
              ┌────────────────────────────────────┐
              │       Groq Vision LLM              │
              │      Multi-Violation Detection     │
              └──────────────────┬─────────────────┘
                                 │
                                 ▼
                   ┌────────────────────────┐
                   │ Detected Violations    │
                   │ • No Helmet            │
                   │ • Triple Ride          │
                   └────────────┬───────────┘
                                │
                                ▼
              ┌────────────────────────────────────┐
              │       PostgreSQL: chalan_db        │
              │         Fine Lookup & Rules         │
              └──────────────────┬─────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ Fine Breakdown + Total │
                    └────────────┬───────────┘
                                 │
                 ┌───────────────┴────────────────┐
                 │                                │
                 ▼                                ▼
      ┌──────────────────────┐        ┌──────────────────────┐
      │ OpenCV Plate Detector│        │ Groq Vision LLM      │
      │ Canny + Haar Cascade │───────▶│ Number Plate OCR     │
      └──────────┬───────────┘        └──────────┬───────────┘
                 │                               │
                 └──────────────┬────────────────┘
                                ▼
                    ┌────────────────────────┐
                    │    Vehicle Number      │
                    └────────────┬───────────┘
                                 │
                                 ▼
              ┌────────────────────────────────────┐
              │       PostgreSQL: user_db          │
              │    Owner Lookup + Fuzzy Matching   │
              └──────────────────┬─────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ Owner Name + Mobile    │
                    └────────────┬───────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
          ┌───────────────────┐     ┌────────────────────┐
          │ PDF E-Chalan      │     │ WhatsApp Link      │
          │     ReportLab     │     │     wa.me          │
          └───────────────────┘     └────────────────────┘
```

---

## 🛠️ Technology Stack

| Component            | Technology               |
| -------------------- | ------------------------ |
| Programming Language | Python 3.10+             |
| Computer Vision      | OpenCV                   |
| Edge Detection       | Canny                    |
| Object Detection     | Haar Cascade             |
| AI / Vision LLM      | Groq API                 |
| LLM Model            | `qwen/qwen3.8-27b`       |
| Database             | PostgreSQL 15+           |
| PDF Generation       | ReportLab                |
| Web Interface        | Streamlit                |
| Notification         | WhatsApp `wa.me`         |
| Configuration        | YAML + `python-dotenv`   |
| Logging              | Python `logging`         |
| Fuzzy Matching       | Python `SequenceMatcher` |

---

## 📁 Project Structure

```text
traffic-chalan-automation/
│
├── app.py                         # Streamlit application
├── main.py                        # CLI entry point
├── config.yaml                    # Application configuration
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variable template
├── .gitignore                     # Git ignore rules
│
├── src/
│   ├── vision/
│   │   ├── plate_detector.py      # Number plate detection
│   │   └── image_utils.py         # Image processing utilities
│   │
│   ├── llm/
│   │   ├── client.py              # Groq API client
│   │   ├── violation_detector.py  # Traffic violation detection
│   │   └── plate_reader.py        # Number plate OCR
│   │
│   ├── database/
│   │   ├── connection.py          # PostgreSQL connection
│   │   ├── chalan_repo.py         # Chalan database operations
│   │   └── user_repo.py           # Vehicle/owner lookup
│   │
│   ├── chalan/
│   │   ├── fine_calculator.py     # Fine calculation
│   │   └── pdf_generator.py       # PDF e-chalan generation
│   │
│   ├── notification/
│   │   └── whatsapp_web.py        # WhatsApp notification link
│   │
│   ├── pipeline/
│   │   └── runner.py              # End-to-end pipeline
│   │
│   └── utils/
│       ├── config_loader.py       # Configuration loader
│       └── logger.py              # Logging configuration
│
├── models/
│   └── *.xml                      # Haar Cascade model files
│
├── data/
│   ├── input/                     # Input traffic images
│   ├── output/                    # Processing output
│   └── chalan_pdfs/               # Generated e-chalans
│
├── tests/                         # Unit tests
│
└── logs/                          # Application log files
```

---

# 🚀 Getting Started

## Prerequisites

Before running the project, make sure you have:

* Python **3.10 or higher**
* PostgreSQL **15 or higher**
* A Groq API key
* Git
* A Windows/Linux/macOS environment

---

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/traffic-chalan-automation.git
cd traffic-chalan-automation
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file from the provided example:

### Windows

```bash
copy .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

Update the `.env` file with your configuration:

```env
DB_HOST=localhost
DB_PORT=5432

CHALAN_DB_NAME=chalan_db
USER_DB_NAME=user_db

DB_USER=postgres
DB_PASSWORD=your_password

GROQ_API_KEY=your_groq_api_key
GROQ_VISION_MODEL=qwen/qwen3.8-27b
```

> ⚠️ **Security:** Never commit your `.env` file or API keys to GitHub.

You can obtain a Groq API key from the [Groq Console](https://console.groq.com/keys).

---

## 5. Set Up PostgreSQL

Create the required databases:

```bash
createdb chalan_db
createdb user_db
```

Alternatively, create them using **pgAdmin** or the PostgreSQL command-line interface.

Run the database schema scripts provided in:

```text
src/database/schema.sql
```

The two-database design separates:

* **`chalan_db`** — violation and fine-related information
* **`user_db`** — vehicle-owner information

---

# 🎮 Usage

## Streamlit Web Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Open the application in your browser:

```text
http://localhost:8501
```

Upload a traffic image and click **Analyze** to start the automated processing pipeline.

---

## Command-Line Interface

The system can also be executed directly from the terminal:

```bash
python main.py data/input/test3.jpg
```

The CLI processes the image and displays the detected violations, fine details, vehicle information, generated PDF path, and WhatsApp notification link.

---

# 📊 Example Output

```text
============================================================
RESULT
============================================================

Violations  : No Helmet, Triple Ride

Fine breakdown:
  • No Helmet   : Rs. 200
  • Triple Ride : Rs. 1000
  -------------------------
  TOTAL         : Rs. 1200

Plate       : MH01AB1234
Owner       : Deepak Yadav
Mobile      : 7684051736

PDF         : data/chalan_pdfs/chalan_MH01AB1234_xxx.pdf
WhatsApp    : https://wa.me/...

============================================================
```

---

# 🔍 Number Plate Detection Pipeline

The system uses a **three-layer fallback strategy** to improve number-plate detection reliability.

### Layer 1 — Canny Edge Detection

The system first identifies potential plate regions using:

* Grayscale conversion
* Canny edge detection
* Contour analysis
* Aspect-ratio filtering

### Layer 2 — Haar Cascade

If the primary detection method does not produce a suitable plate region, the system uses a Haar Cascade classifier as a fallback.

### Layer 3 — Vision LLM OCR

If traditional computer-vision methods fail or produce an unreadable crop, the full image is sent to the Vision LLM for number-plate recognition.

```text
Traffic Image
     │
     ▼
Canny + Contour Detection
     │
     ├── Plate Found ──────► OCR
     │
     └── Plate Not Found
              │
              ▼
       Haar Cascade
              │
              ├── Plate Found ──────► OCR
              │
              └── Plate Not Found
                       │
                       ▼
                Full Image → LLM OCR
```

If the LLM returns `UNREADABLE`, the system automatically retries using the full image.

---

# 🧠 Design Decisions

## 1. Separate PostgreSQL Databases

The project uses two databases:

```text
chalan_db
    └── Violations + Fine Information

user_db
    └── Vehicle + Owner Information
```

This separation provides a logical boundary between violation-related information and personally identifiable information.

---

## 2. Vision LLM for Violation Detection and OCR

Instead of maintaining separate models for violation classification and OCR, the system uses a Vision LLM for both tasks.

This simplifies the architecture while allowing the system to process different traffic-image scenarios.

---

## 3. Fuzzy Number-Plate Matching

OCR can produce character-level errors.

For example:

```text
Actual : MH01AB1234
OCR    : MH01AB12B4
```

The system uses fuzzy string matching with an **80% similarity threshold** to improve vehicle-record matching despite minor OCR errors.

---

## 4. WhatsApp `wa.me` Notification

Instead of integrating a third-party WhatsApp messaging API, the system generates a WhatsApp URL that allows the notification to be sent manually.

This keeps the notification workflow simple and avoids requiring automated messaging infrastructure.

---

## 5. Structured Logging

The application uses Python's `logging` framework to maintain application logs.

Logs can help with:

* Debugging
* Monitoring pipeline execution
* Identifying API/database failures
* Tracking processing steps
* Troubleshooting OCR and detection issues

---

# 🔄 End-to-End Processing Flow

```text
Image Upload
     │
     ▼
Violation Detection
     │
     ▼
Multiple Violations
     │
     ▼
Fine Lookup
     │
     ▼
Fine Calculation
     │
     ▼
Number Plate Detection
     │
     ▼
Number Plate OCR
     │
     ▼
Vehicle Database Lookup
     │
     ▼
Fuzzy Matching
     │
     ▼
Owner Information
     │
     ├───────────────┐
     ▼               ▼
PDF E-Chalan    WhatsApp Link
```

---

# 🧪 Testing

Unit tests are maintained inside the:

```text
tests/
```

directory.

Run the test suite using:

```bash
pytest
```

For more detailed output:

```bash
pytest -v
```

---

# 🔐 Security Considerations

The project handles sensitive information such as vehicle-owner details and API credentials.

Recommended practices:

* Never commit `.env` files.
* Never expose API keys in source code.
* Use `.env.example` for configuration templates.
* Restrict database credentials to the required permissions.
* Avoid exposing personally identifiable information in logs.
* Do not upload real-world vehicle-owner data to public repositories.
* Use synthetic or anonymized data for demonstrations and testing.

---

# ⚠️ Important Notes

This project is intended primarily for **educational, research, and portfolio purposes**.

The accuracy of AI-based traffic-violation detection and number-plate recognition can vary depending on:

* Image quality
* Lighting conditions
* Camera angle
* Plate visibility
* Occlusion
* Traffic density
* LLM/OCR performance

For real-world deployment, AI-generated results should be validated against applicable traffic laws, official vehicle databases, and authorized enforcement procedures.

---

# 🚧 Future Enhancements

Potential future improvements include:

* [ ] Real-time CCTV/video stream processing
* [ ] Automatic violation evidence cropping
* [ ] Additional traffic violation categories
* [ ] Advanced ANPR models
* [ ] Real-time dashboard and analytics
* [ ] Authentication and role-based access control
* [ ] Cloud deployment
* [ ] REST API integration
* [ ] Automated notification service
* [ ] Database administration dashboard
* [ ] Improved OCR using specialized ANPR models
* [ ] Docker containerization
* [ ] Automated CI/CD pipeline

---

# 📸 Demo

---

## 🎬 Demo

### Streamlit UI

![Streamlit Demo](docs/demo_streamlit.png)

Upload an image, click **Analyze**, and get the full chalan preview —
including detected violations, total fine, owner details, PDF download,
and WhatsApp link.

### CLI Output

![CLI Demo](docs/demo_cli.png)


### Generated PDF Chalan

![PDF Demo](docs/demo_pdf.png)

Each e-chalan is a professionally formatted PDF with a breakdown of
all detected violations and the total fine.
### Generated PDF Chalan

![PDF Demo](docs/demo_pdf.png)

Each e-chalan is a professionally formatted PDF with a breakdown of
all detected violations and the total fine.


Recommended screenshots:

```text
docs/
├── dashboard.png
├── violation-detection.png
├── plate-detection.png
├── fine-calculation.png
└── generated-chalan.png
```

Example:

```markdown
![Traffic Chalan Dashboard](docs/dashboard.png)
```

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

### Steps

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/your-feature
```

3. Commit your changes

```bash
git commit -m "Add your feature"
```

4. Push the branch

```bash
git push origin feature/your-feature
```

5. Open a Pull Request


---

# 👨‍💻 Author

## Sachin Sakti Ranjan

**MCA Graduate | Aspiring Software Engineer | Python & Java Developer | Full-Stack & AI Enthusiast**

* **GitHub:** [Sachins179](https://github.com/Sachins179)
* **LinkedIn:** [Sachin Sakti Ranjan on LinkedIn](www.linkedin.com/in/sachin-sakti-ranjan-78a8bb268)

---

## ⭐ Support

If you find this project useful for learning or research, consider giving the repository a ⭐ on GitHub.
