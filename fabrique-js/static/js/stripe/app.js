/*Script Jquery qui permet d'extraire les données entrées dans les inputs */

$(function() {
  
  /*Traduction des erreurs Jquery*/
  var errorMessages = {
    incorrect_number: "Le numéro de carte est incorrect.",
    invalid_number: "Veuillez vérifier votre numéro de carte ou la date d'expiration.",
    invalid_expiry_month: "Le mois d'expiration de la carte est invalide.",
    invalid_expiry_year: "L'année d'expiration de la carte est invalide.",
    invalid_cvc: "Le numéro secret de la carte est invalide.",
    expired_card: "La carte a expiré.",
    incorrect_cvc: "Le numéro secret de la carte est incorrecte.",
    incorrect_zip: "Le code postal de la carte est incorrect.",
    card_declined: "Le paiement a été refusé.",
    missing: "There is no card on a customer that is being charged.",
    processing_error: "Une erreur s'est produite pendant le traitement du paiement. Veuillez réessayer ou contacter le service client.",
    rate_limit:  "An error occurred due to requests hitting the API too quickly. Please let us know if you're consistently running into this error."
  };

  $("#cart-payment").submit(function() {
    var form = this;

    var card = {
      number: $("#id_card_number").val(),
      exp_month: $("#id_card_validity_date").val().substr(0,2), /*Extrait les 2 premiers caractères de la date de validité --> Année*/
      exp_year: $("#id_card_validity_date").val().substr(-2), /*Extraire les 2 dernier caractère de l'input de la date de valdiité --> Année*/
      cvc: $("#id_cvv_number").val(),
    };

    Stripe.createToken(card, function(status, response) {
      if (status === 200) {
        console.log(status, response);
        $("#id_stripe_id").val(response.id);
        form.submit();

      } else {
          $("#stripe-error-card").show(); /*Permet d'afficher le message d'erreur qui est en hidden dans le fichier css.*/
          $("#stripe-error-card").text(errorMessages[ response.error.code ]);
/*        $("#stripe-error-message").text(response.error.message);
        console.log(status, response);
        alert(response.error.code);
        $("#cart-payment").attr("disabled", false);*/

      }
    });

    return false;

  });

});

/*Mise en forme du champ date de la carte --> Insertion automatique d'un slash entre le mois et l'année*/
function formatCode(str){
    var result = str;

    str = str.replace(/\D+/g, "");
    var m = str.match(/^(\d\d)(?:([2-90]\d|1)(?:(\d\d\d)(\d+)?)?)?$/);

    if(m){
        result = m[1] + "/";
        if(m[2]) result += m[2] + "";

    }
    
    return result;
}

function update(obj){
    var val = obj.value;
    var got = formatCode(val);
    
    if(got != val)
        obj.value = got;
}

var timer;
var prev_val = "";

$('#id_card_validity_date').keyup(function(){
    clearTimeout(timer);
    
    // when adding numbers at the end of input, update at once
    // don't want to update when editing in the middle of the string or removing parts
    // because it would move the carret location to the end of input, and make it unusable
    if(this.value.indexOf(prev_val) == 0){
        update(this);
        prev_val = this.value;
        return;
    }
    
    prev_val = this.value;
    
    // else update 1 second after the changes are done
    timer = setTimeout(update, 1000, this);
});