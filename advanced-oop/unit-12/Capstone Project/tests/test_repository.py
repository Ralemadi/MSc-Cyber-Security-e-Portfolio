from __future__ import annotations
from pathlib import Path
from base_test_case import BankSecureTestCase



class RepositoryTests(BankSecureTestCase):
    #Verify that repository initialisation creates a missing database parent directory automatically
    def test_database_parent_folder_is_created_automatically(self) -> None:
            db_path = Path(self.app.repository.db_path)
            self.assertTrue(
                db_path.parent.exists()
            )
            self.assertTrue(
                db_path.exists()
            )

