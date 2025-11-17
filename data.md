
📊 ENTITÉS & ATTRIBUTS DÉTAILLÉS
1. USER (Utilisateurs Système) 👤
Description : Personnel administratif qui accède au système
sqlUSER
├── user_id (PK, INT, AUTO_INCREMENT)
├── email (VARCHAR(255), UNIQUE, NOT NULL)
├── password_hash (VARCHAR(255), NOT NULL)
├── first_name (VARCHAR(100), NOT NULL)
├── last_name (VARCHAR(100), NOT NULL)
├── phone (VARCHAR(20))
├── role (ENUM: 'admin', 'manager', 'supervisor', 'hr', 'finance')
├── is_active (BOOLEAN, DEFAULT TRUE)
├── last_login (DATETIME)
├── created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
├── updated_at (TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP)
└── created_by (FK -> USER.user_id)
Attributs Recommandés Supplémentaires :

profile_picture (VARCHAR(255)) - URL photo
department (VARCHAR(100)) - RH, Finance, Opérations
permissions (JSON) - Permissions granulaires
two_factor_enabled (BOOLEAN) - Sécurité 2FA
password_reset_token (VARCHAR(255))
password_reset_expires (DATETIME)


2. AGENT (Agents de Sécurité) 🛡️
Description : Personnel de sécurité déployé sur les sites
sqlAGENT
├── agent_id (PK, INT, AUTO_INCREMENT)
├── employee_code (VARCHAR(20), UNIQUE, NOT NULL)
├── first_name (VARCHAR(100), NOT NULL)
├── last_name (VARCHAR(100), NOT NULL)
├── date_of_birth (DATE, NOT NULL)
├── gender (ENUM: 'M', 'F', 'Other')
├── national_id (VARCHAR(50), UNIQUE)
├── phone_primary (VARCHAR(20), NOT NULL)
├── phone_secondary (VARCHAR(20))
├── email (VARCHAR(255))
├── address (TEXT)
├── city (VARCHAR(100))
├── postal_code (VARCHAR(10))
├── emergency_contact_name (VARCHAR(100))
├── emergency_contact_phone (VARCHAR(20))
├── emergency_contact_relationship (VARCHAR(50))
│
├── hire_date (DATE, NOT NULL)
├── contract_type (ENUM: 'permanent', 'temporary', 'contract')
├── contract_end_date (DATE) - Si temporaire
├── employment_status (ENUM: 'active', 'suspended', 'terminated', 'on_leave')
├── termination_date (DATE)
├── termination_reason (TEXT)
│
├── hourly_rate (DECIMAL(10,2))
├── bank_name (VARCHAR(100))
├── bank_account_number (VARCHAR(50))
├── tax_id (VARCHAR(50))
│
├── uniform_size (VARCHAR(10))
├── badge_number (VARCHAR(20), UNIQUE)
├── security_clearance_level (INT) - 1-5
├── has_firearm_license (BOOLEAN)
├── firearm_license_number (VARCHAR(50))
├── firearm_license_expiry (DATE)
│
├── profile_photo (VARCHAR(255))
├── notes (TEXT)
├── is_active (BOOLEAN, DEFAULT TRUE)
├── created_at (TIMESTAMP)
├── updated_at (TIMESTAMP)
└── created_by (FK -> USER.user_id)
Attributs Critiques Supplémentaires :

blood_type (VARCHAR(5)) - Urgences médicales
has_drivers_license (BOOLEAN)
drivers_license_number (VARCHAR(50))
languages_spoken (JSON) - ['French', 'English', 'Creole']
medical_conditions (TEXT, ENCRYPTED) - Allergies, conditions
training_level (VARCHAR(50)) - 'Basic', 'Advanced', 'Specialized'


