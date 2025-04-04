from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import User, production

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.autodiscover()

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("nom_cli","logo_vendeur", "email","numero_cli","commerçant","adresse_cli","ville_cli","code_postal_cli","pays_cli")}),  # Utilisation de "nom_cli" au lieu de "name"
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username",'commerçant','id','logo_vendeur', "nom_cli",'numero_cli','adresse_cli','ville_cli','code_postal_cli','pays_cli','is_superuser']  # Affichage de "nom_cli" au lieu de "name"
    search_fields = ("username", "nom_cli", "email")

    # Assurez-vous de ne pas inclure les champs qui ne sont plus présents dans le modèle
    filter_horizontal = ("groups", "user_permissions")
    
