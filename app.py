from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import os
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'bda41a8bf2c54f55a62db0177f12e859cfad2344a302fce73f40e4729ec4b47c'

file_name = "user_data.xlsx"
plans_file_name = "plans.xlsx"
vi_file_name = "VI_Plans.xlsx"

# Function to save data to Excel
def save_to_excel(data):
    if os.path.exists(file_name):
        existing_data = pd.read_excel(file_name)
        combined_data = pd.concat([existing_data, data], ignore_index=True)
    else:
        combined_data = pd.DataFrame(data)
    combined_data.to_excel(file_name, index=False)

# Function to load plans from Excel
def load_plans():
    if os.path.exists(plans_file_name):
        try:
            return pd.read_excel(plans_file_name)
        except Exception as e:
            print(f"Error reading the Excel file: {e}")
            return None
    return None

# Function to load VI_Plans data
def load_vi_plans():
    if os.path.exists(vi_file_name):
        try:
            return pd.read_excel(vi_file_name)
        except Exception as e:
            print(f"Error reading the VI_Plans Excel file: {e}")
            return None
    return None

# Directly route to the carrier page
@app.route('/')
def home():
    return redirect(url_for('carrier'))

# Route for fetching plans dynamically based on selected carrier
@app.route('/get_plans')
def get_plans():
    carrier = request.args.get('carrier')
    plans_data = load_plans()
    if plans_data is not None and carrier:
        filtered_data = plans_data[plans_data['Carrier'] == carrier]
        plan_validity_map = filtered_data[['Plan', 'Validity']].drop_duplicates().to_dict('records')
        return jsonify({'plan_validity_map': plan_validity_map})
    return jsonify({'plan_validity_map': []})

# Route for the carrier details page
@app.route('/carrier', methods=['GET', 'POST'])
def carrier():
    plans_data = load_plans()
    vi_plans_data = load_vi_plans()
    error_message = None

    if plans_data is None or vi_plans_data is None:
        error_message = "One or more required Excel files are missing or invalid."

    if request.method == 'POST' and plans_data is not None and vi_plans_data is not None:
        family_phones = request.form.getlist('family_phone[]')
        family_names = request.form.getlist('family_name[]')
        family_carriers = request.form.getlist('family_carrier[]')
        family_plans = list(map(int, request.form.getlist('family_plan[]')))
        family_validities = list(map(int, request.form.getlist('family_validity[]')))

        unique_id = str(uuid.uuid4())[:8]  # Generate a unique ID
        current_date = datetime.now().strftime('%d-%m-%Y')  # Get system date

        # Calculate family members' costs and prepare data to save
        family_data = []
        for i in range(len(family_phones)):
            amount = (family_plans[i] / family_validities[i]) * 30
            family_data.append({
                'phone': family_phones[i],
                'name': family_names[i],
                'carrier': family_carriers[i],
                'plan': family_plans[i],
                'validity': family_validities[i],
                'amount': amount,
            })

        # Save data to Excel
        data_to_save = [{
            'date': current_date,
            'unique_id': unique_id,
            'phone': member['phone'],  # Include phone number
            'name': member['name'],
            'carrier': member['carrier'],
            'plan': member['plan'],
            'validity': member['validity'],
            'amount': member['amount'],  # Optionally save calculated amount
        } for member in family_data]

        save_to_excel(pd.DataFrame(data_to_save))

        # Calculate the number of family members
        member_count = len(family_phones)

        # Function to find matching plans based on amount and member count
        def find_matching_plans(amount, member_count):
            return vi_plans_data[
              
                (vi_plans_data['Count'] == member_count)  # Match the number of members
            ]

        # Match plans based on amount and member count
        family_matches = [
            {
                "phone": member['phone'], 
                "matches": find_matching_plans(member['amount'], member_count).to_dict('records')
            }
            for member in family_data
        ]

        total_spent = sum(member['amount'] for member in family_data)

        # Pass data to result template
        return render_template(
            'result.html',
            family_data=family_data,
            total_spent=total_spent,
            family_matches=family_matches,
            member_count=member_count
        )

    return render_template(
        'carrier.html',
        plans_data=plans_data,
        error_message=error_message
    )

if __name__ == '__main__':
    app.run(debug=True)