3. CLIENT (Entreprises Clientes) 🏢
Description : Organisations qui contractent vos services
sqlCLIENT
├── client_id (PK, INT, AUTO_INCREMENT)
├── company_name (VARCHAR(255), NOT NULL)
├── company_registration_number (VARCHAR(50), UNIQUE)
├── tax_id (VARCHAR(50))
├── industry_sector (VARCHAR(100))
│
├── primary_contact_name (VARCHAR(100), NOT NULL)
├── primary_contact_title (VARCHAR(100))
├── primary_contact_phone (VARCHAR(20), NOT NULL)
├── primary_contact_email (VARCHAR(255), NOT NULL)
│
├── billing_contact_name (VARCHAR(100))
├── billing_contact_phone (VARCHAR(20))
├── billing_contact_email (VARCHAR(255))
│
├── address (TEXT, NOT NULL)
├── city (VARCHAR(100), NOT NULL)
├── postal_code (VARCHAR(10))
├── country (VARCHAR(100), DEFAULT 'Haiti')
│
├── contract_start_date (DATE, NOT NULL)
├── contract_end_date (DATE)
├── contract_status (ENUM: 'active', 'pending', 'suspended', 'terminated')
├── payment_terms (ENUM: '15_days', '30_days', '45_days', '60_days')
├── billing_frequency (ENUM: 'weekly', 'bi-weekly', 'monthly')
├── billing_day (INT) - Jour du mois (1-31)
├── currency (VARCHAR(3), DEFAULT 'HTG')
│
├── credit_limit (DECIMAL(12,2))
├── current_balance (DECIMAL(12,2), DEFAULT 0)
├── total_invoiced (DECIMAL(12,2), DEFAULT 0)
├── total_paid (DECIMAL(12,2), DEFAULT 0)
│
├── service_level_agreement (TEXT) - SLA détails
├── special_requirements (TEXT)
├── logo_url (VARCHAR(255))
├── website (VARCHAR(255))
├── notes (TEXT)
│
├── is_active (BOOLEAN, DEFAULT TRUE)
├── created_at (TIMESTAMP)
├── updated_at (TIMESTAMP)
└── created_by (FK -> USER.user_id)
Attributs Recommandés :

discount_percentage (DECIMAL(5,2)) - Remises volume
requires_background_check (BOOLEAN)
requires_drug_testing (BOOLEAN)
insurance_certificate_required (BOOLEAN)
preferred_communication_method (ENUM: 'email', 'phone', 'sms', 'whatsapp')


4. SITE (Lieux de Travail) 📍
Description : Emplacements spécifiques où agents sont déployés
sqlSITE
├── site_id (PK, INT, AUTO_INCREMENT)
├── client_id (FK -> CLIENT.client_id, NOT NULL)
├── site_name (VARCHAR(255), NOT NULL)
├── site_code (VARCHAR(20), UNIQUE)
├── site_type (ENUM: 'office', 'warehouse', 'retail', 'residential', 
│              'industrial', 'event', 'construction', 'other')
│
├── address (TEXT, NOT NULL)
├── city (VARCHAR(100))
├── postal_code (VARCHAR(10))
├── gps_latitude (DECIMAL(10,8))
├── gps_longitude (DECIMAL(11,8))
├── geofence_radius_meters (INT, DEFAULT 100) - Pour check-in GPS
│
├── site_contact_name (VARCHAR(100))
├── site_contact_phone (VARCHAR(20))
├── site_contact_email (VARCHAR(255))
│
├── required_agents (INT, NOT NULL) - Nombre agents requis
├── shift_pattern (VARCHAR(50)) - '24/7', '8h-17h', 'rotating'
├── access_instructions (TEXT) - Comment accéder au site
├── emergency_procedures (TEXT)
├── special_equipment_required (TEXT) - Radio, torche, etc.
│
├── requires_armed_guard (BOOLEAN, DEFAULT FALSE)
├── requires_dog_unit (BOOLEAN, DEFAULT FALSE)
├── requires_vehicle (BOOLEAN, DEFAULT FALSE)
├── minimum_clearance_level (INT) - Niveau sécurité minimum
│
├── hourly_rate_override (DECIMAL(10,2)) - Si différent du standard
├── billing_rate (DECIMAL(10,2), NOT NULL) - Taux facturation client
│
├── contract_start_date (DATE)
├── contract_end_date (DATE)
├── site_status (ENUM: 'active', 'inactive', 'pending', 'closed')
│
├── site_photo (VARCHAR(255))
├── site_map (VARCHAR(255)) - Plan des lieux
├── notes (TEXT)
│
├── created_at (TIMESTAMP)
├── updated_at (TIMESTAMP)
└── created_by (FK -> USER.user_id)
Attributs Avancés :

