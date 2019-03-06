if (document.querySelector('input[name="csrfmiddlewaretoken"]') != null) {
	Vue.http.interceptors.push((request, next) => {
	  var csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute("value");
	  request.headers.set('X-CSRFTOKEN', csrftoken)
	  next()
	})
}

var demo = new Vue({
	el: '.site-content',
	delimiters: ["[[","]]"],
	data: {
		cart : [],
		items_composed_cart : [],
		final_composed_cart : [],
		groupedByTypologieItem : [],
		active : false,
		cart_composition_alert : '',
		cart_composition_alert_type : '',
	},

	beforeMount: function() {
		// var slug = document.getElementById('slug-id-page').getAttribute('data') || '';
		// var csrf = document.querySelector('meta[name="csrf-token"]').getAttribute('content'
	},

	mounted: function() {
		// Méthode de stockage des cookies de Vue.js
		// Stockage de la composition en cours
		var data_items_composed_cart = localStorage.getItem("items_composed_cart");
			if (data_items_composed_cart != null) {
				this.items_composed_cart = JSON.parse(data_items_composed_cart);
			};

		// Stockage des données du groupbytypologieitem (base / ingrédient)
		var data_groupedByTypologieItem = localStorage.getItem("groupedByTypologieItem");
			if (data_groupedByTypologieItem != null) {
				this.groupedByTypologieItem = JSON.parse(data_groupedByTypologieItem);
			};		

		// Stockage du panier de produits déjà prêts (autre que composition)
		var data_cart = localStorage.getItem("cart");
			if (data_cart != null) {
				this.cart = JSON.parse(data_cart);
			};

		// Stockage de final_composed_cart (stock toutes les compositions terminées)
		var data_final_composed_cart = localStorage.getItem("final_composed_cart");
			if (data_final_composed_cart != null) {
				this.final_composed_cart = JSON.parse(data_final_composed_cart);
			};


		// Fonction qui permet de rectracter le menu des différentes catégories de commandes quand on scrolle vers le bas.
		// Permet d'ajouter ou d'enlever une class à la DIV existante.

		window.document.body.onscroll = function() {
			if (document.body.scrollTop > 300) {				
				document.getElementById("menu-top-commander-id").setAttribute('class' , 'menu-top-commander menu-top-commander-smaller');
				if (document.getElementById("fixed-cart-id") != null) {
					document.getElementById("fixed-cart-id").setAttribute('class' , 'fixed-cart fixed-cart-smaller');
				}
			}
			else {
				document.getElementById("menu-top-commander-id").setAttribute('class' , 'menu-top-commander');
				if (document.getElementById("fixed-cart-id") != null) {
					document.getElementById("fixed-cart-id").setAttribute('class' , 'fixed-cart');
				}
			}
		};
	},

	methods: {

	// Méthode pour ajouter / supprimer des articles non composés
	removeactive: function(){
		this.active = false;
	},

	removedjangopopup: function(event) {
		event.target.closest('.popup-messages-overlay').remove();
	},

	// Méthode pour ajouter au panier un article prêt ou un article servant à composer un plat.

	addtoCart: function(id_article, composer) {
			// On regarde si l'article est présent dans le dictionnaire this.cart. Si = -1 cela veut dire que l'article n'existe pas dans le dictionnaire
			// On ajoute alors l'article au dictionnaire.
			var id_article = Number(id_article); // Obligatoire de convertir en nombre l'id_article sinon créé un bug dans l'ajout au panier via [[cart]]
			var item_type = String(composer);

			// Fonction permettant de grouper un dictionnaire en fonction des données d'une clé. Utilisé pour regrouper les articles de type base et les articles de type ingrédient. Doc --> https://www.consolelog.io/group-by-in-javascript/
			Array.prototype.groupBy = function(prop) {
					return this.reduce(function(groups, item) {
						const val = item[prop]
						groups[val] = groups[val] || []
						groups[val].push(item)
						return groups
					}, {})
				}

			if (item_type === "false") { // Si s'agit d'un article prêt on exécute le code ci-dessous.
				if (this.cart.findIndex(p => p.id_article === id_article) === -1) {		
					this.$http.get('http://127.0.0.1:8000/commander/api/article/' + id_article, {items: [id_article]} ).then((response) => {
						this.cart.push({ 
							'id_article': id_article, 
							'composer': response.data.article.article_composer, 
							'nom': response.data.article.nom, 
							'description': response.data.article.description, 
							'quantity': 1, 
							'price': Number(response.data.prix_vente_unitaire).toFixed(2),
							'ht_price': Number(Number(response.data.prix_vente_unitaire) / Number(response.data.article.taux_TVA.taux_applicable)).toFixed(2),
							'total_price': Number(response.data.prix_vente_unitaire).toFixed(2),
							'total_ht': Number(Number(response.data.prix_vente_unitaire) / Number(response.data.article.taux_TVA.taux_applicable)).toFixed(2),
							'total_tva': Number(Number(response.data.prix_vente_unitaire) - Number(response.data.prix_vente_unitaire) / Number(response.data.article.taux_TVA.taux_applicable)).toFixed(2),
							'taux_tva': Number(response.data.article.taux_TVA.taux_applicable).toFixed(2), 
							'image': response.data.article.image, 
							'small_size_thumbnail': response.data.article.thumbnail_small_size, 
							'middle_size_thumbnail': response.data.article.thumbnail_middle_size
						});
						console.log(response.data);
						// On créé le cookie pour stocker les données du panier.
						localStorage.setItem("cart", JSON.stringify(this.cart));

						},
					(response) => {
						console.log("Erreur - Aucun article ne correspond à l'ID")
					});
				}
				// Si la fonction trouve l'article, on ne modifie alors que la quantité
				else {
					var index = this.cart.findIndex(p => p.id_article === id_article);
					this.cart[index]['quantity'] += 1;
					this.cart[index]['total_price'] = (this.cart[index]['quantity'] * this.cart[index]['price']).toFixed(2);
					this.cart[index]['total_ht'] = (this.cart[index]['quantity'] * this.cart[index]['price'] / this.cart[index]['taux_tva']).toFixed(2);
					this.cart[index]['total_tva'] = (this.cart[index]['total_price'] - this.cart[index]['total_ht']).toFixed(2);
				}
				// Envoi de la requête POST au serveur pour ajouter une quantité.
				this.$http.post('http://127.0.0.1:8000/commander/add/' + id_article +'/', {items: [id_article]} );

				// On créé le cookie pour stocker les données du panier.
				localStorage.setItem("cart", JSON.stringify(this.cart));

			}

			else { //S'il s'agit d'un article servant à composer un plat.
				// typologie_article = Bases, Ingrédients, Plats Prêts
				this.$http.get('http://127.0.0.1:8000/commander/api/article/' + id_article ).then((response) => {
					
					// On contrôle si l'article est présent ou non dans la composition. Impossible d'ajouter le même article deux fois.
					if (this.items_composed_cart.findIndex(p => p.id_article === id_article) === -1) {
						// Si l'article n'est pas présent dans le panier, on vérfie que la personne n'ajoute pas deux bases. Il n'est possible d'ajouter qu'une seule base.
						var numBases = this.items_composed_cart.reduce(function (n, base) {
							return n + (base.typologie_article == 'Bases');
						}, 0);
						// S'il s'agit d'un ingrédient (différent d'une base)
						if (response.data.type_article.nom_type_variation_article !== "Bases") {
							this.items_composed_cart.push({ 
								'id_article': id_article, 
								'typologie_article': response.data.type_article.nom_type_variation_article, 
								'composer': response.data.article.article_composer, 
								'nom': response.data.article.nom, 
								'description': response.data.article.description, 
								'quantity': 1, 
								'price': Number(response.data.prix_vente_unitaire), 
								'total_price': Number(response.data.prix_vente_unitaire), 
								'taux_tva': Number(response.data.article.taux_TVA.taux_applicable),  
								'image': response.data.article.image, 
								'small_size_thumbnail': response.data.article.thumbnail_small_size, 
								'middle_size_thumbnail': response.data.article.thumbnail_middle_size,
								'ht_price': Number(Number(response.data.prix_vente_unitaire) / Number(response.data.article.taux_TVA.taux_applicable)),
								'total_tva': Number(Number(response.data.prix_vente_unitaire) - Number(response.data.prix_vente_unitaire) / Number(response.data.article.taux_TVA.taux_applicable)),
							});
							console.log("L'ingrédient a bien été ajouté");
							this.groupedByTypologieItem = this.items_composed_cart.groupBy('typologie_article'); // Création d'un regroupement par type article (type article d'ingrédient)
							console.log(this.groupedByTypologieItem);

							// On créé le cookie pour stocker les données du panier.
							localStorage.setItem("items_composed_cart", JSON.stringify(this.items_composed_cart));

							// On créé le cookie pour stocker les données du panier regroupé par typologie (Base, Ingrédients)
							localStorage.setItem("groupedByTypologieItem", JSON.stringify(this.groupedByTypologieItem));
						}
						// S'il n'y a pas de base de présente dans le dictionnaire, on ajoute la base sélectionnée.
						else if (response.data.type_article.nom_type_variation_article === "Bases" && numBases === 0 ) {
							this.items_composed_cart.push({ 
								'id_article': id_article, 
								'typologie_article': response.data.type_article.nom_type_variation_article, 
								'composer': response.data.article.article_composer, 
								'nom': response.data.article.nom, 
								'description': response.data.article.description, 
								'quantity': 1, 
								'price': Number(response.data.prix_vente_unitaire), 
								'total_price': Number(response.data.prix_vente_unitaire), 
								'taux_tva': Number(response.data.article.taux_TVA.taux_applicable), 
								'image': response.data.article.image, 
								'small_size_thumbnail': response.data.article.thumbnail_small_size, 
								'middle_size_thumbnail': response.data.article.thumbnail_middle_size,
								'ht_price': Number(Number(response.data.prix_vente_unitaire) / Number(response.data.article.taux_TVA.taux_applicable)),
								'total_tva': Number(Number(response.data.prix_vente_unitaire) - Number(response.data.prix_vente_unitaire) / Number(response.data.article.taux_TVA.taux_applicable)),
							});
							console.log("La base a bien été ajoutée");
							this.groupedByTypologieItem = this.items_composed_cart.groupBy('typologie_article'); // Création d'un regroupement par type article.
							console.log(this.groupedByTypologieItem);
							
							// On créé le cookie pour stocker les données du panier.
							localStorage.setItem("items_composed_cart", JSON.stringify(this.items_composed_cart));

							// On créé le cookie pour stocker les données du panier regroupé par typologie (Base, Ingrédients)
							localStorage.setItem("groupedByTypologieItem", JSON.stringify(this.groupedByTypologieItem));
						}
						// Si déjà une base présente dans le dictionnaire alors un message d'erreur doit apparaître.
						else {
							console.log("Impossible d'ajouter 2 bases à votre composition");
							this.cart_composition_alert = '<p>OUPS !</p><p> Veuillez n\'ajouter qu\'une seule base à votre composition! </p>';
							this.cart_composition_alert_type = 'Error';
							this.active = true;
						}
					}
					
					// Si l'article est déjà présent dans le panier, on n'ajoute pas l'article et on informe via une popup.
					else {
						console.log("Ce produit a déjà été ajouté");
						this.cart_composition_alert = '<p>Vous ne pouvez pas ajouter deux fois le même article !</p>';
						this.cart_composition_alert_type = 'Error';
						this.active = true;		
					}

					},

				(response) => {
					console.log("Erreur - Aucun article ne correspond à l'ID");
					this.cart_composition_alert = '<p>Erreur - Aucun article ne correspond à l\'ID</p>';
					this.cart_composition_alert_type = 'Error';
					this.active = true;
				});			
								

			}
		},


	// Fonction qui permet d'augmenter la quantité d'une compostion dans le panier finale.

	addToFinalComposedCart: function(key) {

		var next = window.location.href;
		var composition_key = String(key);

		var index = this.final_composed_cart.findIndex(p => p.key === composition_key);

		this.$http.post('http://127.0.0.1:8000/commander/cart-add-quantity-final-composed-cart/' + composition_key +'/', {next: next}).then(response => {
			this.final_composed_cart[index]['quantity'] += 1;
			this.final_composed_cart[index]['total_price'] = (this.final_composed_cart[index]['quantity'] * this.final_composed_cart[index]['price']).toFixed(2);
			this.final_composed_cart[index]['total_tva'] = (this.final_composed_cart[index]['quantity'] * this.final_composed_cart[index]['tva']).toFixed(2);
			this.final_composed_cart[index]['total_ht'] = (this.final_composed_cart[index]['quantity'] * this.final_composed_cart[index]['ht_price']).toFixed(2);
			// On créé le cookie pour stocker les données du panier.
			localStorage.setItem("final_composed_cart", JSON.stringify(this.final_composed_cart));
		}, response => {
				this.cart_composition_alert = '<p>Une erreur interne s\'est produite !</p><p> Mais rassurez-vous, vous n\y êtes pour rien.</p>';
				this.cart_composition_alert_type = 'Error';
				this.active = true;

		});	
	},

	// Fonction qui permet de diminuer la quantité d'une compostion dans le panier finale.
	removeFromFinalComposedCart: function(key) {

		var next = window.location.href;
		var composition_key = String(key);

		var index = this.final_composed_cart.findIndex(p => p.key === composition_key);

		this.$http.post('http://127.0.0.1:8000/commander/remove-one-final-composed-cart/' + composition_key +'/', {next: next}).then(response => {
			// Si la quantité de l'article est supérieure à 1, on diminue la quantité d'un
			if (this.final_composed_cart[index]['quantity'] > 1) {
				this.final_composed_cart[index]['quantity'] -= 1;
				this.final_composed_cart[index]['total_price'] = (this.final_composed_cart[index]['quantity'] * this.final_composed_cart[index]['price']).toFixed(2);
				this.final_composed_cart[index]['total_tva'] = (this.final_composed_cart[index]['quantity'] * this.final_composed_cart[index]['tva']).toFixed(2);
				this.final_composed_cart[index]['total_ht'] = (this.final_composed_cart[index]['quantity'] * this.final_composed_cart[index]['ht_price']).toFixed(2);		
				// On créé le cookie pour stocker les données du panier.
				localStorage.setItem("final_composed_cart", JSON.stringify(this.final_composed_cart));
			}
			else {
				this.final_composed_cart.splice(index, 1); // Si article est en quantité de 1, on le supprime du dictionnaire.
				// On créé le cookie pour stocker les données du panier.
				localStorage.setItem("final_composed_cart", JSON.stringify(this.final_composed_cart));
			}
		}, response => {
				this.cart_composition_alert = '<p>Une erreur interne s\'est produite !</p><p> Mais rassurez-vous, vous n\y êtes pour rien.</p>';
				this.cart_composition_alert_type = 'Error';
				this.active = true;

		});	
	},

	removeAllfromFinalComposedCart: function(key) {
			// On regarde si l'article est présent dans le dictionnaire this.cart. Si = -1 cela veut dire que l'article n'existe pas dans le dictionnaire
			// On ajoute alors l'article au dictionnaire.
			var next = window.location.href;
			var composition_key = String(key);

			if (this.final_composed_cart.findIndex(p => p.key === composition_key) === -1) {		
				console.log("L'article n'est pas présent dans le panier");
				this.cart_composition_alert = '<p>Erreur - L\'article n\'est pas présent dans le panier</p>';
				this.cart_composition_alert_type = 'Error';
				this.active = true;
			}
			// Si la fonction trouve l'article, on ne modifie alors que la quantité
			else {
				var index = this.final_composed_cart.findIndex(p => p.key === composition_key);

				this.$http.get('http://127.0.0.1:8000/commander/remove-final-composed-cart/' + composition_key +'/').then(response => {
					this.final_composed_cart.splice(index, 1); // Si article est en quantité de 1, on le supprime du dictionnaire.			
					// On créé le cookie pour stocker les données du panier.
					localStorage.setItem("final_composed_cart", JSON.stringify(this.final_composed_cart));

				}, response => {
					this.cart_composition_alert = '<p>Une erreur interne s\'est produite !</p><p> Mais rassurez-vous, vous n\y êtes pour rien.</p>';
					this.cart_composition_alert_type = 'Error';
					this.active = true;

				});
			}
		},

	modifyCompositionFinalComposedCart: function(key, slug, id) {
			
			// Fonction GroupBy
			Array.prototype.groupBy = function(prop) {
				return this.reduce(function(groups, item) {
					const val = item[prop]
					groups[val] = groups[val] || []
					groups[val].push(item)
					return groups
				}, {})
			}

			// Définition des variables
			var composition_key = String(key);
			var slug = String(slug);
			var id = String(id);

			if (this.final_composed_cart.findIndex(p => p.key === composition_key) === -1) {		
				console.log("L'article n'est pas présent dans le panier");
				this.cart_composition_alert = '<p>Erreur - L\'article n\'est pas présent dans le panier</p>';
				this.cart_composition_alert_type = 'Error';
				this.active = true;
			}
			// Si la fonction trouve l'article, on ne modifie alors que la composition et on réoriente vers la page souhaitée.
			else {
				var index = this.final_composed_cart.findIndex(p => p.key === composition_key);
				console.log("Vous allez modifier votre panier");

				// On envoie une requête GET au serveur avec le numéro de l'item à modifier.
				this.$http.get('http://127.0.0.1:8000/commander/cart-modify-final-composed-cart/'+ id + '-' + composition_key +'/').then(response => {
					
					// On créé un boucle et on réinjecte la création dans l'objet contenant la création.
					for (var item of this.final_composed_cart[index].items) {
					this.items_composed_cart.push(item)
					}

					// On créé le cookie pour stocker les données du panier.
					localStorage.setItem("items_composed_cart", JSON.stringify(this.items_composed_cart));
					// On créé le cookie pour stocker les données du panier regroupé par typologie (Base, Ingrédients)
					this.groupedByTypologieItem = this.items_composed_cart.groupBy('typologie_article');
					localStorage.setItem("groupedByTypologieItem", JSON.stringify(this.groupedByTypologieItem));

					// On supprime la composition du panier final
					this.final_composed_cart.splice(index, 1); // Si article est en quantité de 1, on le supprime du dictionnaire.			
					// On créé le cookie pour stocker les données du panier.
					localStorage.setItem("final_composed_cart", JSON.stringify(this.final_composed_cart));
					window.location.replace('http://127.0.0.1:8000/commander/composer/' + slug + '-' + id);

				}, response => {
					this.cart_composition_alert = '<p>Une erreur interne s\'est produite !</p><p> Mais rassurez-vous, vous n\y êtes pour rien.</p>';
					this.cart_composition_alert_type = 'Error';
					this.active = true;

				});				
			}
	},

	removefromCart: function(id_article, composer) {
			// On regarde si l'article est présent dans le dictionnaire this.cart. Si = -1 cela veut dire que l'article n'existe pas dans le dictionnaire
			// On ajoute alors l'article au dictionnaire.
			var id_article = Number(id_article); // Obligatoire de convertir en nombre l'id_article sinon créé un bug dans l'ajout au panier via [[cart]]
			var item_type = String(composer);

			// Fonction permettant de grouper un dictionnaire en fonction des données d'une clé. Utilisé pour regrouper les articles de type base et les articles de type ingrédient. Doc --> https://www.consolelog.io/group-by-in-javascript/
			Array.prototype.groupBy = function(prop) {
					return this.reduce(function(groups, item) {
						const val = item[prop]
						groups[val] = groups[val] || []
						groups[val].push(item)
						return groups
					}, {})
				}


			if (item_type === "false") { // Si s'agit d'un article prêt on exécute le code ci-dessous.
				if (this.cart.findIndex(p => p.id_article === id_article) === -1) {		
					console.log("L'article n'est pas présent dans le panier");
					this.cart_composition_alert = '<p>Erreur - L\'article n\'est pas présent dans le panier</p>';
					this.cart_composition_alert_type = 'Error';
					this.active = true;
				}
				// Si la fonction trouve l'article, on ne modifie alors que la quantité
				else {
					var index = this.cart.findIndex(p => p.id_article === id_article);

					this.$http.post('http://127.0.0.1:8000/commander/remove-one/' + id_article +'/').then(response => {
						// Si la quantité de l'article est supérieure à 1, on diminue la quantité d'un
						if (this.cart[index]['quantity'] > 1) {
							this.cart[index]['quantity'] -= 1;
							this.cart[index]['total_price'] = (this.cart[index]['quantity'] * this.cart[index]['price']).toFixed(2);
							this.cart[index]['total_ht'] = (this.cart[index]['quantity'] * this.cart[index]['price'] / this.cart[index]['taux_tva']).toFixed(2);
							this.cart[index]['total_tva'] = (this.cart[index]['total_price'] - this.cart[index]['total_ht']).toFixed(2);
							// On créé le cookie pour stocker les données du panier.
							localStorage.setItem("cart", JSON.stringify(this.cart));
						}
						else {
							this.cart.splice(index, 1); // Si article est en quantité de 1, on le supprime du dictionnaire.
							
							// On créé le cookie pour stocker les données du panier.
							localStorage.setItem("cart", JSON.stringify(this.cart));
						}
					}, response => {
						this.cart_composition_alert = '<p>Une erreur interne s\'est produite !</p><p> Mais rassurez-vous, vous n\y êtes pour rien.</p>';
						this.cart_composition_alert_type = 'Error';
						this.active = true;

					});		
				}
			}
			// Si c'est un article en composition, on supprime directement l'ingrédient où la base car il n'y forcément qu'une quantité d'une.
			else {
				if(this.items_composed_cart.findIndex(p => p.id_article === id_article) === -1) {
					console.log("L'article n'est pas présent dans le panier");
					this.cart_composition_alert = '<p>Erreur - L\'article n\'est pas présent dans le panier</p>';
					this.cart_composition_alert_type = 'Error';
					this.active = true;
				}

				else {
					var index = this.items_composed_cart.findIndex(p => p.id_article === id_article);

					this.items_composed_cart.splice(index, 1);	
					// On créé le cookie pour stocker les données du panier
					localStorage.setItem("items_composed_cart", JSON.stringify(this.items_composed_cart));

					this.groupedByTypologieItem = this.items_composed_cart.groupBy('typologie_article');
					// On créé le cookie pour stocker les données du panier regroupé par typologie (Base, Ingrédients)
					localStorage.setItem("groupedByTypologieItem", JSON.stringify(this.groupedByTypologieItem));

				}
			}
		
		},	


		removeAllfromCart: function(id_article, composer) {
			// On regarde si l'article est présent dans le dictionnaire this.cart. Si = -1 cela veut dire que l'article n'existe pas dans le dictionnaire
			// On ajoute alors l'article au dictionnaire.
			var id_article = Number(id_article); // Obligatoire de convertir en nombre l'id_article sinon créé un bug dans l'ajout au panier via [[cart]]
			var item_type = String(composer);

			if (item_type === "false") { // Si s'agit d'un article prêt on exécute le code ci-dessous.
				if (this.cart.findIndex(p => p.id_article === id_article) === -1) {		
					console.log("L'article n'est pas présent dans le panier");
					this.cart_composition_alert = '<p>Erreur - L\'article n\'est pas présent dans le panier</p>';
					this.cart_composition_alert_type = 'Error';
					this.active = true;
				}
				// Si la fonction trouve l'article, on ne modifie alors que la quantité
				else {
					var index = this.cart.findIndex(p => p.id_article === id_article);

					this.$http.get('http://127.0.0.1:8000/commander/remove/' + id_article +'/').then(response => {
						this.cart.splice(index, 1); // Si article est en quantité de 1, on le supprime du dictionnaire.			
						// On créé le cookie pour stocker les données du panier.
						localStorage.setItem("cart", JSON.stringify(this.cart));

					}, response => {
						this.cart_composition_alert = '<p>Une erreur interne s\'est produite !</p><p> Mais rassurez-vous, vous n\y êtes pour rien.</p>';
						this.cart_composition_alert_type = 'Error';
						this.active = true;

					});		
				}
			}


		},

		// Fin méthode pour ajouter / supprimer des articles non composés

		// Début méthode validation du panier et envoi du panier dans FinalComposedCart
		// Avant validation, il faut contrôler si :
		// - La composition n'est pas vide,
		// - Si la composition dispose bien d'au moins une base et un ingrédient.

		add_to_final_composed_cart: function(sous_categories_articles, event) {

			// ID de la sous catégorie associé à l'ajout du panier (par exemple, sandwiches, salades...)
			var sous_categories_articles = Number(sous_categories_articles);

			// On récupère l'URL d'où a été posté le formulaire et l'intègre à la variable next
			var next = window.location.href;		

			// On extrait les éléments relatifs à un possible commentaires, que l'on conertit en string et que l'on intègre à une variable.
			var comment = String(document.querySelector('textarea[name="comment"]').value)

			// On récupère la catégorie correspond à la composition (sandwiches, soupes, salades...). 
			var id_categorie_composition = Number(id_categorie_composition);

			// On compte le nombre de bases présentes dans le panier
			var numBases = this.items_composed_cart.reduce(function (n, base) {
							return n + (base.typologie_article == 'Bases');
						}, 0);

			// On compte le nombre d'ingrédients présents dans le panier
			var numIngrédients = this.items_composed_cart.reduce(function (n, ingredients) {
							return n + (ingredients.typologie_article == 'Ingrédients');
						}, 0);

			// Condition qui permet d'éviter l'ajout d'une composition vide ou d'une composition qui ne contient pas au moins un ingrédient ou pas de base
			// On ne soumet pas le formulaire d'ajout au panier final.
			if(numBases !== 1 || numIngrédients <= 0) {

				this.cart_composition_alert = '<p>AIE AIE AIE !</p><p> Veuillez au moins ajouter une base et un accompagnement à votre composition !</p>';
				this.cart_composition_alert_type = 'Error';
				this.active = true;
			}

			// On s'assure que la zone commentaire ne contient pas plus de 150 caractères. Si supérieur ou égal à 150 caractères on montre un message d'erreur
			else if(comment.length >= 150 ) {
				this.cart_composition_alert = '<p>Vous êtes trop bavard !</p><p> Le commentaire ne doit pas dépasser 150 caractères.</p>';
				this.cart_composition_alert_type = 'Error';
				this.active = true;
			}

			// Si la composition est ok, alors on peut poster tous les éléments de la compositions vers composed_cart. Et ensuite réaliser le post vers final_composed_cart
			else {
				this.$http.get('http://127.0.0.1:8000/commander/api/sous-categories-article/' + sous_categories_articles ).then((response) => {
					var sous_categories_articles_data = response.data;
					
					// On créé un dictionnaire qui va recevoir les ID des différents articles de la composition.
					var dict_items_id_composition = [];
					// On ajoute à ce dictionnaire vide les ID des articles ajoutés.
					this.items_composed_cart.forEach((d) => {
						dict_items_id_composition.push(d.id_article)
					});

					// On récupère l'ID du dernier article ajouté (nécessaire pour réaliser la POST request)
					var id_last_item_composition = dict_items_id_composition.slice(-1)[0]

					// On réalise la requête
						this.$http.post('http://127.0.0.1:8000/commander/add/' + id_last_item_composition +'/', {items: dict_items_id_composition}).then((response) => {
							if (response.status == 200) {
								// Si la requête a été un succès on vide la compositon et la variable du dernier article ajouté.
								dict_items_id_composition = [];
								id_last_item_composition = [];

								// On calcule le prix total d'une composition finalisée
								var total_tva_compostion = 0;
								var total_ht_composition = 0;
								var total_price_composition = 0;
								this.items_composed_cart.forEach((d) => {
									total_price_composition += Number(d.price);
									total_tva_compostion += Number(d.total_tva);
									total_ht_composition += Number(d.ht_price);
								});

								this.$http.post('http://127.0.0.1:8000/commander/add-composed-cart/' + sous_categories_articles + '/',{next: next, comment: comment}).then(response => {
									this.final_composed_cart.push({
									'key': Object.keys(response.data.data).slice(-1)[0], 
									'quantity': 1, 
									'price': total_price_composition.toFixed(2),
									'ht_price': total_ht_composition,
									'tva': total_tva_compostion,
									'total_tva': total_tva_compostion.toFixed(2),
									'total_ht': total_ht_composition.toFixed(2),
									'total_price': total_price_composition.toFixed(2), 
									'comment': comment, 
									'categorie_composition': sous_categories_articles_data, 
									'items': this.items_composed_cart
									}); // On intègre la composition dans le panier final_composed_cart en récupérant l'ID unique du panier généré par le backend et retourné dans la requête AJAX.
									document.querySelector('textarea[name="comment"]').value = ''; //On vide le champ commenaire après la validation du formulaire.
									
									// Popup de l'ajout avec succès.
									this.cart_composition_alert_type = 'Sucess';
									this.cart_composition_alert = '<p>YAHOU !</p><p>Votre composition a bien été ajoutée à votre panier !</p>'
									this.active = true;

									// On met à jour les cookies de composition.
									// On créé le cookie pour stocker les données du panier composition et du groupby typologie article.
									this.items_composed_cart = []; // On vide le panier composition après la validation de la compositon.
									localStorage.setItem("items_composed_cart", JSON.stringify(this.items_composed_cart));
									this.groupedByTypologieItem = [];// On vide le groupby également une fois le panier validé.
									localStorage.setItem("groupedByTypologieItem", JSON.stringify(this.groupedByTypologieItem));

									// On sauvegarde le panier final_composition dans les cookies.
									localStorage.setItem("final_composed_cart", JSON.stringify(this.final_composed_cart));
								},
								(response) => {
									this.cart_composition_alert = '<p>Erreur - Aucun article ne correspond à l\'ID</p>';
									this.cart_composition_alert_type = 'Error';
									this.active = true;
								});


							}
						}, response => {
							this.cart_composition_alert = '<p>Une erreur interne s\'est produite !</p><p> Mais rassurez-vous, vous n\y êtes pour rien.</p>';
							this.cart_composition_alert_type = 'Error';
							this.active = true;
						})

				}, response => {
					this.cart_composition_alert = '<p>Une erreur interne s\'est produite !</p><p> Mais rassurez-vous, vous n\y êtes pour rien.</p>';
					this.cart_composition_alert_type = 'Error';
					this.active = true;
				});
			}
		},

		remove_composed_cart : function(sous_categories_articles) {

			if(this.items_composed_cart.length > 0) {
				this.items_composed_cart = [];		
				// On créé le cookie pour stocker les données du panier
				localStorage.setItem("items_composed_cart", JSON.stringify(this.items_composed_cart));
				this.groupedByTypologieItem = [];
				// On créé le cookie pour stocker les données du panier regroupé par typologie (Base, Ingrédients)
				localStorage.setItem("groupedByTypologieItem", JSON.stringify(this.groupedByTypologieItem));
			}
		},

	},

	// Permet de surveiller l'ajout d'élément à la composition en cours. Si composition en cours, on demande si la personne veut réellement quitter la page.
	// Si la personne quitte la page alors, on supprime la composition en cours.
	updated: function () {

		var items_composed_cart_length = this.items_composed_cart.length;

		window.onbeforeunload = function (e) {
			if(items_composed_cart_length !== 0 && location.href !== 'http://127.0.0.1:8000/commander/panier/')
				return "Si vous quittez ou rechargez la page, votre composition ne sera pas sauvegardée.";
		};

		// On vide les cookies créés.
		if(items_composed_cart_length !== 0 && location.href !== 'http://127.0.0.1:8000/commander/panier/') 
		{
			window.onunload = e => {
				this.items_composed_cart = [];
					
				// On créé le cookie pour stocker les données du panier
				localStorage.setItem("items_composed_cart", JSON.stringify(this.items_composed_cart));

				this.groupedByTypologieItem = [];
				
				// On créé le cookie pour stocker les données du panier regroupé par typologie (Base, Ingrédients)
				localStorage.setItem("groupedByTypologieItem", JSON.stringify(this.groupedByTypologieItem));
			};
		}
	},


	computed: {
		total_cart: function() {
			var total_ready_cart = 0;

			if ((this.cart === undefined || this.cart.length == 0) && (this.final_composed_cart === undefined || this.final_composed_cart.length == 0)) {
				return "0,00"
			}

			else if ((this.cart !== undefined || this.cart.length > 0) && (this.final_composed_cart === undefined || this.final_composed_cart.length == 0)) {

				this.cart.forEach(function(item) {				
					total_ready_cart += Number(item['total_price']);
				});
				return total_ready_cart.toFixed(2) // toFixed ==> Arrondi à 2 chiffres après la virgule

			}

			else if ((this.cart === undefined || this.cart.length == 0) && (this.final_composed_cart !== undefined || this.final_composed_cart.length > 0)) {
				
				this.final_composed_cart.forEach(function(item) {				
					total_ready_cart += Number(item['total_price']);
				});
				return total_ready_cart.toFixed(2) // toFixed ==> Arrondi à 2 chiffres après la virgule
			}

			else if ((this.cart !== undefined || this.cart.length > 0) && (this.final_composed_cart !== undefined || this.final_composed_cart.length > 0)) {

				this.cart.forEach(function(item) {				
					total_ready_cart += Number(item['total_price']);
				});
				this.final_composed_cart.forEach(function(item) {				
					total_ready_cart += Number(item['total_price']);
				});
				return total_ready_cart.toFixed(2)				
			}

		},

		total_ht_cart: function() {
			var total_ready_cart = 0;

			if ((this.cart === undefined || this.cart.length == 0) && (this.final_composed_cart === undefined || this.final_composed_cart.length == 0)) {
				return "0,00"
			}

			else if ((this.cart !== undefined || this.cart.length > 0) && (this.final_composed_cart === undefined || this.final_composed_cart.length == 0)) {

				this.cart.forEach(function(item) {				
					total_ready_cart += Number(item['total_ht']);
				});
				return total_ready_cart.toFixed(2) // toFixed ==> Arrondi à 2 chiffres après la virgule

			}

			else if ((this.cart === undefined || this.cart.length == 0) && (this.final_composed_cart !== undefined || this.final_composed_cart.length > 0)) {
				
				this.final_composed_cart.forEach(function(item) {				
					total_ready_cart += Number(item['total_ht']);
				});
				return total_ready_cart.toFixed(2) // toFixed ==> Arrondi à 2 chiffres après la virgule
			}

			else if ((this.cart !== undefined || this.cart.length > 0) && (this.final_composed_cart !== undefined || this.final_composed_cart.length > 0)) {

				this.cart.forEach(function(item) {				
					total_ready_cart += Number(item['total_ht']);
				});
				this.final_composed_cart.forEach(function(item) {				
					total_ready_cart += Number(item['total_ht']);
				});
				return total_ready_cart.toFixed(2)				
			}

		},

		total_tva_cart: function() {
			var total_ready_cart = 0;

			if ((this.cart === undefined || this.cart.length == 0) && (this.final_composed_cart === undefined || this.final_composed_cart.length == 0)) {
				return "0,00"
			}

			else if ((this.cart !== undefined || this.cart.length > 0) && (this.final_composed_cart === undefined || this.final_composed_cart.length == 0)) {

				this.cart.forEach(function(item) {				
					total_ready_cart += Number(item['total_tva']);
				});
				return total_ready_cart.toFixed(2) // toFixed ==> Arrondi à 2 chiffres après la virgule

			}

			else if ((this.cart === undefined || this.cart.length == 0) && (this.final_composed_cart !== undefined || this.final_composed_cart.length > 0)) {
				
				this.final_composed_cart.forEach(function(item) {				
					total_ready_cart += Number(item['total_tva']);
				});
				return total_ready_cart.toFixed(2) // toFixed ==> Arrondi à 2 chiffres après la virgule
			}

			else if ((this.cart !== undefined || this.cart.length > 0) && (this.final_composed_cart !== undefined || this.final_composed_cart.length > 0)) {

				this.cart.forEach(function(item) {				
					total_ready_cart += Number(item['total_tva']);
				});
				this.final_composed_cart.forEach(function(item) {				
					total_ready_cart += Number(item['total_tva']);
				});
				return total_ready_cart.toFixed(2)				
			}

		},


		// Compter le nombre d'Item d'un panier

		items_quantities: function() {
			var quantities = 0;

			if ((this.cart === undefined || this.cart.length == 0) && (this.final_composed_cart === undefined || this.final_composed_cart.length == 0)) {
				return "0"
			}

			else if ((this.cart !== undefined || this.cart.length > 0) && (this.final_composed_cart === undefined || this.final_composed_cart.length == 0)) {

				this.cart.forEach(function(item) {				
					quantities += Number(item['quantity']);
				});
				return quantities

			}

			else if ((this.cart === undefined || this.cart.length == 0) && (this.final_composed_cart !== undefined || this.final_composed_cart.length > 0)) {
				
				this.final_composed_cart.forEach(function(item) {				
					quantities += Number(item['quantity']);
				});
				return quantities
			}

			else if ((this.cart !== undefined || this.cart.length > 0) && (this.final_composed_cart !== undefined || this.final_composed_cart.length > 0)) {

				this.cart.forEach(function(item) {				
					quantities += Number(item['quantity']);
				});
				this.final_composed_cart.forEach(function(item) {				
					quantities += Number(item['quantity']);
				});
				return quantities			
			}
		},

	},

});

	// addtoCart: function(id_article) {
	// 	// Fonction qui permet de savoir si un article est présent ou non dans un panier.
	// 	var found = this.cart.find(function(element) {
	// 		return element === id_article;
	// 		});

	// 	if (found === id_article) { // Si l'article est présent dans le panier, je ne modifie que la quantité.
	// 		// Fonction qui permet de récupérer l'index de l'article dans la liste.
	// 		function findIndexIdArticle(element_index) {
	// 			return element_index === id_article;
	// 		}

	// 		// La quantité à modifier se trouve dans l'object juste après l'ID Article
	// 		var IndexIdArticle = this.cart.findIndex(findIndexIdArticle) + 1  // On récupérer l'index de l'article qui est déjà présent et on sélectionne le dictionnaire d'informations de l'article.
	// 		this.cart[IndexIdArticle].quantity += 1 // On augmente la quantité de 1 à chaque fois que l'on clique sur le bouton.
	// 		this.cart[IndexIdArticle].total_price = this.cart[IndexIdArticle].quantity * this.cart[IndexIdArticle].price
	// 	}
	// 	else {
	// 		console.log("Article non présent dans le panier - Article ajouté");
	// 		this.$http.get('http://127.0.0.1:8000/commander/api/article/' + id_article ).then((response) => {
	// 			this.cart.push(id_article,{ 'nom': response.data.article.nom, 'description': response.data.article.description, 'quantity': 1, 'price': Number(response.data.prix_vente_unitaire), 'total_price': Number(response.data.prix_vente_unitaire), 'image': response.data.article.image});
	// 			},
	// 		(response) => {
	// 			console.log("Erreur - Aucun article ne correspond à l'ID")
	// 		});
	// 	}
	// 	// Envoi de la requête POST au serveur pour ajouter une quantité.
	// 	// this.$http.post('http://127.0.0.1:8000/commander/add/' + id_article +'/');
		
	// 	},




					// var id_article = 14;
					// var dict_data = [14, 4, 1];
					// 	this.$http.post('http://127.0.0.1:8000/commander/add/' + id_article +'/', {items: dict_data}).then((response) => {
					// 		console.log(response.data);
					// 	}, response => {
					// 		console.log("Erreur");
					// 	})
				// for (const item of this.items_composed_cart) {
				// 	this.$http.post('http://127.0.0.1:8000/commander/add/' + item.id_article +'/', {next: 'test', items: 'comment'}).then(async (response) => {
				// 		const body = await response.text();
				// 		if (response.status != 200) throw Error(body.message);
				// 		// if everything is fine resiolve to true or for example your body content
				// 		return Promise.resolve(true);
				// 	}, response => {
				// 		console.log("Erreur");
				// 		return Promise.resolve(false);
				// 	});					
				// }

				// for (const item of this.items_composed_cart) {
				// 	this.$http.post('http://127.0.0.1:8000/commander/add/' + item.id_article +'/').then(async (response) => {
				// 		const body = await response.text();
				// 		if (response.status != 200) throw Error(body.message);
				// 		// if everything is fine resiolve to true or for example your body content
				// 		return Promise.resolve(true);
				// 	}, response => {
				// 		console.log("Erreur");
				// 		return Promise.resolve(false);
				// 	});					
				// }
				// 	this.items_composed_cart.forEach((d) => {
				// 		this.$http.post('http://127.0.0.1:8000/commander/add/' + d.id_article +'/').then(async (response) => {
				// 			const body = await response.text();
				// 			if (response.status != 200) throw Error(body.message);
				// 			// if everything is fine resiolve to true or for example your body content
				// 			return Promise.resolve(true);
				// 		}, response => {
				// 			console.log("Erreur");
				// 			return Promise.resolve(false);
				// 		});
				// });

					// this.$http.post('http://127.0.0.1:8000/commander/add-composed-cart/' + sous_categories_articles + '/',{next: next, comment: comment}).then(response => {
					// 	this.final_composed_cart.push({'key': Object.keys(response.data.data).slice(-1)[0], 'quantity': 1, 'comment': comment, 'categorie_composition': sous_categories_articles_data, 'items': this.items_composed_cart}); // On intègre la composition dans le panier final_composed_cart en récupérant l'ID unique du panier généré par le backend et retourné dans la requête AJAX.
					// 	document.querySelector('textarea[name="comment"]').value = ''; //On vide le champ commenaire après la validation du formulaire.
						
					// 	// Popup de l'ajout avec succès.
					// 	this.cart_composition_alert_type = 'Sucess';
					// 	this.cart_composition_alert = '<p>YAHOU !</p><p>Votre composition a bien été ajoutée à votre panier !</p>'
					// 	this.active = true;

					// 	// On met à jour les cookies de composition.
					// 	// On créé le cookie pour stocker les données du panier composition et du groupby typologie article.
					// 	this.items_composed_cart = []; // On vide le panier composition après la validation de la compositon.
					// 	localStorage.setItem("items_composed_cart", JSON.stringify(this.items_composed_cart));
					// 	this.groupedByTypologieItem = [];// On vide le groupby également une fois le panier validé.
					// 	localStorage.setItem("groupedByTypologieItem", JSON.stringify(this.groupedByTypologieItem));

					// 	// On sauvegarde le panier final_composition dans les cookies.
					// 	localStorage.setItem("final_composed_cart", JSON.stringify(this.final_composed_cart));
					// },
					// (response) => {
					// 	console.log("Erreur - Aucun article ne correspond à l'ID")
					// });


	// updated: function () {

	// 	// On récupère le CSRF Token
	// 	if (document.querySelector('input[name="csrfmiddlewaretoken"]') != null) {
	// 		var csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute("value");
	// 	}

	// 	// S'il y a une composition en cours, on affiche un mssage d'erreur.
	// 	var items_composed_cart_length = this.items_composed_cart.length;

	// 	// On récupère les variables nécessaires à la requête POST
	// 	var next = window.location.href; // On récupère l'URL de la page de soumission du formulaire.
	// 	var sous_categories_articles = Number(next.slice(-1)); // On récupère dans l'URL le numéro de la catégorie (dernier digit de l'URL).

	// 	window.onbeforeunload = function (e) {
	// 		if(items_composed_cart_length !== 0)
	// 			return "Si vous quittez ou rechargez la page, votre composition ne sera pas sauvegardée.";
	// 	};

	// 	// On vide les cookies créés et on réalise une requête POST pour vider côté serveur.
	// 	window.onunload = e => {
	// 		// console.log(csrftoken);
	// 		// console.log(sous_categories_articles);
	// 		this.$http.post('http://127.0.0.1:8000/commander/remove-composed-cart/' + sous_categories_articles + '/',{next: next});
	// 		$.ajax({
	// 			type: 'POST',
	// 			async: false,
	// 			url: 'http://127.0.0.1:8000/commander/remove-composed-cart/' + sous_categories_articles + '/',
	// 			data : { 'csrfmiddlewaretoken' : csrftoken, 'next': next },

	// 		});
	// 		localStorage.removeItem('items_composed_cart');
	// 		localStorage.removeItem('groupedByTypologieItem');
	// 	};
	// },