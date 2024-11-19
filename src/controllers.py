from flask import render_template, request

def index():
    result = None
    if request.method == "POST":
        try:
            num1 = float(request.form.get("num1", 0))
            num2 = float(request.form.get("num2", 0))
            result = num1 + num2
        except ValueError:
            result = "Invalid input. Please enter numbers only."
    return render_template("index.html", result=result)
