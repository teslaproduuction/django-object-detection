from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import MLModel


class MLModelCreateView(LoginRequiredMixin, CreateView):
    model = MLModel
    fields = ['pth_file', 'class_file',
              'description', 'version', 'public']

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        form.save(commit=False)
        if not MLModel.objects.filter(name=form.instance.pth_filename).exists():
            form.instance.name = form.instance.pth_filename
            if not MLModel.objects.filter(class_filename=form.instance.cls_filename).exists():
                form.instance.class_filename = form.instance.cls_filename
            messages.success(self.request,
                             f'Pre-trained model {form.instance.pth_filename} uploaded successfully.'
                             )
            return super().form_valid(form)
        else:
            form.add_error(
                'pth_file',
                f'Ml Model with the name {form.instance.name}, already exists in the database.'
            )
            context = {
                'form': form
            }
            return render(self.request, 'modelmanager/mlmodel_form.html', context)


class MLModelUpdateView(LoginRequiredMixin, CreateView):
    model = MLModel
    fields = ['name', 'description', 'version', 'public']

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        form.save(commit=False)
        if not MLModel.objects.filter(name=form.instance.pth_filename).exists():
            form.instance.name = form.instance.pth_filename
            messages.success(self.request,
                             f'Pre-trained model {form.instance.pth_filename} uploaded successfully.'
                             )
            return super().form_valid(form)
        else:
            form.add_error(
                'pth_file',
                f'Ml Model with the name {form.instance.name}, already exists in the database.'
            )
            context = {
                'form': form
            }
            return render(self.request, 'modelmanager/mlmodel_form.html', context)


class UserMLModelListView(LoginRequiredMixin, ListView):
    model = MLModel
    context_object_name = 'user_models'
    template_name: str = 'modelmanager/mlmodel_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(uploader=self.request.user).order_by('-created')

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class PublicMLModelListView(LoginRequiredMixin, ListView):
    model = MLModel
    context_object_name = 'public_models'
    template_name: str = 'modelmanager/mlmodel_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(public=True).order_by('-created')


from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404



class ModelTrainingStatsView(LoginRequiredMixin, TemplateView):
    """Представление для отображения статистики обучения модели."""
    template_name = "modelmanager/model_training_stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем модель, если указан ID
        model_id = self.kwargs.get('model_id')
        if model_id:
            model = get_object_or_404(MLModel, id=model_id)
            context['model'] = model

            # Определяем тип модели - кастомная для снежных барсов или стандартная YOLOv8
            if "snow" in model.name.lower() or "leopard" in model.name.lower() or "bars" in model.name.lower():
                context['is_custom_snow_leopard'] = True
                context['model_type'] = "snow_leopard"
            else:
                context['is_custom_snow_leopard'] = False
                context['model_type'] = "standard"
        else:
            # Если ID не указан, показываем статистику для стандартной YOLOv8
            context['is_custom_snow_leopard'] = False
            context['model_type'] = "standard"

        return context