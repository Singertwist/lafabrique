            $(function(){
        
                $('.composition-panier-final-info-date').each(function(i){
                    $('#id_picking_date').datetimepicker({
                        timeFormat: 'HH:mm',
                        dateFormat: 'dd.mm.yy',
                        firstDay: 1,
                        stepHour: 1,
                        stepMinute: 10,
                        hourMin: 8,
                        hourMax: 16,
                        monthNames: ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre'],
                        monthNamesShort: ['Jan','Fév','Mar','Avr','Mai','Jui','Jui','Aoû','Sep','Oct','Nov','Déc'],
                        dayNames: ['Dimanche','Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi'],
                        dayNamesShort: ['Dim','Lun','Mar','Mer','Jeu','Ven','Sam'],
                        dayNamesMin: ['Di','Lu','Ma','Me','Je','Ve','Sa'],
                        prevText: 'Précédent',
                        nextText: 'Suivant',
                    });
                });
            });
            