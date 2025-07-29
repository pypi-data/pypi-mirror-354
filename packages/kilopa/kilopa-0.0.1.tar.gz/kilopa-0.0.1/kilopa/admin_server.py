# kilopa/admin_server.py
from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import json
import os
import time
import hashlib
import webbrowser
import threading

app = Flask(__name__)
CORS(app)

payments = []
payments_file = "kilopa_payments.json"

def load_payments():
    global payments
    try:
        if os.path.exists(payments_file):
            with open(payments_file, 'r', encoding='utf-8') as f:
                payments = json.load(f)
    except:
        payments = []

def save_payments():
    try:
        with open(payments_file, 'w', encoding='utf-8') as f:
            json.dump(payments, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения: {e}")

def find_payment(user_id, product_id):
    for payment in payments:
        if payment['userId'] == user_id and payment['productId'] == product_id:
            return payment
    return None

@app.route('/')
def admin_panel():
    return render_template_string(ADMIN_TEMPLATE)

@app.route('/pay')
def payment_page():
    user_id = request.args.get('userId', '')
    product = request.args.get('product', '')
    return render_template_string(PAYMENT_TEMPLATE, user_id=user_id, product=product)

@app.route('/api/payments')
def get_payments():
    load_payments()
    return jsonify(payments)

@app.route('/api/add-payment', methods=['POST'])
def add_payment():
    try:
        data = request.json
        existing = find_payment(data['userId'], data['productId'])
        if existing:
            return jsonify({'success': True, 'paymentId': existing['id']})
        
        payment = {
            'id': f"PAY_{int(time.time())}_{data['userId'][-4:]}",
            'userId': data['userId'],
            'productId': data['productId'],
            'amount': data.get('amount', 1500),
            'email': data.get('email', ''),
            'timestamp': time.time(),
            'confirmed': False,
            'blocked': False
        }
        
        payments.append(payment)
        save_payments()
        return jsonify({'success': True, 'paymentId': payment['id']})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/check-payment', methods=['POST'])
def check_payment():
    try:
        data = request.json
        load_payments()
        payment = find_payment(data.get('userId'), data.get('productId'))
        
        if not payment:
            return jsonify({'status': 'pending', 'message': 'Платеж не найден'})
        
        if payment.get('blocked'):
            return jsonify({'status': 'blocked', 'message': 'Заблокирован'})
        
        if payment.get('confirmed'):
            license_key = hashlib.sha256(f"{payment['userId']}-{time.time()}".encode()).hexdigest()[:32].upper()
            return jsonify({'status': 'paid', 'licenseKey': license_key, 'message': 'Подтвержден'})
        
        return jsonify({'status': 'pending', 'message': 'Ожидает подтверждения'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/confirm-payment', methods=['POST'])
def confirm_payment():
    try:
        payment_id = request.json.get('paymentId')
        load_payments()
        
        for payment in payments:
            if payment['id'] == payment_id:
                payment['confirmed'] = True
                payment['confirmedAt'] = time.time()
                save_payments()
                return jsonify({'success': True})
        
        return jsonify({'success': False, 'error': 'Платеж не найден'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/block-user', methods=['POST'])
def block_user():
    try:
        payment_id = request.json.get('paymentId')
        load_payments()
        
        for payment in payments:
            if payment['id'] == payment_id:
                payment['blocked'] = True
                payment['blockedAt'] = time.time()
                save_payments()
                return jsonify({'success': True})
        
        return jsonify({'success': False, 'error': 'Платеж не найден'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

ADMIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🛡️ Kilopa Admin</title>
    <meta charset="utf-8">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 30px; 
            border-radius: 10px; 
            margin-bottom: 30px; 
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        }
        .stat-card.pending { background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); }
        .stat-card.confirmed { background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); }
        .stat-card.blocked { background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%); }
        .payment { 
            border: 1px solid #e0e0e0; 
            margin: 15px 0; 
            padding: 20px; 
            border-radius: 10px; 
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .payment.confirmed { 
            background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c8 100%);
            border-color: #4CAF50;
        }
        .payment.blocked { 
            background: linear-gradient(135deg, #ffeaea 0%, #ffcaca 100%);
            border-color: #f44336;
        }
        .payment.pending { 
            background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
            border-color: #ff9800;
        }
        button { 
            padding: 10px 20px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer; 
            margin: 5px;
            font-weight: bold;
            transition: all 0.3s;
        }
        .confirm-btn { 
            background: linear-gradient(135deg, #4caf50 0%, #45a049 100%); 
            color: white;
        }
        .confirm-btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(76,175,80,0.4); }
        .block-btn { 
            background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%); 
            color: white;
        }
        .block-btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(244,67,54,0.4); }
        .refresh-btn { 
            background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%); 
            color: white; 
            padding: 15px 30px;
            font-size: 16px;
        }
        .refresh-btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(33,150,243,0.4); }
        .payment-id { font-weight: bold; color: #1976d2; }
        .status-badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }
        .status-confirmed { background: #4CAF50; color: white; }
        .status-pending { background: #ff9800; color: white; }
        .status-blocked { background: #f44336; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Kilopa Admin Panel</h1>
            <p>Управление лицензиями и платежами</p>
            <p style="font-size: 14px; opacity: 0.8;">Версия 1.1.0 • Обновляется автоматически</p>
        </div>
        
        <div class="stats" id="stats">
            <div class="stat-card pending">
                <h3>⏳ Ожидают</h3>
                <div style="font-size: 24px; font-weight: bold;" id="pending-count">0</div>
            </div>
            <div class="stat-card confirmed">
                <h3>✅ Подтверждены</h3>
                <div style="font-size: 24px; font-weight: bold;" id="confirmed-count">0</div>
            </div>
            <div class="stat-card blocked">
                <h3>🚫 Заблокированы</h3>
                <div style="font-size: 24px; font-weight: bold;" id="blocked-count">0</div>
            </div>
            <div class="stat-card">
                <h3>💰 Общая сумма</h3>
                <div style="font-size: 24px; font-weight: bold;" id="total-amount">0₽</div>
            </div>
        </div>
        
        <div style="margin-bottom: 20px; text-align: center;">
            <button class="refresh-btn" onclick="loadPayments()">🔄 Обновить данные</button>
        </div>
        
        <div id="payments">Загрузка платежей...</div>
    </div>

    <script>
        function loadPayments() {
            fetch('/api/payments')
                .then(response => response.json())
                .then(data => {
                    displayPayments(data);
                    updateStats(data);
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                    document.getElementById('payments').innerHTML = '<p style="color: red;">Ошибка загрузки данных</p>';
                });
        }

        function updateStats(payments) {
            const pending = payments.filter(p => !p.confirmed && !p.blocked).length;
            const confirmed = payments.filter(p => p.confirmed).length;
            const blocked = payments.filter(p => p.blocked).length;
            const totalAmount = payments.reduce((sum, p) => sum + (p.amount || 0), 0);
            
            document.getElementById('pending-count').textContent = pending;
            document.getElementById('confirmed-count').textContent = confirmed;
            document.getElementById('blocked-count').textContent = blocked;
            document.getElementById('total-amount').textContent = totalAmount + '₽';
        }

        function displayPayments(payments) {
            const container = document.getElementById('payments');
            
            if (payments.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #666; font-style: italic;">Платежей пока нет</p>';
                return;
            }

            // Сортируем по времени (новые сверху)
            payments.sort((a, b) => b.timestamp - a.timestamp);

            container.innerHTML = payments.map(payment => {
                const status = payment.blocked ? 'blocked' : (payment.confirmed ? 'confirmed' : 'pending');
                const statusText = payment.blocked ? 'Заблокирован' : (payment.confirmed ? 'Подтвержден' : 'Ожидает');
                const date = new Date(payment.timestamp * 1000).toLocaleString('ru-RU');
                const statusBadge = `<span class="status-badge status-${status}">${statusText}</span>`;
                
                return `
                    <div class="payment ${status}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <span class="payment-id">${payment.id}</span>
                            ${statusBadge}
                        </div>
                        <div style="margin-bottom: 15px;">
                            <strong>👤 Пользователь:</strong> ${payment.userId}<br>
                            <strong>📦 Продукт:</strong> ${payment.productId}<br>
                            <strong>💰 Сумма:</strong> ${payment.amount}₽<br>
                            <strong>📧 Email:</strong> ${payment.email || 'Не указан'}<br>
                            <strong>📅 Дата:</strong> ${date}
                        </div>
                        <div>
                            <button class="confirm-btn" onclick="confirmPayment('${payment.id}')" ${payment.confirmed || payment.blocked ? 'disabled' : ''}>
                                ✅ Подтвердить оплату
                            </button>
                            <button class="block-btn" onclick="blockUser('${payment.id}')" ${payment.blocked ? 'disabled' : ''}>
                                🚫 Заблокировать пользователя
                            </button>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function confirmPayment(paymentId) {
            if (!confirm('Подтвердить оплату? Пользователь получит полную лицензию.')) return;
            
            fetch('/api/confirm-payment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ paymentId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    loadPayments();
                } else {
                    alert('Ошибка: ' + data.error);
                }
            });
        }

        function blockUser(paymentId) {
            if (!confirm('Заблокировать пользователя? Это действие нельзя отменить!')) return;
            
            fetch('/api/block-user', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ paymentId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    loadPayments();
                } else {
                    alert('Ошибка: ' + data.error);
                }
            });
        }

        // Автообновление каждые 10 секунд
        setInterval(loadPayments, 10000);
        
        // Загружаем данные при старте
        loadPayments();
    </script>
</body>
</html>
'''

PAYMENT_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>💳 Оплата Kilopa</title>
    <meta charset="utf-8">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            min-height: 100vh; 
            display: flex; 
            align-items: center; 
            justify-content: center;
            margin: 0;
            padding: 20px;
        }
        .container { 
            background: white; 
            border-radius: 20px; 
            max-width: 500px; 
            width: 100%; 
            padding: 40px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
            text-align: center;
        }
        .logo {
            font-size: 48px;
            margin-bottom: 20px;
        }
        .price { 
            font-size: 48px; 
            font-weight: bold; 
            color: #4CAF50; 
            text-align: center; 
            margin: 30px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .info-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #667eea;
        }
        input { 
            width: 100%; 
            padding: 15px; 
            margin: 10px 0; 
            border: 2px solid #ddd; 
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus {
            border-color: #667eea;
            outline: none;
        }
        .pay-button { 
            width: 100%; 
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); 
            color: white; 
            padding: 18px; 
            border: none; 
            border-radius: 10px; 
            font-size: 20px; 
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 20px;
        }
        .pay-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(76,175,80,0.4);
        }
        .features {
            text-align: left;
            margin: 20px 0;
        }
        .feature {
            margin: 10px 0;
            color: #555;
        }
        .check-button {
            background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🛡️</div>
        <h1>Покупка Kilopa Protection</h1>
        
        <div class="info-card">
            <p><strong>📦 Продукт:</strong> {{ product }}</p>
            <p><strong>🆔 ID пользователя:</strong> {{ user_id }}</p>
        </div>
        
        <div class="price">1500₽</div>
        
        <div class="features">
            <h3>🎯 Что вы получите:</h3>
            <div class="feature">✅ Безлимитное время работы</div>
            <div class="feature">✅ Снятие всех ограничений</div>
            <div class="feature">✅ Доступ ко всем функциям</div>
            <div class="feature">✅ Техническая поддержка</div>
            <div class="feature">✅ Бесплатные обновления</div>
        </div>
        
        <form onsubmit="processPay(event)">
            <input type="email" placeholder="📧 Ваш email" id="email" required>
            <input type="text" placeholder="💳 Номер карты (1234 5678 9012 3456)" pattern="[0-9\\s]{13,19}" required>
            <input type="text" placeholder="📅 MM/YY" pattern="[0-9]{2}/[0-9]{2}" required>
            <input type="text" placeholder="🔒 CVV" pattern="[0-9]{3,4}" required>
            <button type="submit" class="pay-button">💳 Оплатить 1500₽</button>
        </form>
        
        <div style="margin-top: 30px;">
            <p style="color: #666;">После оплаты нажмите кнопку ниже:</p>
            <button class="check-button" onclick="checkPayment()">🔍 Проверить статус оплаты</button>
        </div>
        
        <div style="margin-top: 20px; font-size: 12px; color: #888;">
            🔒 Безопасная оплата • SSL шифрование • Защита данных
        </div>
    </div>

    <script>
        function processPay(event) {
            event.preventDefault();
            const email = document.getElementById('email').value;
            
            // Симуляция обработки оплаты
            document.querySelector('.pay-button').innerHTML = '⏳ Обработка...';
            document.querySelector('.pay-button').disabled = true;
            
            setTimeout(() => {
                fetch('/api/add-payment', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        userId: '{{ user_id }}',
                        productId: '{{ product }}',
                        amount: 1500,
                        email: email
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.querySelector('.pay-button').innerHTML = '✅ Платеж отправлен!';
                        document.querySelector('.pay-button').style.background = 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)';
                        alert('✅ Платеж успешно отправлен!\\n\\n📧 Уведомление отправлено администратору\\n🔍 Нажмите "Проверить статус" для получения лицензии');
                    } else {
                        document.querySelector('.pay-button').innerHTML = '❌ Ошибка оплаты';
                        document.querySelector('.pay-button').style.background = '#f44336';
                        alert('❌ Произошла ошибка при обработке платежа');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('❌ Ошибка соединения с сервером');
                })
                .finally(() => {
                    setTimeout(() => {
                        document.querySelector('.pay-button').disabled = false;
                        document.querySelector('.pay-button').innerHTML = '💳 Оплатить 1500₽';
                        document.querySelector('.pay-button').style.background = 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)';
                    }, 3000);
                });
            }, 2000);
        }
        
        function checkPayment() {
            fetch('/api/check-payment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    userId: '{{ user_id }}',
                    productId: '{{ product }}'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'paid') {
                    alert('🎉 ПОЗДРАВЛЯЕМ!\\n\\n✅ Оплата подтверждена!\\n🔑 Лицензия активирована!\\n\\nПерезапустите приложение для активации полной версии.');
                } else if (data.status === 'blocked') {
                    alert('🚫 Ваш аккаунт заблокирован\\n\\nОбратитесь в техподдержку');
                } else {
                    alert('⏳ Платеж в обработке\\n\\nАдминистратор еще не подтвердил оплату.\\nПовторите проверку через несколько минут.');
                }
            })
            .catch(error => {
                alert('❌ Ошибка проверки статуса');
            });
        }
    </script>
</body>
</html>
'''

def start_server(port=8888):
    load_payments()
    print(f"🚀 Kilopa Admin запущен на порту {port}")
    print(f"🌐 Админ-панель: http://localhost:{port}")
    threading.Timer(1, lambda: webbrowser.open(f"http://localhost:{port}")).start()
    app.run(host='localhost', port=port, debug=False)

def main():
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8888
    start_server(port)

if __name__ == '__main__':
    start_server()