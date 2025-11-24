## Plan Projet – CCSS Ops

### Phase 0 – Préparation
- [x] Audit structure, choix `backendfinal/` & `frontendfinal/`.
- [x] Archivage des anciens dossiers (`archive/backend`, `archive/frontend`).
- [x] Cahier des charges (voir `CAHIER_DES_CHARGES.md`).

### Phase 1 – Backend (Flask)
1. **Modèles & migrations**
   - Étendre `app/models.py` avec toutes les entités de `data.md`.
   - Créer migrations/alembic si nécessaire (sinon `db.create_all` pour dev).
2. **Routes/Blueprints**
   - Auth enrichi (rôles/permissions, 2FA, audit).
   - CRUD + filtres : Agents, Clients, Sites, Shifts, Attendances, Corrections, Payrolls, Leaves, Incidents, Invoices, Equipment, Training, Documents, Notifications.
   - Endpoints spécifiques : génération planning, approbations, calcul paie, envoi notifications.
3. **Business logic**
   - Calcul heures, déclencheurs Attendance/Payroll.
   - Limitation opérateur (une modification par shift) avec verrous en base.
   - Scripts seed (admin, opérateurs, agents, planning exemple).
4. **Tests**
   - Unitaires sur modèles/services.
   - Tests API (auth, planning, corrections, paie).

### Phase 2 – Frontend (React/Vite)
1. **Fondations**
   - Types partagés (`src/lib/types.ts`), hooks API, gestion auth/roles.
   - Layout dashboard, navigation, états chargement/erreur.
2. **Modules existants**
   - Mettre à jour Agents/Clients/Sites/Attendance/Corrections/Payrolls pour supporter les champs étendus.
3. **Nouveaux modules**
   - Planning/Shifts : tableau hebdo/mensuel, filtres, actions opérateur/admin, historique modifications.
   - Leaves, Incidents, Invoices, Equipment, Training, Documents, Notifications.
   - Paramètres (ex. configuration rôles, SLA, etc.).
4. **UX & validations**
   - Formulaires avec validations avancées (dates, montants, fichiers).
   - Composants réutilisables (badges statuts, timeline, modales).
5. **Tests**
   - Tests unitaires (hooks, utils) + tests e2e critiques (auth, planning, correction).

### Phase 3 – Documentation & Livraison
- Mettre à jour `README.md`, `SETUP_GUIDE.md`, `START_SERVERS.md`, `IMPLEMENTATION_STATUS.md`.
- Ajouter manuel utilisateur rapide (opérateur/admin).
- Checklist de déploiement (env vars, migrations, seeds).
- CI/CD : lint, tests, build, blocage si anciens dossiers modifiés.

### Jalons & priorités
1. **M1** – Backend complet (modèles/endpoints/tests de base).
2. **M2** – Frontend modules principaux (Agents→Payroll) + Planning opérateur.
3. **M3** – Modules avancés (Incidents, Leaves, Invoices, etc.) + notifications.
4. **M4** – Documentation, seeds, QA finale, mise en production.

### Risques & atténuation
- **Complexité modèle** : démarrer par noyau (User/Agent/Site/Shift/Attendance/Payroll) puis itérer.
- **Règles opérateur/admin** : définir clairement les scénarios, créer tests d’intégration.
- **Charge front** : réutiliser composants, prévoir design system simple.
- **Données sensibles** : chiffrer, limiter téléchargements, ajouter audits.

### Suivi
- Utiliser issues/tickets par entité ou fonctionnalité.
- Mettre à jour `IMPLEMENTATION_STATUS.md` à chaque jalon.
- Revue code systématique pour chaque PR majeure.

