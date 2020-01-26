class DBHandler:
    def get_issuers(self):
        return [
            {
                'id': 1,
                'name': "Blink's School of Enchanting Minds"
            },
            {
                'id': 2,
                'name': "Elise's College of Defense and Weapon Mastery"
            },
            {
                'id': 3,
                'name': "Ashran's School of Thieves"
            }
        ]

    def get_document_types(self, issuer_id: int):
        return [
            {
                "id": 1,
                "name": "Black Iron Chain: Induction Course"
            },
            {
                "id": 2,
                "name": "Black Iron Chain: Outstanding Performance Award"
            }
        ]

    def get_document_template(self, issuer_id: int, document_type_id: int):
        return [
            "Outstanding Performance Award\n*Is awarded to\n*(?P<firstName>.*) (?P<lastName>.*)\n*for (?P<reason>.*)",
            "AWARDED: (?P<date>.*)"
        ]