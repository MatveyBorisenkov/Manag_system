from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.views.generic import ListView
from .models import Entities, Files
from .forms import EntitiesForm, DocumentsAddForm, FilesAddForm, RegisterUserForm
from django.views.generic import ListView, DetailView, CreateView, View, TemplateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

# Create your views here.

# class EntitiesByCategoryView(ListView):
#     context_object_name = 'category_test'
#     template_name = 'post_list.html'
#
#     def get_queryset(self):
#         self.category = Entities.objects.get(self.kwargs)
#
#         return self.category
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['ent_name'] = self.category
#         return context


class EntitiesListView(ListView):
    """
    A view that displays a list of all entities (categories).

    Attributes:
    -----------
    model : Model
        The model that the view will use to retrieve the data.
    template_name : str
        The name of the template that the view will use to render the data.

    Methods:
    --------
    get_queryset(self)
        Returns the queryset that the view will use to retrieve the data.

    get_context_data(self, **kwargs)
        Returns the context dictionary that the view will use to render the data.

    """
    model = Entities
    template_name = "base.html"


def category_detail(request, my_id):
    """
    Renders a category detail page with a list of all entities and additional information about the current category.

    Args:
        request (HttpRequest): The HTTP request object.
        my_id (int): The ID of the current category.

    Returns:
        HttpResponse: The HTTP response object containing the rendered category detail page.
    """

    nodes = Entities.objects.all()
    context = {
        'object_list': nodes,
        'current_category': Entities.objects.get(id=my_id),
        'root_category_id': Entities.objects.get(id=my_id).get_root().id,

    }

    return render(request, 'base.html', context=context)



class DocumentCreate(CreateView):
    """
    View for creating new documents.

    Attributes:
    -----------
    form_class : DocumentsAddForm
        The form class used for creating new documents.
    template_name : str
        The name of the template used for rendering the document creation form.
    success_url : str
        The URL to redirect to after successfully creating a new document.

    Methods:
    --------
    get(self, request, *args, **kwargs)
        Handles GET requests and returns a rendered document creation form.
    post(self, request, *args, **kwargs)
        Handles POST requests and creates a new document if the form is valid.

    Returns:
    --------
    A rendered document creation form or a redirect to the success URL.
    """
    form_class = DocumentsAddForm
    template_name = 'document_create_form.html'
    success_url = reverse_lazy('document-form')


#TODO:remake entities_form function in class method
def entities_form(request):
    """
    This function handles the creation of entities form. It takes in a request object and returns a rendered HTML page with the form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A rendered HTML page with the form.

    Raises:
        None
    """
    if request.method == 'POST':
        form=EntitiesForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect("/form")
                #return redirect('form-test')
            except:
                form.add_error(None, 'Add data error')
    else:
        form=EntitiesForm()
    return render(request, 'entities_create_form.html', {'form': form})



#Form for add new documents
# def document_form(request):
#     if request.method == 'POST':
#         form=DocumentsAddForm(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 form.save()
#                 return HttpResponseRedirect("/add-document")
#                 #return redirect('form-test')
#             except:
#                 form.add_error(None, 'Add data error')
#     else:
#         form=DocumentsAddForm()
#     return render(request, 'document_create_form.html', {'form': form})


#TODO:remake files_form function in class method
def files_form(request):
    """
    This function handles the creation of a new file through a form submission. It takes in a request object and returns a rendered HTML template with the form.

    Args:
        request (HttpRequest): The HTTP request object containing the form data.

    Returns:
        HttpResponse: A rendered HTML template with the form.
    """
    if request.method == 'POST':
        form=FilesAddForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect("/add-file")
                #return redirect('form-test')
            except:
                form.add_error(None, 'Add data error')
    else:
        form=FilesAddForm()
    return render(request, 'file_create_form.html', {'form': form})


#Users registration
# class RegisterUser(CreateView):
#     form_class = RegisterUserForm
#     group_required = [u'Нет']
#     default_group, created = Group.objects.get_or_create(name='Нет')
#     User.groups.default(default_group)
#     group = Group.objects.get(name='Нет')
#     user = super().save(commit=False)
#     user.groups.add(group)
#     template_name = 'register.html'
#     success_url = reverse_lazy("login")
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         #c_def = self.get_user_context(title='Registration')
#         return dict(list(context.items()))

#TODO: remake function in class method
def UserRegister(request):
    """
    Registers a new user with the provided request data.

    Args:
        request (HttpRequest): The HTTP request object containing user registration data.

    Returns:
        HttpResponseRedirect: A redirect to the login page upon successful user registration.

    Raises:
        N/A

    Example:
        UserRegister(request)

    """
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Нет')
            user.groups.add(group)
            return redirect('login')
    else:
        form = RegisterUserForm()
    return render(request, 'register.html', {'form': form})


# Авторизация пользователей
class LoginUser(LoginView):
    """
            A class-based view for user login.

            :param form_class: The form class to use for user authentication.
            :type form_class: django.forms.Form
            :param template_name: The name of the template to use for rendering the login page.
            :type template_name: str
            """
    form_class=AuthenticationForm
    template_name = 'login.html'
    #success_url = reverse_lazy("category-list")
    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Returns a dictionary of context data for the current view.

        :param object_list: A list of objects to be used in the view.
        :type object_list: list, optional
        :param kwargs: Additional keyword arguments to be passed to the parent method.
        :type kwargs: dict
        :return: A dictionary of context data for the current view.
        :rtype: dict
        """

        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        """
        Returns the URL to redirect to after a successful form submission.

        :return: A string representing the URL to redirect to.
        :rtype: str
        """
        return reverse_lazy('category-list')

def logout_user(request):
    """
    Logs out the user associated with the given request and redirects to the category list page.

    Args:
        request (HttpRequest): The request object representing the current request.

    Returns:
        HttpResponseRedirect: A redirect response to the category list page.
    """
    logout(request)
    return redirect('category-list')


class ViewFiles(ListView):
    """
        A class-based view that displays a list of files.

        Args:
            ListView: A Django generic view that displays a list of objects.

        Attributes:
            model (Model): The model that the view will use to retrieve the list of files.
            template_name (str): The name of the template that will be used to render the view.

        Returns:
            A rendered HTML template displaying a list of files.
    """
    model = Files
    template_name = 'files_view.html'


