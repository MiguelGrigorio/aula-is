from flask import Flask, render_template

app = Flask(__name__)

@app.route('/Boas-vindas')
def BoasVindas():
    return render_template('boasvindas.html')
    
app.run(host= '0.0.0.0', port=8000)
