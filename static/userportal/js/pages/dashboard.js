//------------- Dashboard.js -------------//
$(document).ready(function() {
    
     $("#basic-datepicker").datepicker();
    //multiple date
    $("#multiple-datepicker").datepicker({
    	multidate: true
    });
    //date range
    $(".input-daterange").datepicker();
    //inline
    $("#inline-datepicker").datepicker();
    
    
    
    
    
    
    
    
    
    
    
   

	//------------- Sparklines in header stats -------------//
	$('#spark-visitors').sparkline([5,8,10,8,7,12,11,6,13,8,5,8,10,11,7,12,11,6,13,8], {
		type: 'bar',
		width: '100%',
		height: '20px',
		barColor: '#dfe2e7',
		zeroAxis: false,
	});

	$('#spark-templateviews').sparkline([12,11,6,13,8,5,8,10,12,11,6,13,8,5,8,10,12,11,6,13,8,5,8], {
		type: 'bar',
		width: '100%',
		height: '20px',
		barColor: '#dfe2e7',
		zeroAxis: false,
	});

	$('#spark-sales').sparkline([19,18,20,17,20,18,22,24,23,19,18,20,17,20,18,22,24,23,19,18,20,17], {
		type: 'bar',
		width: '100%',
		height: '20px',
		barColor: '#dfe2e7',
		zeroAxis: false,
	});

	//------------- Animated progressbars on tiles -------------//
	//animate bar only when reach the bottom of screen
	$('.animated-bar .progress-bar').waypoint(function(direction) {
		$(this).progressbar({display_text: 'none'});
	}, { offset: 'bottom-in-view' });
	
	//------------- CounTo for tiles -------------//
	$('.stats-number').countTo({
        speed: 1000,
        refreshInterval: 50
    });

    //------------- Flot charts -------------//

	//define chart colours first
	var chartColours = {
		gray: '#bac3d2',
		teal: '#43aea8',
		blue: '#60b1cc',
		red: '#df6a78',
		orange: '#cfa448',
		gray_lighter: '#e8ecf1',
		gray_light: '#777777',
		gridColor: '#bfbfbf'
	}

	//convert the object to array for flot use
	var chartColoursArr = Object.keys(chartColours).map(function (key) {return chartColours[key]});

	//generate random number for charts
	randNum = function(series){
		return (Math.floor( Math.random()* (1+10-1) + series));
	}

	//-------------Line chart -------------//
	/*
    $(function () {
		//some data

		var d1 = [];
		var d2 = [];

		for (i = 0; i < 31; i++) { 
		    d1.push([new Date(Date.today().add(i).days().getTime()), i + randNum(10)]);
		    d2.push([new Date(Date.today().add(i).days().getTime()), i + randNum(20)]);
		}

		
		var chartMinDate = d1[1][0]; //first day
    	var chartMaxDate = d1[30][0];//last day

    	var tickSize = [1, "day"];
    	var tformat = "%d/%b";

		var options = {
			grid: {
				show: true,
			    aboveData: true,
			    color: chartColours.gridColor,
			    labelMargin: 15,
			    axisMargin: 0, 
			    borderWidth: 0,
			    borderColor:null,
			    minBorderMargin: 5,
			    clickable: true, 
			    hoverable: true,
			    autoHighlight: true,
			    mouseActiveRadius: 20
			},
	        series: {
	        	grow: {active:true},
	            lines: {
            		show: true,
            		fill: false,
            		lineWidth: 2,
            		steps: false
	            },
	            curvedLines: {
                    apply: false,
                    active: true,
                    monotonicFit: true
                },
	            points: {show:false}
	        },
	        legend: { 
	        	position: "ne", 
	        	margin: [0,-25], 
	        	noColumns: 0,
	        	labelBoxBorderColor: null,
	        	labelFormatter: function(label, series) {
				    // just add some space to labes
				    return '&nbsp;&nbsp;' + label + ' &nbsp;&nbsp;';
				},
				width: 30,
				height: 2
	    	},
	        yaxis: { min: 0 },
		    xaxis: {
		    	mode: "time",
	        	minTickSize: tickSize,
	        	timeformat: tformat,
	        	min: chartMinDate,
	        	max: chartMaxDate,
	        	tickLength: 0
		    },
	        colors: chartColoursArr,
        	shadowSize:1,
	        tooltip: true, //activate tooltip
			tooltipOpts: {
				content: "%s : %y.0" + " $",
				shifts: {
					x: -30,
					y: -50
				}
			}
	    };   

    	$.plot($("#line-chart-payments"), [ 
    		{
    			label: "Sales", 
    			data: d1,
    			lines: {fillColor: chartColours.gray}	
    		}, 
    		{	
    			label: "Profits", 
    			data: d2,
    			lines: {fillColor: chartColours.teal}
    		} 

    	], options);

	});*/
    
    
    
    	$(function () {
		//some data
	
	    var d2 = [];
	    for (var i = 0; i <= 10; i += 1)
	        d2.push([i, parseInt(Math.random() * 30)]);
	 
	    var d3 = [];
	    for (var i = 0; i <= 10; i += 1)
	        d3.push([i, parseInt(Math.random() * 30)]);
	 
	    var ds = new Array();
	 
	   
	    ds.push({
	    	label: "Sales",
	        data:d2,
	        bars: {order: 2}
	    });
	    ds.push({
	    	label: "Profit",
	        data:d3,
	        bars: {order: 3}
	    });

	    var stack = 0, bars = false, lines = false, steps = false;

		var options = {
				bars: {
					show:true,
					barWidth: 0.3,
					fill:1
				},
				grid: {
					show: true,
				    aboveData: false,
				    color: chartColours.gridColor,
				    labelMargin: 5,
				    axisMargin: 0, 
				    borderWidth: 0,
				    borderColor:null,
				    minBorderMargin: 5 ,
				    clickable: true, 
				    hoverable: true,
				    autoHighlight: false,
				    mouseActiveRadius: 20
				},
		        series: {
		        	stack: stack
		        },
		        legend: { 
		        	position: "ne", 
		        	margin: [0,-25], 
		        	noColumns: 0,
		        	labelBoxBorderColor: null,
		        	labelFormatter: function(label, series) {
					    // just add some space to labes
					    return '&nbsp;&nbsp;' + label + ' &nbsp;&nbsp;';
					},
					width: 30,
					height: 2
		    	},
		        colors: chartColoursArr,
		        tooltip: true, //activate tooltip
				tooltipOpts: {
					content: "%s : %y.0",
					shifts: {
						x: -30,
						y: -50
					}
				}
		};

		$.plot($("#ordered-bars-chart"), ds, options);
	});

	//------------- Sparkline in payment received chart -------------//
	$('.spark-payments').sparkline([5,8,10,8,7,12,11,6,13,8,5,8,10,11,7,12,11,6,13], {
		type: 'bar',
		width: '100%',
		height: '20px',
		barColor: '#a8aeb7',
		zeroAxis: false,
	});

	//------------- User satisfaction chart -------------//
	var customerProgress = new ProgressBar.Circle('#customer-exp', {
	    color: '#0a97b9',
	    strokeWidth: 2,
	    fill: '#d0f1f9',
	    duration: 4000,
	    easing: 'bounce'
	});
	customerProgress.animate(0.8);

	

	//------------- New user notifications -------------//
	function capitalise(string) {
	    return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
	}
	setTimeout(function(){ 
		$.ajax({
		  	url: 'http://api.randomuser.me/',
		  	dataType: 'json',
		  	success: function(data){
		    	res = data.results[0].user;
			    $.gritter.add({
					title: capitalise(res.name.first) + ' ' + capitalise(res.name.last),
					text: 'Is come online',
					image: res.picture.thumbnail,
					close_icon: 'l-arrows-remove s16'
				});	
		  	}
		});		
	}, 10000);
    
    
    
    
    
    
    
    


    
    
    
    
    

});