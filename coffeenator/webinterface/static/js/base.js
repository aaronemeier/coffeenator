$(document).ready(function(){
	$(".accept-dialog").dialog({
		autoOpen: false,
		height: 300,
		width: 400,
		modal: true
	});
 	$("#acceptlogout").click(function() {
		$( "#logout-dialog" ).dialog( "open" );
	});
	$("#logoutuser").click(function(){
		$.ajax({
		    url: "/login/ajax/",
		    type: "POST",
		    data: "logout=1",
		    success: function(msg){
		        if(parseInt(msg)!=0){
		            function sleep(milliSeconds){
		                document.devCheater.sleep(milliSeconds);
		            }
		        }
		        window.location = "/login/";
		    }
		});
		return false;
	});
}); 