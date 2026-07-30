# Great GASPI  
## Geopolitical & Administrative Structural Analysis Protocol  
### Master Protocol & Unified Data Schema

**Purpose**  
Great GASPI is an empirical data-harvesting protocol for 16 disputed, insular, or non-sovereign territories. Each territory is examined through two institutional perspectives so that official records, security rationales, legal instruments, and material conditions can be captured symmetrically and without narrative adjudication.

**Methodological Rules**

1. Dual institutional perspectives are required for every territory.  
2. Prompts are executed in the primary administrative or customary language of the target institution.  
3. The model functions only as a harvester. No qualitative ratings, composite scores, or moral judgments are permitted.  
4. Strategic terrain is described solely by physical geometry: observation, fire control, movement corridors, and relation to water or critical infrastructure. Political or aggressive intent is never attributed.  
5. Every restriction, barrier, or control measure must record both the managing authority’s stated justification and the opposing institutional or civil characterization.  
6. Quantitative values require a point estimate, the full range when sources disagree, and a direct citation. If no verifiable figure exists, the field is marked `"data not available"`. Numbers are never invented.  
7. All geographic features, checkpoints, and infrastructure nodes use WGS84 decimal-degree coordinates.  
8. Output is a single valid JSON object conforming exactly to the schema below. Keys remain in English; string values retain native official terminology where appropriate.

**Schema Authority**  
All harvests must conform to the Great GASPI Data Schema defined in this document. No other structure is valid.

---

