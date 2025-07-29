import typing as t

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class AbstractConst(object):
  view_conf: dict = {"compute_task": False}
  system_name: str = "Meterhub"


def create_views(const: AbstractConst):
  class BaseContextView(TemplateView):
    page_name: str = ""

    def get_context_data(self, **kwargs: t.Any) -> t.Dict[str, t.Any]:
      context = super().get_context_data(**kwargs)
      context["view_conf"] = const.view_conf
      context["DEBUG"] = settings.DEBUG
      context["system_name"] = const.system_name
      context["page_name"] = self.page_name
      return context

  class LoginRequiredView(BaseContextView, LoginRequiredMixin):
    """Inherit from BaseConetextView. User Must login, and cannot be Anonymous."""

    login_url = "/login"
    redirect_field_name = "login"

    def dispatch(self, request, *args, **kwargs):
      if request.user.is_anonymous:
        return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)

  class BaseView(LoginRequiredView):
    """Every view should inherit this view."""

    pass

  return BaseContextView, LoginRequiredView, BaseView
