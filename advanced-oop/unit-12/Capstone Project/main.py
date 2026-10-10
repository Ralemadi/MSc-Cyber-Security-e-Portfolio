from banking.app.container import ApplicationContainer
from banking.config import DEFAULT_AUDIT_PATH, DEFAULT_DB_PATH
from banking.ui.application import BankingCLI
from banking.ui.console import Console


#Build the application and start the requested BankSecure workflow.
def main() -> None:
    #Build the application and hand control to the terminal UI.
    app = ApplicationContainer(
        db_path=DEFAULT_DB_PATH,
        audit_path=DEFAULT_AUDIT_PATH,
        seed_demo_data=True,
    )
    BankingCLI(
        app=app,
        console=Console(),
    ).run()


if __name__ == "__main__":
    main()
