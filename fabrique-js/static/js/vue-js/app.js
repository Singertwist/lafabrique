Vue.http.interceptors.push((request, next) => {
  var csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute("value");
  request.headers.set('X-CSRFTOKEN', csrftoken)
  next()
})

var demo = new Vue({
	el: '.site-content',
	delimiters: ["[[","]]"],
	data: {
		loading: false,
		cart : [],
		items_composed_cart : [],
	},

	beforeMount: function() {
		// var slug = document.getElementById('slug-id-page').getAttribute('data') || '';
		// var csrf = document.querySelector('meta[name="csrf-token"]').getAttribute('content'
	},

	mounted: function() {

	},

	methods: {

	// Méthode pour ajouter / supprimer des articles non composés
	addtoCart: function(id_article, composer) {
			// On regarde si l'article est présent dans le dictionnaire this.cart. Si = -1 cela veut dire que l'article n'existe pas dans le dictionnaire
			// On ajoute alors l'article au dictionnaire.
			var id_article = Number(id_article); // Obligatoire de convertir en nombre l'id_article sinon créé un bug dans l'ajout au panier via [[cart]]
			var item_type = String(composer);

			if (item_type === "false") { // Si s'agit d'un article prêt on exécute le code ci-dessous.
				if (this.cart.findIndex(p => p.id_article === id_article) === -1) {		
					this.$http.get('http://127.0.0.1:8000/commander/api/article/' + id_article ).then((response) => {
						this.cart.push({ 'id_article': id_article, 'composer': response.data.article.article_composer, 'nom': response.data.article.nom, 'description': response.data.article.description, 'quantity': 1, 'price': Number(response.data.prix_vente_unitaire).toFixed(2), 'total_price': Number(response.data.prix_vente_unitaire).toFixed(2),  'image': response.data.article.image});
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
				// this.$http.post('http://127.0.0.1:8000/commander/add/' + id_article +'/');
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
						}

						else if (response.data.type_article.nom_type_variation_article === "Bases" && numBases === 0 ) {
							this.items_composed_cart.push({ 'id_article': id_article, 'typologie_article': response.data.type_article.nom_type_variation_article, 'composer': response.data.article.article_composer, 'nom': response.data.article.nom, 'description': response.data.article.description, 'quantity': 1, 'price': Number(response.data.prix_vente_unitaire).toFixed(2), 'total_price': Number(response.data.prix_vente_unitaire).toFixed(2),  'image': response.data.article.image});
							console.log("La base a bien été ajoutée");
						}
						// Si déjà une base présente dans le dictionnaire alors un message d'erreur doit apparaître.
						else {
							console.log("Impossible d'ajouter 2 bases à votre composition");
						}
					}
					
					// Si l'article est déjà présent dans le panier, on n'ajoute pas l'article et on informe via une popup.
					else {
						console.log("Ce produit a déjà été ajouté");			
					}

					},

				(response) => {
					console.log("Erreur - Aucun article ne correspond à l'ID");
				});			
				
				// if (this.items_composed_cart.findIndex(p => p.id_article === id_article) === -1) {
				// }

			}
		},

	removefromCart: function(id_article, composer) {
			// On regarde si l'article est présent dans le dictionnaire this.cart. Si = -1 cela veut dire que l'article n'existe pas dans le dictionnaire
			// On ajoute alors l'article au dictionnaire.
			var id_article = Number(id_article); // Obligatoire de convertir en nombre l'id_article sinon créé un bug dans l'ajout au panier via [[cart]]
			var item_type = String(composer);

			if (item_type === "false") {
				if (this.cart.findIndex(p => p.id_article === id_article) === -1) {		
					console.log("L'article n'est pas présent dans le panier");
				}
				// Si la fonction trouve l'article, on ne modifie alors que la quantité
				else {
					var index = this.cart.findIndex(p => p.id_article === id_article);
					// Si la quantité de l'article est supérieure à 1, on diminue la quantité d'un
					if (this.cart[index]['quantity'] > 1) {
						this.cart[index]['quantity'] -= 1;
						this.cart[index]['total_price'] = (this.cart[index]['quantity'] * this.cart[index]['price']).toFixed(2);
					}
					else {
						this.cart.splice(index, 1); // Si article est en quantité de 1, on le supprime du dictionnaire.
					}

					// this.$http.post('http://127.0.0.1:8000/commander/remove-one/' + id_article +'/')
				}
			}
		
		},	
		// Fin méthode pour ajouter / supprimer des articles non composés

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