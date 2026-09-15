
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
        max_length=100,
        required=False
    )

    age = forms.IntegerField(
        min_value=1,
        required=False
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

    def clean(self):
        cleaned_data = super().clean()

        role = cleaned_data.get("role")
        name = cleaned_data.get("name")
        age = cleaned_data.get("age")

        if role == "Student":
            if not name:
                self.add_error("name", "Name is required for students.")

            if age is None:
                self.add_error("age", "Age is required for students.")

        return cleaned_data

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
                )

        return user