patrol_checkpoints (JSON) - Points de ronde
restricted_areas (JSON) - Zones d'accès limité
key_holder_contacts (JSON) - Contacts urgence
alarm_code (VARCHAR(50), ENCRYPTED)
wifi_ssid (VARCHAR(100))
wifi_password (VARCHAR(100), ENCRYPTED)


5. SHIFT (Horaires/Quarts de Travail) 🕐
Nouvelle Entité Recommandée :
sqlSHIFT
├── shift_id (PK, INT, AUTO_INCREMENT)
├── site_id (FK -> SITE.site_id, NOT NULL)
├── agent_id (FK -> AGENT.agent_id, NOT NULL)
├── shift_date (DATE, NOT NULL)
├── shift_type (ENUM: 'day', 'night', 'swing', 'split')
├── scheduled_start_time (TIME, NOT NULL)
├── scheduled_end_time (TIME, NOT NULL)
├── scheduled_hours (DECIMAL(5,2)) - Calculé
│
├── shift_status (ENUM: 'scheduled', 'confirmed', 'in_progress', 
│                'completed', 'no_show', 'cancelled')
├── assigned_by (FK -> USER.user_id)
├── assigned_at (TIMESTAMP)
│
├── special_instructions (TEXT)
├── required_equipment (TEXT)
│
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

6. ATTENDANCE (Présence Réelle) ✅
Description : Enregistrement réel des heures travaillées
sqlATTENDANCE
├── attendance_id (PK, INT, AUTO_INCREMENT)
├── shift_id (FK -> SHIFT.shift_id, NOT NULL)
├── agent_id (FK -> AGENT.agent_id, NOT NULL)
├── site_id (FK -> SITE.site_id, NOT NULL)
├── attendance_date (DATE, NOT NULL)
│
├── clock_in_time (DATETIME)
├── clock_in_method (ENUM: 'gps', 'biometric', 'manual', 'qr_code', 'nfc')
├── clock_in_gps_lat (DECIMAL(10,8))
├── clock_in_gps_lng (DECIMAL(11,8))
├── clock_in_photo (VARCHAR(255)) - Selfie check-in
├── clock_in_verified (BOOLEAN, DEFAULT FALSE)
│
├── clock_out_time (DATETIME)
├── clock_out_method (ENUM: 'gps', 'biometric', 'manual', 'qr_code', 'nfc')
├── clock_out_gps_lat (DECIMAL(10,8))
├── clock_out_gps_lng (DECIMAL(11,8))
├── clock_out_photo (VARCHAR(255))
├── clock_out_verified (BOOLEAN, DEFAULT FALSE)
│
├── total_hours (DECIMAL(5,2)) - Calculé automatiquement
├── regular_hours (DECIMAL(5,2))
├── overtime_hours (DECIMAL(5,2))
├── night_shift_hours (DECIMAL(5,2)) - Si prime nuit
├── holiday_hours (DECIMAL(5,2)) - Si jour férié
│
├── break_start_time (DATETIME)
├── break_end_time (DATETIME)
├── total_break_minutes (INT)
│
├── attendance_status (ENUM: 'present', 'late', 'early_departure', 
│                      'absent', 'no_show', 'on_leave', 'sick')
├── is_late (BOOLEAN)
├── late_minutes (INT)
├── early_departure (BOOLEAN)
├── early_departure_minutes (INT)
│
├── incident_reported (BOOLEAN, DEFAULT FALSE)
├── incident_description (TEXT)
│
├── supervisor_notes (TEXT)
├── verified_by (FK -> USER.user_id)
├── verified_at (TIMESTAMP)
│
├── requires_correction (BOOLEAN, DEFAULT FALSE)
├── correction_reason (TEXT)
│
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
Attributs Importants :

