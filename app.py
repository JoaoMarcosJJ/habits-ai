import os
import json
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_cors import CORS
from dotenv import load_dotenv

import google.generativeai as genai

load_dotenv()
app = Flask(__name__, static_folder='static', template_folder='templates')

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("Aviso: Variável de ambiente GEMINI_API_KEY não definida.")

else:
    genai.configure(api_key=GEMINI_API_KEY)

class Habit(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.Date, nullable=False, default=lambda: datetime.now(timezone.utc).date())
    completed_dates = db.Column(db.String(200), nullable=False, default='[]')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'completed_dates': json.loads(self.completed_dates)
        }
    
@app.route('/api/habits', methods=['GET'])
def get_habits():
    try:
        habits = Habit.query.all()
        habits_list = [h.to_dict() for h in habits]
        return jsonify(habits_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/habits', methods=['POST'])
def add_habit():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Nome é obrigatório'}), 400
        
    try:
        new_habit = Habit(name=data['name'], completed_dates='[]')
        db.session.add(new_habit)
        db.session.commit()
        return jsonify(new_habit.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/habits/<int:habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    try:
        habit = db.session.get(Habit, habit_id)
        if not habit:
            return jsonify({'error': 'Hábito não encontrado'}), 404
        
        db.session.delete(habit)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Hábito deletado.'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/habits/<int:habit_id>/toggle', methods=['POST'])
def toggle_habit_completion(habit_id):
    
    data = request.json
    if not data or 'date' not in data:
        return jsonify({'error': 'Data é obrigatória'}), 400
    
    date_str = data['date']

    try:
        habit = db.session.get(Habit, habit_id)
        if not habit:
            return jsonify({'error': 'Hábito não encontrado'}), 404
        
        completed_dates = json.loads(habit.completed_dates)
        
        if date_str in completed_dates:
            completed_dates.remove(date_str)
        else:
            completed_dates.append(date_str)
            completed_dates.sort()

        habit.completed_dates = json.dumps(completed_dates)
        db.session.commit()

        return jsonify(habit.to_dict()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/suggest', methods=['POST'])
def gemini_suggest():

    if not GEMINI_API_KEY:
        return jsonify({'error': 'API Key do Gemini não está configurada no servidor.'}), 503
    
    data = request.json
    if not data or 'goal' not in data:
        return jsonify({'error': 'Meta (goal) é obrigatória'}), 400
    
    goal = data['goal']

    try:
        model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')

        schema = {
            "type": "OBJECT",
            "properties": {
                "habits": {
                    "type": "ARRAY",
                    "items": { "type": "STRING"}
                }
            },
            "required": ["habits"]
        }

        system_prompt = f""" Você é um choach de produtividade. Sua tarefa é quebrar uma grande meta em 3 a 5 hábitos diários, pequenos e rastreáveis.
        Retorne APENAS o objetivo JSON com a chave "habits".
        Meta do Usuário: "{goal}" """

        response = model.generate_content( 
            system_prompt,
            generation_config=genai.GenerationConfig( 
                response_mime_type="application/json",
                response_schema=schema
            )
        )    

        suggestions = json.loads(response.text) 
        new_habits_list = []

        if 'habits' in suggestions and suggestions['habits']:
            for habit_name in suggestions['habits']:
                new_habit = Habit(name=habit_name, completed_dates='[]')
                db.session.add(new_habit)
                new_habits_list.append(new_habit)

            db.session.commit()

            created_habits_json = [h.to_dict() for h in new_habits_list]
            return jsonify({'success': True, 'created_habits': created_habits_json}), 201
        else:
            return jsonify({'error': 'Não foi possível gerar sugestão'}), 400
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao gerar sugestão: {e}")
        return jsonify({'error': f'Erro ao processar sugestão: {e}'}), 500
    
@app.route('/')
def index():
    return render_template('index.html')
    

if __name__ == '__main__':
    with app.app_context():
        instance_path = os.path.join(app.root_path, 'instance')
        os.makedirs(instance_path, exist_ok=True)
        db.create_all()

    app.run(debug=True, host='0.0.0.0', port=5000)