print("=" * 50)
print("APP.PY IS RUNNING!")
print("=" * 50)
from flask import Flask, request ,jsonify
from flask_cors import CORS
import sqlite3

app=Flask(__name__)
CORS(app)

def init_db():
    conn=sqlite3.connect('blog.db')
    cursor=conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS posts ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   author TEXT NOT NULL,
                   content TEXT NOT NULL,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
                   ''')
    conn.commit()
    conn.close()

@app.route('/posts' , methods=['GET'])
def get_posts():
    conn=sqlite3.connect('blog.db')
    cursor=conn.cursor()
    cursor.execute(''' 
                    SELECT* FROM posts ORDER BY created_at DESC
                    ''')
    results=cursor.fetchall()
    conn.close()
    return jsonify(results) , 200

@app.route('/posts' , methods=['POST'])
def create_posts():
    data=request.get_json()
    title=data['title']
    author=data['author']
    content=data['content']
    conn=sqlite3.connect('blog.db')
    cursor=conn.cursor()
    cursor.execute('''
                    INSERT INTO posts (title,author,content) VALUES (?,?,?)
                   ''',(title,author,content) )
    conn.commit()
    conn.close()
    return jsonify({'message':'Post Created'}),201

@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    conn=sqlite3.connect('blog.db')
    cursor=conn.cursor()
    cursor.execute(''' 
                    SELECT* FROM posts WHERE id = ? 
                    ''',(id,))
    result=cursor.fetchone()
    conn.close()
    if result:
        return jsonify(result) , 200
    else:
        return jsonify({'error':'Post not found'}),404

@app.route('/posts/<int:id>' ,methods=['DELETE'])
def delete_post(id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    if cursor.rowcount>0:
        return jsonify({'message':'Post Deleted'}),200
    else:
        return jsonify({'error':'Post not found'}),404

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0',port=5000,debug=True)
    