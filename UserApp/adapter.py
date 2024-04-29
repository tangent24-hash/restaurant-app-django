from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.fullname = data.get('fullname')
        user.mobile = data.get('mobile')
        user.facebook_id = data.get('facebook_id')
        user.date_of_birth = data.get('date_of_birth')
        user.save()
        return user
