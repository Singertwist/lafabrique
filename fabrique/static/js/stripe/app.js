$(function() {

  $("#cart-payment").submit(function() {
    var form = this;

    var card = {
      number: $("#id_card_number").val(),
      exp_month: $("#id_card_validity_date").val().substr(0,2), /*Extrait les 2 premiers caractères*/
      exp_year: $("#id_card_validity_date").val().substr(-2), /*Extraire les 2 dernier caractère de l'input*/
      cvc: $("#id_cvv_number").val(),
    };

    Stripe.createToken(card, function(status, response) {
      if (status === 200) {
        console.log(status, response);
        $("#id_stripe_id").val(response.id);
        form.submit();

      } else {
        $("#stripe-error-message").text(response.error.message);
        console.log(status, response);
        /*$("#cart-payment").attr("disabled", false);*/

      }
    });

    return false;

  });

});