device_id (VARCHAR(100)) - ID appareil check-in
ip_address (VARCHAR(45))
attendance_signature (VARCHAR(255)) - Signature digitale
weather_condition (VARCHAR(50)) - Si travail extérieur


7. CORRECTION (Corrections Présence) ✏️
Description : Demandes de correction d'heures
sqlCORRECTION
├── correction_id (PK, INT, AUTO_INCREMENT)
├── attendance_id (FK -> ATTENDANCE.attendance_id, NOT NULL)
├── agent_id (FK -> AGENT.agent_id, NOT NULL)
├── requested_by (FK -> USER.user_id) - Qui demande
│
├── correction_type (ENUM: 'missed_clock_in', 'missed_clock_out', 
│                    'wrong_time', 'wrong_site', 'system_error', 'other')
├── reason (TEXT, NOT NULL)
│
├── original_clock_in (DATETIME)
├── original_clock_out (DATETIME)
├── requested_clock_in (DATETIME)
├── requested_clock_out (DATETIME)
│
├── supporting_document (VARCHAR(255)) - Photo/PDF preuve
│
├── correction_status (ENUM: 'pending', 'approved', 'rejected', 'cancelled')
├── reviewed_by (FK -> USER.user_id)
├── review_notes (TEXT)
├── reviewed_at (TIMESTAMP)
│
├── applied_at (TIMESTAMP) - Quand correction appliquée
│
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
```

**Workflow Recommandé :**
```
Agent → Demande Correction
  ↓
Superviseur → Revoit Demande
  ↓
[Approuvé] → Mise à jour automatique ATTENDANCE
[Rejeté] → Notification agent avec raison

8. PAYROLL (Paie) 💰
Description : Calculs et paiements salaires
sqlPAYROLL
├── payroll_id (PK, INT, AUTO_INCREMENT)
├── agent_id (FK -> AGENT.agent_id, NOT NULL)
├── pay_period_start (DATE, NOT NULL)
├── pay_period_end (DATE, NOT NULL)
├── payment_date (DATE)
│
├── total_regular_hours (DECIMAL(7,2))
├── total_overtime_hours (DECIMAL(7,2))
├── total_night_shift_hours (DECIMAL(7,2))
├── total_holiday_hours (DECIMAL(7,2))
│
├── hourly_rate (DECIMAL(10,2))
├── overtime_rate (DECIMAL(10,2)) - Généralement 1.5x
├── night_shift_rate (DECIMAL(10,2))
├── holiday_rate (DECIMAL(10,2)) - Généralement 2x
│
├── gross_regular_pay (DECIMAL(12,2))
├── gross_overtime_pay (DECIMAL(12,2))
├── gross_night_shift_pay (DECIMAL(12,2))
├── gross_holiday_pay (DECIMAL(12,2))
├── gross_total (DECIMAL(12,2))
│
├── bonus_amount (DECIMAL(12,2), DEFAULT 0)
├── bonus_description (TEXT)
├── allowances (DECIMAL(12,2), DEFAULT 0) - Transport, repas
├── allowances_description (TEXT)
│
├── deduction_tax (DECIMAL(12,2), DEFAULT 0)
├── deduction_social_security (DECIMAL(12,2), DEFAULT 0)
├── deduction_insurance (DECIMAL(12,2), DEFAULT 0)
├── deduction_uniform (DECIMAL(12,2), DEFAULT 0)
├── deduction_loan (DECIMAL(12,2), DEFAULT 0)
├── deduction_other (DECIMAL(12,2), DEFAULT 0)
├── deduction_other_description (TEXT)
├── total_deductions (DECIMAL(12,2))
│
├── net_pay (DECIMAL(12,2)) - Salaire net à payer
│
├── payment_method (ENUM: 'bank_transfer', 'cash', 'check', 'mobile_money')
├── payment_reference (VARCHAR(100))
├── payment_status (ENUM: 'draft', 'approved', 'paid', 'cancelled')
│
├── approved_by (FK -> USER.user_id)
├── approved_at (TIMESTAMP)
├── paid_by (FK -> USER.user_id)
├── paid_at (TIMESTAMP)
│
├── payslip_generated (BOOLEAN, DEFAULT FALSE)
├── payslip_url (VARCHAR(255))
│
├── notes (TEXT)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
Formules Automatiques :
sqlgross_total = gross_regular_pay + gross_overtime_pay 
              + gross_night_shift_pay + gross_holiday_pay

