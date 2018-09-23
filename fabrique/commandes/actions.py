# Fonction d'export au format CSV
from django.http import HttpResponse
import csv
import datetime

# Méthode utilisable uniquement pour exporter l'ongler des ventes. Créé une ligne pour item présent dans la commande.
def export_to_csv_sales(modeladmin, request, queryset):
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
					values = list(getattr(obj, field.name).all().values_list('id', flat=True)) # On récupérère sous forme de liste les id relatifs aux articles.
				except:
					value = str(obj).replace(";", "") # Replace permet de supprimer les point virgule des chaines de caractères afin de ne pas interférer avec le séparateur du CSV.
			else:
				value = str(getattr(obj, field.name)).replace(";", "") # Replace permet de supprimer les point virgule des chaines de caractères afin de ne pas interférer avec le séparateur du CSV.
			if isinstance(value, datetime.datetime):
				value = value.strftime('%d/%m/%Y')
			data_row.append(value) # On aggrège toutes les données d'une ligne dans la liste data_row.

		# Si values est différent de None, cela veut dire que l'on a une liste présente dans la commande. Donc une composition. On va créé pour une ligne pour chaque item de la composition. 
		if values != None:
			for data in values: # On parcours la liste contenant les différents ingrédients de la commande.
				data_row[-1] = data # On remplace la liste par les données de la liste. Pour sélectionner la dernière colonne contenant les produits, on utilise l'index [-1], le -1 signifie que l'on sélection la première colonne en partant de la fin.
				writer.writerow(data_row) # On écrit une ligne avec l'ID qui a été inséré
		else:
			writer.writerow(data_row) # S'il n'y a pas de composition on écrit la ligne normalement.
	return response
export_to_csv_sales.short_description = 'Export to CSV'


# Il s'agit des exports normaux. On ne créé pas de ligne si présence d'une liste dans une cellule.
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
					values = list(getattr(obj, field.name).all().values_list('id', flat=True)) # On récupérère sous forme de liste les id relatifs aux articles.
					value = ','.join(map(str, values))
				except:
					value = str(obj).replace(";", "") # Replace permet de supprimer les point virgule des chaines de caractères afin de ne pas interférer avec le séparateur du CSV.
			else:
				value = str(getattr(obj, field.name)).replace(";", "") # Replace permet de supprimer les point virgule des chaines de caractères afin de ne pas interférer avec le séparateur du CSV.
			if isinstance(value, datetime.datetime):
				value = value.strftime('%d/%m/%Y')
			data_row.append(value) # On aggrège toutes les données d'une ligne dans la liste data_row.
		writer.writerow(data_row)
	return response
export_to_csv.short_description = 'Export to CSV'


		# if id_list != None:
		# 	data_index = 0
		# 	for data in id_list:
		# 		for test in value:
		# 			if isinstance(test, list):
		# 				data_index = value.index(test)
		# 		data_row[data_index] = data
		# 		writer.writerow(data_row)
		# else:
		# 	writer.writerow(data_row)
		# if any(isinstance(data, list) for data in data_row):

		# On créé le nombre de lignes nécessaires. Si un champ many to many dispose de 4 items, alors on créé 4 lignes.
		# r = 0
		# while r < number_of_rows:
		# 	writer.writerow(data_row)
		# 	r += 1


		# for data in values: # On récupère la liste contenant tous les ID du champ many to many, on créé une boucle pour parcourir la liste.
		# 	data_row[-1] = data # On a la liste contentant toutes les données d'une ligne (data_row). On met 
		# 	writer.writerow(data_row)
		# if values != None:
		# 	for data in values:
		# 		data_row[-1] = data
		# 		writer.writerow(data_row)
		# writer.writerow(data_row)