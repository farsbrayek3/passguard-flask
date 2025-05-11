# PassGuard – Modern Flask Password Manager

<img src="https://cdn-icons-png.flaticon.com/512/3064/3064197.png" alt="PassGuard Logo" height="48" />

A beautifully designed, modern, and secure password manager built with Flask, SQLAlchemy, Flask-Login, and Tailwind CSS.  
Manage your secrets and credentials with confidence—your data is encrypted, and only you have access.

---

## 🚀 Features

- **Modern, Responsive UI** — Built with [Tailwind CSS](https://tailwindcss.com/) for a clean, mobile-friendly experience.
- **User Registration & Authentication** — Secure sign-up and login with hashed passwords.
- **Password Vault** — Store credentials (site, login, password, notes, links) for unlimited accounts.
- **Strong Encryption** — All passwords are encrypted in the database using [cryptography](https://cryptography.io/) Fernet symmetric encryption.
- **Reveal Password** — Click-to-show/hide password fields for extra privacy.
- **Flash Messages** — Friendly feedback for actions like login, logout, registration, and password saving.
- **Session Management** — Uses Flask-Login for secure user sessions.
- **Easy Deployment** — Runs anywhere Python does.

---

## 🖼️ Screenshots

![Landing Page](https://img001.prntscr.com/file/img001/jGgUsQl9QhOduTxVHXrhEA.png)
![Dashboard](https://img001.prntscr.com/file/img001/VyQK1FrYRgGKIgEm7TXagw.png)
![Add Password](https://img001.prntscr.com/file/img001/A3InThfAQe6-ZkboleuoTg.png)

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/farsbrayek3/passguard-flask.git
cd passguard-flask
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

**The app will be available at** [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔐 Security

- **Passwords are never stored in plaintext!**
- Each password is encrypted with a strong, randomly generated Fernet key (`secret.key`).
- User authentication uses securely hashed passwords.
- Built for demo and personal use. For production, use HTTPS and a more robust database.

---

## 📂 Project Structure

```
passguard-flask/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── instance/
│   └── users.db           # SQLite database (auto-created)
├── secret.key             # Fernet encryption key (auto-created)
└── templates/
    ├── base.html
    ├── index.html
    ├── register.html
    ├── login.html
    ├── dashboard.html
    └── add_password.html
```

---

## ✨ Customization

- **UI**: Easily adjust colors and layouts in `base.html` (Tailwind-powered).
- **Encryption**: The app uses [cryptography.fernet](https://cryptography.io/en/latest/fernet/) for symmetric encryption.
- **Database**: Uses SQLite for simplicity; swap for Postgres/MySQL for production.

---

## 📦 Dependencies

- Flask
- Flask-WTF
- Flask-Login
- Flask-SQLAlchemy
- cryptography
- tailwindcss (via CDN)

See `requirements.txt` for exact versions.

---

## 🙋 FAQ

**Q: Can I deploy this publicly?**  
A: Yes, but use HTTPS and consider deploying with a production WSGI server (e.g., Gunicorn), and store the Fernet key securely.

**Q: Is this suitable for team/shared use?**  
A: This is a single-user-per-account manager. For multi-user/collaboration, extend user permissions and roles.

**Q: How do I reset my database?**  
A: Stop the app, delete `instance/users.db`, then restart.

---

## 📄 License

MIT License.  
Feel free to use, modify, and contribute!

---

## 🤝 Contributing

Pull requests and issues are welcome!  
Please open an issue for suggestions or bugs.

---

## ⭐️ Show your support

If you like this project, please give it a ⭐️ on GitHub!

---

**Built with love and Flask.**
