"""HTML forms for learner submissions."""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Submission


class RegistrationForm(UserCreationForm):
    """Create a learner account using Django's built-in password validation."""

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username",)
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "autocomplete": "username",
                    "placeholder": "vd. minhnguyen",
                }
            )
        }

    def __init__(self, *args, **kwargs):
        """Add accessible, consistently styled password controls."""
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update(
            {"autocomplete": "new-password", "placeholder": "Tối thiểu 8 ký tự"}
        )
        self.fields["password2"].widget.attrs.update(
            {"autocomplete": "new-password", "placeholder": "Nhập lại mật khẩu"}
        )


class LoginForm(AuthenticationForm):
    """Authentication form with the same accessible UI metadata as registration."""

    def __init__(self, *args, **kwargs):
        """Preserve Django authentication while adding helpful form metadata."""
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "autocomplete": "username",
                "placeholder": "Tên đăng nhập của bạn",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "autocomplete": "current-password",
                "placeholder": "Mật khẩu của bạn",
            }
        )


class SubmissionImageForm(forms.ModelForm):
    """Validate an uploaded screenshot before it reaches the OCR service."""

    max_image_size = 5 * 1024 * 1024
    allowed_content_types = {"image/jpeg", "image/png", "image/webp"}

    class Meta:
        model = Submission
        fields = ("image",)
        widgets = {
            "image": forms.ClearableFileInput(
                attrs={
                    "accept": "image/png,image/jpeg,image/webp",
                    "class": "file-input",
                }
            )
        }

    def clean_image(self):
        image = self.cleaned_data["image"]
        content_type = getattr(image, "content_type", "")

        if content_type and content_type not in self.allowed_content_types:
            raise forms.ValidationError(
                "Only PNG, JPEG, and WebP images are supported."
            )
        if image.size > self.max_image_size:
            raise forms.ValidationError("The image must be 5 MB or smaller.")
        return image
