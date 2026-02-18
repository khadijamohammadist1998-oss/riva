
## FastAPI Admin / SQLAdmin

from sqladmin import ModelView
from markupsafe import Markup
import json
from models.user import User
from models.clinical_case import ClinicalCase
from markupsafe import Markup
    
class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

    column_list = [ User.id, User.email, User.full_name, User.created_at]
    column_searchable_list = [ User.email, User.full_name,]
    
    can_create = False


class ClinicalCaseAdmin(ModelView, model=ClinicalCase):
   
    name = "Clinical Case"
    name_plural = "Clinical Cases"
    icon = "fa-solid fa-stethoscope"

    # Audio Player Renderer
    @staticmethod
    def audio_player(model, prop):
        # prop هنا هو اسم العمود كنص
        path = getattr(model, prop, None)

        if not path:
            return "—"

        return Markup(f"""
            <audio controls style="width:250px">
                <source src="/{path}" type="audio/mp4">
                Your browser does not support audio
            </audio>
        """)

        
    # Formatter mapping 
    column_formatters_detail  = {
        ClinicalCase.cough_audio_path: audio_player,
        ClinicalCase.breath_audio_path: audio_player,
    }
    # ما يظهر في القائمة
    column_list = [
        ClinicalCase.id,
        ClinicalCase.age,
        ClinicalCase.gender,
        ClinicalCase.country,
        ClinicalCase.final_diagnosis,
        ClinicalCase.confidence,
        ClinicalCase.created_at,
    ]

    # عند فتح التفاصيل → تظهر كل الحقول
    column_details_list = [
        ClinicalCase.id,
        ClinicalCase.user,
        ClinicalCase.age,
        ClinicalCase.gender,
        ClinicalCase.country,
        ClinicalCase.marital_status,
        ClinicalCase.is_pregnant,

        ClinicalCase.symptoms,
        ClinicalCase.symptoms_duration,

        ClinicalCase.smoking_exposure,
        ClinicalCase.ex_smoker_duration,

        ClinicalCase.cough_details,
        ClinicalCase.sputum_color,

        ClinicalCase.medical_history,
        ClinicalCase.family_history,
        ClinicalCase.surgery_details,

        ClinicalCase.additional_notes,

        ClinicalCase.breath_audio_path,
        ClinicalCase.cough_audio_path,

        ClinicalCase.final_diagnosis,
        ClinicalCase.confidence,
        ClinicalCase.supporting_evidence,

        ClinicalCase.ai_model,
        ClinicalCase.ai_version,

        ClinicalCase.created_at,
    ]


    column_sortable_list = [
        ClinicalCase.created_at,
        ClinicalCase.confidence
    ]
    
    # الحقول القابلة للتعديل
    form_columns = [
        "age",
        "gender",
        "country",
        "marital_status",
        "is_pregnant",

        "symptoms",
        "symptoms_duration",

        "smoking_exposure",
        "ex_smoker_duration",

        "cough_details",
        "sputum_color",

        "medical_history",
        "family_history",
        "surgery_details",

        "additional_notes",

        "final_diagnosis",
        "confidence",
        "supporting_evidence",
    ]
    
    can_create = False
    can_delete = True
    can_edit = False

'''
 
 


    # فلاتر جانبية 🔍
    column_filters = [
        ClinicalCase.gender,
        ClinicalCase.country,
        ClinicalCase.confidence,
        ClinicalCase.final_diagnosis,
        ClinicalCase.created_at,
    ]
    
     # أعمدة قابلة للبحث
    column_searchable_list = [
        ClinicalCase.country,
        ClinicalCase.final_diagnosis,
        ClinicalCase.confidence,
    ]
    
    # ترتيب افتراضي
    column_default_sort = ("created_at", True)



class DiagnosisRequestAdmin(ModelView, model=DiagnosisRequest):

    # 1️⃣ الأعمدة التي تظهر في الجدول الرئيسي
    column_list = [
        DiagnosisRequest.id,
        DiagnosisRequest.created_at,
        DiagnosisRequest.final_diagnosis,
        DiagnosisRequest.confidence
    ]

    # 2️⃣ الأعمدة التي تظهر في صفحة التفاصيل
    column_details = [
        DiagnosisRequest.id,
        DiagnosisRequest.created_at,
        DiagnosisRequest.final_diagnosis,
        DiagnosisRequest.confidence,
        DiagnosisRequest.patient_data,
        DiagnosisRequest.supporting_evidence
    ]

    # 3️⃣ البحث والترتيب
    column_searchable_list = [
        DiagnosisRequest.final_diagnosis
    ]

    column_sortable_list = [
        DiagnosisRequest.created_at,
        DiagnosisRequest.confidence
    ]

    # 4️⃣ الصلاحيات
    can_delete = True
    can_edit = True
    can_create = False 
    
'''
'''
    # 5️⃣ دالة تنسيق بيانات المريض
    def format_patient_data(self, model):
            #data = value or {}
            if not model:
                return "-"

            #  إذا كان String نحوله إلى dict
            if isinstance(model, str):
                try:
                    print(model)
                    data = json.loads(model.replace("'", '"'))
                except Exception:
                    return model
            else:
                data = model
            return Markup(f"""
            <h4>Patient Info</h4>
            <ul>
                <li><b>Country:</b> {data.get("country", "-")}</li>
                <li><b>Age:</b> {data.get("age", "-")}</li>
                <li><b>Gender:</b> {data.get("gender", "-")}</li>
                <li><b>Marital status:</b> {data.get("marital_status", "-")}</li>
                <li><b>Pregnant:</b> {data.get("is_pregnant", "-")}</li>
            </ul>
            """)

    # 6️⃣ دالة تنسيق الأدلة
    def format_supporting_evidence(self, value):
        data = value or {}
        if not value:
                return "-"

        if isinstance(value, str):
            try:
                data = json.loads(value.replace("'", '"'))
            except Exception:
                return value
        else:
            data = value
        
        evidence = data.supporting_evidence or []

        html = "<h4>Supporting Evidence</h4><ul>"
        for e in evidence:
            html += f"<li>{e}</li>"
        html += "</ul>"

        return Markup(html)

    # 7️⃣ ربط الأعمدة مع دوال التنسيق
   
    column_formatters_detail = {
        DiagnosisRequest.patient_data: format_patient_data,
        DiagnosisRequest.supporting_evidence: format_supporting_evidence
    } ''' 
    