net_pay = gross_total + bonus_amount + allowances - total_deductions
```

---

## 🔗 **RELATIONS ENTRE ENTITÉS**

### **Diagramme ERD (Entity Relationship Diagram)**
```
USER (1) ──creates──> (N) CLIENT
USER (1) ──creates──> (N) AGENT
USER (1) ──creates──> (N) SITE
USER (1) ──approves─> (N) CORRECTION
USER (1) ──approves─> (N) PAYROLL

CLIENT (1) ──has────> (N) SITE
CLIENT (1) ──has────> (N) INVOICE

SITE (1) ──requires─> (N) SHIFT
SITE (1) ──has──────> (N) ATTENDANCE

AGENT (1) ──assigned> (N) SHIFT
AGENT (1) ──records─> (N) ATTENDANCE
AGENT (1) ──requests> (N) CORRECTION
AGENT (1) ──receives> (N) PAYROLL

SHIFT (1) ──generates> (1) ATTENDANCE
SHIFT (N) ──part_of──> (1) SITE

ATTENDANCE (1) ──may_have─> (N) CORRECTION
ATTENDANCE (N) ──used_in──> (1) PAYROLL

CORRECTION (1) ──updates──> (1) ATTENDANCE

📋 TABLES SUPPLÉMENTAIRES RECOMMANDÉES
9. TRAINING (Formations) 📚
sqlTRAINING
├── training_id (PK)
├── training_name (VARCHAR(200))
├── training_type (ENUM: 'mandatory', 'optional', 'certification')
├── duration_hours (INT)
├── valid_for_months (INT) - Durée validité
├── description (TEXT)
└── created_at (TIMESTAMP)

AGENT_TRAINING
├── agent_training_id (PK)
├── agent_id (FK -> AGENT)
├── training_id (FK -> TRAINING)
├── completion_date (DATE)
├── expiry_date (DATE) - Auto-calculé
├── score (DECIMAL(5,2))
├── certificate_url (VARCHAR(255))
└── created_at (TIMESTAMP)
```

**Relations :**
```
AGENT (N) ──completes──> (N) TRAINING [via AGENT_TRAINING]

10. INCIDENT (Incidents/Rapports) 🚨
sqlINCIDENT
├── incident_id (PK)
├── site_id (FK -> SITE)
├── agent_id (FK -> AGENT) - Reporter
├── attendance_id (FK -> ATTENDANCE, NULL)
├── incident_date (DATETIME, NOT NULL)
├── incident_type (ENUM: 'theft', 'vandalism', 'trespassing', 
│                  'fire', 'medical', 'suspicious_activity', 
│                  'equipment_failure', 'other')
├── severity (ENUM: 'low', 'medium', 'high', 'critical')
├── description (TEXT, NOT NULL)
├── action_taken (TEXT)
├── police_notified (BOOLEAN)
├── police_report_number (VARCHAR(50))
├── client_notified (BOOLEAN)
├── client_notified_at (DATETIME)
├── witnesses (TEXT)
├── evidence_photos (JSON) - Array of URLs
├── incident_status (ENUM: 'open', 'investigating', 'resolved', 'closed')
├── resolved_by (FK -> USER)
├── resolved_at (TIMESTAMP)
├── resolution_notes (TEXT)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
```

**Relations :**
```
SITE (1) ──has───────> (N) INCIDENT
AGENT (1) ──reports──> (N) INCIDENT

