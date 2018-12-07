Vue.http.interceptors.push((request, next) => {
  var csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute("value");
  request.headers.set('X-CSRFTOKEN', csrftoken)
  next()
})

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
		// var items_composed_cart_length = 0;
		// items_composed_cart_length = this.items_composed_cart.length
		// window.onbeforeunload = function (e) {
		// 	if(items_composed_cart_length !== 0)
		// 		return "Are you sure to exit?";
		// }
		
		// Méthode de stockage des cookies de Vue.js
		var data_items_composed_cart = localStorage.getItem("items_composed_cart");
			if (data_items_composed_cart != null) {
				this.items_composed_cart = JSON.parse(data_items_composed_cart);
			};

		var data_cart = localStorage.getItem("cart");
			if (data_cart != null) {
				this.cart = JSON.parse(data_cart);
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
					this.$http.get('http://127.0.0.1:8000/commander/api/article/' + id_article ).then((response) => {
						this.cart.push({ 'id_article': id_article, 'composer': response.data.article.article_composer, 'nom': response.data.article.nom, 'description': response.data.article.description, 'quantity': 1, 'price': Number(response.data.prix_vente_unitaire).toFixed(2), 'total_price': Number(response.data.prix_vente_unitaire).toFixed(2),  'image': response.data.article.image});
						
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
				}
				// Envoi de la requête POST au serveur pour ajouter une quantité.
				this.$http.post('http://127.0.0.1:8000/commander/add/' + id_article +'/');

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
						// S'il n'y a pas de base de présente dans le dictionnaire, on ajouter la base sélectionnée.
						if (response.data.type_article.nom_type_variation_article !== "Bases") {
							this.items_composed_cart.push({ 'id_article': id_article, 'typologie_article': response.data.type_article.nom_type_variation_article, 'composer': response.data.article.article_composer, 'nom': response.data.article.nom, 'description': response.data.article.description, 'quantity': 1, 'price': Number(response.data.prix_vente_unitaire).toFixed(2), 'total_price': Number(response.data.prix_vente_unitaire).toFixed(2),  'image': response.data.article.image});
							console.log("L'ingrédient a bien été ajouté");
							this.groupedByTypologieItem = this.items_composed_cart.groupBy('typologie_article'); // Création d'un regroupement par type article (type article d'ingrédient)
							console.log(this.groupedByTypologieItem);
							this.$http.post('http://127.0.0.1:8000/commander/add/' + id_article +'/');

							// On créé le cookie pour stocker les données du panier.
							localStorage.setItem("items_composed_cart", JSON.stringify(this.items_composed_cart));
						}

						else if (response.data.type_article.nom_type_variation_article === "Bases" && numBases === 0 ) {
							this.items_composed_cart.push({ 'id_article': id_article, 'typologie_article': response.data.type_article.nom_type_variation_article, 'composer': response.data.article.article_composer, 'nom': response.data.article.nom, 'description': response.data.article.description, 'quantity': 1, 'price': Number(response.data.prix_vente_unitaire).toFixed(2), 'total_price': Number(response.data.prix_vente_unitaire).toFixed(2),  'image': response.data.article.image});
							console.log("La base a bien été ajoutée");
							this.groupedByTypologieItem = this.items_composed_cart.groupBy('typologie_article'); // Création d'un regroupement par type article.
							console.log(this.groupedByTypologieItem);
							this.$http.post('http://127.0.0.1:8000/commander/add/' + id_article +'/');
							
							// On créé le cookie pour stocker les données du panier.
							localStorage.setItem("items_composed_cart", JSON.stringify(this.items_composed_cart));
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

	removefromCart: function(id_article, composer) {
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
					// Si la quantité de l'article est supérieure à 1, on diminue la quantité d'un
					if (this.cart[index]['quantity'] > 1) {
						this.cart[index]['quantity'] -= 1;
						this.cart[index]['total_price'] = (this.cart[index]['quantity'] * this.cart[index]['price']).toFixed(2);
						
						// On créé le cookie pour stocker les données du panier.
						localStorage.setItem("cart", JSON.stringify(this.cart));
					}
					else {
						this.cart.splice(index, 1); // Si article est en quantité de 1, on le supprime du dictionnaire.
						
						// On créé le cookie pour stocker les données du panier.
						localStorage.setItem("cart", JSON.stringify(this.cart));
					}

					this.$http.post('http://127.0.0.1:8000/commander/remove-one/' + id_article +'/')
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
					this.groupedByTypologieItem = this.items_composed_cart.groupBy('typologie_article');
					
					// On créé le cookie pour stocker les données du panier
					localStorage.setItem("items_composed_cart", JSON.stringify(this.items_composed_cart));
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
				this.$http.post('http://127.0.0.1:8000/commander/add-composed-cart/' + sous_categories_articles + '/',{next: next, comment: comment})
				this.final_composed_cart.push(this.items_composed_cart); // On intègre la composition dans le panier final_composed_cart
				this.items_composed_cart = []; // On vide le panier composition après la validation de la compositon.
				document.querySelector('textarea[name="comment"]').value = ''; //On vide le champ commenaire après la validation du formulaire.
				
				// Popup de l'ajout avec succès.
				this.cart_composition_alert_type = 'Sucess';
				this.cart_composition_alert = '<p>YAHOU !</p><p>Votre composition a bien été ajoutée à votre panier !</p>'
				this.active = true;
			}
		},

		remove_composed_cart : function(sous_categories_articles) {

			// ID de la sous catégorie associé à la suppression du panier (par exemple, sandwiches, salades...)
			var sous_categories_articles = Number(sous_categories_articles);

			// On récupère l'URL d'où a été posté le formulaire et l'intègre à la variable next
			var next = window.location.href;

			if(this.items_composed_cart.length > 0) {
				this.$http.post('http://127.0.0.1:8000/commander/remove-composed-cart/' + sous_categories_articles + '/',{next: next});
				this.items_composed_cart = [];
				
				// On créé le cookie pour stocker les données du panier
				localStorage.setItem("items_composed_cart", JSON.stringify(this.items_composed_cart));
			}
		},

	},

	computed: {
		total_cart: function() {
			if (this.cart === undefined || this.cart.length == 0) {
				return "0,00"
			}

			else {
				var total_ready_cart = 0;
				this.cart.forEach(function(item) {				
					total_ready_cart += Number(item['total_price']);
				});
				return total_ready_cart.toFixed(2) // toFixed ==> Arrondi à 2 chiffres après la virgule
			}
		}
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