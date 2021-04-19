from django.contrib import admin

from .models import Customer, Product, Sale, Location


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'get_full_name',
        'mobile_number',
        'email',
        'deal_stage',
        'date_created',
        'date_to_be_contacted'
    ]
    list_filter = [
        'deal_stage',
        'date_created',
    ]

    def save_model(self, request, obj, form, change):
        '''
        Method to ensure saved customers will be automatically assigned to the creator.
        :param request: request object
        :param obj: instance of Customer
        :param form: N/A
        :param change: N/A
        :return: N/A
        '''

        obj.created_by = request.user
        obj.save()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass
