import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave-local-temporaria")

@app.route("/", methods=["GET", "POST"])
def login():
    erro = None

    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        login_correto = os.environ.get("LOGIN_USER", "aluno")
        senha_hash = os.environ.get("LOGIN_PASSWORD_HASH")

        if usuario == login_correto and senha_hash and check_password_hash(senha_hash, senha):
            session["usuario"] = usuario
            return redirect(url_for("boas_vindas"))
        else:
            erro = "Usuário ou senha incorretos."

    return render_template("login.html", erro=erro)

@app.route("/boas-vindas")
def boas_vindas():
    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template("boas_vindas.html", usuario=session["usuario"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
