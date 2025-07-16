from flask import Flask, request, render_template, send_file
import pandas as pd
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/foreclosure')
def foreclosure():
    return render_template('foreclosure.html')

@app.route('/generate', methods=['POST'])
def generate_excel():
    P = float(request.form['principal'])
    annual_rate = float(request.form['rate'])
    n = int(request.form['months'])
    r = annual_rate / 12

    EMI = P * r * (1 + r)**n / ((1 + r)**n - 1)

    schedule = []
    remaining_principal = P

    for month in range(1, n + 1):
        interest = remaining_principal * r
        principal = EMI - interest
        remaining_principal -= principal
        if remaining_principal < 0:
            remaining_principal = 0
        
        schedule.append({
            "Month": month,
            "EMI": round(EMI, 2),
            "Interest Paid": round(interest, 2),
            "Principal Paid": round(principal, 2),
            "Remaining Balance": round(remaining_principal, 2)
        })

    df = pd.DataFrame(schedule)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Schedule')
    output.seek(0)

    return send_file(
        output,
        download_name="loan_amortization_schedule.xlsx",
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@app.route('/calculate_foreclosure', methods=['POST'])
def calculate_foreclosure():
    P = float(request.form['principal'])
    annual_rate = float(request.form['rate'])
    n = int(request.form['months'])
    foreclosure_month = int(request.form['foreclose_month'])
    r = annual_rate / 12

    EMI = P * r * (1 + r)**n / ((1 + r)**n - 1)

    remaining_principal = P
    for month in range(1, foreclosure_month + 1):
        interest = remaining_principal * r
        principal_paid = EMI - interest
        remaining_principal -= principal_paid
        if remaining_principal < 0:
            remaining_principal = 0
            break

    remaining_balance = round(remaining_principal, 2)
    foreclosure_charge = round(0.04 * remaining_balance, 2)
    gst = round(0.18 * foreclosure_charge, 2)
    total_foreclosure_amount = round(remaining_balance + foreclosure_charge + gst, 2)

    return render_template('foreclosure.html', results={
        'month': foreclosure_month,
        'remaining_balance': remaining_balance,
        'charge': foreclosure_charge,
        'gst': gst,
        'total': total_foreclosure_amount
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
