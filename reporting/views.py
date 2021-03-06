import reporting

from django.http import Http404, HttpResponseForbidden
from django.views.generic import TemplateView


class ReportListView(TemplateView):
    template_name = 'reporting/list.html'

    def get(self, *args, **kwargs):
        self.reports = self.get_reports()
        if not self.reports:
            return HttpResponseForbidden()
        return super(ReportListView, self).get(*args, **kwargs)

    def get_reports(self):
        report_classes = reporting.user_reports(self.request)
        reports = []
        for slug, klass in report_classes:
            reports.append((slug, klass(self.request),))
        return reports

    def get_context_data(self, **kwargs):
        context = super(ReportListView, self).get_context_data(**kwargs)
        data = {'reports': self.reports}
        context.update(data)
        return context


class ReportView(TemplateView):
    template_name = 'reporting/view.html'

    def get(self, request, slug, **kwargs):
        self.slug = slug
        self.report = self.get_report(self.slug)
        if not self.report.has_view_permission(request):
            return HttpResponseForbidden()
        return super(ReportView, self).get(request, **kwargs)

    def get_report(self, slug):
        try:
            return reporting.get_report(slug)(self.request)
        except reporting.ReportNotFound:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        data = {'report': self.report, 'title': self.report.verbose_name,
                'media': self.report.admin.media}
        context.update(data)
        return context
