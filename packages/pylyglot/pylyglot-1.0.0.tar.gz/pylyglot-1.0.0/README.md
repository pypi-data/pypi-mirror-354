# PyLyglot

**PyLyglot** est une bibliothèque Python de traduction simple, extensible et thread-safe, utilisant le pattern singleton pour centraliser la gestion des langues. Elle permet la traduction de clés hiérarchiques avec gestion du fallback et formatage dynamique.

## 📦 Fonctionnalités

- Chargement automatique de fichiers JSON de traduction.
- Détection automatique de la langue du système.
- Fallback intelligent vers des langues plus générales (ex: `fr-CA` → `fr` → `en`).
- Clés hiérarchiques via la notation `dot.key`.
- Formatage avec `str.format()`.
- Gestion personnalisée des clés manquantes.

## 🛠 Installation

```bash
pip install pylyglot
```
Ou ajoute-le directement à ton pyproject.toml si tu utilises Poetry.

## 📁 Structure des fichiers
Les fichiers de langue doivent être placés dans un répertoire lang/ à la racine de ton projet.
Exemple :
```pgsql
lang/
├── en.json
├── fr.json
```
Exemple de fichier en.json :
```json
{
    "_meta": {
      "version": "1.0",
      "author": "Your Name"
    },
    "menu": {
        "start": "Start",
        "quit": "Quit"
    },
    "welcome": "Welcome, {username}!"
}
```
## 🚀 Utilisation
 - 1 Créer le dossier /lang à la racine de votre proket
 - 2 ajouter les fichiers de langues
```python
from pylyglot import PyLyglot

def missing_key_handler(key):
    return f"<<{key}>>"

pl = PyLyglot(missing_key_handler=missing_key_handler)

print(pl("menu.start"))              # Start
print(pl("menu.quit"))               # Quit
print(pl("welcome", username="Alice"))  # Welcome, Alice!
```
