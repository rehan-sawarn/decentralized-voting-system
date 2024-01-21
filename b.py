from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from web3 import Web3
from web3.middleware import geth_poa_middleware
import contract
import matplotlib.pyplot as plt
from io import BytesIO
import base64
app = Flask(__name__)
app.secret_key = 'secret_key'  

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
try:
    w3.eth.getBlock('latest')  # Test connection to Ethereum node
except:
    print("Error connecting to Ethereum node. Make sure your node is running.")
contract = w3.eth.contract(address=contract.contract_address, abi=contract.contract_abi)
account_address = '0x343b3c9f9eaB34e122040848a93e7AC5C3ec0A52'  #  Ethereum account address
private_key = '0xc61abb8cd22120b634f5550584aa3d620d5f4ea36477f22197b7d432abe5baa9'  # private key
nonce = w3.eth.get_transaction_count(account_address)

_ballotName = "Example Ballot"
_ballotImage = "ballot_image_url.jpg"
_startTime = 1644072000   
_endTime = 1644158400    
_entryRestriction = True 
_candidateName = "John Doe"
_partyLogo = "party_logo_url.jpg"
partyName = "Example Party"

transaction = contract.functions.createBallot(
    _ballotName, _ballotImage, _startTime, _endTime, _entryRestriction, _candidateName, _partyLogo
).build_transaction({
    'from': account_address,
    'gas': 0.000001,
    'gasPrice': 0.000002, # web3.utils.toWei('1.1', 'gwei')),
    'nonce': nonce
})

signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

# Call the addParty function
add_party_transaction = contract.functions.addParty(_ballotName, partyName, _candidateName).build_transaction({
    'from': account_address,
    'gas': 30000000,
    'gasPrice': w3.to_wei('50', 'gwei'),
    'nonce': nonce + 1  # Increment nonce for each new transaction
})

# Sign and send the transaction
signed_add_party_transaction = w3.eth.account.sign_transaction(add_party_transaction, private_key)
add_party_transaction_hash = w3.eth.send_raw_transaction(signed_add_party_transaction.rawTransaction)

# Assuming partyIndex is an integer, you need to convert it to uint256
partyIndex = 1  # Replace with the actual party index you want to vote for

vote_transaction = contract.functions.voteForParty(_ballotName, partyIndex).build_transaction({
    'from': account_address,
    'gas': 2000000,
    'gasPrice': w3.to_wei('50', 'gwei'),
    'nonce': nonce + 2  # Increment nonce for each new transaction
})



# Sign and send the transaction
signed_vote_transaction = w3.eth.account.sign_transaction(vote_transaction, private_key)
vote_transaction_hash = w3.eth.send_raw_transaction(signed_vote_transaction.rawTransaction)

print(f'Vote Transaction Hash: {vote_transaction_hash.hex()}')

print(f'Add Party Transaction Hash: {add_party_transaction_hash.hex()}')

print(f'Transaction Hash: {transaction_hash.hex()}')

# Create SQLite database and table
conn = sqlite3.connect('voting_system.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

# Database helper functions
def get_user_by_email(email):
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(email, full_name, password):
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (email, full_name, password) VALUES (?, ?, ?)', (email, full_name, password))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('loginEmail')
        password = request.form.get('loginPassword')

        user = get_user_by_email(email)

        if user and check_password_hash(user[3], password):
            session['user_email'] = email
            return redirect(url_for('dashboard'))  # Redirect to the parties page (dashboard)
        else:
            return jsonify({'status': 'error', 'message': 'Invalid email or password'})

    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('registerFullName')
        email = request.form.get('registerEmail')
        password = request.form.get('registerPassword')
        confirm_password = request.form.get('confirmRegisterPassword')

        if get_user_by_email(email):    
            return jsonify({'status': 'error', 'message': 'Email already registered'})

        if password != confirm_password:
            return jsonify({'status': 'error', 'message': 'Passwords do not match'})

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        create_user(email, full_name, hashed_password)
        return jsonify({'status': 'success', 'message': 'Registration successful'})
    else:
        return render_template('register.html')

# Add a route to serve the CSS file
@app.route('/static/styles.css')
def serve_css():
    return app.send_static_file('styles.css')

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('index'))

# ... (your existing code)

@app.route('/dashboard')
def dashboard():
    # Replace "your_ballot_name" with the actual ballot name you want to retrieve parties for
    ballot_name = "your_ballot_name"
    parties = contract.functions.getAllParties(ballot_name).call()


    return render_template('dashboard.html', parties=parties)

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        # Retrieve the selected ballot and party indices from the form
        selected_ballot_index = int(request.form.get('ballotIndex'))
        selected_party_index = int(request.form.get('partyIndex'))

        # Call the voteForParty function in the smart contract
        vote_transaction = contract.functions.voteForParty(selected_ballot_index, selected_party_index).build_transaction({
            'from': account_address,
            'gas': 2000000,
            'gasPrice': w3.to_wei('50', 'gwei'),
            'nonce': nonce + 2  # Increment nonce for each new transaction
        })

        # Sign and send the transaction
        signed_vote_transaction = w3.eth.account.sign_transaction(vote_transaction, private_key)
        vote_transaction_hash = w3.eth.send_raw_transaction(signed_vote_transaction.rawTransaction)

        print(f'Vote Transaction Hash: {vote_transaction_hash.hex()}')

        # Redirect to the results page
        return redirect(url_for('results'))

    # Retrieve the list of ballots and parties to display in the form
    ballots = contract.functions.getAllBallots().call()
    parties = contract.functions.getAllParties().call()

    return render_template('vote.html', ballots=ballots, parties=parties)


@app.route('/results')
def results():
    # Retrieve the results from the smart contract
    results = contract.functions.getResults().call()

    # Process the results for generating a pie chart
    labels = [party['name'] for party in results]
    votes = [party['votes'] for party in results]

    # Generate a pie chart
    fig, ax = plt.subplots()
    ax.pie(votes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular

    # Save the plot to a BytesIO object
    img_stream = BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)

    # Convert the plot to base64 for embedding in HTML
    img_base64 = base64.b64encode(img_stream.read()).decode('utf-8')

    plt.close()  # Close the plot to free up resources

    return render_template('results.html', img_base64=img_base64)


if __name__ == '__main__':
    app.run(debug=True)
