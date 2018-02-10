function remove_div_ft(id){
	var total = $('#rsvp').children('div').length;
	var value = id.slice(4);
//	alert("value is"+value);
	$('#div_'+value).remove();
	for (var i = parseInt(value)+1; i < total; i++) {
//		alert("In loop: "+i);
		$('#ft_cb_'+i).attr('name','ft_cb_'+(i-1))
		$('#ft_cb_'+i).attr('id','ft_cb_'+(i-1))
		$('#div_'+i+' span').text(i);
		$('#del_'+i).attr('id','del_'+(i-1));
		$('#input_'+i).attr('name','ft_'+(i-1));
		$('#input_'+i).attr('id','input_'+(i-1))
		$('#div_'+i).attr('id','div_'+(i-1));
	}
}

function decrese_choice(id){
	var div = $('#mc_'+id+' div').first();
	var total = div.children('div').length;
	for (var i=0;i<total;i++){
		$('#mc_del_'+id+"_"+i).attr('id','mc_del_'+(id-1)+"_"+i);
		$('#mc_'+id+"_"+i+' input').first().attr('name','mc_'+(id-1)+"_"+i);
		$('#mc_'+id+"_"+i).attr('id','mc_'+(id-1)+"_"+i);
	}
}

function remove_div_mc_q(id){
	var total = $('#mc').children('div').length;
	var value = id.slice(7);
//	alert("value is"+value);
	$('#mc_'+value).remove();
	for (var i = parseInt(value)+1; i < total; i++) {
		
		decrese_choice(i);
//		alert("In loop: "+i);
		$('#mc_cb_'+i).attr('name', '#mc_cb_'+(i-1))
		$('#mc_cb_'+i).attr('id', '#mc_cb_'+(i-1))
		$('#mc_del_'+i).attr('id','mc_del_'+(i-1));
		$('#mc_add_choice_'+i).attr('id','mc_add_choice_'+(i-1));
		$('#mc_'+i+' input').first().attr('name','mc_'+(i-1));
		$('#mc_'+i).attr('id','mc_'+(i-1));
	}

}

function delete_choice(id){
	var part = id.split('_');
	var cid = part[3];
	var qid = part[2];
	var total = $('#mc_'+qid+" div").first().children('div').length;
	$('#mc_'+qid+"_"+cid).remove();
	console.log(total);
	for (var i = parseInt(cid)+1; i < total; i++) {
		$('#mc_del_'+qid+"_"+i).attr('id','mc_del_'+qid+"_"+(i-1));
		$('#mc_'+qid+"_"+i+" input").first().attr('name','mc_'+qid+"_"+(i-1));
		$('#mc_'+qid+"_"+i).attr('id','mc_'+qid+"_"+(i-1));
	}
}

function add_choice(id){	
	var value = id.slice(14);
	var total = $('#mc_'+value+' div').first().children('div').length;
//	console.log(total);
	$('#mc_'+value+' div').first().append(
		"<div id='mc_"+value+"_"+total+"'><input type='text' name='mc_"+value+"_"+total+"'/><input id='mc_del_"+value+"_"+total+"' type='button' value='delete choice'/></div>"
	);
	$("#mc_del_"+value+"_"+total).click(function() {
	    	delete_choice($(this).attr('id'))
	    });
}

$(document).ready(function() {
	$('#add_more_mc_q').click(function(){
		var total = $('#mc').children('div').length;
		$('#mc').append(
			"<div id='mc_"+total+"'>Question: <input type='text' name='mc_"+total+"'/><br/><div></div>Vendor can see<input id='mc_cb_"+total+"' type='checkbox' name='mc_cb_"+total+"'><br/><input id='mc_del_"+total+"' type='button' value='delete question'/><input id='mc_add_choice_"+total+"' type='button' value='add choice'/><hr/></div>"
			);
		$('#mc_del_'+total).click(function(){
			remove_div_mc_q($(this).attr('id'))
	    });

	    $('#mc_add_choice_'+total).click(function() {
	    	add_choice($(this).attr('id'))
	    });
	});

    $('#add_more_rsvp').click(function() {
        var total = $('#rsvp').children('div').length;
	    $('#rsvp').append("<div id='div_"+total+"'>Question <span>"+(total+1)+"</span><input id='input_"+total+"' type='text' name='ft_"+total+"'/><br/>Vendor can see<input id='ft_cb_"+total+"' type='checkbox' name='ft_cb_"+total+"'><input type='button' value='delete' class='deleteRsvp' id='del_"+total+"'/></div>");
	    $('#del_'+total).click(function(){
			remove_div_ft($(this).attr('id'))
	    });
    });
});