## Great GASPI Data Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Great GASPI Data Schema",
  "type": "object",
  "required": [
    "prompt_id",
    "territory_name",
    "perspective",
    "language",
    "years_of_scope",
    "wgs84_center",
    "topographic_and_control_data",
    "hydrology_data",
    "environmental_degradation_incidents",
    "infrastructure_and_logistics_data",
    "jurisprudence_and_statutory_friction",
    "security_and_justification_data"
  ],
  "properties": {
    "prompt_id": { "type": "string", "example": "prompt-1" },
    "territory_name": { "type": "string", "example": "West Bank" },
    "perspective": { "type": "string", "example": "State of Israel / Civil Administration" },
    "language": { "type": "string", "example": "Hebrew" },
    "years_of_scope": { "type": "string", "example": "1967-2026" },
    "wgs84_center": {
      "type": "object",
      "required": ["lat", "lng"],
      "properties": {
        "lat": { "type": "number" },
        "lng": { "type": "number" }
      }
    },

    "topographic_and_control_data": {
      "type": "object",
      "required": ["total_area_sqkm", "accessible_area_sqkm", "control_zones", "demographics", "named_high_ground_features", "physical_barriers"],
      "properties": {
        "total_area_sqkm": { "type": ["number", "string"] },
        "accessible_area_sqkm": { "type": ["number", "string"] },
        "control_zones": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["zone_name", "area_sqkm", "area_pct", "governing_authority", "access_restrictions", "strategic_features_located_here"],
            "properties": {
              "zone_name": { "type": "string" },
              "area_sqkm": { "type": ["number", "string"] },
              "area_pct": { "type": ["number", "string"] },
              "governing_authority": { "type": "string" },
              "access_restrictions": { "type": "string" },
              "strategic_features_located_here": { "type": "array", "items": { "type": "string" } }
            }
          }
        },
        "demographics": {
          "type": "object",
          "required": ["population_category_a", "population_category_b", "density_per_sqkm", "displacement_or_refugee_count", "notes", "citation"],
          "properties": {
            "population_category_a": { "type": ["number", "string"] },
            "population_category_b": { "type": ["number", "string"] },
            "density_per_sqkm": { "type": ["number", "string"] },
            "displacement_or_refugee_count": { "type": ["number", "string"] },
            "notes": { "type": "string" },
            "citation": { "type": "string" }
          }
        },
        "named_high_ground_features": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "lat", "lng", "elevation_m", "functional_strategic_description", "control_zone", "citation"],
            "properties": {
              "name": { "type": "string" },
              "lat": { "type": "number" },
              "lng": { "type": "number" },
              "elevation_m": { "type": ["number", "string"] },
              "functional_strategic_description": { "type": "string" },
              "control_zone": { "type": "string" },
              "citation": { "type": "string" }
            }
          }
        },
        "physical_barriers": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "type", "lat", "lng", "length_km", "temporal_variations", "stated_justification", "opposing_characterization", "citation"],
            "properties": {
              "name": { "type": "string" },
              "type": { "type": "string", "enum": ["natural", "manmade", "hybrid"] },
              "lat": { "type": "number" },
              "lng": { "type": "number" },
              "length_km": { "type": ["number", "string"] },
              "temporal_variations": { "type": "string" },
              "stated_justification": { "type": "string" },
              "opposing_characterization": { "type": "string" },
              "citation": { "type": "string" }
            }
          }
        }
      }
    },

    "hydrology_data": {
      "type": "object",
      "required": ["upstream_downstream_position", "water_infrastructure", "per_capita_water_consumption_l_d", "agriculture"],
      "properties": {
        "upstream_downstream_position": { "type": "string", "enum": ["upstream", "downstream", "shared", "not_applicable"] },
        "water_infrastructure": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "type", "lat", "lng", "controlling_entity", "capacity_or_flow_rate", "citation"],
            "properties": {
              "name": { "type": "string" },
              "type": { "type": "string" },
              "lat": { "type": "number" },
              "lng": { "type": "number" },
              "controlling_entity": { "type": "string" },
              "capacity_or_flow_rate": { "type": "string" },
              "citation": { "type": "string" }
            }
          }
        },
        "per_capita_water_consumption_l_d": {
          "type": "object",
          "required": ["population_a", "population_b", "who_reference_standard", "citation"],
          "properties": {
            "population_a": { "type": ["number", "string"] },
            "population_b": { "type": ["number", "string"] },
            "who_reference_standard": { "type": "number", "default": 100.0 },
            "citation": { "type": "string" }
          }
        },
        "agriculture": {
          "type": "object",
          "required": ["arable_land_pct", "irrigated_land_pct", "food_import_dependency_pct", "citation"],
          "properties": {
            "arable_land_pct": { "type": ["number", "string"] },
            "irrigated_land_pct": { "type": ["number", "string"] },
            "food_import_dependency_pct": { "type": ["number", "string"] },
            "citation": { "type": "string" }
          }
        }
      }
    },

    "environmental_degradation_incidents": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["incident_type", "chemical_or_hazard_agents", "toxicological_classification", "affected_area_sqkm", "first_documented_year", "ongoing", "stated_justification", "opposing_characterization", "documenting_orgs", "citations"],
        "properties": {
          "incident_type": { "type": "string" },
          "chemical_or_hazard_agents": { "type": "array", "items": { "type": "string" } },
          "toxicological_classification": { "type": "string" },
          "affected_area_sqkm": { "type": ["number", "string"] },
          "first_documented_year": { "type": ["integer", "string"] },
          "ongoing": { "type": "boolean" },
          "stated_justification": { "type": "string" },
          "opposing_characterization": { "type": "string" },
          "documenting_orgs": { "type": "array", "items": { "type": "string" } },
          "citations": { "type": "array", "items": { "type": "string" } }
        }
      }
    },

    "infrastructure_and_logistics_data": {
      "type": "object",
      "required": ["airspace_and_spectrum", "maritime_and_cabotage", "trade_and_dual_use_controls", "checkpoints_and_gates", "utilities_and_energy_grid"],
      "properties": {
        "airspace_and_spectrum": {
          "type": "object",
          "required": ["cellular_tech_allowed", "flight_corridor_control", "stated_justification", "citation"],
          "properties": {
            "cellular_tech_allowed": { "type": "string" },
            "flight_corridor_control": { "type": "string" },
            "stated_justification": { "type": "string" },
            "citation": { "type": "string" }
          }
        },
        "maritime_and_cabotage": {
          "type": "object",
          "required": ["eez_claimed_sqkm", "eez_accessible_sqkm", "accessible_ports_count", "fishing_zone_nautical_miles", "cabotage_or_merchant_marine_restrictions", "stated_justification", "citation"],
          "properties": {
            "eez_claimed_sqkm": { "type": ["number", "string"] },
            "eez_accessible_sqkm": { "type": ["number", "string"] },
            "accessible_ports_count": { "type": ["integer", "string"] },
            "fishing_zone_nautical_miles": { "type": ["number", "string"] },
            "cabotage_or_merchant_marine_restrictions": { "type": "string" },
            "stated_justification": { "type": "string" },
            "citation": { "type": "string" }
          }
        },
        "trade_and_dual_use_controls": {
          "type": "object",
          "required": ["controlled_item_categories", "transit_permit_regimes", "stated_justification", "citation"],
          "properties": {
            "controlled_item_categories": { "type": "array", "items": { "type": "string" } },
            "transit_permit_regimes": { "type": "string" },
            "stated_justification": { "type": "string" },
            "citation": { "type": "string" }
          }
        },
        "checkpoints_and_gates": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "lat", "lng", "permit_type_required", "stated_justification", "citation"],
            "properties": {
              "name": { "type": "string" },
              "lat": { "type": "number" },
              "lng": { "type": "number" },
              "permit_type_required": { "type": "string" },
              "stated_justification": { "type": "string" },
              "citation": { "type": "string" }
            }
          }
        },
        "utilities_and_energy_grid": {
          "type": "object",
          "required": ["official_currency", "local_informal_currency", "power_generating_assets", "daily_electricity_hours_avg", "power_grid_self_sufficiency_pct", "fuel_import_dependency_pct", "debt_or_fiscal_transfer_mechanisms", "citation"],
          "properties": {
            "official_currency": { "type": "string" },
            "local_informal_currency": { "type": "string" },
            "power_generating_assets": { "type": "array", "items": { "type": "string" } },
            "daily_electricity_hours_avg": { "type": ["number", "string"] },
            "power_grid_self_sufficiency_pct": { "type": ["number", "string"] },
            "fuel_import_dependency_pct": { "type": ["number", "string"] },
            "debt_or_fiscal_transfer_mechanisms": { "type": "string" },
            "citation": { "type": "string" }
          }
        }
      }
    },

    "jurisprudence_and_statutory_friction": {
      "type": "object",
      "required": ["enforced_system_name", "preferred_or_prior_system_name", "population_under_special_or_external_law", "enforced_statutes_cited", "landmark_jurisprudence_and_treaties", "documented_statutory_conflicts"],
      "properties": {
        "enforced_system_name": { "type": "string" },
        "preferred_or_prior_system_name": { "type": "string" },
        "population_under_special_or_external_law": { "type": ["number", "string"] },
        "enforced_statutes_cited": { "type": "array", "items": { "type": "string" } },
        "landmark_jurisprudence_and_treaties": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["judicial_body_or_treaty", "case_or_resolution_name", "year", "holding_or_standard", "official_legal_rationale", "citation"],
            "properties": {
              "judicial_body_or_treaty": { "type": "string" },
              "case_or_resolution_name": { "type": "string" },
              "year": { "type": ["integer", "string"] },
              "holding_or_standard": { "type": "string" },
              "official_legal_rationale": { "type": "string" },
              "citation": { "type": "string" }
            }
          }
        },
        "documented_statutory_conflicts": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["legal_domain", "enforced_clause_reference", "preferred_or_prior_clause_reference", "conflict_description", "citation"],
            "properties": {
              "legal_domain": { "type": "string" },
              "enforced_clause_reference": { "type": "string" },
              "preferred_or_prior_clause_reference": { "type": "string" },
              "conflict_description": { "type": "string" },
              "citation": { "type": "string" }
            }
          }
        }
      }
    },

    "security_and_justification_data": {
      "type": "object",
      "required": ["official_threat_assessments_or_attack_statistics", "stated_administrative_or_security_rationales"],
      "properties": {
        "official_threat_assessments_or_attack_statistics": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["description", "time_period", "numbers_or_incidents", "source", "citation"],
            "properties": {
              "description": { "type": "string" },
              "time_period": { "type": "string" },
              "numbers_or_incidents": { "type": "string" },
              "source": { "type": "string" },
              "citation": { "type": "string" }
            }
          }
        },
        "stated_administrative_or_security_rationales": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["measure", "official_rationale", "citation"],
            "properties": {
              "measure": { "type": "string" },
              "official_rationale": { "type": "string" },
              "citation": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
```

---

# Pure-Language Prompt Suite (Prompts 1–32)

> **Execution Note:** Copy only the pure target-language text between the matching `=== START PROMPT N ===` and `=== END PROMPT N ===` markers when executing individual harvest tasks.
# Great GASPI — Pure-Language Prompt Suite — Batch 7 (Prompts 25–28)

**How to use**  
Copy **only** the text between the matching `=== START PROMPT N ===` and `=== END PROMPT N ===` markers.  
That block is pure target language. Do not include any English headers when pasting into the model.

All outputs must conform to the Great GASPI Data Schema.

---

## Prompt 1
**Perspective:** Israeli Civil Administration (West Bank / Judea & Samaria)  
**Language:** Hebrew

=== START PROMPT 1 ===
פעל כחוקר גיאופוליטי ומשפטי בכיר. משימתך היא לאסוף נתונים עובדתיים ומוכחים בלבד עבור אזור יהודה ושומרון מנקודת המבט הרשמית של מדינת ישראל, המנהל האזרחי ביהודה ושומרון, מפקדת כוחות צה"ל באזור, מתפ"ש ומשרד הביטחון. עליך לחלץ מסמכים ראשוניים, צווים צבאיים, פסיקות בג"ץ, נתוני הלמ"ס, דוחות רשמיים והערכות איום ביטחוניות, ולכסות את כל ארבעת המכלולים באופן מלא.

אל תבצע הערכות איכותיות או דירוגים. ספק ערכים מספריים, נתוני טווח, נ"צ ברשת WGS84 וציטוטים ישירים. אם נתון אינו זמין במקורות רשמיים ציין במפורש "data not available".

1. מכלול 1: גיאוגרפיה פיזית ודמוגרפיה
   - רשום תוואי שטח ורכסים אסטרטגיים (גבעות 877, רכס שכם, הר עיבל, הר גריזים, מעלה אדומים ואחרים) עם קואורדינטות WGS84 וגובה במטרים.
   - עבור כל רכס או נקודת גובה גבוהה חובה לכלול תיאור אסטרטגי פונקציונלי המבוסס על טופוגרפיה בלבד: שליטה בתצפית, שליטה באש, שליטה במסדרונות תנועה, ומיקום יחסית לאזורי הזנה של אקוויפר ההר. אין לייחס כוונות.
   - חלץ נתוני שטח כולל בקמ"ר, שטח נגיש, והתפלגות מדויקת של שטחי א, ב ו-ג לפי הסכמי אוסלו ב' (1995) כולל אזור התפר ומרחב התפר. ציין במפורש אילו רכסים אסטרטגיים ואזורי הזנה של אקוויפר ההר נמצאים בכל אחד מהשטחים.
   - אסוף נתוני אוכלוסייה עדכניים: תושבים ישראלים (התיישבות) לעומת אוכלוסייה פלסטינית, וצפיפות אוכלוסין לקמ"ר.
   - מפה מכשולים פיזיים (גדר ההפרדה / מכשול התפר) כולל אורך בק"מ, סוג המכשול ונ"צ.
   - תעד את הנימוק הביטחוני הרשמי לבניית המכשול ולקביעת תוואי אזור התפר, כולל נתוני פיגועי התאבדות, ירי, חדירות ומנהרות שקדמו להחלטה, כפי שפורסמו על ידי צה"ל, שב"כ או משרד הביטחון.

2. מכלול 2: הידרופוליטיקה ואירועים סביבתיים
   - תעד מיקום הירדן ואקוויפר ההר (אגן מערבי, צפון-מזרחי ומזרחי) עם נ"צ של אזורי ההזנה העיקריים.
   - מפה תשתיות מים מרכזיות: קידוחים, תחנות שאיבה ומתקני מקורות עם נ"צ.
   - אסוף נתוני צריכת מים יומית לנפש (ליטר לאדם ליום) לאוכלוסייה הישראלית והפלסטינית מנתוני ועדת המים המשותפת ורשות המים, בהשוואה לתקן ארגון הבריאות העולמי של 100 ליטר לאדם ליום.
   - רשום אחוז קרקע חקלאית, שטחים מושקים ותלות ביבוא מזון.
   - תעד אירועי מפגעים סביבתיים: שפכים לא מטופלים, מזבלות פיראטיות, חומרים כימיים, שטח מושפע. ציין בנפרד את הנימוק הרשמי של המנהל האזרחי ואת טענות הארגונים.

3. מכלול 3: תשתיות וכלכלה
   - תקשורת ותדרים: טכנולוגיה סלולרית מורשית, מגבלות תדרים ושליטה במרחב האווירי.
   - חופש תנועה: מפה מעברים ונתיבים (מחסום חוצה שומרון, מעבר אפרים, מחסום קלנדיה, מחסום מעלה אדומים) עם נ"צ וסוג היתרי הכניסה הנדרשים.
   - תעד את הנימוק הביטחוני הרשמי לקיומם של המחסומים ולהגבלות התנועה, כולל נתוני פיגועים או ניסיונות חדירה שדווחו באזורי המחסומים.
   - מטבע ושירותים: מטבע רשמי (שקל חדש), תלות ברשת החשמל הארצית ותלות ביבוא דלק.

4. מכלול 4: חיכוך משפטי וסטטוטורי
   - המערכת האוכפת: פרט את מסגרת התחיקה הביטחונית כולל צו בדבר הוראות ביטחון נוסח משולב מספר 1651, צו בדבר חוק תכנון ערים וכפרים מספר 418, וצווים בדבר תפיסת מקרקעין.
   - תעד פסיקות בג"ץ המכשירות או מסדירות תפיסת קרקעות לפי חוק הקרקעות העות'מאני משנת 1858, ואת הנימוקים הביטחוניים שהוצגו בבג"ץ.
   - הצג התנגשות חוקית ישירה: ציין סעיפים ספציפיים בחוק הצבאי או הישראלי מול החוק הירדני מספר 79 משנת 1966 או החוק העות'מאני בתחומי תכנון, בנייה ומקרקעין.
   - ציין את גודל האוכלוסייה הכפופה לחוק הצבאי.

החזר את כל הנתונים כבלוק JSON מובנה בדיוק לפי הסכמה הסטנדרטית של Great GASPI. אם נתון מסוים אינו זמין ציין "data not available".
=== END PROMPT 1 ===

---

## Prompt 2
**Perspective:** Palestinian Land Rights / Palestinian Authority (West Bank)  
**Language:** Arabic

=== START PROMPT 2 ===
بصفتك باحثاً جغرافياً وقانونياً مستقلاً. مهمتك هي جمع بيانات وثائقية وأدلة ميدانية وأرقام رسمية موثقة للضفة الغربية من واقع سجلات السلطة الوطنية الفلسطينية، سلطة الأراضي، سلطة المياه الفلسطينية، الجهاز المركزي للإحصاء الفلسطيني، والأرشيف العثماني والأردني.

لا تقم بأي تقييمات كيفيّة أو إعطاء درجات. اجمع أرقاماً محددة، إحداثيات WGS84، ونصوصاً قانونية صريحة. إذا لم تتوفر معلومة محددة في المصادر الرسمية فاكتب "data not available".

1. الركن الأول: الجغرافيا الفيزيائية والديموغرافيا
   - وثّق التضاريس والجبال المهددة بالسيطرة (جبل عيبال، جبل جرزيم، طمون، مسافر يطا وغيرها) مع إحداثيات WGS84 والارتفاع بالأمتار.
   - لكل مرتفع أو سلسلة جبلية يجب تضمين وصف استراتيجي وظيفي مبني على التضاريس فقط: السيطرة على الرصد، السيطرة على النيران، السيطرة على ممرات الحركة، وموقعها بالنسبة لمناطق تغذية الحوض الجبلي. لا تنسب نوايا.
   - حدد المساحة الإجمالية بالكيلومتر المربع، المساحة المتاحة للاستخدام الفلسطيني، وتوزيع المناطق أ وب وج وفق اتفاقية أوسلو 2 لعام 1995 ومساحة جدار الفصل والمناطق المغلقة أمنياً. حدد صراحة أي المرتفعات الاستراتيجية ومناطق تغذية الحوض الجبلي تقع داخل كل منطقة.
   - اجمع أعداد السكان: السكان الفلسطينيين الأصليين مقابل المستوطنين، وحساب الكثافة السكانية لكل كيلومتر مربع.
   - وثّق جدار الضم والتوسع والموانع الفيزيائية: الإحداثيات، الطول الإجمالي بالكيلومتر، ونوع المانع.

2. الركن الثاني: الهيدروبوليتيك والانتهاكات البيئية
   - سجل موقع الحوض المائي الجبلي (الحوض الغربي والشرقي والشمالي الشرقي) ونهر الأردن مع إحداثيات مناطق التغذية الرئيسية.
   - أدرج آبار المياه والينابيع ومحطات الضخ المغلقة أو المصادرة مع إحداثيات WGS84.
   - استخرج أرقام استهلاك المياه اليومي للفرد (لتر/فرد/يوم) للسكان الفلسطينيين مقارنة بالمستوطنين واستناداً لتقارير سلطة المياه والمنظمات الدولية مقارنة بحد منظمة الصحة العالمية البالغ 100 لتر/فرد/يوم.
   - سجل نسبة الأراضي الصالحة للزراعة، الأراضي المروية، ونسبة الاعتماد على استيراد الأغذية.
   - وثّق حوادث التدهور البيئي والزراعي: اقتلاع الأشجار، تجريف الأراضي، رش المبيدات، عوادم المستوطنات والمجاري، مع تحديد المواد الكيماوية والمساحة المتضررة والتبرير المعلن للجيش الإسرائيلي مقابل التوثيق الحقوقي الفلسطيني.

3. الركن الثالث: البنية التحتية والاقتصاد
   - الاتصالات والترددات: أجيال الشبكات المسموح بها للفلسطينيين والقيود على نطاقات التردد.
   - حرية الحركة والمناطق المحاصرة: حصر البوابات والحواجز العسكرية (حاجز قلنديا، حاجز حوارة، حاجز زعترة، حاجز الحفيرة) مع إحداثيات WGS84 ونوع التصاريح المطلوبة.
   - النقد والخدمات: العملات المتداولة (الشيكل والدينار والدولار)، نسبة التبعية لشبكة الكهرباء الإسرائيلية والاعتماد على المحروقات المستوردة.

4. الركن الرابع: الاحتكاك القانوني والتشريعي
   - النظام المطبق: وثّق قرارات المصادرة العسكرية وأوامر وضع اليد لأغراض عسكرية وأوامر الهدم الصادرة عن الإدارة المدنية الإسرائيلية.
   - النظام المحلي المفضل: وثّق الأحكام والتشريعات السارية بموجب قانون تنظيم المدن والقرى والأبنية الأردني رقم 79 لسنة 1966 وسجلات الطابو العثماني وقوانين الملكية المشاعية.
   - التعارض التشريعي المباشر: وثّق التعارض بين الأمر العسكري الإسرائيلي رقم 418 والقانون الأردني رقم 79 لسنة 1966.
   - عدد السكان الفلسطينيين الخاضعين للأوامر العسكرية وحكم الطوارئ.

أخرج جميع البيانات في قالب JSON الموحد المطابق تماماً لـ Standardized Great GASPI JSON Schema. إذا لم تتوفر معلومة محددة فاكتب "data not available".
=== END PROMPT 2 ===

---

## Prompt 3
**Perspective:** Israeli Southern Command / COGAT (Gaza Strip)  
**Language:** Hebrew

=== START PROMPT 3 ===
פעל כחוקר גיאופוליטי וביטחוני בכיר. משימתך היא לאסוף נתונים עובדתיים ומוכחים בלבד עבור רצועת עזה מנקודת המבט הרשמית של מדינת ישראל, מפקדת פיקוד הדרום, חיל הים, מתפ"ש ומשרד הביטחון. עליך לחלץ מסמכים ראשוניים, נהלים ביטחוניים, הודעות לימאים, נתוני תשתיות והערכות איום, ולכסות את כל ארבעת המכלולים באופן מלא.

אל תבצע הערכות איכותיות או דירוגים. ספק ערכים מספריים, נתוני טווח, נ"צ ברשת WGS84 וציטוטים ישירים. אם נתון אינו זמין ציין "data not available".

1. מכלול 1: גיאוגרפיה פיזית ודמוגרפיה
   - רשום את תוויי השטח, פרימטר הביטחון ואזור חיץ ביטחוני (Access Restricted Area) לאורך הגבול היבשתי עם נ"צ WGS84. ציין את רוחב האזור החיץ לפי התקופות השונות אם יש הבדלים.
   - חלץ נתוני שטח כולל בקמ"ר, שטח מורשה לגישה, והתפלגות הנפות (צפון עזה, עזה, דיר אל-בלח, חאן יונס, רפיח).
   - אסוף נתוני אוכלוסייה מקומית, צפיפות אוכלוסין לקמ"ר ונתוני פינוי או מעבר.
   - מפה מכשולים פיזיים: המכשול התת-קרקעי והעילי סביב עזה כולל אורך, גובה ומאפיינים טכנולוגיים עם נ"צ.
   - תעד את הנימוק הביטחוני הרשמי לקביעת אזור החיץ ולמכשול, כולל נתוני ירי רקטות, מנהרות התקפיות, חדירות ופיגועים שקדמו להחלטות, כפי שפורסמו על ידי צה"ל או משרד הביטחון.

2. מכלול 2: הידרופוליטיקה ואירועים סביבתיים
   - תעד מיקום אקוויפר החוף ונחל הבשור עם נ"צ.
   - מפה תשתיות מים: קווי מים ישירים מישראל (קווי נגב של מקורות), תחנות התפלה ומעברים עם נ"צ.
   - אסוף נתוני צריכת מים יומית לנפש (ליטר לאדם ליום) המועברים לרצועה בהשוואה לתקן ארגון הבריאות העולמי של 100 ליטר לאדם ליום.
   - רשום אחוז קרקע חקלאית בתוך ומחוץ לאזור החיץ, שטחים מושקים ותלות באספקת מזון חיצונית.
   - תעד אירועים סביבתיים וריסוס אווירי: פעולות חישוף וריסוס קוטלי עשבים לאורך הפרימטר, חומרים כימיים, שטח מושפע. ציין בנפרד את הנימוק הביטחוני הרשמי של צה"ל (מניעת הסתרה וקו ראייה) ואת טענות הארגונים.

3. מכלול 3: תשתיות וכלכלה
   - תקשורת ותדרים: טכנולוגיה סלולרית מאושרת לרצועה, תדרים מוקצים ושליטה במרחב האווירי.
   - מרחב ימי: שטח ימי מורשה לדייג (גבול לפי הודעות חיל הים) ונמלים מורשים. ציין את השינויים בגבול הימי לפי תקופות אם קיימים, ואת הנימוק הביטחוני הרשמי להגבלות (מניעת הברחות נשק דרך הים).
   - חופש תנועה ומעברים: מפה מעברי גבול (מעבר כרם שלום, מעבר ארז) עם נ"צ וסיווג ציוד לפי רשימת הציוד הדו-שימושי המפוקח.
   - תעד את הנימוק הביטחוני הרשמי לרשימת הציוד הדו-שימושי ולהגבלות על הכנסת חומרים, כולל דוגמאות של שימוש צבאי בחומרים אזרחיים לכאורה.
   - דלק וחשמל: קווי מתח ישירים מחברת החשמל לישראל, מכסות סולר לתחנת הכוח בעזה ותלות באנרגיה חיצונית.

4. מכלול 4: חיכוך משפטי וסטטוטורי
   - המערכת האוכפת: פרט את הנהלים הביטחוניים, צווי המצור או הסגר הימי והיבשתי ותחיקת הפיקוח על היצוא הביטחוני והדו-שימושי.
   - תעד פסיקות בג"ץ בעתירות לגבי אספקת חשמל, מים וציוד רפואי, ואת הנימוקים הביטחוניים שהוצגו על ידי המדינה.
   - הצג התנגשות חוקית ישירה: צווי פיקוח ביטחוניים ישראליים מול תקנות החברה והאזרחות של הרשות הפלסטינית או המנהל המקומי בעזה.
   - ציין גודל אוכלוסייה הכפופה למשטר הפיקוח וההיתרים.

החזר את כל הנתונים כבלוק JSON מובנה בדיוק לפי הסכמה הסטנדרטית של Great GASPI. אם נתון מסוים אינו זמין ציין "data not available".
=== END PROMPT 3 ===

---

## Prompt 4
**Perspective:** Palestinian Civil & Environmental Agencies (Gaza Strip)  
**Language:** Arabic

=== START PROMPT 4 ===
بصفتك باحثاً جغرافياً وبنياً تحتياً. مهمتك هي جمع بيانات وثائقية وأدلة ميدانية وأرقام رسمية موثقة لقطاع غزة من واقع سجلات سلطة الطاقة الفلسطينية، سلطة المياه، شركة توزيع الكهرباء، مصلحة مياه بلديات الساحل، وزارة الاتصالات، والمراكز الحقوقية الميدانية.

لا تقم بأي تقييمات كيفيّة أو إعطاء درجات. اجمع أرقاماً محددة، إحداثيات WGS84، ونصوصاً قانونية صريحة. إذا لم تتوفر معلومة محددة فاكتب "data not available".

1. الركن الأول: الجغرافيا الفيزيائية والديموغرافيا
   - وثّق الشريط الحدودي والمنطقة المقيدة أمنياً (Access Restricted Area) مع إحداثيات WGS84 لمواقع الجريفات وشبكات الجدار. حدد عرض المنطقة المقيدة حسب الفترات الزمنية إن وجدت اختلافات.
   - حدد المساحة الإجمالية لقطاع غزة، المساحة المتاحة للزراعة والسكن، والمحافظات الخمس (شمال غزة، غزة، دير البلح، خانيونس، رفح).
   - اجمع أعداد السكان المحليين، نسبة اللاجئين المسجلين، وحساب الكثافة السكانية لكل كيلومتر مربع.
   - وثّق الموانع العسكرية الحصينة: الجدار الفولاذي الأرضي، الأسلاك الشائكة، وأبراج المراقبة الآلية مع الإحداثيات والأطوال.

2. الركن الثاني: الهيدروبوليتيك والانتهاكات البيئية
   - سجل حالة الخزان الجوفي الساحلي، أرقام الملوحة وارتفاع نسبة الكلورايد والنيترات واستنزاف المياه.
   - أدرج محطات التحلية (الجنوب والوسط والشمال) ومحطات المعالجة مع إحداثيات WGS84 وتأثرها بنقص الوقود.
   - استخرج أرقام استهلاك المياه اليومي للفرد (لتر/فرد/يوم) المتاحة للشرب والاستخدام المنزلي مقارنة بحد منظمة الصحة العالمية البالغ 100 لتر/فرد/يوم.
   - سجل نسبة الأراضي الصالحة للزراعة المتبقية، الأراضي المدمّرة في المنطقة العازلة، ونسبة الفقر الغذائي والاعتماد على المساعدات.
   - وثّق حوادث التدهور البيئي والزراعي: عمليات الرش الجوي لمبيدات الأعشاب من قبل الطائرات الإسرائيلية، تدمير المزارع، تلوث البحر بمياه الصرف الصحي غير المعالجة، مع تحديد المواد الكيماوية والمساحة الزراعية المتضررة والتبرير الإسرائيلي المعلن مقابل التوثيق الحقوقي والبيئي الفلسطيني.

3. الركن الثالث: البنية التحتية والاقتصاد
   - الاتصالات والترددات: حظر شبكات الأجيال المتقدمة، منع إدخال الفايبر وأجهزة المقاسم، وتدمير أبراج التغطية.
   - القطاع البحري: حدود مسافة الصيد البحري المسموح بها، عدد المراكب المتضررة، وميناء غزة. حدد التغيرات في الحدود البحرية حسب الفترات إن وجدت.
   - حرية الحركة والمعابر: حصر حركة البضائع عبر معبر كرم أبو سالم، منع إدخال المواد المصنفة مزدوجة الاستخدام مع إحداثيات المعابر.
   - الطاقة والكهرباء: خطوط الكهرباء العشرة، ساعات وصل وقطع الكهرباء، قدرة محطة توليد الكهرباء الوحيدة، والاعتماد الكامل على الديزل المستورد.

4. الركن الرابع: الاحتكاك القانوني والتشريعي
   - النظام المطبق: وثّق قرارات الحصار المرفوعة، قوائم المواد الممنوعة، والقرارات العسكرية التي تحكم المنافذ البرية والبحرية والجوية.
   - النظام المحلي الساري: وثّق اللوائح التنظيمية الصادرة عن المجلس التشريعي أو الوزارات المحلية والمجلس الأعلى للقضاء الشرعي والنظام المدني.
   - التعارض التشريعي المباشر: وثّق التعارض بين قوانين حظر الدخول والمواد مزدوجة الاستخدام الإسرائيلية وبين القرارات المحلية الساعية لتطوير البنية التحتية والتجارة.
   - عدد السكان الخاضعين للحصار والقيود المباشرة.

أخرج جميع البيانات في قالب JSON الموحد المطابق تماماً لـ Standardized Great GASPI JSON Schema. إذا لم تتوفر معلومة محددة فاكتب "data not available".
=== END PROMPT 4 ===

---


---

## Prompt 5
**Perspective:** Kingdom of Morocco / Ministry of Interior / Southern Provinces Administration  
**Language:** French

=== START PROMPT 5 ===
Agissez en tant que chercheur géopolitique et juridique senior. Votre mission est de collecter des données factuelles et vérifiables concernant les Provinces du Sud (Sahara Marocain) du point de vue officiel du Royaume du Maroc, du Ministère de l'Intérieur, de l'Agence pour le développement des provinces du Sud et des institutions compétentes. Vous devez extraire des documents primaires, des Dahirs, des bulletins officiels, des données d'infrastructures et des justifications sécuritaires officielles, en couvrant intégralement les quatre piliers.

Ne procédez à aucune évaluation qualitative ni attribution de notes. Fournissez des valeurs numériques, des coordonnées WGS84 et des citations directes. Si une donnée n'est pas disponible dans les sources officielles, inscrivez "data not available".

1. Pilier 1 : Géographie physique et démographie
   - Listez les reliefs stratégiques et zones frontières (Plateau du Draa, Zemmour, Dakhla-Oued Ed-Dahab et autres) avec coordonnées WGS84 et altitudes en mètres.
   - Pour chaque relief ou point élevé, incluez obligatoirement une description stratégique fonctionnelle fondée uniquement sur la topographie : contrôle de l'observation, contrôle du feu, contrôle des corridors de mouvement, et position relative aux ressources hydriques. N'attribuez aucune intention.
   - Extrayez la superficie totale en km², la superficie accessible, et le découpage administratif officiel des trois régions du Sud (Guelmim-Oued Noun, Laâyoune-Sakia El Hamra, Dakhla-Oued Ed-Dahab). Précisez explicitement quels reliefs stratégiques se trouvent dans quelles zones de contrôle.
   - Collectez les données démographiques du Haut-Commissariat au Plan : population totale, densité au km² et programmes de développement urbain.
   - Cartographiez le Mur de défense marocain (Le Berm) : longueur totale, coordonnées WGS84, structure et zones sécurisées.
   - Documentez la justification sécuritaire officielle de la construction et du maintien du Berm, y compris les menaces et incidents de sécurité cités par les autorités marocaines (incursions, attentats, activités armées) ayant précédé ou motivé son édification et son renforcement.

2. Pilier 2 : Hydropolitique et données environnementales
   - Documentez les bassins hydrographiques (Saguia el-Hamra) et les stations de dessalement (Laâyoune, Dakhla) avec coordonnées WGS84 et capacités.
   - Relevez les données d'exploitation minière du Groupe OCP à Bou Craa : volumes d'extraction de phosphate, convoyeur et permis.
   - Collectez la consommation d'eau quotidienne par habitant et la part des terres agricoles irriguées.
   - Documentez les incidents environnementaux et risques : mines terrestres le long du Berm, zones de pâturage affectées. Séparez clairement la justification sécuritaire officielle des rapports d'ONG.

3. Pilier 3 : Infrastructures et économie
   - Télécommunications : couverture réseau (3G/4G/5G) par les opérateurs marocains et gestion de l'espace aérien.
   - Maritime et pêche : superficie de la ZEE, activité des ports de Laâyoune et Dakhla, données de l'accord de partenariat de pêche Maroc-UE.
   - Postes frontières : cartographiez le poste de Guerguerat avec coordonnées WGS84, flux commerciaux et permis de transit. Documentez la justification sécuritaire officielle du contrôle de ce point de passage.
   - Monnaie et énergie : utilisation du Dirham marocain, raccordement au réseau électrique national (ONEE) et projets d'énergies renouvelables.

4. Pilier 4 : Friction juridique et statutaire
   - Système appliqué : détaillez les Dahirs publiés au Bulletin Officiel étendant le droit civil, pénal et commercial marocain aux Provinces du Sud.
   - Documentez les décrets d'investissement et les incitations fiscales territoriales.
   - Identifiez le conflit statutaire direct : opposez les lois d'administration territoriale marocaine aux revendications du Front POLISARIO et aux avis consultatifs de la CIJ et de la CJUE, en citant les justifications juridiques officielles marocaines.
   - Indiquez la population régie par l'administration marocaine.

Restituez l'ensemble des données sous forme de bloc JSON conforme au Standardized Great GASPI JSON Schema. Si une donnée n'est pas disponible, inscrivez "data not available".
=== END PROMPT 5 ===

---

## Prompt 6
**Perspective:** POLISARIO Front / SADR Authorities  
**Language:** Spanish

=== START PROMPT 6 ===
Actúe como investigador geográfico y jurídico independiente. Su misión es recopilar datos documentales, evidencia de campo y cifras oficiales verificadas sobre el Sahara Occidental desde los registros de la República Árabe Saharaui Democrática (RASD), el Frente POLISARIO y los dictámenes de tribunales internacionales (CIJ, TJUE).

No realice evaluaciones cualitativas ni otorgue calificaciones. Recopile números concretos, coordenadas WGS84 y citas jurídicas explícitas. Si un dato no está disponible, escriba "data not available".

1. Pilar 1: Geografía física y demografía
   - Documente la geografía de los Territorios Liberados y los campos de refugiados de Tindouf (Tifariti, Bir Lehlou, Mehaires) con coordenadas WGS84 y altitudes.
   - Para cada elevación o cadena montañosa incluya obligatoriamente una descripción estratégica funcional basada únicamente en la topografía: control de la observación, control del fuego, control de los corredores de movimiento y posición relativa a los recursos hídricos. No atribuya intenciones.
   - Determine la superficie total del territorio (aproximadamente 266.000 km²), la proporción dividida por el Muro militar marroquí (El Berm) y el área bajo control de la RASD. Precise explícitamente qué relieves estratégicos se encuentran en cada zona de control.
   - Recopile datos demográficos de la población saharaui refugiada y en zonas disputadas según fuentes de ACNUR y la RASD.
   - Mapee el Muro militar de separación: coordenadas WGS84, campos de minas asociados, radares y fortificaciones.
   - Documente las caracterizaciones oficiales de la RASD y el POLISARIO sobre el Berm como instrumento de ocupación y separación, junto con los datos de desplazados y minas.

2. Pilar 2: Hidropolítica y recursos naturales
   - Mapee los pozos de agua, acuíferos subterráneos y oasis en la Zona Liberada con coordenadas WGS84.
   - Recopile datos sobre la extracción de recursos naturales: fosfatos en Bou Craa, licencias de pesca concedidas por Marruecos en aguas saharauis y exportación de arena.
   - Extraiga las sentencias del Tribunal de Justicia de la Unión Europea que anulan los acuerdos comerciales y de pesca UE-Marruecos en territorio saharaui.
   - Documente incidentes de degradación ambiental: impacto de minas antipersona en el pastoreo nómada y denuncias presentadas ante la ONU. Separe las justificaciones oficiales marroquíes de las caracterizaciones saharauis.

3. Pilar 3: Infraestructura y control económico
   - Telecomunicaciones y espectro: restricciones de conectividad en las zonas bajo control marroquí y redes de comunicación de la RASD.
   - Dominio marítimo y fronteras: ZEE saharaui reclamada, control del paso fronterizo de Guerguerat y denuncias sobre el tránsito comercial no autorizado.
   - Movilidad y puestos de control: bloqueos militares a lo largo del muro y permisos de entrada a los Territorios Liberados.
   - Moneda y servicios: uso de la Peseta Saharaui, Dinar Argelino en campamentos y grado de dependencia de la ayuda humanitaria internacional.

4. Pilar 4: Fricción jurídica y estatutaria
   - Sistema en vigor (RASD): documente la Constitución de la RASD, los decretos del Consejo Nacional Saharaui y las licencias expedidas por la Autoridad Saharaui de Petróleo y Minería.
   - Conflicto estatutario directo: documente la contradicción entre los Dahirs de anexión marroquíes y el dictamen consultivo de la Corte Internacional de Justicia de 1975, la Resolución 1514 (XV) de la ONU y las sentencias del TJUE sobre el consentimiento del pueblo saharaui.
   - Población saharaui afectada por el conflicto y la separación territorial.

Exporte todos los datos en un bloque JSON estructurado estrictamente según el Standardized Great GASPI JSON Schema. Si un dato no está disponible, escriba "data not available".
=== END PROMPT 6 ===

---

## Prompt 7
**Perspective:** Pridnestrovian Moldavian Republic (PMR) / Transnistrian authorities  
**Language:** Russian

=== START PROMPT 7 ===
Действуйте как старший геополитический и экономический исследователь. Ваша задача — собрать исключительно фактические и проверенные данные по Приднестровской Молдавской Республике (ПМР) с официальной точки зрения государственных органов ПМР, Верховного Совета ПМР, Приднестровского республиканского банка и администрации Молдавской ГРЭС. Вы должны извлечь первичные документы, законодательные акты, данные инфраструктуры, таможенную статистику и официальные обоснования безопасности, охватывая все четыре блока.

Не производите качественных оценок и не ставьте рейтингов. Предоставляйте точные числовые значения, координаты WGS84 и прямые цитаты. Если конкретные данные отсутствуют, укажите "data not available".

1. Блок 1: Физическая география и демография
   - Укажите ключевые географические объекты, реки и высоты (река Днестр, Рыбницкие высоты, Бендерский опорный пункт и другие) с координатами WGS84 и высотой в метрах.
   - Для каждого возвышенного пункта или хребта обязательно включите функциональное стратегическое описание, основанное только на топографии: контроль наблюдения, контроль огня, контроль коридоров движения и положение относительно водных ресурсов. Не приписывайте намерений.
   - Извлеките данные о общей площади территории ПМР (около 4163 км²), площади подконтрольных земель и административном делении (Тирасполь, Бендеры, Рыбницкий, Дубоссарский, Слободзейский, Григориопольский, Каменский районы). Явно укажите, какие стратегические высоты находятся в каких зонах контроля.
   - Соберите демографические данные Государственной службы статистики ПМР: численность населения, плотность на км².
   - Зафиксируйте миротворческие и контрольные посты: координаты WGS84 постов Совместных миротворческих сил и пограничной службы МГБ ПМР.
   - Задокументируйте официальное обоснование безопасности существования контрольных постов и миротворческой операции, включая данные об инцидентах и угрозах, на которые ссылаются власти ПМР.

2. Блок 2: Гидрополитика и экологические данные
   - Задокументируйте расположение бассейна реки Днестр и Дубоссарского водохранилища.
   - Нанесите на карту ключевые гидротехнические и энергетические объекты: Дубоссарскую ГЭС, Молдавскую ГРЭС (в Днестровске) с координатами WGS84 и мощностью.
   - Извлеките данные по суточному потреблению воды на душу населения и статистику орошаемых сельскохозяйственных земель.
   - Зафиксируйте экологические инциденты и риски: состояние склада боеприпасов в Колбасне, выбросы промышленных предприятий. Разделяйте официальные позиции МПР ПМР и внешние претензии.

3. Блок 3: Инфраструктура и экономика
   - Связь и частоты: разрешенные стандарты мобильной связи (Интерднестрком), используемые частоты и контроль воздушного пространства.
   - Транспорт и пункты пропуска: нанесите на карту пограничные пункты пропуска (Кучурган, Бендеры, Дубоссары) с координатами WGS84, типы таможенных режимов и требования к автотранспорту.
   - Задокументируйте официальное обоснование таможенных и пограничных режимов ПМР.
   - Валюта и энергетика: официальная валюта — Приднестровский рубль, газовые взаиморасчеты, экспорт электроэнергии с МГРЭС.

4. Блок 4: Юридические и административные конфликты
   - Применяемая система: детализируйте законодательную базу ПМР, Конституцию ПМР, Таможенный кодекс ПМР и законы о налоговой системе.
   - Зафиксируйте статус Оперативной группы российских войск и правовые акты, регламентирующие миротворческую операцию (Соглашение 1992 года), включая официальные обоснования её необходимости.
   - Прямой правовой конфликт: укажите конкретные статьи законов ПМР, вступающие в противоречие с законодательством Республики Молдова.
   - Укажите численность населения, проживающего под юрисдикцией властей ПМР.

Выведите все данные в виде структурированного JSON-блока строго по Standardized Great GASPI JSON Schema. Если конкретные данные отсутствуют, укажите "data not available".
=== END PROMPT 7 ===

---

## Prompt 8
**Perspective:** Republic of Moldova / Bureau for Reintegration  
**Language:** Romanian

=== START PROMPT 8 ===
Acționați ca un cercetător geopolitic și juridic senior. Misiunea dumneavoastră este de a colecta date obiective și verificate privind teritoriul din stînga Nistrului (Regiunea Transnistreană) din perspectiva oficială a autorităților Republicii Moldova, Biroului Politici de Reintegrare și Serviciului Vamal al RM. Trebuie să extrageți documente primare, legi, hotărâri de Guvern, date de infrastructură și caracterizările oficiale ale autorităților moldovenești, acoperind integral cei patru piloni.

Nu efectuați evaluări calitative și nu acordați note. Furnizați valori numerice, coordonate WGS84 și citate directe. Dacă o dată nu este disponibilă, scrieți "data not available".

1. Pilonul 1: Geografie fizică și demografie
   - Enumerați reliefurile și zonele de securitate (cursul fluviului Nistru, platourile Cocieri, Coșnița, Varnița și altele) cu coordonate WGS84 și altitudini în metri.
   - Pentru fiecare punct elevat sau lanț includeți obligatoriu o descriere strategică funcțională bazată exclusiv pe topografie: controlul observației, controlul focului, controlul coridoarelor de mișcare și poziția relativă față de resursele de apă. Nu atribuiți intenții.
   - Extrageți suprafața totală a unităților administrativ-teritoriale din stînga Nistrului (aproximativ 4163 km²), suprafața controlată de facto de autoritățile constituționale și diferențele de zonare. Precizați explicit care reliefuri strategice se află în care zone de control.
   - Colectați datele demografice ale Biroului Național de Statistică și Agenției Servicii Publice: numărul cetățenilor RM deținători de pașapoarte moldovenești în regiune, populația totală și densitatea pe km².
   - Cartografiați posturile de control ale structurilor de la Tiraspol: coordonate WGS84, amplasare în Zona de Securitate și restricții de circulație.
   - Documentați caracterizările oficiale ale autorităților Republicii Moldova privind aceste posturi ca ilegale și obstacole în calea reintegrării, împreună cu datele privind incidentele de securitate.

2. Pilonul 2: Hidropolitică și date de mediu
   - Documentați bazinul fluviului Nistru, sursă strategică de apă potabilă pentru Chișinău și alte localități.
   - Cartografiați infrastructura hidrotehnică și energetică: Centrala Hidroelectrică de la Dubăsari și Centrala Termoelectrică de la Cuciurgan (MGRES) cu coordonate WGS84.
   - Extrageți datele privind consumul de apă și accesul fermierilor moldoveni din raionul Dubăsari la terenurile agricole.
   - Documentați incidentele de mediu: poluarea Nistrului, depozitul de muniții de la Cobasna și deșeurile industriale. Separați pozițiile oficiale ale RM de cele ale autorităților de la Tiraspol.

3. Pilonul 3: Infrastructură și economie
   - Telecomunicații și frecvențe: utilizarea spectrului radio autorizat de ANRCETI, interferențele rețelelor neautorizate și controlul spațiului aerian.
   - Transport și vamă: cartografiați punctele de trecere a frontierei moldo-ucrainene (sectorul transnistrean) și punctele interne de control cu coordonate WGS84; înregistrarea agenților economici din regiune la Camera Înregistrării de Stat a RM.
   - Documentați caracterizările oficiale ale autorităților moldovenești privind regimurile vamale și de control din stînga Nistrului.
   - Monedă și energie: utilizarea leului moldovenesc versus rubla transnistreană, schema de import a gazelor naturale și acumularea datoriei istorice pe malul stâng.

4. Pilonul 4: Fricțiune juridică și statutară
   - Sistem aplicat: detaliați cadrul legal al RM, inclusiv Legea Nr. 221/2005 cu privire la prevederile de bază ale statutului juridic special al localităților din stînga Nistrului și Codul Vamal al RM.
   - Documentați deciziile Curții Europene a Drepturilor Omului privind încălcarea drepturilor omului în regiune (de exemplu cauza Catan și alții).
   - Identificați conflictul statutar direct: opuneți legislația constituțională a RM și Codul Vamal unitar actelor emise de autoritățile de la Tiraspol.
   - Indicați populația supusă dublei jurisdicții sau afectată de lipsa garanțiilor constituționale.

Restituiți toate datele sub formă de bloc JSON conform Standardized Great GASPI JSON Schema. Dacă o dată nu este disponibilă, scrieți "data not available".
=== END PROMPT 8 ===

---

---

## Prompt 9
**Perspective:** U.S. Federal Government / Financial Oversight and Management Board (FOMB) / Department of the Interior (Puerto Rico)  
**Language:** English

=== START PROMPT 9 ===
Act as a senior geopolitical and federal legal researcher. Your mission is to collect strictly factual and objective empirical data for the unincorporated territory of Puerto Rico from the official perspective of the U.S. Federal Government, the Financial Oversight and Management Board (FOMB), the Maritime Administration (MARAD), the Department of the Interior Office of Insular Affairs, and federal judicial dockets. You must extract primary statutes, court dockets, infrastructure data, fiscal reports, and official justifications, covering all four pillars.

Do not perform qualitative assessments or assign ratings. Provide explicit numerical values, range estimates, WGS84 coordinates, and direct legal citations. If a specific data point is missing from public records, output "data not available".

1. Pillar 1: Physical Geography & Demographics
   - List key geographic features, mountain ranges, and federal reservations (Cordillera Central, El Yunque National Forest, Roosevelt Roads naval site and others) with WGS84 coordinates and elevation in meters.
   - For every high-ground feature include a functional strategic description based solely on topography: observation control, fire control, movement-corridor control, and position relative to water resources or critical infrastructure. Do not attribute intent.
   - Extract total land area (approximately 9104 sq km), accessible land area, and administrative breakdown across 78 municipalities. Explicitly note which strategic features fall under which federal or local jurisdictions.
   - Collect U.S. Census Bureau demographic data: total island population, citizen classification, population density per sq km, and net migration rates to the U.S. mainland.
   - Map physical or coastal defense barriers and federal restricted installations with WGS84 coordinates.
   - Document the official federal and FOMB justifications for fiscal oversight, land-use restrictions, and any security or emergency measures, including cited threats to fiscal stability, public safety, or critical infrastructure.

2. Pillar 2: Hydropolitics & Environmental Data
   - Map primary watersheds, rivers (Río Grande de Loíza, Río de la Plata), and major water supply reservoirs (Carraízo, Dos Bocas, Lucchetti) managed by PRASA under EPA regulations with WGS84 coordinates.
   - Report per-capita daily water consumption (L/c/d) compared against WHO reference standards (100 L/c/d).
   - Document agricultural parameters: arable land percentage, crop yield data, and total food import dependency percentage.
   - Document environmental degradation incidents: EPA Superfund sites (Vieques bombing range, Caño Martín Peña contamination), toxicological classifications, affected areas. Separately record official federal remediation justifications versus local civil claims.

3. Pillar 3: Infrastructure & Economic Data
   - Spectrum & Airspace: FCC regulated telecommunications spectrum (3G/4G/5G standards), FAA controlled commercial flight corridors, and airport authority (SJU).
   - Maritime Shipping & Cabotage: total claimed EEZ, accessible commercial ports (Port of San Juan, Port of Ponce), and enforcement data of Section 27 of the Merchant Marine Act of 1920 (Jones Act). Document the official federal justification for Jones Act application to Puerto Rico.
   - Mobility & Ports: List named commercial border ports of entry and CBP inspection checkpoints with WGS84 coordinates.
   - Currency & Fiscal Restructuring: Official currency (USD), LUMA Energy / Genera PR power grid generation and transmission dependency, and PREPA debt restructuring data under Title III of PROMESA. Document the official FOMB justifications for fiscal controls and debt restructuring measures.

4. Pillar 4: Legal & Administrative Friction
   - Enforced System: Detail Title 48 of the U.S. Code (Territories and Insular Possessions), the Puerto Rico Oversight, Management, and Economic Stability Act (PROMESA), and the supremacy of the U.S. Constitution under Article IV, Section 3 (Territory Clause).
   - Document key U.S. Supreme Court jurisprudence establishing territorial status: Insular Cases (Downes v. Bidwell, Balzac v. Porto Rico) and modern precedents (Puerto Rico v. Sanchez Valle, Financial Oversight Board v. Aurelius, Vaello Madero). Include the official federal legal rationales presented in those cases.
   - Direct Statutory Conflict: Cite explicit statutory overlaps between federal PROMESA board fiscal plan mandates and local Puerto Rico Legislative Assembly statutes (Act 22 / Act 60 tax incentive codes, local labor laws).
   - Report the total population subject to federal statutory supremacy without federal voting representation in Congress.

Return all data as a structured JSON block strictly matching the Standardized Great GASPI JSON Schema. If a specific data point is missing from public records, output "data not available".
=== END PROMPT 9 ===

---

## Prompt 10
**Perspective:** Puerto Rican Autonomy / Civil Advocates / Legislative Assembly perspective  
**Language:** Spanish

=== START PROMPT 10 ===
Actúe como investigador geográfico, fiscal y jurídico independiente. Su misión es recopilar datos documentales, evidencia de campo y cifras oficiales verificadas sobre Puerto Rico desde los registros de la Asamblea Legislativa de Puerto Rico, los informes del Centro de Periodismo Investigativo, organizaciones sindicales (UTIER) y archivos judiciales locales.

No realice evaluaciones cualitativas ni otorgue calificaciones. Recopile números concretos, coordenadas WGS84 y citas jurídicas explícitas. Si un dato no está disponible, escriba "data not available".

1. Pilar 1: Geografía física y demografía
   - Documente las zonas geográficas vulnerables, cuencas hidrográficas en riesgo y franjas costeras amenazadas por la gentrificación y erosión con coordenadas WGS84 y altitudes.
   - Para cada elevación o característica de alto terreno incluya obligatoriamente una descripción estratégica funcional basada únicamente en la topografía: control de la observación, control del fuego, control de los corredores de movimiento y posición relativa a los recursos hídricos. No atribuya intenciones.
   - Determine la superficie total (aproximadamente 9104 km²), la distribución por 78 municipios y el impacto del desplazamiento poblacional y la migración forzada por razones económicas. Precise qué rasgos estratégicos caen bajo qué jurisdicciones.
   - Recopile datos demográficos del Instituto de Estadísticas de Puerto Rico: población residente, nivel de pobreza infantil y densidad poblacional.
   - Mapee las propiedades públicas e instalaciones militares transferidas o restringidas con coordenadas WGS84.
   - Documente las caracterizaciones oficiales y civiles locales sobre el control federal de tierras e instalaciones, junto con datos de desplazamiento y pérdida de acceso.

2. Pilar 2: Hidropolítica y recursos naturales
   - Mapee los embalses principales (Carraízo, Dos Bocas) y el estado de la infraestructura de la Autoridad de Acueductos y Alcantarillados con coordenadas WGS84, registrando la pérdida de agua por salideros.
   - Reporte los datos de consumo de agua potable por habitante y el impacto de los racionamientos durante sequías.
   - Recopile datos sobre la inseguridad alimentaria: porcentaje de tierras agrícolas de alta capacidad desplazadas por proyectos solares o desarrollos urbanos, y la dependencia alimentaria.
   - Documente incidentes de degradación ambiental: contaminación por cenizas de carbón en Peñuelas, vertederos en violación con la EPA, zonas afectadas. Separe las justificaciones corporativas o estatales de las denuncias de las comunidades locales.

3. Pilar 3: Infraestructura y control económico
   - Telecomunicaciones y energía: apagones recurrentes bajo la privatización de LUMA Energy y Genera PR, costo del kilovatio-hora comparado con el promedio de EE. UU., y estado de la red eléctrica.
   - Ley de Cabotaje (Jones Act): impacto económico estimado del requisito de usar barcos de bandera estadounidense en las importaciones, sobrecosto en fletes marítimos y congestión en el Puerto de San Juan. Documente las caracterizaciones locales del Jones Act como carga económica.
   - Exenciones fiscales y gentrificación: pérdida de ingresos fiscales por la Ley 22 / Ley 60, número de propiedades adquiridas por beneficiarios de la ley y desplazamiento comunitario.
   - Moneda y deuda: uso del Dólar estadounidense, monto de la deuda pública reestructurada y recortes presupuestarios impuestos a la Universidad de Puerto Rico y municipios por la Junta (FOMB).

4. Pilar 4: Fricción jurídica y estatutaria
   - Sistema preferido/local: documente la Constitución del Estado Libre Asociado de Puerto Rico (1952) y las leyes aprobadas por la Asamblea Legislativa para proteger recursos locales.
   - Conflicto estatutario directo: documente la contradicción abierta entre las secciones de la Ley PROMESA (que otorgan poder de veto absoluto a la Junta sobre leyes locales) y las leyes estatales aprobadas democráticamente (presupuestos locales, leyes laborales o la Ley de Retiro Digno).
   - Población total gobernada bajo un régimen territorial sin representación con voto en el Congreso de los EE. UU.

Exporte todos los datos en un bloque JSON estructurado estrictamente según el Standardized Great GASPI JSON Schema. Si un dato no está disponible, escriba "data not available".
=== END PROMPT 10 ===

---

## Prompt 11
**Perspective:** Turkish Republic of Northern Cyprus (TRNC) / Turkish State Authorities  
**Language:** Turkish

=== START PROMPT 11 ===
Kıdemli bir jeopolitik ve hukuki araştırmacı olarak hareket edin. Göreviniz, Kuzey Kıbrıs Türk Cumhuriyeti (KKTC) ve Türkiye Cumhuriyeti makamlarının resmi perspektifinden KKTC bölgesi için sadece somut ve doğrulanabilir verileri toplamaktır. KKTC Resmî Gazetesi'nden, Taşınmaz Mal Komisyonu kararlarından, Devlet Su İşleri raporlarından, altyapı verilerinden ve resmi güvenlik gerekçelerinden dört sütunun tamamını kapsayan birincil belgeleri çıkarmalısınız.

Niteliksel değerlendirmeler yapmayın veya puanlama vermeyin. Kesin sayısal değerler, WGS84 koordinatları ve doğrudan hukuki atıflar sağlayın. Belirli bir veri resmi kayıtlarda yoksa "data not available" yazın.

1. Sütun 1: Fiziki coğrafya ve demografi
   - Stratejik coğrafi yapıları, Beşparmak Dağları'nı, Mesarya Ovası'nı ve geçitleri WGS84 koordinatları ve yükseklikleriyle (m) listeleyin.
   - Her yüksek nokta veya sırt için yalnızca topografyaya dayalı zorunlu işlevsel stratejik tanım ekleyin: gözlem kontrolü, ateş kontrolü, hareket koridorları kontrolü ve su kaynaklarına göre konum. Niyet atfetmeyin.
   - Toplam kara alanını (yaklaşık 3355 km²), erişilebilir alanı ve 6 ilçeye (Lefkoşa, Gazimağusa, Girne, Güzelyurt, İskele, Lefke) göre idari dağılımı çıkarın. Hangi stratejik yükseltilerin hangi kontrol bölgelerinde olduğunu açıkça belirtin.
   - KKTC İstatistik Kurumu nüfus verilerini toplayın: yerleşik nüfus, vatandaşlık dağılımı ve km² başına nüfus yoğunluğu.
   - Sınır engellerini ve BM Yeşil Hat sınır boyundaki askeri güvenlik hatlarını WGS84 koordinatları, uzunlukları ve engel türleriyle haritalandırın.
   - Yeşil Hat ve güvenlik önlemlerinin resmi güvenlik gerekçesini belgeleyin; KKTC ve Türkiye makamlarının atıfta bulunduğu tehditler, olaylar ve emniyet değerlendirmelerini dahil edin.

2. Sütun 2: Hidropolitik ve çevresel veriler
   - Doğu Akdeniz hidroloji konumunu, Güzelyurt ve Gazimağusa akiferlerinin durumunu belgeleyin.
   - "Türkiye'den KKTC'ye Su Temini Projesi" altyapısını haritalandırın: Alaköprü Barajı, deniz altı boru hattı, Geçitköy Barajı ve arıtma tesislerini WGS84 koordinatlarıyla listeleyin.
   - Kişi başı günlük su tüketim miktarlarını ve tarımsal sulama oranlarını toplayın.
   - Çevresel olayları ve riskleri belgeleyin: akiferlerin tuzlanması, maden atıkları (Lefke CMC). Resmi iyileştirme gerekçelerini ve dış iddiaları ayrı tutun.

3. Sütun 3: Altyapı ve ekonomi
   - Telekomünikasyon ve spektrum: izin verilen hücresel teknoloji (3G/4G/4.5G), BTHK spektrum düzenlemeleri ve Ercan Havalimanı hava sahası uçuş kontrolü.
   - Deniz sahası ve limanlar: Münhasır Ekonomik Bölge anlaşmaları, Gazimağusa ve Girne limanlarının ticari kapasitesi.
   - Hareketlilik ve sınır kapıları: Yeşil Hat üzerindeki resmi geçiş kapılarını (Metehan, Lokmacı, Beyarmudu, Bostancı) WGS84 koordinatları ve istenen kimlik/pasaport türleriyle listeleyin. Resmi güvenlik gerekçesini belgeleyin.
   - Para birimi ve enerji: resmi para birimi Türk Lirası, KIB-TEK elektrik şebekesi, Türkiye'den kablo ile elektrik getirme projesi ve yakıt ithalat bağımlılığı.

4. Sütun 4: Hukuki ve idari sürtüşme
   - Uygulanan sistem: KKTC Anayasası'nı, 67/2005 sayılı Taşınmaz Mal Komisyonu Yasası'nı ve Resmî Gazete'de yayımlanan mülkiyet mevzuatını detaylandırın.
   - İnsan Hakları Avrupa Mahkemesi tarafından etkili bir iç hukuk yolu olarak tanınan TMK kararlarını, ödenen tazminat miktarlarını ve iade/takas verilerini belgeleyin. Resmi hukuki gerekçeleri dahil edin.
   - Doğrudan kanuni çatışma: KKTC mülkiyet ve imar yasaları ile Güney Kıbrıs Rum Yönetimi yasaları ve AİHM kararlarındaki mülkiyet hakları çatışmalarını somut maddelerle belgeleyin.
   - KKTC hukuki rejimi altında yaşayan toplam nüfus miktarını belirtin.

Tüm verileri Standardized Great GASPI JSON Schema'ya kesinlikle uygun olarak yapılandırılmış bir JSON bloğu olarak döndürün. Belirli bir veri resmi kayıtlarda yoksa "data not available" yazın.
=== END PROMPT 11 ===

---

## Prompt 12
**Perspective:** Republic of Cyprus / UN Buffer Zone Framework  
**Language:** Greek

=== START PROMPT 12 ===
Ενεργήστε ως ακαδημαϊκός και νομικός ερευνητής. Η αποστολή σας είναι να συλλέξετε αυστηρά αντικειμενικά και επιβεβαιωμένα δεδομένα για τις κατεχόμενες περιοχές της Κυπριακής Δημοκρατίας από την επίσημη σκοπιά των αρχών της Κυπριακής Δημοκρατίας, του Τμήματος Κτηματολογίου και Χωρομετρίας, και των αποφάσεων διεθνών δικαστηρίων (ΕΔΔΑ, ΔΕΕ). Πρέπει να εξαγάγετε πρωτογενή έγγραφα, νόμους, ψηφίσματα του ΟΗΕ και δεδομένα υποδομών που καλύπτουν πλήρως και τους 4 πυλώνες.

Μην προβαίνετε σε ποιοτικές αξιολογήσεις και μην δίνετε βαθμολογίες. Παρέχετε συγκεκριμένες αριθμητικές τιμές, συντεταγμένες WGS84 και αδιαμφισβήτητες νομικές παραπομπές. Εάν κάποιο δεδομένο δεν είναι διαθέσιμο στις επίσημες πηγές, αναγράψτε "data not available".

1. Πυλώνας 1: Φυσική γεωγραφία και δημογραφία
   - Καταγράψτε τα κύρια γεωγραφικά στοιχεία, την οροσειρά του Πενταδακτύλου, την πεδιάδα της Μεσαορίας και τις κατεχόμενες παραλιακές ζώνες με συντεταγμένες WGS84 και υψόμετρα (m).
   - Για κάθε υψηλό σημείο ή οροσειρά συμπεριλάβετε υποχρεωτικά λειτουργική στρατηγική περιγραφή βασισμένη αποκλειστικά στην τοπογραφία: έλεγχος παρατήρησης, έλεγχος πυρός, έλεγχος διαδρόμων κίνησης και θέση σε σχέση με υδάτινους πόρους. Μην αποδίδετε προθέσεις.
   - Εξαγάγετε τη συνολική έκταση των κατεχομένων περιοχών (περίπου 36,2% της επικράτειας της Δημοκρατίας — περίπου 3355 τ.χλμ.) και την έκταση της Νεκρής Ζώνης (Buffer Zone — UNFICYP). Προσδιορίστε ρητά ποια στρατηγικά υψώματα βρίσκονται σε ποιες ζώνες ελέγχου.
   - Συλλέξτε δημογραφικά στοιχεία της Στατιστικής Υπηρεσίας της Κυπριακής Δημοκρατίας: εκτοπισμένοι Ελληνοκύπριοι πρόσφυγες του 1974, εκτιμώμενος αριθμός εποίκων από την Τουρκία και δημογραφική αλλοίωση.
   - Χαρτογραφήστε τη γραμμή κατάπαυσης του πυρός (Πράσινη Γραμμή): συντεταγμένες WGS84, μήκος, στρατιωτικά φυλάκια και οχυρώσεις.
   - Τεκμηριώστε τις επίσημες θέσεις της Κυπριακής Δημοκρατίας σχετικά με την Πράσινη Γραμμή και τις στρατιωτικές ζώνες ως αποτέλεσμα παράνομης κατοχής, μαζί με δεδομένα εκτοπισμού.

2. Πυλώνας 2: Υδροπολιτική και περιβαλλοντικά δεδομένα
   - Χαρτογραφήστε τους υδάτινους πόρους, τον υπόγειο φορέα της Μόρφου και τις ζημίες από την υπεράντληση με συντεταγμένες WGS84.
   - Καταγράψτε τις παράνομες υποδομές μεταφοράς νερού από την Τουρκία και την εξάρτηση των κατεχομένων περιοχών, καθώς και την κατάσταση του φράγματος της Μόρφου.
   - Αναφέρετε την ημερήσια κατανάλωση νερού ανά κάτοικο και την απώλεια πρόσβασης των εκτοπισμένων γεωργών στις εύφορες εκτάσεις της Μεσαορίας και της Μόρφου.
   - Τεκμηριώστε περιστατικά περιβαλλοντικής υποβάθμισης: παράνομη αμμοληψία, καταστροφή φυσικών βιοτόπων, βιομηχανική μόλυνση στο Λεύκα. Διαχωρίστε τις επίσημες καταγγελίες της Κυπριακής Δημοκρατίας από άλλες θέσεις.

3. Πυλώνας 3: Υποδομές και οικονομία
   - Τηλεπικοινωνίες και φάσμα: παράνομη χρήση συχνοτήτων στο FIR Λευκωσίας, παρεμβολές στις τηλεπικοινωνίες της Δημοκρατίας και έλεγχος του εναέριου χώρου από την Άγκυρα.
   - Θαλάσσια ζώνη και λιμάνια: κήρυξη των λιμανιών της Αμμοχώστου και της Κερύνειας ως παράνομων σημείων εισόδου/εξόδου από την Κυπριακή Δημοκρατία, και παραβιάσεις στην ΑΟΖ.
   - Σημεία διέλευσης: καταγράψτε τα εγκεκριμένα σημεία διέλευσης της Πράσινης Γραμμής (Άγιος Δομέτιος, Λήδρας, Οδόφραγμα Λήδρα Πάλας, Αστρομερίτης) με συντεταγμένες WGS84 και εφαρμογή του Κανονισμού της Πράσινης Γραμμής. Τεκμηριώστε τις επίσημες θέσεις για τους περιορισμούς.
   - Νόμισμα και οικονομικές επιπτώσεις: παράνομη σφετεριστική χρήση περιουσιών, απώλεια τουρισμού και εξαναγκαστική χρήση της Τουρκικής Λίρας στις κατεχόμενες περιοχές.

4. Πυλώνας 4: Νομική και διοικητική σύγκρουση
   - Εφαρμοστέο σύστημα: τεκμηριώστε το σύνταγμα και τους νόμους της Κυπριακής Δημοκρατίας, τα ψηφίσματα του Συμβουλίου Ασφαλείας του ΟΗΕ (ειδικά τα Ψηφίσματα 541/1983 και 550/1984 που κηρύσσουν την αποσχιστική οντότητα νομικά άκυρη).
   - Τεκμηριώστε τις ιστορικές αποφάσεις του Ευρωπαϊκού Δικαστηρίου Δικαιωμάτων του Ανθρώπου: Λοϊζίδου κατά Τουρκίας, Τέταρτη Διακρατική Προσφυγή Κύπρος κατά Τουρκίας, και αποφάσεις για το καθεστώς της περιεκλειστης περιοχής των Βαρωσίων.
   - Άμεση νομοθετική σύγκρουση: παραθέστε τη σύγκρουση μεταξύ του κυπριακού ποινικού/αστικού κώδικα (Νόμος περί Σφετερισμού Ελληνοκυπριακών Περιουσιών) και των παράνομων "τίτλων ιδιοκτησίας" που εκδίδονται από την αποσχιστική αρχή.
   - Αναφέρετε το μέγεθος του πληθυσμού που επηρεάζεται από τη στρατιωτική κατοχή.

Επιστρέψτε όλα τα δεδομένα ως δομημένο JSON block αυστηρά σύμφωνα με το Standardized Great GASPI JSON Schema. Εάν κάποιο δεδομένο δεν είναι διαθέσιμο στις επίσημες πηγές, αναγράψτε "data not available".
=== END PROMPT 12 ===

---


---

## Prompt 13
**Perspective:** PRC Central Government / Tibet Autonomous Region Administration  
**Language:** Mandarin Chinese (简体中文)

=== START PROMPT 13 ===
扮演一名高级地缘政治与法学研究员。你的任务是从中华人民共和国中央人民政府、西藏自治区人民政府、水利部及国家自然资源部等官方机构的视角，收集关于西藏自治区及涉藏州县的客观、可验证的实证数据。你必须提取一手法律文件、政府白皮书、水利及基础设施建设规划、人口普查数据、官方安全与治理理由，全面覆盖全部四个核心要素。

切勿进行任何主观定性评价或评分。请提供具体的数值、范围估计、WGS84地理坐标及直接的法律/法规引用。若某项特定数据在官方公开记录中缺失，请明确注明 "data not available"。

1. 要素一：物理地理与人口数据
   - 列出战略性地形、山脉及边境要隘（冈底斯山脉、喜马拉雅山脉要隘、雅鲁藏布江大峡谷、亚东、吉隆口岸等），并附带 WGS84 坐标和海拔高度（米）。
   - 对于每一个高地或山脊，必须包含仅基于地形的功能性战略描述：观察控制、火力控制、移动走廊控制，以及相对于水资源或关键基础设施的位置。不要归因意图。
   - 提取西藏自治区总面积（约122.8万平方公里）、可开发与利用土地面积，以及七个地级行政区（拉萨、日喀则、昌都、林芝、山南、那曲、阿里）的行政划分数据。明确指出哪些战略高地属于哪些管辖或管控区域。
   - 收集国家统计局与自治区统计局的人口普查数据：常住人口总量、藏族及其他少数民族人口比例、汉族人口比例，以及每平方公里的人口密度。
   - 绘制边境管控设施与网格化管理区域：WGS84 坐标、管控范围及边境小康村建设数据。
   - 记录官方安全与治理理由：边境管控、网格化社会管理服务以及相关措施的正式依据与威胁评估（如分裂活动、境外干扰等官方表述）。

2. 要素二：水文政治与环境数据
   - 记录主要水系与跨界河流（雅鲁藏布江/布拉马普特拉河、澜沧江/湄公河、怒江/萨尔温江、狮泉河/印度河）的水文位置与流速数据。
   - 绘制重大水利与水电基础设施：藏木水电站、加查水电站、三江源国家公园生态保护区，标注 WGS84 坐标与装机容量。
   - 收集人均日用水量（L/c/d）以及可耕地面积比例、灌溉农田比例与粮食自给率。
   - 记录环境治理与生态保护项目：生态移民安置数据、退耕还林还草面积、官方生态补偿标准。将官方理由与外部质疑分开记录。

3. 要素三：基础设施与经济数据
   - 电信与频谱管理：工信部许可的移动通信技术标准（3G/4G/5G 覆盖率）、无线电频谱管控规则，以及民用航空局对拉萨贡嘎机场、林芝米林机场等高高原机场的空域管理。
   - 交通与物流通道：川藏铁路、青藏铁路、G318/G219 国道交通节点，标注 WGS84 坐标与通行能力。
   - 陆路口岸：樟木口岸、吉隆口岸、亚东口岸的 WGS84 坐标与海关通关数据。记录官方对口岸管控的安全与经济理由。
   - 货币与转移支付：人民币流通数据、中央财政对西藏自治区的转移支付比例及电力网络供电自给率。

4. 要素四：法律与行政摩擦
   - 实施法律体系：详细阐述《中华人民共和国宪法》、《中华人民共和国民族区域自治法》、《西藏自治区自治条例（草案）》及《宗教事务条例》（特别是藏传佛教活佛转世管理办法）。
   - 记录寺庙管理委员会的行政架构以及中央对自治区治理的法定依据与官方理由。
   - 直接法律冲突：对比中央人民政府的法定行政管理法规与历史上《十七条协议》或达赖喇嘛流亡政府所主张的法律诉求之间的条款性分歧，并记录官方立场。
   - 列出受民族区域自治法及国家安全法规管辖的区域总人口数。

将所有数据严格按照 Standardized Great GASPI JSON Schema 格式整合并返回 JSON 模块。若某项特定数据在官方公开记录中缺失，请明确注明 "data not available"。
=== END PROMPT 13 ===

---

## Prompt 14
**Perspective:** Central Tibetan Administration / Customary & Rights Advocates  
**Language:** Tibetan (བོད་ཡིག)

=== START PROMPT 14 ===
ཁྱེད་ནི་ས་ཁམས་སྲིད་དོན་དང་ཁྲིམས་ལུགས་ཞིབ་འཇུག་པ་ཆེན་པོ་ཞིག་ཡིན། ཁྱེད་ཀྱི་ལས་འགན་ནི་དབུས་བོད་མིའི་སྒྲིག་འཛུགས་དང་། བོད་ཀྱི་འགྲོ་བ་མིའི་ཐོབ་ཐང་དང་མང་གཙོ་འཕེལ་རྒྱས་ལྟེ་གནས། སྲོལ་རྒྱུན་ས་ཞིང་བདག་དབང་འཛིན་མཁན་བཅས་ཀྱི་ཡིག་ཆ་དང་སྙན་ཐོ་གཞིར་བཟུང་སྟེ། བོད་ཀྱི་ས་ཁུལ་ཡོངས་ཀྱི་གནས་ཚུལ་དངོས་རྣམས་སྡུད་རུབ་བྱེད་རྒྱུ་དེ་ཡིན། ཀོར་བཞི་ཡོངས་རྫོགས་གསལ་པོར་ཁྱབ་དགོས།

རང་སྣང་གང་ཤར་གྱི་ཐག་གཅོད་དང་ཨང་རིམ་འདོགས་པ་གཏན་ནས་མི་བྱེད་པར། ཨང་རྩིས་གསལ་པོ། WGS84 ས་ཁྲའི་གནས་ས། ཁྲིམས་ལུགས་ཀྱི་ལུང་འདྲེན་དངོས་རྣམས་མཁོ་སྤྲོད་བྱེད་དགོས། གལ་ཏེ་གནས་ཚུལ་དེ་དག་གཞུང་ཕྱོགས་ཡིག་ཆའི་ནང་མེད་ཚེ་ "data not available" ཞེས་བྲི་དགོས།

༡། ཀོར་དང་པོ། ས་ཁམས་ཆགས་སྟངས་དང་མི་འབོར་གནས་ཚུལ།
   - རྒྱ་ནག་གཞུང་གིས་དམ་སྒྲག་བྱེད་བཞིན་པའི་གལ་ཆེའི་རི་རྒྱུད་དང་། གནས་ཆེན། སྲོང་ལམ་ (གངས་རིན་པོ་ཆེ། ཡར་ལྷ་ཤམ་པོ། དཔའ་ཤོད་ལ་བཅས) WGS84 坐标 དང་མཐོ་ཚད་ (མི་ཊར) བཅས་བྲིས་ཤིག
   - མཐོ་ས་རེ་རེར་ས་ཁམས་ཁོ་ན་ལ་གཞིགས་པའི་བྱེད་ནུས་ཀྱི་གསལ་བཤད་ངེས་པར་དུ་འཇུག་དགོས། ལྟ་ཞིབ་དབང་ཚད། མེ་མདའི་དབང་ཚད། འགྲུལ་ལམ་གྱི་དབང་ཚད། ཆུ་ཐོན་ཁུངས་ལ་གཞིགས་པའི་གནས་བབ། དམིགས་ཡུལ་མི་འཇོག
   - བོད་ཀྱི་ས་མཚམས་ཡོངས་རྫོགས་ཀྱི་རྒྱ་ཁྱོན་དང་། བོད་རང་སྐྱོང་ལྗོངས་དང་བོད་རིགས་རང་སྐྱོང་ཁུལ་ཁག་གི་ས་ཁྲའི་འཁོད་སྟངས་བསྡུ་རུབ་བྱེད། གང་དུ་མཐོ་ས་གང་ཡོད་པ་གསལ་པོར་བྲིས།
   - མི་འབོར་གནས་ཚུལ། བོད་མི་དངོས་ཀྱི་མི་འབོར་དང་། རྒྱ་རིགས་གནས་སྤོས་པའི་མི་འབོར། མི་འབོར་སྟུག་ཚད་བཅས་བསྡུ་རུབ་བྱེད།
   - འགྲིམ་འགྲུལ་བཀག་སྡོམ་དང་དམག་དོན་མཁར་རྫོང་། དམ་སྒྲག་དྲ་བའི་བཀག་སྡོམ་ས་ཚིགས་ཁག་ WGS84 坐标 དང་རིང་ཚད་བཅས་བཀོད་དགོས།
   - བོད་མིའི་གཞུང་དང་ཐོབ་ཐང་ཚོགས་པའི་ངོས་ནས་བཀག་སྡོམ་དང་དམ་སྒྲག་ལ་བཞག་པའི་ཁ་གསལ་དང་གནས་ཚུལ་བསྡུ་རུབ་བྱེད།

༢། ཀོར་གཉིས་པ། ཆུ་སྲིད་དང་ཁོར་ཡུག་ཉམས་རྒུད།
   - བོད་ཀྱི་གཙང་པོ་ཆེན་པོ་ཁག་ (ཡར་ཀླུང་གཙང་པོ། རྫ་ཆུ། རྒྱལ་མོ་རྔུལ་ཆུ། སེང་གེ་གཙང་པོ) ཡི་ཆུ་ལག་དང་ཆུ་འགོའི་གནས་བབ་བཀོད་དགོས།
   - རྒྱ་ནག་གཞུང་གིས་རྒྱག་བཞིན་པའི་ཆུ་མཛོད་དང་ཆུ་གློག་ཁང་ WGS84 坐标 དང་གློག་ཤུགས་ཆེ་ཆུང་བྲིས་ཤིག
   - འབྲོག་པ་ས་གནས་ནས་གནས་སྤོས་བཏང་བའི་ "འབྲོག་ལས་འཕོ་འགྱུར་" གྱི་འབྲོག་པ་མི་འབོར་དང་། ས་ཞིང་ཤོར་བའི་རྒྱ་ཁྱོན།
   - གཏེར་ཁ་ཁྲོག་འདོན་གྱིས་ཁོར་ཡུག་ལ་བཟོས་པའི་གཏོར་བཤིག རྒྱ་ནག་གཞུང་གི་རྒྱུ་མཚན་དང་བོད་མིས་ངོས་འཛིན་བྱེད་པའི་གནས་ཚུལ་སོ་སོར་བསྡུ་རུབ་བྱེད།

༣། ཀོར་གསུམ་པ། གཞི་རྟེན་སྒྲིག་ཆས་དང་དཔལ་འབྱོར།
   - བརྡ་འཕྲིན་དང་དྲ་བའི་བཀག་སྡོམ། ཁ་པར་དང་དྲ་རྒྱའི་རྒྱ་ལམ་བཀག་སྡོམ་དང་། སྐད་འཕྲིན་སོགས་ལ་སོ་ལྟ་བྱེད་པའི་གནས་ཚུལ།
   - འགྲིམ་འགྲུལ་དང་མཚོ་ལམ། ལྕགས་ལམ་དང་དམག་སྤྱོད་གནམ་ཐང་ཁག་གི་ WGS84 坐标།
   - འགྲུལ་བཞུད་བཀག་སྡོམ། དགོན་པ་དང་ས་གནས་ཕན་ཚུན་གྱི་བཀག་སྡོམ་ས་ཚིགས་ཁག་ WGS84 坐标 དང་དགོས་པའི་ལག་ཁྱེར་རིགས།
   - ཤོག་སྒོར་དང་ནུས་པ། རྒྱ་སྒོར་བཙན་འཛུལ་བྱས་པ་དང་། བོད་ཀྱི་རང་བྱུང་ནུས་པ་རྒྱ་ནག་ནང་ལོགས་སུ་སྐྱེལ་འདྲེན་བྱེད་པའི་གནས་ཚུལ།

༤། ཀོར་བཞི་པ། ཁྲིམས་ལུགས་དང་འཛིན་སྐྱོང་གི་རྩོད་རྙོག
   - ལག་བསྟར་བྱེད་བཞིན་པའི་ཁྲིམས་ལུགས། རྒྱ་ནག་གཞུང་གི་ "རྒྱལ་ཁབ་ཉེན་སྲུང་ཁྲིམས་ལུགས་" དང་། "ཆོས་ལུགས་དོན་བྱེད་ཁྲིམས་ལུགས"། དགོན་པ་འཛིན་སྐྱོང་ཨུ་ཡོན་ལྷན་ཁང་གི་བཀོད་ཁྱབ།
   - བོད་མིའི་འདོད་བློ་ཡོད་པའི་ཁྲིམས་ལུགས། ༡༩༥༡ ལོའི་ "དོན་ཚན་བཅུ་བདུན་ཆིངས་ཡིག" གི་རང་དབང་ཐོབ་ཐང་དང་། བོད་མིའི་སྲོལ་རྒྱུན་ས་ཞིང་བདག་དབང་།
   - ཁྲིམས་ལུགས་གདོང་ཐུག རྒྱ་ནག་གི་འཛིན་སྐྱོང་བཀོད་ཁྱབ་དང་བོད་མིའི་སྲོལ་རྒྱུན་ཐོབ་ཐང་། ༧རྒྱལ་བ་རིན་པོ་ཆེའི་ཡང་སྲིད་ངོས་འཛིན་སྐོར་གྱི་ཁྲིམས་ལུགས་གདོང་ཐུག
   - རྒྱ་ནག་གི་དྲག་པོའི་ཁྲིམས་ལུགས་འོག་ཡོད་པའི་བོད་མི་མི་འབོར་ཡོངས་རྫོགས།

གནས་ཚུལ་ཡོངས་རྫོགས་ Standardized Great GASPI JSON Schema ལྟར་ JSON བཟོ་བཀོད་ནང་ཕྱིར་འདོན་བྱེད་དགོས། གལ་ཏེ་གནས་ཚུལ་དེ་དག་གཞུང་ཕྱོགས་ཡིག་ཆའི་ནང་མེད་ཚེ་ "data not available" ཞེས་བྲི་དགོས།
=== END PROMPT 14 ===

---

## Prompt 15
**Perspective:** U.S. Department of Defense / Joint Region Marianas (Guam)  
**Language:** English

=== START PROMPT 15 ===
Act as a senior geopolitical and military land-use researcher. Your mission is to collect strictly factual, empirical data for the unincorporated territory of Guam (Guåhan) from the official perspective of the U.S. Department of Defense, Joint Region Marianas, Marine Corps Activity Guam, Andersen Air Force Base, Naval Base Guam, and federal statutory records. You must extract primary environmental impact statements, master installation plans, federal property records, judicial dockets, and official security justifications, covering all four pillars.

Do not perform qualitative evaluations or assign ratings. Provide explicit numerical values, range estimates, WGS84 coordinates, and direct legal citations. If a specific data point is missing from official records, output "data not available".

1. Pillar 1: Physical Geography & Demographics
   - List key geographic features, strategic high ground, and military reservations (Mount Lamlam, Ritidian Point, Orote Peninsula, Fena Valley Reservoir and others) with WGS84 coordinates and elevation in meters.
   - For every high-ground feature include a functional strategic description based solely on topography: observation control, fire control, movement-corridor control, and position relative to water resources or critical infrastructure. Do not attribute intent.
   - Extract total island land area (approximately 544 sq km), land area reserved for DoD use, and municipal administrative breakdowns across 19 villages. Explicitly note which strategic features fall under military versus civilian jurisdiction.
   - Collect U.S. Census Bureau demographic data: total island population, native Chamorro population, active-duty military and dependent population, and population density per sq km.
   - Map physical defense installations, perimeter fences, and restricted military zones (Andersen AFB, Naval Base Guam, Camp Blaz) with WGS84 coordinates and total fence-line length.
   - Document the official DoD and Joint Region Marianas security justifications for land reservations, firing ranges, and access restrictions, including cited threats, force-protection requirements, and strategic posture assessments.

2. Pillar 2: Hydropolitics & Environmental Data
   - Map the Northern Guam Lens Aquifer, primary production wells, and Fena Valley Reservoir managed jointly or independently by the Guam Waterworks Authority and Navy Public Works with WGS84 coordinates.
   - Report per-capita daily water consumption (L/c/d) for military versus civilian populations compared against WHO reference standards (100 L/c/d).
   - Document agricultural land percentage, arable land loss due to military firing-range construction (Mason Live-Fire Training Range Complex at Ritidian), and total food import dependency percentage.
   - Document environmental degradation incidents: PFAS contamination in NGLA monitoring wells, clearing of native limestone forest acreage, DoD cleanup justifications versus local EPA/GEPA findings. Keep official justifications and local findings separate.

3. Pillar 3: Infrastructure & Economic Data
   - Spectrum & Airspace: FCC regulated spectrum allocations, FAA controlled commercial and military airspace corridors (Andersen AFB), and commercial telecommunications undersea cable landing sites (Tanguisson, Piti) with WGS84 coordinates.
   - Maritime & Ports: Total claimed EEZ, commercial port capacity at Port Authority of Guam (Cabras Island / Apra Harbor), and Jones Act coastwise shipping trade enforcement parameters. Document official federal justification for Jones Act application.
   - Checkpoints & Access Restrictions: List named military access gates requiring Defense Biometric Identification System credentials with WGS84 coordinates. Document official force-protection rationales.
   - Currency & Energy: Official currency (USD), Guam Power Authority grid self-sufficiency percentage, and fuel import dependency percentage for power generation plants.

4. Pillar 4: Legal & Administrative Friction
   - Enforced System: Detail 48 U.S.C. Chapter 8A (The Organic Act of Guam, 1950), federal eminent domain takings (Naval Military Government Land Acquisition Orders 1948–1950), and Article IV, Section 3 of the U.S. Constitution (Territory Clause).
   - Document federal court rulings enforcing federal jurisdiction over local programs: Davis v. Guam (striking down Chamorro-only plebiscite under the 15th Amendment) and Guam v. United States (Superfund cleanup litigation). Include the official federal legal rationales.
   - Direct Statutory Conflict: Cite explicit legal conflicts between U.S. Federal Equal Protection Clause mandates and local Guam statutes (Guam Public Law 22-143 establishing the Chamorro Land Trust Commission, and 21 GCA Chapter 75 restricting ancestral leases).
   - Report the total population subject to federal statutory authority without federal voting representation in the U.S. Congress.

Return all data as a structured JSON block strictly matching the Standardized Great GASPI JSON Schema. If a specific data point is missing from official records, output "data not available".
=== END PROMPT 15 ===

---

## Prompt 16
**Perspective:** CHamoru Land Rights / Decolonization Advocates / Chamorro Land Trust Commission  
**Language:** English (with CHamoru terms)

=== START PROMPT 16 ===
Act as an independent geographic, ancestral-domain, and human-rights researcher. Your mission is to collect documentary evidence, field data, and verified official figures regarding Guåhan (Guam) from the records of the Chamorro Land Trust Commission, Guam Ancestral Lands Commission, I Liheslaturan Guåhan (Guam Legislature), and native land-defense movements (Prutehi Litekyan / Save Ritidian).

Do not perform qualitative evaluations or assign ratings. Collect specific numbers, WGS84 coordinates, and explicit statutory citations. If a specific data point is not available, output "data not available".

1. Pillar 1: Physical Geography & Demographics
   - Document ancestral lands, sacred sites, and condemned properties (Litekyan / Ritidian, Pagat, Sumay, Jinapsan and others) with WGS84 coordinates and elevation in meters.
   - For every high-ground or sacred elevated feature include a functional strategic description based solely on topography: observation control, fire control, movement-corridor control, and position relative to water resources or traditional use areas. Do not attribute intent.
   - Determine total land area (approximately 544 sq km), proportion of land taken by U.S. military condemnation after WWII, and remaining land available for CHamoru housing and agriculture. Explicitly note which strategic or sacred features fall under military versus ancestral jurisdiction.
   - Collect demographic data from the Guam Department of Public Health and local agencies: native CHamoru population displacement, poverty rates, and population density per sq km.
   - Map military fences and firing ranges cutting off access to ancestral fishing grounds and forests with WGS84 coordinates and lengths.
   - Document local and CHamoru characterizations of military land takings, access restrictions, and displacement, together with data on lost ancestral access.

2. Pillar 2: Hydropolitics & Ancestral Resources
   - Map the Northern Guam Lens Aquifer, local GWA production wells, and contamination threat zones from military firing ranges with WGS84 coordinates.
   - Report daily water consumption constraints on civilian communities during dry seasons versus priority military allocations.
   - Document loss of arable land: destruction of native limestone forest ecosystems at Litekyan, loss of traditional medicinal plants (Åmot CHamoru), and food import dependency.
   - Document environmental degradation incidents: lead contamination risks over the aquifer from the Mason Live-Fire Training Range Complex, open detonation at Tarague Beach, chemical spills. Separate military environmental justifications from local CHamoru protests and EPA violation findings.

3. Pillar 3: Infrastructure & Economic Control
   - Telecommunications & Landings: Undersea fiber-optic cable landings situated on public or ancestral beach zones and local spectrum limitations.
   - Maritime Bottlenecks & Jones Act: Economic cost imposed on local goods by the Merchant Marine Act of 1920, shipping monopoly bottlenecks at Jose D. Leon Guerrero Commercial Port. Document local characterizations of the Jones Act burden.
   - Land Access & Military Checkpoints: List ancestral properties where original land-owning families are barred from entry by DoD security gates with WGS84 coordinates.
   - Currency & Fiscal Dependence: Use of USD, cost of imported fuel for GPA power generation, and military tax exemptions under the Soldiers’ and Sailors’ Civil Relief Act impacting local revenues.

4. Pillar 4: Legal & Administrative Friction
   - Preferred / Customary System: Document the Treaty of Paris (1898) Article IX promises, 21 GCA Chapter 75 (Chamorro Land Trust Act), 21 GCA Chapter 80 (Guam Ancestral Lands Commission Act), and 1 GCA Chapter 21 (Self-Determination Plebiscite Law).
   - Direct Statutory Conflict: Document the direct contradiction between federal court decisions (Davis v. Guam striking down native voting rights under federal equal protection) and native CHamoru statutory rights to ancestral land distribution and self-determination plebiscites under local law.
   - Total native CHamoru population governed under unincorporated territorial status without sovereign land control.

Export all data in a structured JSON block strictly matching the Standardized Great GASPI JSON Schema. If a specific data point is not available, output "data not available".
=== END PROMPT 16 ===

---


--

## Prompt 17
**Perspective:** Russian Federation / Republic of Crimea / Sevastopol authorities  
**Language:** Russian

=== START PROMPT 17 ===
Действуйте как старший геополитический и правовой исследователь. Ваша задача — собрать исключительно фактические и проверенные данные по Республике Крым и городу федерального значения Севастополю с официальной точки зрения государственных органов Российской Федерации, Государственного Совета Республики Крым, Росреестра и Министерства энергетики РФ. Вы должны извлечь первичные документы, федеральные конституционные законы, данные инфраструктурных программ, данные гидротехнических сооружений и официальные обоснования безопасности, охватывая все четыре блока.

Не производите качественных оценок и не ставьте рейтингов. Предоставляйте точные числовые значения, координаты WGS84 и прямые цитаты. Если конкретные данные отсутствуют в официальных источниках, укажите "data not available".

1. Блок 1: Физическая география и демография
   - Укажите ключевые стратегические географические объекты, Крымские горы, гряды и перевалы (Роман-Кош, Ангарский перевал, Сапун-гора, Перекопский перешеек и другие) с координатами WGS84 и высотой в метрах.
   - Для каждого возвышенного пункта или хребта обязательно включите функциональное стратегическое описание, основанное только на топографии: контроль наблюдения, контроль огня, контроль коридоров движения и положение относительно водных ресурсов. Не приписывайте намерений.
   - Извлеките данные об общей площади полуострова (около 27 000 км²), площади административных районов и распределении земель между Республикой Крым и Севастополем. Явно укажите, какие стратегические высоты находятся в каких зонах контроля.
   - Соберите данные Росстата: общая численность населения, этнический состав, показатели естественного и миграционного прироста, плотность населения на км².
   - Зафиксируйте военные и фортификационные объекты: координаты WGS84 Крымского моста, объектов Черноморского флота РФ и ключевых узлов обороны.
   - Задокументируйте официальные обоснования безопасности и стратегической необходимости мер по интеграции, охране границ и военной инфраструктуры, включая угрозы и инциденты, на которые ссылаются власти РФ.

2. Блок 2: Гидрополитика и экологические данные
   - Задокументируйте инфраструктуру Северо-Крымского канала, водохранилищ естественного стока (Симферопольское, Тайганское, Белогорское) и артезианских водозаборов с координатами WGS84.
   - Извлеките данные по объему подачи воды до 2014 года, в период водной блокировки (2014–2022 гг.) и после восстановления работы гидроузлов; суточное потребление воды на душу населения в сравнении со стандартом ВОЗ (100 л/чел/день).
   - Извлеките данные по площади орошаемых земель, урожайности сельскохозяйственных культур и продовольственной самообеспеченности.
   - Зафиксируйте экологические инциденты: засоление почв из-за использования подземных вод, выбросы на заводе «Крымский Титан» в Армянске. Разделяйте официальные меры ликвидации и внешние претензии.

3. Блок 3: Инфраструктура и экономика
   - Связь и частоты: разрешенные стандарты мобильной связи, операторы, использование радиочастотного спектра ГКРЧ и контроль воздушного пространства.
   - Морская зона и порты: портовая инфраструктура (Северная и Южная бухты Севастополя, Евпатория, Феодосия, Керчь), судоходство в Керченском проливе.
   - Пункты пропуска и логистика: нанесите на карту транспортные артерии — автодорогу «Таврида», Крымский мост, КПП на административной границе с координатами WGS84. Задокументируйте официальные обоснования режима пунктов пропуска.
   - Валюта и энергетика: денежное обращение — Российский рубль, энергомост «Кубань — Крым», Таврическая и Балаклавская ПГУ-ТЭС, степень самообеспеченности электроэнергией.

4. Блок 4: Юридические и административные конфликты
   - Применяемая система: детализируйте Федеральный конституционный закон № 6-ФКЗ от 21.03.2014, законы Республики Крым и Указ Президента РФ № 201 от 20.03.2020.
   - Зафиксируйте правовые акты о перерегистрации недвижимости в Росреестре и выдаче российских паспортов, включая официальные правовые обоснования.
   - Прямой правовой конфликт: укажите конкретные статьи законодательства РФ, перекрывающие законодательство Украины и решения международных судов.
   - Укажите численность населения, подпадающего под юрисдикцию законодательства РФ в Крыму.

Выведите все данные в виде структурированного JSON-блока строго по Standardized Great GASPI JSON Schema. Если конкретные данные отсутствуют в официальных источниках, укажите "data not available".
=== END PROMPT 17 ===

---

## Prompt 18
**Perspective:** Ukraine / Representation of the President in the Autonomous Republic of Crimea / Crimean Tatar Mejlis  
**Language:** Ukrainian

=== START PROMPT 18 ===
Дійте як старший геополітичний, правовий та правозахисний дослідник. Ваша місія — зібрати об'єктивні, емпіричні та задокументовані дані щодо Автономної Республіки Крим та міста Севастополя з офіційної позиції державних органів України, Представництва Президента України в АРК, Меджлісу кримськотатарського народу та рішень міжнародних судових інстанцій. Ви мусите витягнути первинні закони, нормативні акти, дані правозахисних моніторингів та інженерні показники по всіх 4 блоках.

Не робіть суб'єктивних оцінок та не ставте рейтингів. Надавайте точні числові значення, координати WGS84 та прямі юридичні цитати. Якщо певні дані відсутні в офіційних українських або міжнародних реєстрах, вкажіть "data not available".

1. Блок 1: Фізична географія та демографія
   - Вкажіть ключові географічні об'єкти, Кримські гори та кримськотатарські історичні топоніми (Qarasuvbazar, Bağçasaray, Aqmescit, Perekop та інші) з координатами WGS84 та висотами в метрах.
   - Для кожного висотного пункту або хребта обов'язково включіть функціональний стратегічний опис, заснований лише на топографії: контроль спостереження, контроль вогню, контроль коридорів руху та положення відносно водних ресурсів. Не приписуйте намірів.
   - Витягніть дані про загальну площу АР Крим (близько 26 081 км²) та Севастополя (близько 864 км²), адміністративний поділ за законодавством України. Явно вкажіть, які стратегічні висоти знаходяться в яких зонах контролю.
   - Зберіть демографічні дані Державної служби статистики України та Меджлісу: демографічні зміни внаслідок заміщення населення, кількість внутрішньо переміщених осіб та щільність населення на км².
   - Зафіксуйте фортифікаційні споруди, мілітаризовані зони та експропрійовані об'єкти з координатами WGS84.
   - Документуйте офіційні позиції України та Меджлісу щодо мілітаризації, експропріації та зміни демографії як наслідків окупації, разом із даними про переміщення.

2. Блок 2: Гідрополітика та екологічні дані
   - Задокументуйте інфраструктуру Північно-Кримського каналу, дамбу в Херсонській області та обсяги перекриття дніпровської води (до 2022 року) з координатами WGS84.
   - Витягніть дані щодо виснаження підземних водоносних горизонтів, засолення ґрунтів у степовому Криму та обмежень споживання води для цивільного населення порівняно зі стандартом ВООЗ (100 л/ос/день).
   - Зафіксуйте втрати сільськогосподарських угідь: скорочення площ зрошуваних земель та показники харчової залежності.
   - Зафіксуйте екологічні катастрофи: хімічний викид на заводі «Кримський Титан» в Армянську, виснаження лісових та заповідних зон, мілітаризацію заповідників. Розділяйте позицію державних органів України та правозахисників від інших обґрунтувань.

3. Блок 3: Інфраструктура та економічний контроль
   - Зв'язок та частоти: незаконне захоплення українських радіочастот, блокування українського мовлення, обмеження доступу до незалежних веб-ресурсів.
   - Морський режим та санкції: закриття Україною морських портів Криму, закриття повітряного простору над Кримом ICAO та санкційний режим у Чорному морі.
   - Незаконне будівництво та мілітаризація: експропріація державного та приватного майна України, будівництво мосту через Керченську протоку з координатами WGS84. Документуйте офіційні українські характеристики цих дій.
   - Валюта та економічний тиск: примусове вилучення гривні, витіснення українських банків та збитки від втрати надр на шельфі Чорного моря.

4. Блок 4: Юридичний та адміністративний конфлікт
   - Переважна / законна система: деталізуйте Конституцію України, Закон України «Про забезпечення прав і свобод громадян та правовий режим на тимчасово окупованій території України» (№ 1207-VII) та Закон України «Про корінні народи України».
   - Документуйте рішення Міжнародного Суду ООН, накази про тимчасові заходи та рішення ЄСПЛ у справах Україна проти Росії (щодо Криму).
   - Прямий правовий конфлікт: задокументуйте пряму суперечність між російськими указами про вилучення землі та примусову мобілізацію і нормами 4-ї Женевської конвенції 1949 року та Кримінального кодексу України.
   - Загальна кількість громадян України в Криму, які піддаються примусовій правовій інтеграції та переслідуванням (зокрема заборона Меджлісу у 2016 році).

Сформуйте вихідний JSON у форматі Standardized Great GASPI JSON Schema. Якщо певні дані відсутні в офіційних українських або міжнародних реєстрах, вкажіть "data not available".
=== END PROMPT 18 ===

---

## Prompt 19
**Perspective:** Union Government of India / Ministry of Home Affairs / Jammu & Kashmir UT Administration  
**Language:** English

=== START PROMPT 19 ===
Act as a senior geopolitical and constitutional law researcher. Your mission is to collect strictly factual and objective empirical data for the Union Territory of Jammu & Kashmir from the official perspective of the Government of India, the Ministry of Home Affairs, the Civil Administration of J&K, and Indian statutory records. You must extract primary parliamentary acts, Supreme Court judgments, hydrological treaty filings, infrastructure development projects, and official security justifications, covering all four pillars.

Do not perform qualitative evaluations or assign ratings. Provide explicit numerical values, range estimates, WGS84 coordinates, and direct legal citations. If a specific data point is missing from official Indian records, output "data not available".

1. Pillar 1: Physical Geography & Demographics
   - List key geographic features, mountain passes, and strategic high ground (Zoji La, Banihal Pass, Pir Panjal Range, Siachen Glacier, Line of Control and others) with WGS84 coordinates and elevation in meters.
   - For every high-ground feature include a functional strategic description based solely on topography: observation control, fire control, movement-corridor control, and position relative to water resources or critical infrastructure. Do not attribute intent.
   - Extract total land area of the Union Territory of J&K under Indian administration (approximately 55 538 sq km), accessible land area, and administrative division across 20 districts. Explicitly note which strategic features fall under which security or administrative zones.
   - Collect Census of India demographic data: total UT population, religious demographic breakdown, density per sq km, and new domicile certificate issuance numbers post-2019.
   - Map physical security barriers, fencing along the Line of Control (Anti-Infiltration Obstacle System), military cantonments, and police checkpoints with WGS84 coordinates and total fence length.
   - Document the official security justifications of the Government of India and security forces for the LoC fencing, checkpoints, and special security measures, including cited threats, infiltration attempts, and attack data that preceded or motivated these measures.

2. Pillar 2: Hydropolitics & Environmental Data
   - Map primary rivers and basins under the Indus Waters Treaty (1960) (Indus, Jhelum, Chenab) and major run-of-the-river hydroelectric projects (Kishanganga, Baglihar, Dul Hasti, Ratle) with WGS84 coordinates and megawatt capacity.
   - Report daily per-capita water availability (L/c/d) across urban versus rural districts compared against WHO reference standards (100 L/c/d).
   - Document agricultural parameters: arable land percentage, apple orchard acreage, saffron cultivation areas in Pampore, and food import dependency percentage from other Indian states.
   - Document environmental degradation incidents: Dal Lake and Wular Lake siltation/eutrophication, deforestation in the Pir Panjal range, military land occupation impacts. Separate official pollution-control justifications from local civil concerns.

3. Pillar 3: Infrastructure & Economic Data
   - Spectrum & Communications: TRAI regulated cellular technology standards (transition from 2G caps to 4G/5G rollout post-2021), internet shutdown orders issued under the Temporary Suspension of Telecom Services Rules (2017), and airspace control. Document official security justifications for temporary telecom suspensions.
   - Transport & Mobility: Map primary transit corridors — Jammu-Srinagar National Highway (NH-44), Chenab Rail Bridge, Kazi Gund-Banihal tunnel with WGS84 coordinates and transit capacity.
   - Checkpoints & Security Controls: List major security transit checkpoints requiring specific identity verification. Document official security rationales.
   - Currency & Fiscal Integration: Official currency Indian Rupee, direct fiscal transfers from the Central Government, power grid integration with the Northern Regional Grid, and hydroelectric royalty structures.

4. Pillar 4: Legal & Administrative Friction
   - Enforced System: Detail the Jammu and Kashmir Reorganisation Act, 2019, Presidential Orders C.O. 272 and C.O. 273 (revoking Article 370 and Article 35A), and application of central laws across the UT. Include the official constitutional and security rationales presented by the Union Government.
   - Document the landmark Supreme Court of India Constitution Bench judgment (December 2023) upholding the constitutional validity of the revocation of Article 370, including the official legal arguments accepted by the Court.
   - Direct Statutory Conflict: Cite explicit statutory changes where central Indian legislation (such as the J&K Development Act amendments opening land ownership to non-domiciles) superseded pre-existing state laws (1938 J&K Alienation of Land Act, Big Land Estates Abolition Act of 1950).
   - Report the total population governed under the Union Territory administration and special security acts (AFSPA, Public Safety Act).

Return all data as a structured JSON block strictly matching the Standardized Great GASPI JSON Schema. If a specific data point is missing from official Indian records, output "data not available".
=== END PROMPT 19 ===

---

## Prompt 20
**Perspective:** Local Kashmiri Advocates / Jammu & Kashmir Coalition of Civil Society / High Court Bar Association perspective  
**Language:** English (with Urdu terms where appropriate)

=== START PROMPT 20 ===
Act as an independent geographic, legal, and anti-injustice researcher. Your mission is to collect authentic, documentary, and field data regarding Jammu & Kashmir from the records of the local legal community, High Court Bar Association, Jammu & Kashmir Coalition of Civil Society, and local rights organizations.

Do not perform any subjective assessment or assign ratings. Provide only clear numerical data, WGS84 coordinates, and explicit legal clauses. If a specific data point is not available, write "data not available".

1. Pillar 1: Physical Geography & Demographic Change
   - List key strategic locations in the Kashmir Valley and Jammu, mountain passes, and occupied or controlled lands (Pir Panjal, Zoji La, Gulmarg, Budgam, and others) with WGS84 coordinates and elevation in meters.
   - For every high-ground feature include a functional strategic description based solely on topography: observation control, fire control, movement-corridor control, and position relative to water resources. Do not attribute intent.
   - Determine total area under administration (approximately 55 538 sq km), land available for use by local residents, and data on domicile certificates issued to non-locals after 2019. Explicitly note which strategic features fall under which security zones.
   - Record population of Jammu & Kashmir, changes in the proportion of local Kashmiri Muslim and other communities, and population density per sq km.
   - List military cantonments, sieges, high-security zones, and barriers established on lands with WGS84 coordinates and lengths.
   - Document local characterizations of military presence, high-security zones, and land control, together with data on displacement and restricted access.

2. Pillar 2: Hydropolitics & Environmental Damage
   - Record data on local water scarcity linked to hydroelectric projects on the Jhelum, Chenab, and Indus under the Indus Waters Treaty (Kishanganga, Baglihar, Ratle) with WGS84 coordinates.
   - Compare daily per-capita water availability (L/c/d) for the local population against the WHO standard of 100 L/c/d.
   - Scientific data on conversion of apple orchards and saffron cultivation land (Pampore) due to military occupation or highway projects.
   - Environmental pollution: destruction of Dal Lake and Wular Lake, deforestation. Separate official justifications of the Indian administration from local farmers’ and institutions’ concerns.

3. Pillar 3: Infrastructure & Economic Control
   - Communication and internet suspension: the longest internet shutdown lasting 552 days after 5 August 2019 (2G/4G suspension), violations of communication rights, and digital control. Document local characterizations of these measures.
   - Means of transport: restrictions on civilian movement during security convoys on National Highway NH-44, blockades, and fencing with WGS84 coordinates.
   - Checkposts: security checkpoints established for checking local civilians and search zones under the Public Safety Act and AFSPA.
   - Currency and natural resources: Indian Rupee, transfer of electricity outside the Valley by NHPC and NEPRA, and data on local electricity deficits.

4. Pillar 4: Legal & Constitutional Conflict
   - Preferred / local legal framework: previous Article 370 of the Indian Constitution, Article 35A, the Constitution of Jammu & Kashmir (1956), and the 1950 Land Reforms Act (Big Land Estates Abolition Act).
   - Direct legal conflict: clause-by-clause conflict between the Jammu and Kashmir Reorganisation Act 2019 and amendments to the Land Revenue Act (which allowed non-residents to purchase land) and the traditional land rights of local Kashmiri residents under Article 35A.
   - Total population in Jammu & Kashmir under the Public Safety Act, Unlawful Activities (Prevention) Act, and AFSPA who are detained or affected.

Present all data in a JSON block matching the Standardized Great GASPI JSON Schema. If any specific data is not available, write "data not available".
=== END PROMPT 20 ===

---

*End of Batch 5 (Prompts 17–20). Continue with Batch 6 for Prompts 21–24.*
--

## Prompt 21
**Perspective:** Republic of Indonesia / Central Government / Ministry of Home Affairs & ESDM (West Papua)  
**Language:** Indonesian (Bahasa Indonesia)

=== START PROMPT 21 ===
Bertindaklah sebagai peneliti geopolitik dan hukum pemerintahan senior. Tugas Anda adalah mengumpulkan data empiris yang sepenuhnya faktual dan terverifikasi mengenai wilayah Papua (Provinsi Papua, Papua Barat, Papua Selatan, Papua Tengah, Papua Pegunungan, dan Papua Barat Daya) dari perspektif resmi Pemerintah Republik Indonesia, Kementerian Koordinator Bidang Politik, Hukum, dan Keamanan, Kementerian ESDM, dan dokumen perundang-undangan nasional. Anda harus mengekstrak dokumen primer, undang-undang, izin usaha pertambangan, data pembangunan infrastruktur, dan justifikasi keamanan resmi, mencakup seluruh 4 Pilar.

Dilarang melakukan penilaian kualitatif atau memberikan pemeringkatan. Sediakan nilai numerik yang pasti, rentang perkiraan, koordinat WGS84, dan kutipan hukum langsung. Jika data tertentu tidak tersedia dalam catatan resmi pemerintah, tuliskan "data not available".

1. Pilar 1: Geografi Fisik dan Demografi
   - Daftarkan fitur geografis strategis, pegunungan tinggi, dan wilayah perbatasan (Pegunungan Jayawijaya, Puncak Jaya, Lembah Baliem, wilayah perbatasan RI-PNG di Skouw dan lainnya) beserta koordinat WGS84 dan ketinggian (m).
   - Untuk setiap fitur high ground wajib sertakan deskripsi strategis fungsional yang hanya didasarkan pada topografi: kontrol observasi, kontrol tembakan, kontrol koridor pergerakan, dan posisi relatif terhadap sumber air atau infrastruktur kritis. Jangan menisbatkan niat.
   - Ekstrak total luas wilayah daratan Papua (sekitar 418.707 km²), pembagian administratif 6 provinsi hasil pemekaran, dan luas wilayah yang terintegrasi secara administratif. Nyatakan secara eksplisit fitur strategis mana yang berada di zona kontrol mana.
   - Kumpulkan data demografi Badan Pusat Statistik: total populasi, komposisi Penduduk Asli Papua (PAP) vs. non-PAP, dan kepadatan penduduk per km².
   - Petakan pos pengamanan perbatasan (Satgas Pamtas RI-PNG), benteng pertahanan, dan pos TNI/Polri beserta koordinat WGS84.
   - Dokumentasikan justifikasi keamanan resmi pemerintah untuk operasi pengamanan, pos-pos, dan pembatasan akses, termasuk ancaman dan insiden yang dirujuk oleh pihak berwenang.

2. Pilar 2: Hidropolitik dan Data Lingkungan
   - Petakan sungai-sungai utama (Sungai Mamberamo, Sungai Digul, Sungai Ajkwa) dan cekungan air tanah beserta koordinat WGS84.
   - Dokumentasikan alokasi pertambangan PT Freeport Indonesia (Tambang Grasberg / Ertsberg): luas konsesi (IUPK), kapasitas produksi tembaga/emas, dan lokasi pembuangan sisa pasir tambang (tailing) di sistem Sungai Ajkwa/ModADA.
   - Kumpulkan data konsumsi air harian per kapita (L/c/d) dibandingkan dengan standar acuan WHO (100 L/c/d).
   - Dokumentasikan data sektor pertanian/kehutanan: luas lahan pertanian, konsesi Kawasan Hutan yang dilepas untuk Proyek Strategis Nasional, dan klaim pemulihan lingkungan oleh KLHK. Pisahkan justifikasi resmi dari temuan pihak lain.

3. Pilar 3: Infrastruktur dan Ekonomi
   - Telekomunikasi & Spektrum: teknologi seluler yang diizinkan oleh Kementerian Kominfo (3G/4G/5G), proyek Palapa Timur serat optik, dan pengawasan ruang udara.
   - Transportasi & Jalur Logistik: petakan koridor Jalan Trans-Papua, pelabuhan komersial (Pelabuhan Jayapura, Sorong, Merauke), dan bandara strategis beserta koordinat WGS84.
   - Pos Pemeriksaan & Keamanan: daftar pos pemeriksaan keamanan internal di wilayah rawan konflik beserta koordinat WGS84 dan dokumen perizinan melintas. Dokumentasikan justifikasi resmi.
   - Mata Uang & Fiskal: mata uang resmi Rupiah (IDR), alokasi Dana Otonomi Khusus berdasarkan UU No. 2 Tahun 2021, dan kontribusi penerimaan negara bukan pajak dari sektor migas/tambang.

4. Pilar 4: Gesekan Hukum dan Administratif
   - Sistem yang Diberlakukan: rincikan UU No. 2 Tahun 2021 tentang Perubahan Kedua atas UU No. 21 Tahun 2001 tentang Otonomi Khusus Bagi Provinsi Papua, UU Pokok Agraria (UU No. 5 Tahun 1960), dan penetapan Kawasan Hutan Negara. Sertakan justifikasi hukum resmi.
   - Dokumentasikan putusan Mahkamah Konstitusi terkait pengujian UU Otsus dan legalitas pembentukan daerah otonom baru.
   - Konflik Hukum Langsung: tunjukkan pertentangan pasal secara eksplisit antara hukum agraria nasional yang menetapkan Kawasan Hutan Negara atas tanah Papua dan pengakuan Hak Ulayat berdasarkan hukum adat setempat.
   - Tentukan jumlah populasi yang tunduk pada hukum nasional dan rezim pengamanan otonomi khusus.

Kembalikan seluruh data sebagai blok JSON terstruktur yang ketat sesuai dengan GASPI Schema v2 (Dual-Steel-Man). Jika data tertentu tidak tersedia dalam catatan resmi pemerintah, tuliskan "data not available".
=== END PROMPT 21 ===

---

## Prompt 22
**Perspective:** Indigenous Papuan Customary Council (Dewan Adat Papua) / Majelis Rakyat Papua / Rights Advocates  
**Language:** English (with Indonesian/Papuan terms)

=== START PROMPT 22 ===
Act as an independent geographic, customary-domain, and human-rights researcher. Your mission is to collect documentary evidence, field measurements, and verified official records regarding West Papua from the archives of the Customary Council of Papua (Dewan Adat Papua), the Papuan People’s Assembly (MRP), local legal-aid institutions (LBH Papua), and human-rights monitoring reports.

Do not perform qualitative evaluations or assign ratings. Collect specific numbers, WGS84 coordinates, and explicit statutory citations. If a specific data point is not available, output "data not available".

1. Pillar 1: Physical Geography & Demographics
   - Document customary ancestral territories, sacred mountains, and displacement zones (Nduga Regency, Intan Jaya, Puncak, Maybrat and others) with WGS84 coordinates and elevation in meters.
   - For every high-ground or sacred elevated feature include a functional strategic description based solely on topography: observation control, fire control, movement-corridor control, and position relative to water resources or traditional use areas. Do not attribute intent.
   - Determine total land area (approximately 418 707 sq km), proportion of land claimed under ancestral clan boundaries (Tanah Adat / Hak Ulayat), and forest area converted for palm oil and food estates. Explicitly note which strategic or sacred features fall under which control regimes.
   - Collect demographic data on indigenous Papuans (OAP): population growth disparities, internal displacement numbers due to security operations, and population density per sq km.
   - Map military posts, security checkpoints, and restricted access zones cutting through customary indigenous lands with WGS84 coordinates.
   - Document local and customary characterizations of military posts, checkpoints, and land conversion, together with data on displacement and lost access.

2. Pillar 2: Hydropolitics & Ancestral Resources
   - Map major rivers impacted by industrial extraction (Ajkwa River, Aikwa delta, Lorentz National Park border zone) with WGS84 coordinates.
   - Report environmental degradation data from mining: daily deposition tonnage of tailings from PT Freeport Indonesia into the Ajkwa deposition area, riverbed sedimentation area, and loss of potable water sources for Kamoro and Amungme indigenous communities.
   - Collect agricultural data: loss of traditional sago forests and customary gardens due to the Merauke Integrated Food and Energy Estate / Sugar Estate projects.
   - Document environmental degradation incidents: toxic heavy-metal accumulation in local water basins, deforestation acreage. Separate state environmental clearances from local tribal and NGO contamination documentation.

3. Pillar 3: Infrastructure & Economic Control
   - Telecommunications & Digital Shutdowns: documented internet throttling/blackouts in Papua, cellular-tower military guards, and communication surveillance. Document local characterizations of these measures.
   - Transport Bottlenecks: Trans-Papua Highway segments constructed through customary land without free, prior, and informed consent; commercial transport monopolies.
   - Mobility Restrictions & Checkpoints: List security checkposts where indigenous Papuans require special travel permits (Surat Jalan) or identity verification to access their own customary lands with WGS84 coordinates.
   - Currency & Wealth Extraction: Use of Indonesian Rupiah, resource revenue flight versus local poverty percentages among indigenous Papuans.

4. Pillar 4: Legal & Administrative Friction
   - Preferred / Customary System: Document customary land laws (Hak Ulayat), tribal dispute mechanisms, Article 18B(2) of the 1945 Indonesian Constitution, and the UN Declaration on the Rights of Indigenous Peoples.
   - Direct Statutory Conflict: Document the direct contradiction between National Forest Area designations (UU No. 41/1999) and revised Special Autonomy amendments (UU No. 2/2021) which allow central land acquisition, against local customary land ownership (Hak Ulayat) protected under ancestral law and MRP decrees.
   - Total indigenous Papuan population subject to military security operations and non-consensual provincial restructuring.

Export all data in a structured JSON block strictly matching GASPI Schema v2 (Dual-Steel-Man). If a specific data point is not available, output "data not available".
=== END PROMPT 22 ===

---

## Prompt 23
**Perspective:** PRC Central Government / Xinjiang Uyghur Autonomous Region (XUAR) Authorities / XPCC  
**Language:** Mandarin Chinese (简体中文)

=== START PROMPT 23 ===
扮演一名高级地缘政治与公共行政法学研究员。你的任务是从中华人民共和国中央人民政府、新疆维吾尔自治区人民政府、新疆生产建设兵团及国家发展和改革委员会的官方视角，收集关于新疆维吾尔自治区的客观、可验证的实证数据。你必须提取一手法律法规、兵团行政建制文件、重点基础设施与农业产值数据、人口普查统计、官方安全与去极端化治理理由，全面覆盖全部四个核心要素。

切勿进行任何主观定性评价或评分。请提供具体的数值、范围估计、WGS84地理坐标及直接的法律/法规引用。若某项特定数据在官方公开记录中缺失，请明确注明 "data not available"。

1. 要素一：物理地理与人口数据
   - 列出战略性地形、山脉、盆地及边境口岸（天山山脉、阿尔泰山脉、昆仑山脉、塔里木盆地、准噶尔盆地、霍尔果斯、阿拉山口口岸等），并附带 WGS84 坐标和海拔高度（米）。
   - 对于每一个高地或山脊，必须包含仅基于地形的功能性战略描述：观察控制、火力控制、移动走廊控制，以及相对于水资源或关键基础设施的位置。不要归因意图。
   - 提取新疆维吾尔自治区总面积（约166.49万平方公里）、兵团辖区土地划拨与行政管辖数据。明确指出哪些战略高地属于哪些管辖或管控区域。
   - 收集国家统计局与自治区统计局人口普查数据：全区常住人口总量、维吾尔族及其他少数民族人口数量、汉族人口数量、兵团人口总量，以及每平方公里的人口密度。
   - 绘制边境管控设施、一体化联合作战平台治安检查站与边境防护网：WGS84 坐标、管控范围及兵地融合发展网格。
   - 记录官方安全与去极端化治理理由：反恐、去极端化条例实施以及相关管控措施的正式依据与威胁评估。

2. 要素二：水文政治与环境数据
   - 记录主要水系与内陆/跨界河流（塔里木河、伊犁河、额尔齐斯河、乌伦古河）的水文位置与输水量。
   - 绘制重大水利基础设施：额尔齐斯河-塔里木河调水工程、阿尔塔什水利枢纽、坎儿井保护区，标注 WGS84 坐标与蓄水容量。
   - 收集人均日用水量以及兵团农牧场高效节水灌溉农田面积比例、棉花与番茄种植面积比例。
   - 记录环境治理与沙漠化整治项目：塔克拉玛干沙漠边缘绿化工程、土壤盐碱化治理措施。将官方理由与外部质疑分开记录。

3. 要素三：基础设施与经济数据
   - 电信与频谱管理：工信部许可的 3G/4G/5G 网络建设、网络安全与数据管理规定，以及乌鲁木齐地窝堡国际机场、喀什徕宁国际机场等空域管控规则。
   - 交通与西向开放通道：兰新高铁、南疆铁路、连霍高速、塔里木沙漠公路，标注 WGS84 坐标与货运通关能力。
   - 陆路口岸与物流枢纽：霍尔果斯口岸、阿拉山口口岸、吐尔尕特口岸的 WGS84 坐标及中欧班列集结中心通关数据。记录官方对口岸管控的安全与经济理由。
   - 货币与能源基建：人民币流通数据、西气东输工程气源地、特高压直流输电工程及兵团电力网络自给率。

4. 要素四：法律与行政摩擦
   - 实施法律体系：详细阐述《中华人民共和国宪法》、《中华人民共和国反恐怖主义法》、《新疆维吾尔自治区去极端化条例》及《新疆维吾尔自治区实施〈反恐怖主义法〉办法》。记录官方立法与实施理由。
   - 记录新疆生产建设兵团党政军企合一体制的法定行政授权与兵团城市设市法律依据。
   - 直接法律冲突：对比自治区自治条例、反恐/去极端化法规与传统宗教习俗及外部权利主张之间的分歧，并记录官方立场。
   - 列出受反恐法规与去极端化条例规范的区域总人口数。

将所有数据严格按照 GASPI Schema v2 (Dual-Steel-Man) 格式整合并返回 JSON 模块。若某项特定数据在官方公开记录中缺失，请明确注明 "data not available"。
=== END PROMPT 23 ===

---

## Prompt 24
**Perspective:** Uyghur Rights Preservation / World Uyghur Congress / Diaspora Archives  
**Language:** English (with Uyghur terms where appropriate)

=== START PROMPT 24 ===
Act as an independent journalist, human-rights researcher, and geographic investigator. Your mission is to collect reliable, documented data on land, human rights, re-education facilities, and forced labour in the Xinjiang Uyghur Autonomous Region (East Turkestan) from the archives of the Uyghur Human Rights Project, World Uyghur Congress, human-rights monitoring organisations, and East Turkestan archives.

Provide only clear numerical data, WGS84 coordinates, and legal clauses. Do not assign any ratings. If certain data are not present in the archives, write "data not available".

1. Pillar 1: Geographic Location & Population Data
   - List historical Uyghur territories, sacred cemeteries, mosques, and disappeared villages (Kashgar, Hotan, Aksu, Ghulja, Atush and others) with WGS84 coordinates and elevation.
   - For every elevated or sacred site include a functional strategic description based solely on topography: observation control, fire control, movement-corridor control, and position relative to water resources. Do not attribute intent.
   - Total land area (approximately 1.66 million km²), land occupied by the Xinjiang Production and Construction Corps (Bingtuan), and land remaining under Uyghur population use. Explicitly note which strategic features fall under which control regimes.
   - Uyghur and other local ethnic population numbers, demographic change, number of relocated Han population, and population density per km².
   - Re-education camps (vocational education and training centres), prisons, and checkpoint locations with WGS84 coordinates and scale.
   - Document diaspora and rights-organisation characterisations of camps, checkpoints, and demographic change, together with available quantitative data.

2. Pillar 2: Water Politics & Resource Appropriation
   - Water-resource allocation in the Tarim Basin, Ili River, and the dried Lop Nur lake with WGS84 coordinates.
   - Volume of water used by Bingtuan cotton and energy bases versus restrictions on Uyghur farmers’ water use.
   - Forced labour and cotton fields: number of local people placed in forced labour, proportion of local farmers separated from their land.
   - Environmental and natural-resource damage: Tarim oil field, coal bases. Separate Chinese government land-reclamation justifications from Uyghur organisations’ ecological and land-loss evidence.

3. Pillar 3: Infrastructure & Digital Harm
   - Digital surveillance and communication restrictions: Integrated Joint Operations Platform, facial-recognition camera systems, blocking of Uyghur-language websites, and internet restrictions. Document local/diaspora characterisations.
   - Road and rail connections that link forcibly relocated families and production bases.
   - Checkpoints: scanning and monitoring points required for residents to leave home or travel between cities with WGS84 coordinates.
   - Currency and resource transfer: use of Chinese yuan, proportion of oil, cotton and other resources transferred to inland Chinese provinces.

4. Pillar 4: Legal & Educational Conflicts
   - Active laws: “Maintaining Stability”, “Counter-Terrorism Law”, and “De-extremification Regulations” and the harm they have caused to Uyghur religious, cultural and land rights.
   - Counter-posed legal materials: Beijing government’s obligations under the autonomy law, human-rights documents, and UN human-rights assessment reports.
   - Legal contradiction: conflict between China’s “De-extremification Regulations” and Uyghurs’ rights to custom, religious belief, and mother-tongue education.
   - Total Uyghur population living under the surveillance and camp system.

Export all data in a structured JSON block strictly matching GASPI Schema v2 (Dual-Steel-Man). If certain data are not present in the archives, write "data not available".
=== END PROMPT 24 ===

---

*End of Batch 6 (Prompts 21–24). Continue with Batch 7 for Prompts 25–28.*
--

## Prompt 25
**Perspective:** French State / High Commission of the Republic in New Caledonia / Government of New Caledonia  
**Language:** French

=== START PROMPT 25 ===
Agissez en tant que chercheur géopolitique et juridique senior. Votre mission est de collecter des données factuelles et vérifiables concernant la Nouvelle-Calédonie et dépendances du point de vue officiel de l’État français, du Haut-Commissariat de la République, du Gouvernement de la Nouvelle-Calédonie et des institutions compétentes. Vous devez extraire des documents primaires, des lois organiques, des Accords de Nouméa, des données d’infrastructures minières et des justifications sécuritaires officielles, en couvrant intégralement les quatre piliers.

Ne procédez à aucune évaluation qualitative ni attribution de notes. Fournissez des valeurs numériques, des coordonnées WGS84 et des citations directes. Si une donnée n’est pas disponible dans les sources officielles, inscrivez "data not available".

1. Pilier 1 : Géographie physique et démographie
   - Listez les reliefs stratégiques, massifs miniers et zones côtières (Massif du Sud, Chaîne Centrale, Île des Pins, archipel des Belep et autres) avec coordonnées WGS84 et altitudes en mètres.
   - Pour chaque relief ou point élevé, incluez obligatoirement une description stratégique fonctionnelle fondée uniquement sur la topographie : contrôle de l’observation, contrôle du feu, contrôle des corridors de mouvement, et position relative aux ressources hydriques ou infrastructures critiques. N’attribuez aucune intention.
   - Extrayez la superficie totale (environ 18 575 km²), la répartition entre Grande Terre, Îles Loyauté et îles dépendantes, et le découpage en provinces (Sud, Nord, Îles Loyauté). Précisez explicitement quels reliefs stratégiques se trouvent dans quelles zones de contrôle.
   - Collectez les données démographiques de l’ISEE et de l’INSEE : population totale, répartition Kanak / Européens / Wallisiens-Futuniens / autres, et densité au km².
   - Cartographiez les installations de sécurité, casernes et zones de contrôle des forces de l’ordre avec coordonnées WGS84.
   - Documentez la justification sécuritaire officielle des dispositifs de maintien de l’ordre et des restrictions d’accès, y compris les menaces et incidents cités par les autorités françaises.

2. Pilier 2 : Hydropolitique et données environnementales
   - Documentez les bassins hydrographiques de la Grande Terre, les retenues d’eau et les stations de traitement avec coordonnées WGS84.
   - Relevez les données d’exploitation minière du nickel (SLN, Koniambo, Goro) : volumes d’extraction, sites de stockage de résidus et permis environnementaux.
   - Collectez la consommation d’eau quotidienne par habitant et la part des terres agricoles et coutumières.
   - Documentez les incidents environnementaux liés à l’activité minière et à l’érosion. Séparez clairement la justification officielle des rapports d’organisations locales.

3. Pilier 3 : Infrastructures et économie
   - Télécommunications : couverture réseau (3G/4G/5G) par les opérateurs agréés et gestion de l’espace aérien (aéroport de La Tontouta).
   - Maritime et ports : ports de Nouméa et de Prony, ZEE et activité de pêche.
   - Postes de contrôle et mobilité : cartographiez les points de contrôle et les restrictions de circulation lors des périodes de tension avec coordonnées WGS84. Documentez la justification officielle.
   - Monnaie et énergie : utilisation du Franc CFP, raccordement au réseau électrique et projets d’énergies renouvelables.

4. Pilier 4 : Friction juridique et statutaire
   - Système appliqué : détaillez la loi organique n° 99-209 du 19 mars 1999 relative à la Nouvelle-Calédonie, les Accords de Nouméa (1998) et le partage des compétences entre l’État et le pays.
   - Documentez le corps électoral spécial, les listes électorales gelées et les résultats des référendums d’autodétermination (2018, 2020, 2021). Incluez les justifications juridiques officielles de l’État.
   - Identifiez le conflit statutaire direct : opposez les dispositions de la loi organique et du corps électoral spécial aux revendications d’élargissement du corps électoral et d’indépendance formulées par les organisations kanakes.
   - Indiquez la population régie par le statut particulier de la Nouvelle-Calédonie.

Restituez l’ensemble des données sous forme de bloc JSON conforme au Great GASPI Data Schema. Si une donnée n’est pas disponible, inscrivez "data not available".
=== END PROMPT 25 ===

---

## Prompt 26
**Perspective:** FLNKS / Kanak Customary Authorities / Customary Senate  
**Language:** French

=== START PROMPT 26 ===
Agissez en tant que chercheur indépendant en géographie, droit coutumier et autodétermination. Votre mission est de collecter des données documentaires, des preuves de terrain et des chiffres officiels vérifiés concernant la Nouvelle-Calédonie du point de vue des autorités coutumières kanakes, du Sénat coutumier, du FLNKS et des organisations de défense des droits kanaks.

Ne procédez à aucune évaluation qualitative ni attribution de notes. Fournissez des valeurs numériques, des coordonnées WGS84 et des citations juridiques explicites. Si une donnée n’est pas disponible, inscrivez "data not available".

1. Pilier 1 : Géographie physique et démographie
   - Documentez les terres coutumières, les sites sacrés et les massifs miniers (aires coutumières, chefferies, massifs du Nord et du Sud) avec coordonnées WGS84 et altitudes.
   - Pour chaque relief ou site élevé, incluez obligatoirement une description stratégique fonctionnelle fondée uniquement sur la topographie : contrôle de l’observation, contrôle du feu, contrôle des corridors de mouvement, et position relative aux ressources hydriques ou aux usages traditionnels. N’attribuez aucune intention.
   - Déterminez la superficie totale, la proportion de terres relevant du régime coutumier et la répartition entre provinces. Précisez explicitement quels reliefs stratégiques se trouvent dans quelles zones de contrôle coutumier ou administratif.
   - Collectez les données démographiques sur la population kanake, les taux de chômage et la densité de population.
   - Cartographiez les installations minières et les zones d’exclusion qui affectent les terres coutumières avec coordonnées WGS84.
   - Documentez les caractérisations officielles kanakes et coutumières des dispositifs de sécurité, des listes électorales et de l’exploitation minière, ainsi que les données de déplacement ou de perte d’accès.

2. Pilier 2 : Hydropolitique et ressources coutumières
   - Cartographiez les sources d’eau, les rivières et les zones de pêche coutumières impactées par l’activité minière avec coordonnées WGS84.
   - Relevez les données de pollution et de destruction de milieux liées aux résidus miniers (Goro, Koniambo, SLN).
   - Collectez les données sur la perte de terres agricoles et de forêts coutumières.
   - Documentez les incidents environnementaux et les revendications de réparation. Séparez les justifications des opérateurs miniers et de l’État des caractérisations kanakes.

3. Pilier 3 : Infrastructures et contrôle économique
   - Télécommunications et accès à l’information dans les tribus et zones isolées.
   - Ports et exportation du nickel : contrôle des flux et répartition des retombées économiques.
   - Mobilité et contrôle : restrictions de circulation et postes de contrôle pendant les périodes de tension, avec coordonnées WGS84. Documentez les caractérisations coutumières de ces mesures.
   - Monnaie et dépendance économique : Franc CFP, dépendance aux transferts de l’État et à l’industrie du nickel.

4. Pilier 4 : Friction juridique et statutaire
   - Système préféré / coutumier : documentez le droit coutumier kanak, le rôle du Sénat coutumier, les Accords de Nouméa et le droit à l’autodétermination reconnu par les Nations Unies.
   - Conflit statutaire direct : documentez la contradiction entre le corps électoral spécial gelé par la loi organique et les revendications d’un corps électoral élargi ou d’indépendance, ainsi que les divergences sur la propriété des ressources minières.
   - Population kanake concernée par le statut particulier et les référendums d’autodétermination.

Restituez l’ensemble des données sous forme de bloc JSON conforme au Great GASPI Data Schema. Si une donnée n’est pas disponible, inscrivez "data not available".
=== END PROMPT 26 ===

---

## Prompt 27
**Perspective:** U.S. Department of the Interior / Office of Insular Affairs / American Samoa Government  
**Language:** English

=== START PROMPT 27 ===
Act as a senior geopolitical and federal territorial researcher. Your mission is to collect strictly factual and objective empirical data for the unincorporated territory of American Samoa from the official perspective of the U.S. Department of the Interior Office of Insular Affairs, the American Samoa Government, the U.S. Department of Justice, and federal statutory records. You must extract primary statutes, court dockets, land-tenure records, infrastructure data, and official administrative justifications, covering all four pillars.

Do not perform qualitative evaluations or assign ratings. Provide explicit numerical values, range estimates, WGS84 coordinates, and direct legal citations. If a specific data point is missing from official records, output "data not available".

1. Pillar 1: Physical Geography & Demographics
   - List key geographic features, volcanic high ground, and coastal zones (Mount Matafao, Mount Pioa, Tutuila, Manu’a Islands, Rose Atoll and others) with WGS84 coordinates and elevation in meters.
   - For every high-ground feature include a functional strategic description based solely on topography: observation control, fire control, movement-corridor control, and position relative to water resources or critical infrastructure. Do not attribute intent.
   - Extract total land area (approximately 199 sq km), distribution across Tutuila, Aunu’u, Ofu, Olosega and Ta’ū, and administrative division into districts and counties. Explicitly note which strategic features fall under which jurisdictions.
   - Collect U.S. Census Bureau and local demographic data: total population, Samoan vs non-Samoan residents, population density per sq km, and migration patterns.
   - Map federal and territorial facilities, ports, and restricted areas with WGS84 coordinates.
   - Document the official federal and territorial justifications for land-use rules, immigration controls, and administrative measures, including cited legal and security rationales.

2. Pillar 2: Hydropolitics & Environmental Data
   - Map primary watersheds, streams, and water-supply systems on Tutuila and the Manu’a Islands with WGS84 coordinates.
   - Report per-capita daily water consumption (L/c/d) compared against WHO reference standards (100 L/c/d).
   - Document agricultural land percentage, reliance on imported food, and traditional agroforestry areas.
   - Document environmental degradation incidents: coastal erosion, coral-reef damage, waste-management issues. Separate official remediation justifications from local community concerns.

3. Pillar 3: Infrastructure & Economic Data
   - Spectrum & Airspace: FCC regulated spectrum, commercial and general-aviation corridors, and Pago Pago International Airport.
   - Maritime & Ports: Port of Pago Pago, EEZ, and tuna-cannery related shipping. Document official federal justification for the application of U.S. maritime and customs regimes.
   - Checkpoints & Access: immigration and customs controls at the port and airport with WGS84 coordinates. Document official rationales for the distinct immigration status of American Samoa.
   - Currency & Utilities: Official currency (USD), power generation dependency on imported fuel, and water-utility self-sufficiency.

4. Pillar 4: Legal & Administrative Friction
   - Enforced System: Detail the American Samoa Constitution, the Deed of Cession (1900 and 1904), 48 U.S.C. provisions applicable to American Samoa, and the unique non-citizen national status of persons born in American Samoa.
   - Document federal court rulings on the status of American Samoans (including Fitisemanu v. United States and related litigation) and the official federal legal positions presented in those cases.
   - Direct Statutory Conflict: Cite explicit tensions between the federal Immigration and Nationality Act, the unique jus soli limitations applied to American Samoa, and local customary land-tenure rules that restrict alienation of communal land to non-Samoans.
   - Report the total population subject to the distinct territorial and nationality regime.

Return all data as a structured JSON block strictly matching the Great GASPI Data Schema. If a specific data point is missing from official records, output "data not available".
=== END PROMPT 27 ===

---

## Prompt 28
**Perspective:** Samoan Customary Land / Fa’amatai Advocates / Communal Land Defenders  
**Language:** English (with Samoan terms)

=== START PROMPT 28 ===
Act as an independent researcher of customary land tenure, fa’amatai governance, and territorial status. Your mission is to collect documentary evidence, land-tenure records, and verified figures regarding American Samoa from the perspective of customary land holders, the fa’amatai system, local land commissions, and advocates for the preservation of communal land and Samoan political status.

Do not perform qualitative evaluations or assign ratings. Collect specific numbers, WGS84 coordinates, and explicit statutory or customary citations. If a specific data point is not available, output "data not available".

1. Pillar 1: Physical Geography & Demographics
   - Document customary communal lands, village territories, and high ground of cultural significance (matai titles linked to specific lands, Mount Matafao, coastal villages on Tutuila and Manu’a) with WGS84 coordinates and elevation.
   - For every elevated or culturally significant feature include a functional strategic description based solely on topography: observation control, fire control, movement-corridor control, and position relative to water resources or traditional use areas. Do not attribute intent.
   - Determine total land area (approximately 199 sq km), proportion of land held under communal (customary) tenure versus individually owned or freehold land, and distribution across islands. Explicitly note which strategic or customary features fall under which tenure regimes.
   - Collect demographic data on ethnic Samoans, the proportion of land controlled by aiga (extended families), and population density.
   - Map areas where federal or territorial projects have affected communal land access with WGS84 coordinates.
   - Document local and customary characterisations of land alienation restrictions, immigration rules, and federal status, together with data on land security.

2. Pillar 2: Hydropolitics & Customary Resources
   - Map traditional water sources, streams, and coastal fishing grounds important to villages with WGS84 coordinates.
   - Report water-access issues in villages and any conflicts between territorial utility projects and customary rights.
   - Document agricultural and agroforestry areas under customary management and the degree of food import dependency.
   - Document environmental pressures on reefs, coasts, and forests. Separate official territorial justifications from local village concerns.

3. Pillar 3: Infrastructure & Economic Control
   - Telecommunications and access in outer villages.
   - Port of Pago Pago and the tuna industry: local employment versus foreign control of canneries and shipping.
   - Immigration and travel controls that affect family connections with independent Samoa and the U.S. mainland. Document local characterisations of the non-citizen national status.
   - Currency and economic dependency: use of USD, reliance on federal transfers, and the protection of communal land from free-market alienation.

4. Pillar 4: Legal & Customary Friction
   - Preferred / Customary System: Document the fa’amatai system, communal land tenure under Samoan custom, the Deed of Cession protections, and local statutes that restrict the sale of communal land to non-Samoans.
   - Direct Statutory Conflict: Document the tension between U.S. constitutional birthright citizenship norms and the continued non-citizen national status of persons born in American Samoa, as well as the conflict between free-alienation market principles and the customary prohibition on permanent alienation of communal land.
   - Total population living under the combined fa’amatai and territorial legal regime.

Export all data in a structured JSON block strictly matching the Great GASPI Data Schema. If a specific data point is not available, output "data not available".
=== END PROMPT 28 ===

---

*End of Batch 7 (Prompts 25–28). Continue with Batch 8 for Prompts 29–32.*
--

## Prompt 29
**Perspective:** Autonomous Administration of North and East Syria (AANES) / Syrian Democratic Forces (SDF)  
**Language:** English (with Kurdish terms)

=== START PROMPT 29 ===
Act as a senior geopolitical, administrative, and security researcher. Your mission is to collect strictly factual and verifiable empirical data for the territory under the Autonomous Administration of North and East Syria (AANES / Rojava) from the official perspective of the AANES, the Syrian Democratic Council, the Syrian Democratic Forces (SDF), and related civil institutions. You must extract primary administrative decrees, security assessments, infrastructure records, demographic data, and official justifications, covering all four pillars.

Do not perform qualitative evaluations or assign ratings. Provide explicit numerical values, range estimates, WGS84 coordinates, and direct citations. If a specific data point is missing from official or verifiable records, output "data not available".

1. Pillar 1: Physical Geography & Demographics
   - List key geographic features, mountain ranges, and strategic high ground (Qandil approaches, Mount Abdulaziz, Euphrates valley heights, Manbij plain and others) with WGS84 coordinates and elevation in meters.
   - For every high-ground feature include a functional strategic description based solely on topography: observation control, fire control, movement-corridor control, and position relative to water resources or critical infrastructure. Do not attribute intent.
   - Extract total approximate area under AANES administration, distribution across cantons or regions (Jazira, Euphrates, Afrin remnants, Manbij, Tabqa and others), and administrative divisions. Explicitly note which strategic features fall under which control zones.
   - Collect demographic data: total population estimates, Kurdish / Arab / Assyrian / other community breakdowns, and population density per sq km.
   - Map security perimeters, SDF defensive lines, and internal checkpoints with WGS84 coordinates.
   - Document the official security justifications of the AANES and SDF for defensive postures, checkpoints, and territorial control measures, including cited threats, attacks, and force-protection assessments.

2. Pillar 2: Hydropolitics & Environmental Data
   - Map the Euphrates River course, major dams (Tabqa / Euphrates Dam, Tishrin), irrigation canals, and water infrastructure under AANES influence with WGS84 coordinates.
   - Report per-capita water availability and agricultural irrigation dependence compared against WHO reference standards (100 L/c/d).
   - Document agricultural parameters: arable land percentage, wheat and cotton production areas, and food self-sufficiency estimates.
   - Document environmental degradation incidents: water-flow reductions from upstream, pollution, and damage from conflict. Separate official AANES characterisations from other parties’ statements.

3. Pillar 3: Infrastructure & Economic Data
   - Spectrum & Communications: cellular coverage, internet access constraints, and airspace conditions over AANES areas.
   - Energy & Oil: oil fields (Rmeilan and others), refining capacity, and electricity generation under AANES administration. Document official positions on resource management.
   - Checkpoints & Mobility: list major internal and external checkpoints with WGS84 coordinates and permit requirements. Document official security rationales.
   - Currency & Trade: use of Syrian pound, USD, and other currencies; cross-border trade routes and economic dependencies.

4. Pillar 4: Legal & Administrative Friction
   - Enforced System: detail the Social Contract of the AANES, local councils, women’s and community co-presidency structures, and security regulations issued by the Autonomous Administration.
   - Document official AANES positions on federalism, decentralisation, and relations with Damascus and neighbouring states.
   - Direct Statutory Conflict: cite explicit divergences between AANES administrative decrees and the central Syrian Arab Republic legal framework, as well as Turkish security claims affecting the territory.
   - Report the total population living under AANES civil and security administration.

Return all data as a structured JSON block strictly matching the Great GASPI Data Schema. If a specific data point is missing from official or verifiable records, output "data not available".
=== END PROMPT 29 ===

---

## Prompt 30
**Perspective:** Syrian Arab Republic / Central Government / Damascus authorities  
**Language:** Arabic

=== START PROMPT 30 ===
تصرف كباحث جيوسياسي وقانوني كبير. مهمتك هي جمع بيانات واقعية وموثقة فقط بشأن المناطق الشمالية والشرقية من الجمهورية العربية السورية من المنظور الرسمي لحكومة الجمهورية العربية السورية، ووزارات الدفاع والداخلية والإدارة المحلية، والمؤسسات الرسمية ذات الصلة. يجب استخراج الوثائق الأولية، والمراسيم، والبيانات الأمنية، وبيانات البنية التحتية، والمبررات الرسمية، وتغطية الركائز الأربع بالكامل.

لا تقم بأي تقييمات نوعية أو إعطاء درجات. قدم قيماً رقمية محددة، وإحداثيات WGS84، واستشهادات مباشرة. إذا لم تتوفر معلومة محددة في السجلات الرسمية، فاكتب "data not available".

1. الركيزة الأولى: الجغرافيا الفيزيائية والديموغرافيا
   - سجل التضاريس الاستراتيجية والجبال والمرتفعات (جبل عبد العزيز، مرتفعات الفرات، سهول منبج وغيرها) مع إحداثيات WGS84 والارتفاع بالأمتار.
   - لكل مرتفع أو سلسلة جبلية يجب تضمين وصف استراتيجي وظيفي مبني على التضاريس فقط: السيطرة على الرصد، السيطرة على النيران، السيطرة على ممرات الحركة، وموقعها بالنسبة للموارد المائية أو البنية التحتية الحيوية. لا تنسب نوايا.
   - حدد المساحة الإجمالية للمناطق المعنية، والتقسيمات الإدارية الرسمية للمحافظات (الحسكة، الرقة، دير الزور، أجزاء من حلب)، والمناطق التي تعتبرها الدولة تحت سيادتها. حدد صراحة أي المرتفعات الاستراتيجية تقع داخل كل منطقة.
   - اجمع بيانات السكان الرسمية: العدد الإجمالي، التوزيع الطائفي والعرقي حسب الإحصاءات الرسمية، والكثافة السكانية.
   - وثّق النقاط العسكرية ونقاط التفتيش والمناطق الأمنية التابعة للدولة مع إحداثيات WGS84.
   - وثّق المبررات الأمنية الرسمية للعمليات واستعادة السيطرة ونقاط التفتيش، بما في ذلك التهديدات والهجمات والبيانات التي تستند إليها السلطات السورية.

2. الركيزة الثانية: الهيدروبوليتيك والبيانات البيئية
   - سجل مجرى نهر الفرات والسدود الرئيسية (سد الفرات/الطبقة، تشرين) والبنى التحتية المائية مع إحداثيات WGS84.
   - استخرج أرقام توفر المياه للفرد والاعتماد على الري مقارنة بمعيار منظمة الصحة العالمية (100 لتر/فرد/يوم).
   - سجل نسبة الأراضي الزراعية وإنتاج القمح والقطن والاكتفاء الغذائي حسب البيانات الرسمية.
   - وثّق حوادث التدهور البيئي وتأثيرات الصراع على الموارد. افصل المبررات الرسمية عن ادعاءات الأطراف الأخرى.

3. الركيزة الثالثة: البنية التحتية والاقتصاد
   - الاتصالات والطيف: شبكات الاتصالات الخاضعة لسيطرة الدولة والقيود على الطيف والترددات.
   - الطاقة والنفط: الحقول النفطية في الشمال الشرقي، وقدرات التكرير، وشبكات الكهرباء. وثّق الموقف الرسمي من إدارة الموارد.
   - نقاط التفتيش والتنقل: قائمة نقاط التفتيش الرئيسية مع إحداثيات WGS84 ومتطلبات التصاريح. وثّق المبررات الأمنية الرسمية.
   - العملة والتجارة: الليرة السورية، والممرات التجارية، والتبعيات الاقتصادية.

4. الركيزة الرابعة: الاحتكاك القانوني والإداري
   - النظام المطبق: وثّق الدستور السوري، وقوانين الإدارة المحلية، والمراسيم المتعلقة باستعادة السيادة على كامل الأراضي السورية.
   - وثّق المواقف الرسمية للحكومة السورية بشأن الوحدات الإدارية غير المعترف بها والوجود العسكري الأجنبي.
   - التعارض التشريعي المباشر: وثّق التعارض بين الإطار القانوني للجمهورية العربية السورية والمراسيم الصادرة عن الإدارات المحلية غير المعترف بها، وكذلك الادعاءات الأمنية التركية.
   - عدد السكان الخاضعين للسيادة القانونية السورية في هذه المناطق.

أخرج جميع البيانات في قالب JSON مطابق تماماً لـ Great GASPI Data Schema. إذا لم تتوفر معلومة محددة فاكتب "data not available".
=== END PROMPT 30 ===

---

## Prompt 31
**Perspective:** Republic of Azerbaijan / Karabakh / East Zangezur authorities  
**Language:** English (with Azerbaijani terms)

=== START PROMPT 31 ===
Act as a senior geopolitical, legal, and reconstruction researcher. Your mission is to collect strictly factual and verifiable empirical data for the territories of Karabakh and East Zangezur from the official perspective of the Republic of Azerbaijan, the Special Representative of the President, the Karabakh and East Zangezur economic regions administrations, and relevant Azerbaijani state institutions. You must extract primary laws, presidential decrees, demining and reconstruction reports, demographic data, and official security and administrative justifications, covering all four pillars.

Do not perform qualitative evaluations or assign ratings. Provide explicit numerical values, range estimates, WGS84 coordinates, and direct citations. If a specific data point is missing from official Azerbaijani records, output "data not available".

1. Pillar 1: Physical Geography & Demographics
   - List key geographic features, mountain ranges, and strategic high ground (Karabakh range, Murovdağ, Shusha heights, Lachin corridor area and others) with WGS84 coordinates and elevation in meters.
   - For every high-ground feature include a functional strategic description based solely on topography: observation control, fire control, movement-corridor control, and position relative to water resources or critical infrastructure. Do not attribute intent.
   - Extract total area of the Karabakh and East Zangezur economic regions under Azerbaijani administration, administrative divisions, and land returned to control after 2020 and 2023. Explicitly note which strategic features fall under which control zones.
   - Collect demographic data: pre-conflict population figures, current returnee numbers, and population density projections.
   - Map demining zones, military positions, and reconstruction security perimeters with WGS84 coordinates.
   - Document the official security and administrative justifications of the Republic of Azerbaijan for demining operations, border security, and resettlement measures, including cited threats and prior attack data.

2. Pillar 2: Hydropolitics & Environmental Data
   - Map major rivers and reservoirs (Terter, Khachinchay, Sarsang reservoir and others) with WGS84 coordinates.
   - Report water infrastructure status, irrigation potential, and per-capita water planning against WHO reference standards (100 L/c/d).
   - Document agricultural land recovery, mine contamination of arable land, and food production restart data.
   - Document environmental damage from conflict and mine contamination. Separate official Azerbaijani remediation justifications from other characterisations.

3. Pillar 3: Infrastructure & Economic Data
   - Transport corridors: reconstruction of roads, the Lachin road status, and new transport links with WGS84 coordinates.
   - Energy and utilities: restoration of electricity, gas, and water networks.
   - Checkpoints and border control: list major checkpoints and border points with WGS84 coordinates. Document official security rationales.
   - Currency and reconstruction finance: use of Azerbaijani manat, state investment figures, and economic region development plans.

4. Pillar 4: Legal & Administrative Friction
   - Enforced System: detail the Constitution of the Republic of Azerbaijan, laws on the reintegration of the territories, and presidential decrees establishing the Karabakh and East Zangezur economic regions.
   - Document official Azerbaijani legal positions on sovereignty, the dissolution of prior local structures, and citizenship/returnee rights.
   - Direct Statutory Conflict: cite explicit divergences between current Azerbaijani legislation and prior local administrative acts or Armenian legal claims regarding the territory.
   - Report the population planned for return and currently under Azerbaijani administration.

Return all data as a structured JSON block strictly matching the Great GASPI Data Schema. If a specific data point is missing from official Azerbaijani records, output "data not available".
=== END PROMPT 31 ===

---

## Prompt 32
**Perspective:** Republic of Armenia / Artsakh / Armenian rights and displacement advocates  
**Language:** English (with Armenian terms)

=== START PROMPT 32 ===
Act as an independent geographic, legal, and human-rights researcher. Your mission is to collect documentary evidence, field data, and verified records regarding Nagorno-Karabakh (Artsakh) from the perspective of the Republic of Armenia, former Artsakh authorities, displacement organisations, and Armenian rights documentation centres.

Do not perform qualitative evaluations or assign ratings. Collect specific numbers, WGS84 coordinates, and explicit legal citations. If a specific data point is not available, output "data not available".

1. Pillar 1: Physical Geography & Demographics
   - Document key geographic features, mountain positions, and former population centres (Shushi/Shusha, Stepanakert/Khankendi, Lachin corridor, Martuni and others) with WGS84 coordinates and elevation.
   - For every elevated feature include a functional strategic description based solely on topography: observation control, fire control, movement-corridor control, and position relative to water resources. Do not attribute intent.
   - Determine the approximate area previously administered as Artsakh, the status of the Lachin corridor, and current access conditions. Explicitly note which strategic features fall under which control regimes.
   - Collect demographic data: pre-2020 and pre-2023 population figures, number of displaced persons, and density figures.
   - Map former defensive lines, the Lachin corridor route, and current access restrictions with WGS84 coordinates.
   - Document Armenian and Artsakh characterisations of the military operations, blockade, and displacement, together with available quantitative data on population movement.

2. Pillar 2: Hydropolitics & Environmental Data
   - Map water sources, the Sarsang reservoir, and irrigation systems previously serving Artsakh populations with WGS84 coordinates.
   - Report water access issues during the blockade period and current conditions for remaining or displaced populations.
   - Document agricultural land loss and food security impacts for the displaced population.
   - Document environmental and infrastructure damage from the conflict. Separate official characterisations from other parties’ statements.

3. Pillar 3: Infrastructure & Economic Data
   - Transport and the Lachin corridor: status of the sole previously reliable road link, checkpoints, and access restrictions with WGS84 coordinates.
   - Energy and utilities: previous self-sufficiency levels and disruption data.
   - Mobility restrictions affecting the civilian population. Document local and Armenian characterisations of these measures.
   - Currency and economic collapse: previous use of Armenian dram and local economic indicators before displacement.

4. Pillar 4: Legal & Administrative Friction
   - Preferred / prior system: document the Constitution of the Republic of Artsakh, previous local self-governance structures, and relevant international statements on self-determination and humanitarian access.
   - Direct Statutory Conflict: document the contradiction between prior Artsakh administrative and property acts and current Azerbaijani legislation applied to the territory, as well as Armenian legal and diplomatic positions on the rights of the displaced population.
   - Total population displaced from the territory and currently outside it.

Export all data in a structured JSON block strictly matching the Great GASPI Data Schema. If a specific data point is not available, output "data not available".
=== END PROMPT 32 ===

---
