# Fonction d'export au format CSV
import unicodecsv
from django.http import HttpResponse
import csv
import datetime

def export_as_csv_action(description="Export selected objects as CSV file", fields=None, exclude=None, header=True):

	def export_as_csv(modeladmin, request, queryset):

		opts = modeladmin.model._meta

		if not fields:
			field_names = [field.name for field in opts.fields]
		else:
			field_names = fields

		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=%s.csv' % str(opts).replace('.', '_')

		writer = unicodecsv.writer(response, encoding='utf-8')
		if header:
			writer.writerow(field_names)
		for obj in queryset:
			row = [getattr(obj, field)() if callable(getattr(obj, field)) else getattr(obj, field) for field in field_names]
			writer.writerow(row)
		return response
	export_as_csv.short_description = description
	return export_as_csv




def export_to_csv(modeladmin, request, queryset):
	opts = modeladmin.model._meta
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=%s.csv' % str(opts).replace('.', '_')
	writer = csv.writer(response, delimiter=";")
	# fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
	fields = []
	fields = [field for field in opts.get_fields()]

	# Write a first row with header information
	# writer.writerow([field.verbose_name.title() for field in fields]) # Title nécessaire car sinon ID est le premier champ et provoque un avertissement lors de l'ouverture sous Excel( fichier de type Sylk).
	writer.writerow([field.name.title() for field in fields])


	# Write data rows
	for obj in queryset:
		data_row = []
		for field in fields:		
			if field.many_to_many == True or field.one_to_many == True:
				try:
					value = list(getattr(obj, field.name).all().values_list('id', flat=True)) # On récupérère sous forme de liste les id relatifs aux articles.
				except:
					value = str(obj).replace(";", "") # Replace permet de supprimer les point virgule des chaines de caractères afin de ne pas interférer avec le séparateur du CSV.
			else:
				value = str(getattr(obj, field.name)).replace(";", "") # Replace permet de supprimer les point virgule des chaines de caractères afin de ne pas interférer avec le séparateur du CSV.
			if isinstance(value, datetime.datetime):
				value = value.strftime('%d/%m/%Y')
			data_row.append(value)
		writer.writerow(data_row)
	return response
export_to_csv.short_description = 'Export to CSV'
