# 🚀 Plan d'Implémentation Itérative - BuyBuddy

## 🎯 Approche Progressive

**Principe :** Implémenter étape par étape, tester à chaque étape, voir des résultats concrets avant de continuer.

Chaque étape produit un résultat testable et fonctionnel.

---

## 📋 Roadmap Itérative

### ✅ Milestone 0 : Setup Minimal (30 min)

**Objectif :** Avoir un backend qui démarre et répond

**Résultat attendu :**

- Backend FastAPI démarre
- Endpoint `/health` répond OK
- Pas d'erreurs

**Validation :**

```bash
curl http://localhost:8000/health
# Devrait retourner: {"status": "ok"}
```

---

### ✅ Milestone 1 : Recherche Simple (2-3h)

**Objectif :** Rechercher des produits via SerperDev API

**API choisie :**
1. ✅ **SerperDev** (✅ configuré et fonctionnel)
   - Produits avec prix
   - Images présentes
   - Rapide et fiable
   - 2500 requêtes/mois gratuites

**Stratégie :**
- Utiliser SerperDev pour les produits avec prix
- Simple, rapide et efficace

**Résultat attendu :**

- Endpoint `/api/v1/search` fonctionne
- Recherche "laptop gaming" retourne des produits avec prix
- Affichage JSON avec produits (nom, prix, lien, image)

**Validation :**

```bash
# Test recherche
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "laptop gaming"}'
```

**Fichiers créés :**

- ✅ `backend/app/core/config.py`
- ✅ `backend/app/infrastructure/external_apis/serperdev_client.py`
- ✅ `backend/app/api/v1/endpoints/search.py`

**Configuration requise :**

1. **SerperDev** : ✅ `SERPER_API_KEY` dans `.env` (configuré)
   - 2500 requêtes/mois gratuites
   - Produits avec prix structurés

**Pas encore besoin de :**

- Agents CrewAI
- LangGraph
- Ollama
- RAG

---

### ⏸️ Milestone 2 : Frontend Basique (Reporté)

**Note :** Le frontend React sera implémenté à la fin du projet. On se concentre d'abord sur le backend et l'intelligence des agents.

---

### ✅ Milestone 3 : Ollama + Un Agent Simple (2h)

**Objectif :** Utiliser Ollama pour comprendre la requête utilisateur

**Résultat attendu :**

- Agent "Query Understanding" avec Ollama
- Endpoint `/api/v1/chat` prend une requête
- Retourne requête structurée (type produit, budget, etc.)

**Validation :**

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Je veux un laptop gaming sous 1500€"}'
# Devrait retourner: {"product_type": "laptop", "category": "gaming", "max_price": 1500}
```

**Fichiers à créer :**

- `backend/app/infrastructure/external_apis/ollama_client.py`
- `backend/app/agents/query_understanding.py` (1 agent simple)
- Modification endpoint pour utiliser l'agent

**Amélioration visible :**

- Compréhension intelligente des requêtes
- Extraction automatique budget, type produit

---

### ✅ Milestone 4 : Agent Product Researcher (2h)

**Objectif :** Agent qui recherche des produits avec SerperDev

**Résultat attendu :**

- Agent Product Researcher utilise SerperDev
- Retourne produits structurés
- Endpoint `/api/v1/chat` retourne produits

**Validation :**

- Même test que Milestone 3
- Mais maintenant avec produits réels retournés

**Fichiers à créer :**

- `backend/app/agents/product_researcher.py`
- Modification workflow pour utiliser 2 agents

**Amélioration visible :**

- Recherche intelligente (agent comprend mieux la requête)
- Résultats plus pertinents

---

### ✅ Milestone 5 : Frontend ProductCard (1h)

**Objectif :** Afficher produits joliment avec liens cliquables

**Résultat attendu :**

- ProductCard component joli
- Images produits
- Liens cliquables "Acheter"
- Layout responsive

**Validation :**

- Interface jolie
- Clic sur lien → ouvre site e-commerce

**Fichiers à créer :**

- `frontend/src/components/ProductCard.jsx`
- Styling (CSS ou Tailwind)

**Amélioration visible :**

- Interface professionnelle
- UX meilleure

---

### ✅ Milestone 6 : LangGraph Workflow Simple (3h)

**Objectif :** Workflow LangGraph avec 2 nodes (understand → research)

**Résultat attendu :**

- Workflow LangGraph fonctionne
- 2 nodes : understand_query → research_products
- Même résultat mais avec workflow orchestré

**Validation :**

- Teste endpoint `/api/v1/chat`
- Vérifie logs : workflow s'exécute étape par étape

**Fichiers à créer :**

- `backend/app/workflows/shopping_workflow.py` (simple)
- `backend/app/workflows/state.py`
- `backend/app/workflows/nodes.py` (2 nodes)

**Amélioration visible :**

- Architecture plus propre
- Facile d'ajouter étapes

---

### ✅ Milestone 7 : Recherches Itératives (2h) ✅ **TERMINÉ**

**Objectif :** Si utilisateur dit "je n'aime pas", refaire recherche

**Résultat attendu :**

- ✅ Endpoint accepte feedback : `{"message": "je n'aime pas"}`
- ✅ Nouvelle recherche automatique
- ✅ Exclut produits précédents
- ✅ Gestion de sessions (en mémoire)

**Validation :**

```bash
# Première recherche
curl -X POST ... -d '{"message": "laptop gaming"}'
# Réponse avec produits + session_id

