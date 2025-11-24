## Cahier des Charges – CCSS Ops

### 1. Contexte
Plateforme web destinée aux opérations d'une société de sécurité privée. Objectifs principaux : gestion des agents, clients, sites, plannings, présences, paie et documents, avec workflow complet entre opérateurs et administrateurs.

### 2. Périmètre fonctionnel
1. **Gestion des utilisateurs**
   - Rôles : `admin`, `operator`, `manager`, `supervisor`, `hr`, `finance`.
   - Authentification JWT, 2FA optionnelle, permissions fines.
2. **Agents**
   - Fiches détaillées (identité, contrats, finance, licences, équipement, formations, santé).
   - Historique d’affectation, documents associés, équipements attribués.
3. **Clients & Sites**
   - Contrats, SLA, contacts, conditions financières, exigences par site.
4. **Plannings / Shifts**
   - Grille fixe par site/poste (jour, nuit, swing, etc.).
   - Assignation agents↔sites↔dates, génération automatique, duplication, règles anti-conflits.
5. **Présences & Corrections**
   - Horodatage, GPS, preuves photo, calcul automatique heures, workflow correction.
6. **Paie**
   - Calculs réguliers/heure sup/nuit/jours fériés, primes/déductions, validations multi-rôle, export bulletin.
7. **Congés**
   - Demandes, pièces jointes, validation, prise en compte planning.
8. **Incidents & Documents**
   - Rapports incidents, suivi résolutions, stockage documents (agents/clients/sites/company).
9. **Facturation**
   - Invoices par client/site, lignes détaillées, paiements, relances.
10. **Équipement & Formations**
    - Inventaire équipement, attribution, suivi retours; formations, expirations, certificats.
11. **Notifications**
    - Avertissements planification, documents expirants, corrections, incidents, paie.

### 3. Exigences spécifiques opérateurs
- Lecture complète des données agents/sites/plannings.
- Possibilité d’effectuer **une seule modification par shift** (ex : changer l’agent ou l’horaire). Toute modification supplémentaire doit être validée/envoyée à un admin.
- Traçabilité des changements (qui, quand, pourquoi) accessible aux admins.

### 4. Exigences techniques
- **Backend** : Flask 3 + SQLAlchemy, base PostgreSQL/SQLite, JWT, CORS, architecture REST.
- **Frontend** : React + TypeScript + Vite, design responsive, état global sécurisé, composants modulaires.
- **Documentation** : data model (`data.md`), guides d’installation, cahier des charges (ce fichier), plan projet.
- **Tests** : couverture API + validations UI critiques (auth, planning, paie).
- **Déploiement** : environnements dev/staging/prod, scripts start/seed, CI pour lint/tests + détection modifications dossiers archivés.

### 5. Contraintes & non-fonctionnel
- Sécurité : chiffrement mots de passe, champs sensibles (ex : documents, licences, alarm codes), audit logs.
- Performance : endpoints filtrables, pagination, index DB (cf. recommandations `data.md`).
- UX : latence faible, états de chargement, messages d’erreur clairs, accessibilité, dark mode optionnel.
- Localisation : interface FR/EN (prévoir mécanisme d’i18n).

### 6. Livrables
- Backend ajusté (`backendfinal/`) avec toutes entités, endpoints, tests.
- Frontend ajusté (`frontendfinal/`) couvrant l’intégralité des workflows.
- Données d’exemple + scripts (planning type, agents, clients).
- Documentation complète (guides, plan projet, manuel utilisateur si nécessaire).