11. INVOICE (Factures Clients) 💵
sqlINVOICE
├── invoice_id (PK)
├── client_id (FK -> CLIENT, NOT NULL)
├── invoice_number (VARCHAR(50), UNIQUE, NOT NULL)
├── invoice_date (DATE, NOT NULL)
├── due_date (DATE, NOT NULL)
├── billing_period_start (DATE)
├── billing_period_end (DATE)
│
├── subtotal (DECIMAL(12,2))
├── tax_rate (DECIMAL(5,2))
├── tax_amount (DECIMAL(12,2))
├── discount_percentage (DECIMAL(5,2))
├── discount_amount (DECIMAL(12,2))
├── total_amount (DECIMAL(12,2), NOT NULL)
│
├── invoice_status (ENUM: 'draft', 'sent', 'paid', 'partial', 
│                   'overdue', 'cancelled')
├── amount_paid (DECIMAL(12,2), DEFAULT 0)
├── balance_due (DECIMAL(12,2))
│
├── payment_terms (VARCHAR(50))
├── notes (TEXT)
├── invoice_pdf_url (VARCHAR(255))
│
├── sent_at (TIMESTAMP)
├── paid_at (TIMESTAMP)
├── created_by (FK -> USER)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

INVOICE_LINE_ITEM
├── line_item_id (PK)
├── invoice_id (FK -> INVOICE, NOT NULL)
├── site_id (FK -> SITE)
├── description (TEXT)
├── quantity (DECIMAL(10,2)) - Heures ou jours
├── unit_price (DECIMAL(10,2))
├── line_total (DECIMAL(12,2))
└── created_at (TIMESTAMP)
```

**Relations :**
```
CLIENT (1) ──receives──> (N) INVOICE
INVOICE (1) ──contains─> (N) INVOICE_LINE_ITEM
SITE (1) ──billed_via─> (N) INVOICE_LINE_ITEM

12. LEAVE (Congés) 🏖️
sqlLEAVE
├── leave_id (PK)
├── agent_id (FK -> AGENT, NOT NULL)
├── leave_type (ENUM: 'vacation', 'sick', 'personal', 'maternity',
│               'paternity', 'bereavement', 'unpaid', 'other')
├── start_date (DATE, NOT NULL)
├── end_date (DATE, NOT NULL)
├── total_days (INT) - Auto-calculé
├── reason (TEXT)
├── supporting_document (VARCHAR(255))
│
├── leave_status (ENUM: 'pending', 'approved', 'rejected', 'cancelled')
├── requested_at (TIMESTAMP)
├── reviewed_by (FK -> USER)
├── reviewed_at (TIMESTAMP)
├── review_notes (TEXT)
│
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
```

**Relations :**
```
AGENT (1) ──requests──> (N) LEAVE
USER (1) ──approves──> (N) LEAVE

13. EQUIPMENT (Équipement) 🔦
sqlEQUIPMENT
├── equipment_id (PK)
├── equipment_type (ENUM: 'uniform', 'radio', 'flashlight', 'weapon',
│                   'vehicle', 'phone', 'badge', 'other')
├── equipment_name (VARCHAR(200))
├── serial_number (VARCHAR(100), UNIQUE)
├── purchase_date (DATE)
├── purchase_cost (DECIMAL(10,2))
├── condition (ENUM: 'new', 'good', 'fair', 'poor', 'damaged')
├── status (ENUM: 'available', 'assigned', 'maintenance', 'retired')
├── notes (TEXT)
└── created_at (TIMESTAMP)

EQUIPMENT_ASSIGNMENT
├── assignment_id (PK)
├── equipment_id (FK -> EQUIPMENT, NOT NULL)
├── agent_id (FK -> AGENT, NOT NULL)
├── assigned_date (DATE, NOT NULL)
├── return_date (DATE)
├── assignment_status (ENUM: 'active', 'returned', 'lost', 'damaged')
├── return_condition (TEXT)
├── assigned_by (FK -> USER)
└── created_at (TIMESTAMP)
```

**Relations :**
```
AGENT (N) ──uses──────> (N) EQUIPMENT [via EQUIPMENT_ASSIGNMENT]

