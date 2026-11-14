from flask import Flask, request, session, redirect, render_template_string
from html import escape

app = Flask(__name__)
app.secret_key = "a-remplacer-par-une-cle-secrete-longue"

produits = [
    {"id": 1, "nom": "Sabots roses", "prix": 7, "categorie": "Chaussures", "promo": 0, "tailles": ["38", "39", "40"], "emoji": "👡"},
    {"id": 2, "nom": "Baskets homme", "prix": 19.90, "categorie": "Chaussures", "promo": 10, "tailles": ["40", "41", "42", "43"], "emoji": "👟"},
    {"id": 3, "nom": "Jean homme", "prix": 14.90, "categorie": "Vêtements", "promo": 0, "tailles": ["38", "40", "42", "44"], "emoji": "👖"},
    {"id": 4, "nom": "Sweat à capuche", "prix": 15.90, "categorie": "Vêtements", "promo": 20, "tailles": ["S", "M", "L", "XL"], "emoji": "🧥"},
    {"id": 5, "nom": "Sac à main", "prix": 12.90, "categorie": "Accessoires", "promo": 0, "tailles": ["Unique"], "emoji": "👜"},
    {"id": 6, "nom": "Pull femme", "prix": 12.90, "categorie": "Vêtements", "promo": 10, "tailles": ["S", "M", "L"], "emoji": "👚"},
]

def prix_final(p):
    return round(p["prix"] * (1 - p["promo"] / 100), 2)

def euros(montant):
    return f"{montant:.2f} €".replace(".", ",")

PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>La Bonne Pioche</title>
<style>
* {box-sizing:border-box}
body {margin:0;font-family:Arial,sans-serif;background:#f3f6fb;color:#102e59}
header {background:#073c85;color:white;padding:12px;text-align:center}
header small {font-size:13px}
nav {background:white;padding:17px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.logo {font-size:25px;font-weight:bold;color:#073c85}
a {color:inherit;text-decoration:none}
nav a {padding:8px}
.hero {background:linear-gradient(120deg,#0753a8,#072e68);color:white;text-align:center;padding:45px 15px}
.hero h1 {font-size:38px;margin:8px}
.hero p {font-size:19px}
.promo {display:inline-block;background:#ffb400;color:#142b48;padding:12px;border-radius:10px;font-weight:bold}
.container {max-width:1150px;margin:auto;padding:20px}
.categories {display:flex;gap:10px;flex-wrap:wrap;margin-bottom:22px}
.categories a {background:white;border:1px solid #ddd;border-radius:20px;padding:10px 17px}
.grid {display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px}
.card {background:white;border-radius:14px;padding:18px;box-shadow:0 2px 8px #0001}
.photo {height:130px;display:flex;align-items:center;justify-content:center;background:#eef3f9;border-radius:12px;font-size:75px}
.card h3 {margin-bottom:8px}
.price {color:#e21e29;font-weight:bold;font-size:23px}
.old {text-decoration:line-through;color:gray;font-size:14px}
.badge {background:#e21e29;color:white;padding:5px 9px;border-radius:6px;font-size:12px}
select,input {padding:10px;border:1px solid #ccc;border-radius:7px;max-width:100%}
button,.btn {display:inline-block;background:#ffac00;border:0;border-radius:8px;padding:12px 16px;font-weight:bold;cursor:pointer;color:#102e59}
button:hover,.btn:hover {background:#ffca45}
.card form {display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
table {width:100%;border-collapse:collapse;background:white}
td,th {padding:13px;border-bottom:1px solid #ddd;text-align:left}
.message {padding:20px;background:white;border-radius:10px}
footer {margin-top:40px;background:#073c85;color:white;text-align:center;padding:25px}
</style>
</head>
<body>
<header>
<small>🚚 Livraison en France | 🔒 Paiement sécurisé à venir | 🎁 Petits prix</small>
</header>
<nav>
<a href="/" class="logo">🛍️ La Bonne Pioche</a>
<div>
<a href="/">Accueil</a>
<a href="/?categorie=Vêtements">Vêtements</a>
<a href="/?categorie=Chaussures">Chaussures</a>
<a href="/?categorie=Accessoires">Accessoires</a>
<a href="/panier">🛒 Panier ({{ nombre }})</a>
</div>
</nav>

{% if page == "accueil" %}
<section class="hero">
<h1>LA BONNE PIOCHE</h1>
<p>Des produits à petits prix pour toute la famille !</p>
<span class="promo">🎉 Promotions -10 % et -20 %</span>
</section>
<div class="container">
<h2>Nos catégories</h2>
<div class="categories">
<a href="/">Tous les articles</a>
<a href="/?categorie=Vêtements">👕 Vêtements</a>
<a href="/?categorie=Chaussures">👟 Chaussures</a>
<a href="/?categorie=Accessoires">👜 Accessoires</a>
</div>
<h2>🔥 Nos meilleures offres</h2>
<div class="grid">
{% for p in produits %}
<div class="card">
<div class="photo">{{ p.emoji }}</div>
<h3>{{ p.nom }}</h3>
<p>{{ p.categorie }}</p>
{% if p.promo %}
<span class="badge">-{{ p.promo }} %</span>
<p class="old">{{ p.prix|euro }}</p>
{% endif %}
<p class="price">{{ p|final|euro }}</p>
<form action="/ajouter" method="post">
<input type="hidden" name="id" value="{{ p.id }}">
<select name="taille">
{% for taille in p.tailles %}
<option value="{{ taille }}">{{ taille }}</option>
{% endfor %}
</select>
<button type="submit">Ajouter au panier</button>
</form>
</div>
{% endfor %}
</div>
</div>
{% elif page == "panier" %}
<div class="container">
<h1>🛒 Mon panier</h1>
{% if lignes %}
<table>
<tr><th>Article</th><th>Taille</th><th>Prix</th><th></th></tr>
{% for ligne in lignes %}
<tr>
<td>{{ ligne.nom }}</td>
<td>{{ ligne.taille }}</td>
<td>{{ ligne.prix|euro }}</td>
<td>
<form action="/supprimer" method="post">
<input type="hidden" name="index" value="{{ loop.index0 }}">
<button type="submit">Retirer</button>
</form>
</td>
</tr>
{% endfor %}
</table>
<h2>Total : {{ total|euro }}</h2>
<a class="btn" href="/commande">Passer commande</a>
{% else %}
<p>Votre panier est vide.</p>
<a class="btn" href="/">Voir les produits</a>
{% endif %}
</div>
{% elif page == "commande" %}
<div class="container">
<h1>Finaliser ma commande</h1>
<p>Total : <strong>{{ total|euro }}</strong></p>
<div class="message">
<p>Cette boutique est une démonstration. Aucun paiement réel n'est effectué.</p>
<form method="post">
<p><input name="nom" placeholder="Nom et prénom" required></p>
<p><input name="email" type="email" placeholder="Adresse e-mail" required></p>
<p><input name="adresse" placeholder="Adresse de livraison" required></p>
<p>
<select name="livraison">
<option>Mondial Relay (simulation)</option>
<option>Colissimo (simulation)</option>
</select>
</p>
<button type="submit">Simuler ma commande</button>
</form>
</div>
</div>
{% elif page == "confirmation" %}
<div class="container">
<div class="message">
<h1>✅ Commande simulée !</h1>
<p>Merci {{ nom }} !</p>
<p>Votre simulation de commande est terminée.</p>
<p>Aucun paiement ni aucune livraison n'ont été déclenchés.</p>
<a class="btn" href="/">Retour à la boutique</a>
</div>
</div>
{% endif %}
<footer>
<p>© La Bonne Pioche — Boutique de démonstration</p>
<p>Livraison Mondial Relay et Colissimo : intégration à venir</p>
</footer>
</body>
</html>
"""

app.jinja_env.filters["euro"] = euros
app.jinja_env.filters["final"] = prix_final

def afficher(page, **donnees):
    return render_template_string(
        PAGE, page=page,
        nombre=len(session.get("panier", [])),
        **donnees
    )

@app.route("/")
def accueil():
    categorie = request.args.get("categorie", "")
    selection = [
        p for p in produits
        if not categorie or p["categorie"] == categorie
    ]
    return afficher("accueil", produits=selection)

@app.route("/ajouter", methods=["POST"])
def ajouter():
    try:
        identifiant = int(request.form.get("id", "0"))
    except ValueError:
        return redirect("/")
    p = next((x for x in produits if x["id"] == identifiant), None)
    if p:
        taille = request.form.get("taille", "")
        if taille in p["tailles"]:
            panier = session.get("panier", [])
            panier.append({"id": p["id"], "taille": taille})
            session["panier"] = panier
    return redirect("/panier")

def contenu_panier():
    lignes = []
    for article in session.get("panier", []):
        p = next((x for x in produits if x["id"] == article["id"]), None)
        if p:
            lignes.append({
                "nom": p["nom"],
                "taille": article["taille"],
                "prix": prix_final(p)
            })
    return lignes

@app.route("/panier")
def panier():
    lignes = contenu_panier()
    total = round(sum(x["prix"] for x in lignes), 2)
    return afficher("panier", lignes=lignes, total=total)

@app.route("/supprimer", methods=["POST"])
def supprimer():
    panier = session.get("panier", [])
    try:
        index = int(request.form.get("index", "-1"))
        if 0 <= index < len(panier):
            panier.pop(index)
            session["panier"] = panier
    except ValueError:
        pass
    return redirect("/panier")

@app.route("/commande", methods=["GET", "POST"])
def commande():
    lignes = contenu_panier()
    if not lignes:
        return redirect("/panier")
    if request.method == "POST":
        nom = request.form.get("nom", "").strip()
        if not nom:
            return redirect("/commande")
        session.pop("panier", None)
        return afficher("confirmation", nom=nom)
    total = round(sum(x["prix"] for x in lignes), 2)
    return afficher("commande", total=total)

if __name__ == "__main__":
    app.run(debug=True)
