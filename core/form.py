
from django import forms
from django.contrib.auth.models import User, Group
from .models import Student


class RegisterationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    role = forms.ChoiceField(
        choices=[
            ("Admin", "Admin"),
            ("Teacher", "Teacher"),
            ("Student", "Student"),
        ]
    )

    name = forms.CharField(
        max_length=100
    )

    age = forms.IntegerField(
        min_value=1
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "role",
            "name",
            "age"
        ]

    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data["password"]
        )

        if commit:
            user.save()

            role = self.cleaned_data["role"]

            group = Group.objects.get(
                name=role
            )

            user.groups.add(group)

            if role == "Student":
                Student.objects.create(
                    user=user,
                    name=self.cleaned_data["name"],
                    age=self.cleaned_data["age"],
                    #email=user.email
                )

        return user