14. DOCUMENT (Documents) 📄
sqlDOCUMENT
├── document_id (PK)
├── document_type (ENUM: 'contract', 'id_card', 'certificate', 
│                  'license', 'medical', 'background_check', 'other')
├── entity_type (ENUM: 'agent', 'client', 'site', 'company')
├── entity_id (INT) - ID de l'entité liée
├── document_name (VARCHAR(255))
├── file_url (VARCHAR(255), NOT NULL)
├── file_size_kb (INT)
├── mime_type (VARCHAR(100))
├── issue_date (DATE)
├── expiry_date (DATE)
├── is_verified (BOOLEAN, DEFAULT FALSE)
├── verified_by (FK -> USER)
├── verified_at (TIMESTAMP)
├── uploaded_by (FK -> USER)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
```

**Relations :**
```
AGENT (1) ──has───────> (N) DOCUMENT
CLIENT (1) ──has──────> (N) DOCUMENT
SITE (1) ──has────────> (N) DOCUMENT

15. NOTIFICATION (Notifications) 🔔
sqlNOTIFICATION
├── notification_id (PK)
├── user_id (FK -> USER) - NULL si broadcast
├── agent_id (FK -> AGENT) - NULL si pour users
├── notification_type (ENUM: 'shift_reminder', 'payment_received',
│                      'correction_approved', 'document_expiring',
│                      'incident_reported', 'system', 'other')
├── title (VARCHAR(255))
├── message (TEXT)
├── priority (ENUM: 'low', 'normal', 'high', 'urgent')
├── is_read (BOOLEAN, DEFAULT FALSE)
├── read_at (TIMESTAMP)
├── action_url (VARCHAR(255)) - Lien à cliquer
├── created_at (TIMESTAMP)
└── expires_at (TIMESTAMP)
```

---

## 🔗 **RÉSUMÉ DES RELATIONS COMPLÈTES**
```
┌─────────────────────────────────────────────────────────────┐
│                    RELATIONS PRINCIPALES                     │
└─────────────────────────────────────────────────────────────┘

1. USER → CLIENT (1:N)
   - Un utilisateur crée plusieurs clients

2. CLIENT → SITE (1:N)
   - Un client possède plusieurs sites
   
3. SITE → SHIFT (1:N)
   - Un site a plusieurs quarts de travail

4. AGENT → SHIFT (1:N)
   - Un agent est assigné à plusieurs shifts

5. SHIFT → ATTENDANCE (1:1)
   - Un shift génère une présence

6. ATTENDANCE → CORRECTION (1:N)
   - Une présence peut avoir plusieurs corrections

7. AGENT → PAYROLL (1:N)
   - Un agent reçoit plusieurs paies

8. ATTENDANCE (N) → PAYROLL (1)
   - Plusieurs présences calculent une paie

9. SITE → INCIDENT (1:N)
   - Un site a plusieurs incidents

10. CLIENT → INVOICE (1:N)
    - Un client reçoit plusieurs factures

11. AGENT → LEAVE (1:N)
    - Un agent demande plusieurs congés

12. AGENT ←→ EQUIPMENT (N:N via EQUIPMENT_ASSIGNMENT)
    - Agents utilisent plusieurs équipements

13. AGENT ←→ TRAINING (N:N via AGENT_TRAINING)
    - Agents complètent plusieurs formations

14. AGENT → DOCUMENT (1:N)
    - Un agent a plusieurs documents

15. USER → NOTIFICATION (1:N)
    - Un utilisateur reçoit plusieurs notifications

💡 RECOMMANDATIONS D'IMPLÉMENTATION
1. Index Essentiels
sql-- Performance queries fréquentes
CREATE INDEX idx_attendance_agent_date ON ATTENDANCE(agent_id, attendance_date);
CREATE INDEX idx_shift_site_date ON SHIFT(site_id, shift_date);
CREATE INDEX idx_payroll_agent_period ON PAYROLL(agent_id, pay_period_start, pay_period_end);
CREATE INDEX idx_client_status ON CLIENT(contract_status);
CREATE INDEX idx_site_status ON SITE(site_status);
CREATE INDEX idx_agent_status ON AGENT(employment_status);
2. Triggers Automatiques
sql-- Auto-calculer heures totales
DELIMITER $$
CREATE TRIGGER calculate_attendance_hours 
BEFORE UPDATE ON ATTENDANCE
FOR EACH ROW
BEGIN
    IF NEW.clock