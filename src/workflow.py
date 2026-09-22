from dataclasses import dataclass, asdict

@dataclass
class WorkflowResult:
    request_id: str
    department: str
    risk_level: str
    workflow: list[str]
    human_review_required: bool
    status: str
    def to_dict(self):
        return asdict(self)

def classify_department(title, description):
    text = f"{title} {description}".lower()
    rules = [
        (["x投稿","sns","投稿","instagram","youtube"], "SNS運用"),
        (["請求","経費","会計","売上"], "経理"),
        (["todo","タスク","予定","通知"], "業務管理"),
        (["問い合わせ","顧客","サポート"], "カスタマーサポート"),
        (["システム","開発","bot","自動化"], "システム開発"),
    ]
    for keywords, department in rules:
        if any(k.lower() in text for k in keywords):
            return department
    return "総務・企画"

def determine_risk(priority, contains_sensitive_data, external_publish):
    if contains_sensitive_data or priority == "high":
        return "high"
    if external_publish:
        return "medium"
    return "low"

def process_request(data):
    department = classify_department(data.get("title",""), data.get("description",""))
    risk = determine_risk(
        data.get("priority","normal"),
        bool(data.get("contains_sensitive_data",False)),
        bool(data.get("external_publish",False))
    )
    workflow = [
        "依頼内容の整理",
        f"{department}として処理内容を分析",
        "実行手順の作成",
        "AIによる処理",
        "結果の品質チェック",
    ]
    review = risk == "high" or bool(data.get("external_publish",False))
    workflow.append("人間による確認" if review else "結果を保存")
    return WorkflowResult(
        request_id=data.get("request_id","UNKNOWN"),
        department=department,
        risk_level=risk,
        workflow=workflow,
        human_review_required=review,
        status="waiting_human_review" if review else "completed",
    )
