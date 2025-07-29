from django.views.generic.base import ContextMixin


class SidebarMixin(ContextMixin):
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["system_name"] = self.system_name
    context["description"] = self.description
    context["keywords"] = self.keywords
    return context
