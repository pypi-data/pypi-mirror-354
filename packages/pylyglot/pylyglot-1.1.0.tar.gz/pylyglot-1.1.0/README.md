Pour améliorer le fichier README et en faire une documentation complète et professionnelle, nous devons ajouter des sections détaillées, des exemples d'utilisation, des instructions d'installation, et d'autres informations utiles. Voici une version améliorée du README pour PyLyglot :

```markdown
# PyLyglot

**PyLyglot** est une bibliothèque Python simple, extensible et thread-safe pour la gestion des traductions dans les applications. Elle utilise le pattern Singleton pour centraliser la gestion des langues et permet la traduction de clés hiérarchiques avec gestion du fallback et formatage dynamique.

## 📦 Fonctionnalités

- Chargement automatique de fichiers JSON de traduction.
- Détection automatique de la langue du système.
- Fallback intelligent vers des langues plus générales (ex: `fr-CA` → `fr` → `en`).
- Support des clés hiérarchiques via la notation `dot.key`.
- Formatage des chaînes avec `str.format()`.
- Gestion personnalisée des clés manquantes.
- Thread-safe pour une utilisation dans des environnements multi-threads.

## 🛠 Installation

Pour installer PyLyglot, utilisez pip :

```bash
pip install pylyglot
```

Ou ajoutez-le directement à votre `pyproject.toml` si vous utilisez Poetry :

```toml
[tool.poetry.dependencies]
pylyglot = "^1.0.0"
```

## 📁 Structure des fichiers

Les fichiers de langue doivent être placés dans un répertoire `lang/` à la racine de votre projet. Voici un exemple de structure :

```plaintext
lang/
├── en.json
├── fr.json
```

### Exemple de fichier de langue

Voici un exemple de fichier `en.json` :

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

### Initialisation

Pour initialiser PyLyglot, créez une instance de la classe `PyLyglot` :

```python
from pylyglot import PyLyglot

def missing_key_handler(key):
    return f"<<{key}>>"

pl = PyLyglot(missing_key_handler=missing_key_handler)
```

### Traduction de chaînes

Vous pouvez traduire des chaînes en utilisant des clés simples ou hiérarchiques :

```python
print(pl("menu.start"))  # Affiche "Start"
print(pl("menu.quit"))   # Affiche "Quit"
```

### Formatage des chaînes

PyLyglot supporte le formatage des chaînes avec `str.format()` :

```python
print(pl("welcome", username="Alice"))  # Affiche "Welcome, Alice!"
```

### Gestion des langues

Vous pouvez obtenir la liste des langues disponibles et changer la langue courante :

```python
print("Available languages:", pl.get_available_languages())

pl.set_language("fr")
print(pl("menu.start"))  # Affiche "Démarrer" si la traduction existe
```

### Métadonnées

Vous pouvez accéder aux métadonnées des fichiers de langue :

```python
print(pl.get_metadata("en"))
```

## 🔧 Configuration avancée

### Répertoire des langues personnalisé

Vous pouvez spécifier un répertoire personnalisé pour les fichiers de langue :

```python
from pathlib import Path

custom_lang_dir = Path("/chemin/vers/vos/fichiers/de/langue")
pl = PyLyglot(lang_dir=custom_lang_dir)
```

### Gestion des clés manquantes

Vous pouvez personnaliser la gestion des clés manquantes en fournissant une fonction de rappel :

```python
def custom_missing_key_handler(key):
    return f"Missing: {key}"

pl = PyLyglot(missing_key_handler=custom_missing_key_handler)
```

## 📂 Exemple de projet

Voici un exemple de structure de projet utilisant PyLyglot :

```plaintext
my_project/
├── lang/
│   ├── en.json
│   ├── fr.json
├── main.py
```

Dans `main.py` :

```python
from pylyglot import PyLyglot

def missing_key_handler(key):
    return f"<<{key}>>"

pl = PyLyglot(missing_key_handler=missing_key_handler)

print(pl("menu.start"))  # Affiche "Start"
print(pl("menu.quit"))   # Affiche "Quit"
print(pl("welcome", username="Bob"))  # Affiche "Welcome, Bob!"
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer à PyLyglot, suivez ces étapes :

1. Fork le projet.
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`).
3. Commitez vos changements (`git commit -m 'Add some AmazingFeature'`).
4. Poussez vers la branche (`git push origin feature/AmazingFeature`).
5. Ouvrez une Pull Request.

## 📄 Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.
```
