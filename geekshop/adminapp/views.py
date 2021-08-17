from adminapp.forms import ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.list import ListView
from mainapp.models import Product, ProductCategory
from django.db.models import F,Q


class UsersListView(LoginRequiredMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersListView, self).get_context_data()
        context['title'] = 'админка/пользователи'

        return context

    def get_queryset(self):
        return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')


class UserCreateView(LoginRequiredMixin, CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = "adminapp/user_create.html"
    success_url = '/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data()
        context['title'] = 'пользователи/создать'

        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = ShopUser
    form_class = ShopUserEditForm
    template_name = "adminapp/user_update.html"
    success_url = '/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data()
        context['title'] = 'пользователи/изменить'

        return context


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = ShopUser
    template_name = "adminapp/user_delete.html"
    success_url = reverse_lazy('admin_staff:users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class CategoriesListView(LoginRequiredMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoriesListView, self).get_context_data()
        context['title'] = 'админка/Категории'
        return context

    def get_queryset(self):
        return ProductCategory.objects.all().order_by('-is_active')


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm
    template_name = 'adminapp/category_update.html'
    success_url = '/admin_staff/categories/read/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryCreateView, self).get_context_data()
        context['title'] = 'Категории/создать'

        return context


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm
    template_name = "adminapp/category_update.html"
    success_url = '/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Категория/изменить'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin_staff:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductsListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'adminapp/products.html'
    context_object_name = 'objects'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        category_id = self.kwargs['pk']
        context.update({'category_id': category_id})
        context['title'] = 'админка/продукты'
        return context

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs['pk']).order_by('name')


class ProductDetailsView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailsView, self).get_context_data(**kwargs)
        context['title'] = 'Продукт/Детали'
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductEditForm
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('adminapp:categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreateView, self).get_context_data()
        context['title'] = 'Продукт/создать'
        category_id = self.kwargs['pk']
        context.update({'category_id': category_id})
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('adminapp:categories')
    form_class = ProductEditForm

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data()
        context['title'] = 'Продукт/создать'
        category_id = self.kwargs['pk']
        context.update({'category_id': category_id})
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('adminapp:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
