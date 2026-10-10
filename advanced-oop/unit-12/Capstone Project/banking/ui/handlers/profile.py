from __future__ import annotations
from banking.exceptions import AuthenticationError
from banking.ui.handlers.base import BaseCommandHandler

#Coordinate the current-user password-change workflow
class ProfileCommandHandler(BaseCommandHandler):
    #Verify the current password before replacing it with a policy-compliant new password
    def change_password(self) -> None:
        actor = self.require_login()
        self.console.heading(
            "Change Password"
        )
        self.show_back_option()

        current_password = self.prompt_with_back(
            "Current password",
            secret=True,
        )
        new_password = self.prompt_valid_password(
            actor.username,
            label="New password",
        )

        try:
            self.app.profile_service.change_own_password(
                actor=actor,
                current_password=current_password,
                new_password=new_password,
            )
        except AuthenticationError as exc:
            self.console.error(str(exc))
            return

        self.console.success(
            "Password changed successfully."
        )