# Feedback négatif
curl -X POST ... -d '{"message": "je n'aime pas", "session_id": "xxx"}'
# Nouvelle recherche avec autres produits (exclut les précédents)
```

**Fichiers créés/modifiés :**

- ✅ `backend/app/workflows/nodes.py` (ajouté node check_feedback)
- ✅ `backend/app/workflows/shopping_workflow.py` (ajouté boucle conditionnelle)
- ✅ `backend/app/workflows/session_manager.py` (nouveau : gestion sessions)
- ✅ `backend/app/workflows/state.py` (ajouté session_id, excluded_links, is_negative_feedback)
- ✅ `backend/app/models/schemas.py` (ajouté session_id dans ChatRequest et ChatResponse)

**Amélioration visible :**

- ✅ Recherches itératives fonctionnelles
- ✅ UX améliorée (utilisateur peut refaire recherche)
- ✅ Détection automatique de feedback négatif

---

### ✅ Milestone 8 : Price Comparator Agent (2h) ✅ **TERMINÉ**

**Objectif :** Agent qui compare les prix entre sites

**Résultat attendu :**

- ✅ Price Comparator Agent analyse produits
- ✅ Identifie meilleur prix
- ✅ Retourne recommandation "Meilleur prix : ..."
- ✅ Comparaison automatique des prix entre plateformes

**Validation :**

- ✅ Résultats incluent comparaison prix dans `price_comparison`
- ✅ Identifie clairement le meilleur prix
- ✅ Calcule écart de prix et pourcentage

**Fichiers créés/modifiés :**

- ✅ `backend/app/agents/price_comparator.py` (nouveau)
- ✅ `backend/app/workflows/nodes.py` (ajouté `compare_prices_node`)
- ✅ `backend/app/workflows/shopping_workflow.py` (ajouté node dans workflow)
- ✅ `backend/app/workflows/state.py` (ajouté `price_comparison`)
- ✅ `backend/app/models/schemas.py` (ajouté `price_comparison` dans ChatResponse)
- ✅ `backend/app/api/v1/endpoints/chat.py` (retourne comparaison)

**Amélioration visible :**

- Comparaison automatique des prix
- Recommandation meilleur prix

---

### ✅ Milestone 9 : Chat Interface Frontend (2h) ✅ **TERMINÉ**

**Objectif :** Interface chat conversationnelle complète avec design moderne

**Résultat attendu :**

- ✅ Chat avec historique messages
- ✅ Bouton "Je n'aime pas" pour recherches itératives
- ✅ Affichage produits dans chat avec cartes
- ✅ Comparaison de prix affichée
- ✅ Design moderne style ChatGPT

**Validation :**

- ✅ Conversation fluide
- ✅ Bouton "Je n'aime pas" fonctionne
- ✅ Interface responsive et moderne
- ✅ Affichage produits avec images et prix

**Fichiers créés :**

- ✅ `frontend/package.json` (setup React + Vite + Tailwind)
- ✅ `frontend/vite.config.js` (configuration Vite)
- ✅ `frontend/tailwind.config.js` (configuration Tailwind)
- ✅ `frontend/src/components/ChatInterface.jsx` (interface principale)
- ✅ `frontend/src/components/MessageBubble.jsx` (bulles de message)
- ✅ `frontend/src/components/ProductCard.jsx` (cartes produits)
- ✅ `frontend/src/components/PriceComparison.jsx` (comparaison prix)
- ✅ `frontend/src/hooks/useChat.js` (hook pour chat)
- ✅ `frontend/src/App.jsx` (composant principal)

**Amélioration visible :**

- ✅ Interface conversationnelle moderne
- ✅ UX professionnelle style ChatGPT
- ✅ Design responsive et élégant

---

### ✅ Milestone 10 : SQLite + Historique (2h) ✅ **TERMINÉ**

**Objectif :** Sauvegarder conversations et produits en SQLite

**Résultat attendu :**

- ✅ Conversations sauvegardées
- ✅ Historique accessible via API
- ✅ Cache produits

**Validation :**

- ✅ Relancer recherche → retrouve historique
- ✅ Voir DB avec DB Browser (data/buybuddy.db)
- ✅ Endpoints `/api/v1/history/conversations` et `/api/v1/history/searches`

**Fichiers créés :**

- ✅ `backend/app/core/database.py` (SQLite setup et tables)
- ✅ `backend/app/infrastructure/repositories/sqlite_repository.py` (Repository pattern)
- ✅ `backend/app/api/v1/endpoints/history.py` (Endpoints historique)
- ✅ `backend/app/core/config.py` (ajout database_dir)

**Intégration :**

- ✅ `ShoppingWorkflow` sauvegarde automatiquement conversations, recherches et produits
- ✅ Tables créées : `conversations`, `products`, `searches`
- ✅ Indexes pour performance
- ✅ Repository pattern pour abstraction

**Amélioration visible :**

- ✅ Historique persiste après redémarrage
- ✅ Pas de perte de données
- ✅ Cache produits pour éviter requêtes API redondantes

---

### ✅ Milestone 11 : RAG Basique (3h)

**Objectif :** ChromaDB + indexation avis simples

**Résultat attendu :**

- Avis produits indexés dans ChromaDB
- Recherche sémantique avis fonctionne
- Retourne avis pertinents

**Validation :**

- Indexer quelques avis
- Rechercher → retourne avis pertinents

**Fichiers à créer :**

- `backend/app/rag/vector_store.py`
- `backend/app/rag/indexer.py`
- `backend/app/rag/retriever.py`

**Amélioration visible :**

- RAG fonctionne
- Recherche sémantique avis

---

### ✅ Milestone 12 : Review Analyzer Agent (2h)

**Objectif :** Agent qui analyse avis avec RAG

**Résultat attendu :**

- Review Analyzer Agent utilise RAG
- Analyse sentiment
- Extrait pros/cons

**Validation :**

- Résultats incluent analyse avis
- Pros/cons extraits

**Fichiers à créer :**

- `backend/app/agents/review_analyzer.py`
- Ajouter node dans workflow

**Amélioration visible :**

- Analyse intelligente des avis
- Insights utiles

---

### ✅ Milestone 13 : Recommendation Agent (2h)

**Objectif :** Agent final qui synthétise tout

**Résultat attendu :**

- Recommendation Agent combine tout
- Recommandation personnalisée finale
- Justification claire

**Validation :**

- Recommandation finale cohérente
- Justifie pourquoi ce produit

**Fichiers à créer :**

- `backend/app/agents/recommender.py`
- Ajouter node dans workflow

**Amélioration visible :**

- Recommandations intelligentes
- Expérience complète

---

### ✅ Milestone 14 : Polish & Tests (3h)

**Objectif :** Améliorer, tester, documenter

**Résultat attendu :**

- Tests unitaires basiques
- Documentation API
- README complet
- Code propre

**Validation :**

- Tests passent
- Documentation à jour

---

## 📊 Résumé des Milestones

| Milestone | Durée | Résultat Testable     | Amélioration Visible          |
| --------- | ------ | ---------------------- | ------------------------------ |
| 0         | 30min  | Backend démarre       | ✅ Backend fonctionne          |
| 1         | 1-2h   | Recherche produits     | ✅ Recherche fonctionne        |
| 2         | 1h     | Interface simple       | ✅ Interface visible           |
| 3         | 2h     | Agent comprendre       | ✅ Compréhension intelligente |
| 4         | 2h     | Agent recherche        | ✅ Recherche intelligente      |
| 5         | 1h     | ProductCard joli       | ✅ Interface jolie             |
| 6         | 3h     | Workflow LangGraph     | ✅ Architecture propre         |
| 7         | 2h     | Recherches itératives | ✅ UX améliorée              |
| 8         | 2h     | Comparaison prix       | ✅ Comparaison auto            |
| 9         | 2h     | Chat complet           | ✅ Chat professionnel          |
| 10        | 2h     | Historique SQLite      | ✅ Historique persiste         |
| 11        | 3h     | RAG basique            | ✅ RAG fonctionne              |
| 12        | 2h     | Analyse avis           | ✅ Analyse intelligente        |
| 13        | 2h     | Recommandations        | ✅ Recommandations finales     |
| 14        | 3h     | Polish & Tests         | ✅ Projet complet              |

**Total : ~28h de développement** (réparti sur plusieurs jours)

---

## 🎯 Stratégie de Développement

### Principe : MVP Progressif

1. **Milestone 0-2** : MVP minimal fonctionnel (recherche basique)
2. **Milestone 3-5** : Ajout intelligence (agents, UI)
3. **Milestone 6-7** : Architecture workflow (LangGraph)
4. **Milestone 8-10** : Features avancées (comparaison, chat, historique)
5. **Milestone 11-13** : AI avancé (RAG, analyse, recommandations)
6. **Milestone 14** : Finalisation

### À chaque milestone :

1. ✅ Implémenter uniquement ce milestone
2. ✅ Tester immédiatement
3. ✅ Voir résultat concret
4. ✅ Valider que ça marche
5. ✅ Commit Git
6. ✅ Passer au suivant

### Si ça ne marche pas :

- **Ne pas continuer**
- **Debugger jusqu'à ce que ça marche**
- **Voir résultat avant de continuer**

---

## 🚀 Commencer Maintenant

### Milestone 0 : Setup Minimal (30 min)

**Objectif :** Backend qui démarre

**Fichiers à créer :**

1. `backend/requirements.txt` (minimal)

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.2
python-dotenv==1.0.0
```

