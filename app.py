import os
from pathlib import Path

from flask import Flask, redirect, render_template_string, request, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(32)

produits = [
    {
        "id": 7,
        "nom": "Veste bomber femme",
        "categorie": "Vêtements",
        "prix": 20,
        "description": (
            "Veste courte à finition satinée, avec écussons sur la poitrine, "
            "fermeture à anneau, deux poches zippées et poignets côtelés."
        ),
        "couleurs": [
            "Bleu marine", "Bleu ciel", "Rouge", "Rose",
            "Kaki et jaune", "Kaki et blanc",
        ],
        "tailles": ["S", "M", "L", "XL"],
        "photos": [
            "IMG_5779.jpeg", "IMG_5777.jpeg", "IMG_5778.jpeg",
            "IMG_5785.jpeg", "IMG_5787.jpeg", "IMG_5786.jpeg",
        ],
    },
    {
        "id": 8,
        "nom": "Sabots en feutre",
        "categorie": "Chaussures",
        "prix": 7,
        "description": (
            "Sabots à bout fermé et talon ouvert, avec une bride à boucle "
            "et une semelle rainurée."
        ),
        "couleurs": ["Bleu", "Rose", "Gris anthracite"],
        "tailles": [str(pointure) for pointure in range(36, 46)],
        "photos": ["IMG_5783.jpeg", "IMG_5782.jpeg", "IMG_5784.jpeg"],
    },
    {
        "id": 9,
        "nom": "Chaussures de marche",
        "categorie": "Chaussures",
        "prix": 10,
        "description": (
            "Chaussures basses à lacets, avec un renfort à l’avant "
            "et une semelle crantée."
        ),
        "couleurs": ["Noir", "Marron"],
        "tailles": [str(pointure) for pointure in range(40, 46)],
        "photos": ["IMG_5780.jpeg", "IMG_5781.jpeg"],
    },
]

produits_par_id = {produit["id"]: produit for produit in produits}


@app.template_filter("euro")
def euros(montant):
    return f"{montant:.2f} €".replace(".", ",")


@app.template_test("photo_disponible")
def photo_disponible(nom):
    return (Path(app.root_path) / "static" / nom).is_file()


PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>La Bonne Pioche</title>
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f3f6fb;
    color: #102e59;
}
nav {
    background: white;
    padding: 16px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
}
nav a { color: inherit; }
.logo { font-size: 23px; font-weight: bold; text-decoration: none; }
.hero {
    padding: 32px 16px;
    text-align: center;
    background: #073c85;
    color: white;
}
.hero h1 { margin: 0 0 8px; }
.hero p { margin: 0; }
.container { max-width: 1100px; margin: auto; padding: 20px; }
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr));
    gap: 16px;
}
.card, .message { background: white; border-radius: 12px; padding: 16px; }
.photo {
    display: block;
    width: 100%;
    max-height: 300px;
    object-fit: contain;
    background: #f3f6fb;
    border-radius: 8px;
}
details { margin: 10px 0; }
details .photo { margin-top: 8px; }
summary { cursor: pointer; }
.price { color: #b61923; font-size: 22px; font-weight: bold; }
label { display: block; margin: 10px 0; }
select, input { display: block; width: 100%; padding: 10px; margin-top: 4px; }
button, .btn {
    display: inline-block;
    background: #ffb400;
    color: #102e59;
    border: 0;
    border-radius: 8px;
    padding: 10px 14px;
    font-weight: bold;
    text-decoration: none;
    cursor: pointer;
}
.ligne-panier { margin-bottom: 10px; }
footer { padding: 20px; text-align: center; color: white; background: #073c85; }
</style>
</head>
<body>
<nav aria-label="Navigation principale">
    <a class="logo" href="/">La Bonne Pioche</a>
    <a href="/?categorie=Vêtements">Vêtements</a>
    <a href="/?categorie=Chaussures">Chaussures</a>
    <a href="/panier">Panier ({{ nombre }})</a>
</nav>

{% if page == "accueil" %}
<section class="hero">
    <h1>La Bonne Pioche</h1>
    <p>Vêtements et chaussures à petits prix</p>
</section>
<main class="container">
    <h2>{{ categorie or "Tous les articles" }}</h2>
    <div class="grid">
    {% for produit in catalogue %}
        <article class="card">
            {% set photos = produit.photos | select("photo_disponible") | list %}
            {% if photos %}
            <img class="photo" src="{{ url_for('static', filename=photos[0]) }}"
                 alt="{{ produit.nom }}" loading="lazy">
            {% endif %}
            {% if photos | length > 1 %}
            <details>
                <summary>Voir les autres photos</summary>
                {% for photo in photos[1:] %}
                <img class="photo" src="{{ url_for('static', filename=photo) }}"
                     alt="{{ produit.nom }}" loading="lazy">
                {% endfor %}
            </details>
            {% endif %}
            <h3>{{ produit.nom }}</h3>
            <p>{{ produit.description }}</p>
            <p class="price">{{ produit.prix | euro }}</p>
            <form action="/ajouter" method="post">
                <input type="hidden" name="id" value="{{ produit.id }}">
                <label>Couleur
                    <select name="couleur" required>
                        {% for couleur in produit.couleurs %}
                        <option>{{ couleur }}</option>
                        {% endfor %}
                    </select>
                </label>
                <label>{{ "Taille" if produit.categorie == "Vêtements" else "Pointure" }}
                    <select name="taille" required>
                        {% for taille in produit.tailles %}
                        <option>{{ taille }}</option>
                        {% endfor %}
                    </select>
                </label>
                <button type="submit">Ajouter au panier</button>
            </form>
        </article>
    {% else %}
        <p>Aucun article dans cette catégorie.</p>
    {% endfor %}
    </div>
</main>

{% elif page == "panier" %}
<main class="container">
    <h1>Mon panier</h1>
    {% for ligne in lignes %}
    <article class="card ligne-panier">
        <strong>{{ ligne.produit.nom }}</strong>
        <p>{{ ligne.couleur }} · {{ ligne.taille }} · {{ ligne.produit.prix | euro }}</p>
        <form action="/supprimer" method="post">
            <input type="hidden" name="index" value="{{ loop.index0 }}">
            <button type="submit">Retirer</button>
        </form>
    </article>
    {% else %}
    <p>Votre panier est vide.</p>
    {% endfor %}
    {% if lignes %}
    <p class="price">Total {{ total | euro }}</p>
    <a class="btn" href="/commande">Passer commande</a>
    {% else %}
    <a class="btn" href="/">Voir les articles</a>
    {% endif %}
</main>

{% elif page == "commande" %}
<main class="container">
    <h1>Finaliser ma commande</h1>
    <div class="message">
        <p>Total {{ total | euro }}</p>
        <p>Commande de démonstration. Aucun paiement réel.</p>
        <form method="post">
            <label>Nom et prénom<input name="nom" required></label>
            <label>Adresse e-mail<input name="email" type="email" required></label>
            <label>Adresse de livraison<input name="adresse" required></label>
            <label>Livraison
                <select name="livraison">
                    <option>Mondial Relay (simulation)</option>
                    <option>Colissimo (simulation)</option>
                </select>
            </label>
            <button type="submit">Simuler ma commande</button>
        </form>
    </div>
</main>

{% elif page == "confirmation" %}
<main class="container">
    <h1>Commande simulée</h1>
    <p>Merci {{ nom }}. Aucun paiement ni envoi n’a été déclenché.</p>
    <a class="btn" href="/">Retour à la boutique</a>
</main>
{% endif %}

<footer>La Bonne Pioche · Boutique de démonstration</footer>
</body>
</html>
"""


def lire_panier():
    lignes = []
    for article in session.get("panier", []):
        produit = produits_par_id.get(article.get("id"))
        if produit is None:
            continue
        couleur = article.get("couleur")
        taille = article.get("taille", "")
        if couleur is None:
            couleur, _, taille = taille.partition(" - ")
        if couleur in produit["couleurs"] and taille in produit["tailles"]:
            lignes.append({"produit": produit, "couleur": couleur, "taille": taille})
    return lignes


def enregistrer_panier(lignes):
    session["panier"] = [
        {
            "id": ligne["produit"]["id"],
            "couleur": ligne["couleur"],
            "taille": ligne["taille"],
        }
        for ligne in lignes
    ]


@app.get("/")
def accueil():
    categorie = request.args.get("categorie", "")
    catalogue = [
        produit for produit in produits
        if not categorie or produit["categorie"] == categorie
    ]
    return render_template_string(
        PAGE, page="accueil", catalogue=catalogue,
        categorie=categorie, nombre=len(lire_panier()),
    )


@app.post("/ajouter")
def ajouter():
    produit = produits_par_id.get(request.form.get("id", type=int))
    if produit is None:
        return redirect("/")
    couleur = request.form.get("couleur", "")
    taille = request.form.get("taille", "")
    if couleur in produit["couleurs"] and taille in produit["tailles"]:
        lignes = lire_panier()
        lignes.append({"produit": produit, "couleur": couleur, "taille": taille})
        enregistrer_panier(lignes)
    return redirect("/panier")


@app.get("/panier")
def panier():
    lignes = lire_panier()
    total = sum(ligne["produit"]["prix"] for ligne in lignes)
    return render_template_string(
        PAGE, page="panier", lignes=lignes, total=total, nombre=len(lignes),
    )


@app.post("/supprimer")
def supprimer():
    lignes = lire_panier()
    index = request.form.get("index", default=-1, type=int)
    if 0 <= index < len(lignes):
        lignes.pop(index)
        enregistrer_panier(lignes)
    return redirect("/panier")


@app.route("/commande", methods=["GET", "POST"])
def commande():
    lignes = lire_panier()
    if not lignes:
        return redirect("/panier")
    if request.method == "POST":
        nom = request.form.get("nom", "").strip()
        if not nom:
            return redirect("/commande")
        session.pop("panier", None)
        return render_template_string(
            PAGE, page="confirmation", nom=nom, nombre=0,
        )
    total = sum(ligne["produit"]["prix"] for ligne in lignes)
    return render_template_string(
        PAGE, page="commande", total=total, nombre=len(lignes),
    )


if __name__ == "__main__":
    app.run()
