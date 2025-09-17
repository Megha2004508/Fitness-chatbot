# Fitness Chatbot LLM 🏋️‍♀️🤖

An AI-powered **fitness chatbot** that helps users generate personalized workout plans, answer exercise-related questions, and recommend routines.
It leverages **LLMs** (Cohere API) and a **custom dataset** of gym exercises to provide smart and interactive fitness guidance.

---

## 🚀 Features

* Interactive fitness chatbot for exercise queries.
* Personalized workout suggestions.
* Integration with `megaGymDataset.csv` containing exercise details.
* Simple web-based interface (Streamlit).
* Easy to extend with new datasets or APIs.

---

## 📂 Project Structure

```
fitness_chatbot_LLM/
│── app.py                # Main application script
│── requirements.txt      # Project dependencies
│── megaGymDataset.csv    # Dataset of gym exercises
│── .env                  # Environment variables (API keys)
│── Documentation.docx    # Additional documentation
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/fitness_chatbot_LLM.git
   cd fitness_chatbot_LLM
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Mac/Linux
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   * Create a `.env` file in the project root.
   * Add your API key (for Cohere or other services):

     ```
     COHERE_API_KEY=your_api_key_here
     ```

5. **Run the app**

   ```bash
   streamlit run app.py
   ```

---

## 📊 Dataset

The project uses **megaGymDataset.csv**, which contains structured exercise data (e.g., names, categories, equipment, muscle groups).
This dataset helps the chatbot recommend **personalized workouts**.

---

## 🤝 Contribution

Contributions are welcome!

* Fork the repo
* Create a new branch (`feature-new`)
* Commit changes
* Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** – feel free to use and modify it.

---

## 👨‍💻 Author

Developed by **\[Your Name]** ✨

If you like this project, ⭐ star the repo and share it!