2. `backend/app/core/config.py`

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
  
    class Config:
        env_file = ".env"

settings = Settings()
```

3. `backend/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="BuyBuddy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok", "message": "BuyBuddy API is running"}
```

4. Lancer :

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

5. Tester :

```bash
curl http://localhost:8000/health
# Devrait retourner: {"status": "ok", "message": "BuyBuddy API is running"}
```

**✅ Si ça marche → Milestone 0 terminé !**

**📝 Commit Git :**

```bash
git add .
git commit -m "Milestone 0: Backend setup minimal"
```

**➡️ Passer au Milestone 1**

---

## 📝 Checklist Globale

- [ ] Milestone 0 : Backend démarre
- [ ] Milestone 1 : Recherche produits
- [ ] Milestone 2 : Frontend basique
- [ ] Milestone 3 : Agent comprendre
- [ ] Milestone 4 : Agent recherche
- [ ] Milestone 5 : ProductCard
- [ ] Milestone 6 : Workflow LangGraph
- [ ] Milestone 7 : Recherches itératives
- [ ] Milestone 8 : Comparaison prix
- [ ] Milestone 9 : Chat interface
- [ ] Milestone 10 : Historique SQLite
- [ ] Milestone 11 : RAG basique
- [ ] Milestone 12 : Analyse avis
- [ ] Milestone 13 : Recommandations
- [ ] Milestone 14 : Polish & Tests

---

**🎯 Approche : Un milestone à la fois, tester, valider, continuer !**
