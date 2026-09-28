from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ================= ATM DATA =================
balance = 50000
correct_pin = "1234"

# Mini Statement साठी transactions
transactions_list = []


# ================= HOME / INSERT CARD =================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/insert-card", methods=["POST"])
def insert_card():
    return render_template("pin.html")


# ================= VERIFY PIN =================
@app.route("/verify-pin", methods=["POST"])
def verify_pin():

    pin = request.form.get("pin")

    if pin == correct_pin:
        return redirect(url_for("menu"))

    return render_template(
        "pin.html",
        error="❌ Incorrect PIN. Please try again."
    )


# ================= MAIN MENU =================
@app.route("/menu")
def menu():
    return render_template(
        "mainmenu.html",
        balance=balance
    )


# ================= BALANCE =================
@app.route("/balance")
def show_balance():
    return render_template(
        "balance.html",
        balance=balance
    )


# ================= WITHDRAW =================
@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():

    global balance

    message = ""

    if request.method == "POST":

        try:
            amount = float(request.form["amount"])

            if amount <= 0:
                message = "❌ Enter valid amount."

            elif amount > balance:
                message = "❌ Insufficient Balance."

            else:
                balance -= amount

                transactions_list.append({
                    "type": "Withdraw",
                    "amount": amount,
                    "balance": balance
                })

                message = f"✅ ₹{amount:.2f} Withdraw Successful."

        except ValueError:
            message = "❌ Please enter a valid number."

    return render_template(
        "withdraw.html",
        message=message,
        balance=balance
    )


# ================= DEPOSIT =================
@app.route("/deposit", methods=["GET", "POST"])
def deposit():

    global balance

    message = ""

    if request.method == "POST":

        try:
            amount = float(request.form["amount"])

            if amount <= 0:
                message = "❌ Enter valid amount."

            else:
                balance += amount

                transactions_list.append({
                    "type": "Deposit",
                    "amount": amount,
                    "balance": balance
                })

                message = f"✅ ₹{amount:.2f} Deposit Successful."

        except ValueError:
            message = "❌ Please enter a valid number."

    return render_template(
        "deposit.html",
        message=message,
        balance=balance
    )


# ================= MINI STATEMENT =================
@app.route("/transactions")
def transactions():

    return render_template(
        "transactions.html",
        transactions=transactions_list,
        balance=balance
    )


# ================= CHANGE PIN =================
@app.route("/changepin", methods=["GET", "POST"])
def changepin():

    global correct_pin

    message = ""
    success = False

    if request.method == "POST":

        old_pin = request.form["old_pin"]
        new_pin = request.form["new_pin"]
        confirm_pin = request.form["confirm_pin"]

        if old_pin != correct_pin:

            message = "❌ Old PIN is incorrect."

        elif len(new_pin) != 4 or not new_pin.isdigit():

            message = "❌ New PIN must be exactly 4 digits."

        elif new_pin != confirm_pin:

            message = "❌ New PIN and Confirm PIN do not match."

        else:

            correct_pin = new_pin

            message = "✅ PIN changed successfully!"
            success = True

    return render_template(
        "changepin.html",
        message=message,
        success=success
    )


# ================= EXIT =================
@app.route("/exit")
def exit_atm():

    return """
    <html>

    <head>
        <title>ATM Exit</title>
    </head>

    <body style="text-align:center; padding-top:100px;">

        <h1>🏧 Thank You!</h1>

        <h2>💳 Please Collect Your Card</h2>

        <p>Thank you for using our ATM.</p>

        <br>

        <a href="/">
            <button>🔄 Start Again</button>
        </a>

    </body>

    </html>
    """


# ================= RUN SERVER =================
if __name__ == "__main__":
    app.run(debug=True, port=4478)