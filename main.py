from flask import Flask, render_template, redirect, url_for, session, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
db = SQLAlchemy(app)

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    price = db.Column(db.String(16))
    description = db.Column(db.Text)
    image = db.Column(db.String(128))
    impact = db.Column(db.Text)
    platform = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'price_numeric': float(self.price.replace('£','')),
            'description': self.description,
            'image': self.image,
            'impact': self.impact,
            'platform': self.platform
        }
    
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    customer_name = db.Column(db.String(100))
    customer_email = db.Column(db.String(100))
    total_amount = db.Column(db.Float)
    items = db.relationship('OrderItem',backref='order', lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    game = db.relationship('Game')

@app.route('/')
def galleryPage():
    games = Game.query.all()
    return render_template('index.html', games=games)

@app.route('/game/<int:gameId>')
def singleProductPage(gameId):
    game = Game.query.get_or_404(gameId)
    related_games = Game.query.filter(Game.platform == game.platform, Game.id != game.id).limit(4).all()
    return render_template('SingleItem.html', game=game, related_games = related_games)

@app.route('/cart')
def viewCart():
    cart = session.get('cart', [])
    cart_items = []
    total = 0

    for item in cart:
        game = Game.query.get(item['game_id'])
        if game:
            price = float(game.price.replace('£', ''))
            subtotal = price * item['quantity']
            total += subtotal
            
            cart_items.append({
                'id': game.id,
                'name': game.name,
                'price': game.price,
                'image': game.image,
                'quantity': item['quantity'],
                'subtotal': f'£{subtotal:.2f}'
            })

    return render_template('cart.html', cart_items=cart_items, total=f'£{total:.2f}')

@app.route('/add-to-cart', methods=['POST'])
def addToCart():
    game_id = request.form.get('game_id', type=int)
    quantity = request.form.get('quantity',1,type=int)

    if not game_id:
        return jsonify({'error': 'Invalid game ID'}), 400

    game = Game.query.get_or_404(game_id)

    if 'cart' not in session:
        session['cart'] = []

    cart = session['cart']

    found = False
    for item in cart:
        if item['game_id'] == game_id:
            item['quantity'] += quantity
            found = True
            break

    if not found:
        cart.append({'game_id': game_id, 'quantity': quantity}) 

    session['cart'] = cart
    flash(f'Added {game.name} to your cart!')
    return redirect(url_for('singleProductPage', gameId=game_id))

@app.route('/remove-from-cart/<int:gameId>')
def removeFromCart(gameId):
    if 'cart' not in session:
        return redirect(url_for('viewCart'))
    
    cart = session['cart']
    for item in cart[:]:
        if item['game_id'] == gameId:
            cart.remove(item)
            break
    
    session['cart'] = cart
    return redirect(url_for('viewCart'))

@app.route('/update-cart', methods=['POST'])
def updateCart():
    game_id = request.form.get('game_id',type=int)
    quantity = request.form.get('quantity', 1, type=int)

    if not game_id:
        return jsonify({'error': 'Invalid game ID'}), 400
    
    if 'cart' not in session:
        return redirect(url_for('viewCart'))
    
    cart = session['cart']
    
    for item in cart:
        if item['game_id'] == game_id:
            if quantity <= 0:
                cart.remove(item)
            else:
                item['quantity'] = quantity
            break
    
    session['cart'] = cart
    return redirect(url_for('viewCart'))

@app.route('/checkout')
def checkout():
    cart = session.get('cart', [])
    if not cart:
        flash('The cart is empty!')
        return redirect(url_for('galleryPage'))
    
    cart_items = []
    total = 0

    for item in cart:
        game = Game.query.get(item['game_id'])
        if game:
            price = float(game.price.replace('£', ''))
            subtotal = price * item['quantity']
            total += subtotal

            cart_items.append({
                'id': game.id,
                'name': game.name,
                'price': game.price,
                'image': game.image,
                'quantity': item['quantity'],
                'subtotal': f'£{subtotal:.2f}'
            })
    return render_template('checkout.html',cart_items=cart_items, total=f'£{total:.2f}')

@app.route('/place-order', methods=['POST'])
def placeOrder():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty')
        return redirect(url_for('galleryPage'))
    
    name = request.form.get('name')
    email = request.form.get('email')

    if not name or not email:
        flash('Please fill out all required fields')
        return redirect(url_for('checkout'))
    
    cart = session.get('cart', [])
    total = 0

    for item in cart:
        game = Game.query.get(item['game_id'])
        if game:
            price = float(game.price.replace('£',''))
            total += price * item['quantity']

    order = Order(
        customer_name=name,
        customer_email=email,
        total_amount=total
    )
    db.session.add(order)
    db.session.flush()

    for item in cart:
        game = Game.query.get(item['game_id'])
        if game:
            price = float(game.price.replace('£',''))
            order_item = OrderItem(
                order_id=order.id,
                game_id=game.id,
                quantity=item['quantity'],
                price=price
            )
            db.session.add(order_item)

    db.session.commit()

    session.pop('cart',None)

    flash('Thank you for your order!')
    return redirect(url_for('orderConfirmation', order_id=order.id))

@app.route('/order-confirmation/<int:order_id>')
def orderConfirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_confirmation.html', order=order)

@app.route('/api/cart/count')
def cartCount():
    cart = session.get('cart', [])
    count = sum(item['quantity'] for item in cart)
    return jsonify({'count': count})

@app.route('/api/game/<int:gameId>')
def game_details_api(gameId):
    game = Game.query.get_or_404(gameId)
    return jsonify(game.to_dict())

@app.context_processor
def inject_cart_count():
    cart = session.get('cart', [])
    count = sum(item['quantity'] for item in cart)
    return {'cart_count': count}

if __name__ == '__main__':
    app.run(debug=True, port=5050)