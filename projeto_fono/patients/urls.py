
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^lista$', views.patients_list, name='patients_list'),
    url(r'^cadastrar$', views.patient_register, name='patient_register'),
    url(r'^deletar/(?P<pk>\d+)$', views.patient_delete, name='patient_delete'),
    url(r'^editar/(?P<pk>\d+)/$', views.patient_edit, name='patient_edit'),
    url(r'^planejamento-diario/(?P<pk>\d+)$',
        views.patient_plan, name='patient_plan'),
    url(r'^planejamento-diario/(?P<pk>\d+)/sessao/(?P<sessao>\d+)/deletar$',
        views.session_delete, name='session_delete'),
    url(r'^planejamento-diario/(?P<pk>\d+)/sessao/(?P<sessao>\d+)/objetivo$',
        views.session_objective, name='session_objective'),
    url(r'^planejamento-diario/(?P<pk>\d+)/sessao/(?P<sessao>\d+)/conteudo$',
        views.session_content, name='session_content'),
    url(r'^planejamento-diario/(?P<pk>\d+)/sessao/(?P<sessao>\d+)/atividade$',
        views.session_activity, name='session_activity'),
    url(r'^planejamento-diario/(?P<pk>\d+)/sessao/(?P<sessao>\d+)/observacao$',
        views.session_observation, name='session_observation'),
    url(r'^planejamento-diario/(?P<pk>\d+)/sessao/(?P<sessao>\d+)'
        '/objetivo/(?P<pk_obj>\d+)/deletar$',
        views.objective_delete, name='objective_delete'),
    url(r'^planejamento-diario/(?P<pk>\d+)/sessao/(?P<sessao>\d+)'
        '/conteudo/(?P<pk_obj>\d+)/deletar$',
        views.content_delete, name='content_delete'),
    url(r'^planejamento-diario/(?P<pk>\d+)/sessao/(?P<sessao>\d+)'
        '/atividade/(?P<pk_obj>\d+)/deletar$',
        views.activity_delete, name='activity_delete'),
    url(r'^planejamento-diario/(?P<pk>\d+)/sessao/(?P<sessao>\d+)'
        '/observacao/(?P<pk_obj>\d+)/deletar$',
        views.observation_delete, name='observation_delete'),
    url(r'^planejamento-terapeutico/(?P<pk>\d+)$',
        views.patient_therapy, name='patient_therapy'),
    url(r'^planejamento-terapeutico/(?P<pk>\d+)'
        '/conduta-fonoaudiologia/(?P<conduta>\d+)$',
        views.therapy_coduct, name='therapy_coduct'),
    url(r'^planejamento-terapeutico/(?P<pk>\d+)'
        '/conduta-fonoaudiologia/(?P<conduta>\d+)/deletar$',
        views.therapy_delete, name='therapy_delete'),
    url(r'^planejamento-terapeutico/(?P<pk>\d+)'
        '/conduta-fonoaudiologia/(?P<conduta>\d+)/topico/(?P<topico>\d+)/deletar$',
        views.topic_delete, name='topic_delete')
]
