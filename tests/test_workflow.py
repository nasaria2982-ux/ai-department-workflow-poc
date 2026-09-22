import unittest
from src.workflow import classify_department, determine_risk, process_request

class WorkflowTests(unittest.TestCase):
    def test_sns(self):
        self.assertEqual(classify_department("X投稿を作成","新商品の告知"), "SNS運用")
    def test_sensitive_high_risk(self):
        self.assertEqual(determine_risk("normal", True, False), "high")
    def test_external_publish_requires_review(self):
        result = process_request({
            "request_id":"REQ-001",
            "title":"SNS投稿",
            "description":"公開投稿",
            "priority":"normal",
            "contains_sensitive_data":False,
            "external_publish":True
        })
        self.assertTrue(result.human_review_required)
        self.assertEqual(result.status, "waiting_human_review")
    def test_internal_low_risk(self):
        result = process_request({
            "request_id":"REQ-002",
            "title":"TODO整理",
            "description":"今日のタスク",
            "priority":"normal",
            "contains_sensitive_data":False,
            "external_publish":False
        })
        self.assertEqual(result.department, "業務管理")
        self.assertFalse(result.human_review_required)

if __name__ == "__main__":
    unittest.main()
