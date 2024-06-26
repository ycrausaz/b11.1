from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class GroupRequiredMixin(UserPassesTestMixin):
    group_required = None

    def test_func(self):
        if self.group_required and self.request.user.is_authenticated:
            if self.request.user.groups.filter(name=self.group_required).exists() or self.request.user.is_superuser:
                return True
        raise PermissionDenied

class grIL_GroupRequiredMixin(GroupRequiredMixin):
    group_required = 'grIL'

class grGD_GroupRequiredMixin(GroupRequiredMixin):
    group_required = 'grGD'

class grSMDA_GroupRequiredMixin(GroupRequiredMixin):
    group_required = 'grSMDA'

