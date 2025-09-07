class TestPing:
    def test_health_check(self, ping_api):
        response = ping_api.health_check()
        assert response.status_code == 201