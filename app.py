from flask import Flask, render_template, request, jsonify
import json
import yfinance as yf
from datetime import datetime, timedelta
from markets import MARKETS
from analyzer import analyze_market
from database import get_all_history, get_statistics
from search import search_market, list_all_markets

app = Flask(__name__)

# Enable CORS
from flask_cors import CORS
CORS(app)


@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/markets', methods=['GET'])
def get_markets():
    """Get all available markets"""
    try:
        markets = list_all_markets()
        return jsonify({
            "status": "success",
            "data": markets,
            "count": len(markets)
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/search', methods=['GET'])
def search():
    """Search for a market"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({"status": "error", "message": "Query required"}), 400
        
        results = search_market(query)
        return jsonify({
            "status": "success" if results else "not_found",
            "query": query,
            "data": results if results else {}
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/analyze/<symbol>', methods=['GET'])
def analyze(symbol):
    """Analyze a specific market"""
    try:
        market_name = None
        for name, sym in MARKETS.items():
            if sym == symbol:
                market_name = name
                break
        
        if not market_name:
            return jsonify({"status": "error", "message": "Market not found"}), 404
        
        result = analyze_market(market_name, symbol)
        
        return jsonify({
            "status": "success",
            "market_name": market_name,
            "symbol": symbol,
            "analysis": result,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/history', methods=['GET'])
def history():
    """Get analysis history"""
    try:
        limit = request.args.get('limit', 20, type=int)
        history_data = get_all_history(limit=limit)
        
        return jsonify({
            "status": "success",
            "data": history_data,
            "count": len(history_data)
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/statistics/<market_name>', methods=['GET'])
def statistics(market_name):
    """Get statistics for a market"""
    try:
        stats = get_statistics(market_name)
        
        if not stats:
            return jsonify({"status": "error", "message": "No data found"}), 404
        
        return jsonify({
            "status": "success",
            "data": stats
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/price/<symbol>', methods=['GET'])
def get_price(symbol):
    """Get current price for a symbol"""
    try:
        data = yf.download(symbol, period="1d", progress=False)
        current_price = data['Close'].iloc[-1]
        prev_price = data['Close'].iloc[-2] if len(data) > 1 else current_price
        
        change = current_price - prev_price
        change_percent = (change / prev_price) * 100 if prev_price != 0 else 0
        
        return jsonify({
            "status": "success",
            "symbol": symbol,
            "current_price": round(current_price, 2),
            "previous_price": round(prev_price, 2),
            "change": round(change, 2),
            "change_percent": round(change_percent, 2),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/chart/<symbol>', methods=['GET'])
def get_chart(symbol):
    """Get chart data for a symbol"""
    try:
        period = request.args.get('period', '5d')
        data = yf.download(symbol, period=period, progress=False)
        
        chart_data = {
            "dates": [str(date.date()) for date in data.index],
            "close": data['Close'].tolist(),
            "high": data['High'].tolist(),
            "low": data['Low'].tolist(),
            "volume": data['Volume'].tolist()
        }
        
        return jsonify({
            "status": "success",
            "symbol": symbol,
            "period": period,
            "data": chart_data
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/performance', methods=['GET'])
def performance():
    """Get overall performance metrics"""
    try:
        all_stats = []
        for market_name in MARKETS.keys():
            stats = get_statistics(market_name)
            if stats:
                all_stats.append(stats)
        
        return jsonify({
            "status": "success",
            "markets": all_stats,
            "total_markets": len(all_stats),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
