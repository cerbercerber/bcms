$("document").ready(function(e)
{

$("#devoirs-tab").on('click',function(e){
    $("#modedt").val("devoir");
     $('#calendarel').fullCalendar('refetchEvents');
     $('#calendarel').fullCalendar('changeView', 'agendaWeek');
});
$("#controle-tab").on('click',function(e){
    $("#modedt").val("controle");
     $('#calendarel').fullCalendar('refetchEvents');
     $('#calendarel').fullCalendar('changeView', 'agendaWeek');
});
$("#edt-tab").on('click',function(e){
    $("#modedt").val("edt");
     $("#panelcalendar").css({"visibility": "visible"});       
     $('#calendarel').fullCalendar('refetchEvents');
     $('#calendarel').fullCalendar('changeView', 'month');
});

//if ($('#calendartable:visible').length)
var oTable=$('#calendartable').DataTable( {
    "ajax": {
        "url": "eleveedt",
        "type": "POST",
          data:  function () { // a function that returns an object
                return {
                    disp: "liste",
                    mode: $('#modedt').val(),
                    start: function(d){ if ($('#calendarel').fullCalendar( 'getView')) return $('#calendarel').fullCalendar( 'getView').start;return null; },
                    end: function(d){ if ($('#calendarel').fullCalendar( 'getView')) return $('#calendarel').fullCalendar( 'getView').end;return null; }
   
                } ;} , 
        
    },
    "columns": [
        // { "data": "idcours" },
         { "data": "title" },
         { "data": "start" },
         { "data": "end" },
        { data: 'idcours', render: function (data, type, row) {
            var mode=$('#modedt').val();
            var color="";
            if (mode=="edt") color="style='color:#007bffa'";
            else if (mode=="controle") color="style='color:red'";
            else if (mode=="devoir") color="style='color:#CCCC00'";
            return '<a href="/bo/administratif/cours/'+data+'"><i class="fas fa-info-circle" '+color+'></i>&nbsp;détails</a>';
        } }
          
     ],
      "paging":   false,
       "ordering": true,
       "info":     false,
       "searching": false
    } );
    

/*fullcalendar*/
$('#calendarel').fullCalendar({
    events: 
    {
        url: "eleveedt",
        type: 'POST',
        data:  function () { // a function that returns an object
                return {
                    mode: $('#modedt').val(),
                } ;} , 
        color: '#007bff',   // a non-ajax option
        textColor: 'white' // a non-ajax option
    },
    editable:false,
     header: {
        left: 'prev,next today',
        center: 'title',
        right: 'agendaWeek,agendaDay,month'
      },
    defaultView: 'month',
    allDaySlot : false,
    displayEventEnd:true,
    minTime : "07:00:00",
    maxTime : "21:00:00",
    height:'auto',
    locale: 'fr',
    lazyFetching:false,
      viewRender: function (view, element) {
    //alert("ok");
     oTable.ajax.reload();
    },
    loading: function (bool) {               
                    if (!bool)
                      {                                   
                        $('#loading').hide();
                        $("#panelcalendar").css({"visibility": "visible"});                     
                        $(".fc-button").attr('class',"btn btn-link btn-outline-primary");    
                        $("#panelheadingcalendar").replaceWith($(".fc-toolbar"));    
                        $("#listcal").remove();
                        //console.log($("#calendarel").is(":visible"));
                        if($("#calendarel").is(":visible"))                    
                            $(".fc-right .fc-button-group").append("<button type='button'  id='listcal' class='btn btn-link btn-outline-primary' mode='liste'>Liste</button>");  
                        else
                            $(".fc-right .fc-button-group").append("<button type='button'  id='listcal' class='btn btn-link btn-outline-primary' mode='cal'>Calendrier</button>");                     
                      //hide disp calendar
                        $("#listcal").on('click', function(e)
                         {
                            e.preventDefault();
                            var mode=$(this).attr("mode");
                            if (mode == "liste") {$(this).attr("mode","cal");$(this).html("Calendrier"); $("#calendartablediv").show();$("#calendarel").hide();}
                            else /*if (mode == "cal")*/  {$(this).attr("mode","liste");$(this).html("Liste"); $("#calendartablediv").hide();$("#calendarel").show();$('#calendarel').fullCalendar('refetchEvents');}
                         });  
                      }
                else
                    {
                        $("#panelcalendar").css({"visibility": "hidden"});
                        $('#loading').show();   
               
                    }
                      },
    eventRender: function(event, element) {
        if (parseInt(event.nbdevoirs)>0)         
            element.append("<span class='float-right text-warning'><strong>Devoir</strong></span>");
        if ((parseInt(event.nbdevoirs)>0) && (parseInt(event.nbcont)>0))  element.append("<br/>");
        if (parseInt(event.nbcont)>0)         
            element.append("<span class='float-right text-danger'><strong>Controle</strong></span>");
        if(event.type == "controle") {
                    element.css('background-color', 'red');
                }
         else if(event.type == "devoir") {
                    element.css('background-color', '#CCCC00');
                }
}
                      
});
});