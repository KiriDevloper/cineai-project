from flask import Flask
from flask import Flask, render_template, session, request  
from config import Config

from routes.auth_routes import auth_bp
from routes.review_routes import review_bp



app = Flask(__name__)

app.secret_key = Config.SECRET_KEY
# ── Routes ──
# Danh sách phim (giống home.html, hoặc lưu trong DB/config)
MOVIES = [
    {"id": 0,  "title": "The Dark Knight",          },
    {"id": 1,  "title": "Inception",                },
    {"id": 2,  "title": "Interstellar",             },
    {"id": 3,  "title": "Parasite",                 },
    {"id": 4,  "title": "John Wick: Chapter 3",     },
    {"id": 5,  "title": "Oppenheimer",              },
    {"id": 6,  "title": "The Shawshank Redemption", },
    {"id": 7,  "title": "Pulp Fiction",             },
    {"id": 8,  "title": "Avengers: Endgame",        },
    {"id": 9,  "title": "Get Out",                  },
    {"id": 10, "title": "La La Land",               },
    {"id": 11, "title": "Dune",                     },
]


@app.route("/movie")
def movie_detail():
    movie_id = request.args.get("movie_id", 0, type=int)
    movie    = next((m for m in MOVIES if m["id"] == movie_id), MOVIES[0])
    
    print(f"DEBUG movie được chọn: {movie['title']} | id: {movie['id']}")  # ← log
    
    return render_template("index.html", movie=movie)
@app.route("/")
def home():
    return render_template("home.html")
# register routes
app.register_blueprint(auth_bp)

app.register_blueprint(review_bp)

if __name__ == "__main__":
    app.run(debug=True)