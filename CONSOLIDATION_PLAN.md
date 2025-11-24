## CCSS Ops – Projet unique à consolider

### Dossiers retenus comme sources de vérité
- `backendfinal/` : unique backend Flask (API + modèles). À utiliser pour toute évolution serveur.
- `frontendfinal/` : unique frontend React/Vite. À utiliser pour toute évolution UI.
- Racine : documents partagés (`data.md`, `SETUP_GUIDE.md`, `START_SERVERS.md`, etc.) décrivent la vision fonctionnelle et servent aux deux sous-projets.

> Les anciens dossiers (`backend/`, `frontend/`, `API's/`, etc.) sont conservés **uniquement** comme archives. Ne plus y ajouter de code ni baser les builds dessus.

### Alignement avec `data.md`
`data.md` contient la définition canonique des 15 entités (User, Agent, Client, …, Notification).  
Actions à mener pour garantir l’unicité du modèle :
1. **Backend** (`backendfinal/app/models.py`)
   - Étendre les modèles SQLAlchemy pour inclure l’intégralité des attributs documentés.
   - Réviser les routes/API pour accepter ces champs (CRUD + filtres).
   - Couvrir les nouvelles tables (Shift, Leave, Invoice, Incident, etc.) avec leurs blueprints.
2. **Frontend** (`frontendfinal/src`)
   - Centraliser les types (p.ex. `src/lib/types.ts`) reflétant `data.md`.
   - Adapter les pages & formulaires pour consommer/afficher les nouveaux champs.
   - Garder `src/lib/api.ts` en phase avec les endpoints réellement exposés par le backend.

### Étapes de consolidation proposées
1. **Archiver ou supprimer du build** les anciens dossiers pour éviter les confusions (ex.: ajouter une note dans `README.md` ou déplacer vers `archive/`).
2. **Mettre à jour la documentation** (README/SETUP_GUIDE) pour pointer uniquement vers `backendfinal` et `frontendfinal`.
3. **Synchroniser les dépendances** : s’assurer que les guides d’installation utilisent les requirements/package.json des dossiers `*final`.
4. **Vérifier les scripts de lancement** (`START_SERVERS.md`) afin qu’ils ciblent exclusivement les dossiers finaux.
5. **Mettre en place un contrôle automatique** (script ou tâche CI) qui échoue si quelqu’un modifie les anciens dossiers.

### Prochaines actions recommandées
- Décider si les dossiers historiques doivent être purement supprimés ou déplacés dans `archive/`.
- Prioriser l’implémentation des entités critiques (User/Agent/Client/Site/Shift/Attendance/Payroll) pour assurer la cohérence avec `data.md`.
- Définir une feuille de route pour l’enrichissement progressif du frontend (nouveaux écrans, validations supplémentaires, etc.).

