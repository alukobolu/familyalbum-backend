from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(98) + str(timestamp)  + str(False)
        )

account_activation_token = AccountActivationTokenGenerator()