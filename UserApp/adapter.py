from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        frontend_url = f"{settings.FRONTEND_URL}/signup/verify-email/"
        activate_url = f"{frontend_url}{emailconfirmation.key}"
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "key": emailconfirmation.key,
            "site": settings.SITE_ID,
            "request": request,
        }
        self.send_mail('account/email/email_confirmation', emailconfirmation.email_address.email, ctx)

    # def send_mail(self, template_prefix, email, context):
    #     print(context)
    #     if 'password_reset_url' in context:
    #         context['password_reset_url'] = f"{settings.FRONTEND_URL}/reset-password?uid={context['uid']}&token={context['token']}"
    #
    #     super().send_mail(template_prefix, email, context)

