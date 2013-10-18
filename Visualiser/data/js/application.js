function stripToLatLongTime (tweet)
{
	//console.log (tweet);
	var stripped = {
		lat : tweet.coord[0],
		lon : tweet.coord[1],
		time : createdAtToDate (tweet.created_at),
	};
	return stripped;
}

function createdAtToDate (created_at)
{
	var date = new Date(
    	created_at.replace(/^\w+ (\w+) (\d+) ([\d:]+) \+0000 (\d+)$/,
        "$1 $2 $4 $3 UTC"));
	return date;
}

function stripToLatLong (lltTweet)
{
	return new google.maps.LatLng(lltTweet.lat, lltTweet.lon);
}



      function plot(tweets)
      {
        var points = new Array();
        console.log(tweets.length);
        for (var i = 0; i <tweets.length; i++)
        {
          points.push(stripToLatLong(stripToLatLongTime(tweets[i])));
        }
        var pointArray = new google.maps.MVCArray(points);  
        if(heatmap) heatmap.setMap(null);

        heatmap = new google.maps.visualization.HeatmapLayer({
          data: pointArray
        });
        heatmap.setMap(map);
        document.getElementById("timeslider").style.visibility="visible";
      }

      function changeGradient() {
        var gradient = [
          'rgba(0, 255, 255, 0)',
          'rgba(0, 255, 255, 1)',
          'rgba(0, 191, 255, 1)',
          'rgba(0, 127, 255, 1)',
          'rgba(0, 63, 255, 1)',
          'rgba(0, 0, 255, 1)',
          'rgba(0, 0, 223, 1)',
          'rgba(0, 0, 191, 1)',
          'rgba(0, 0, 159, 1)',
          'rgba(0, 0, 127, 1)',
          'rgba(63, 0, 91, 1)',
          'rgba(127, 0, 63, 1)',
          'rgba(191, 0, 31, 1)',
          'rgba(255, 0, 0, 1)'
        ]
        heatmap.setOptions({
          gradient: heatmap.get('gradient') ? null : gradient
        });
      }

      function changeRadius() {
        heatmap.setOptions({radius: heatmap.get('radius') ? null : 20});
      }

      function changeOpacity() {
        heatmap.setOptions({opacity: heatmap.get('opacity') ? null : 0.2});
      }

      function updateMap(percentage) {
        currentTime = new Date (minTime.getTime() + (percentage*timeRange*0.01));
        filteredTweets = new Array();
        for(var i = 0; i < tweets.length; i++){
          tweetTime = new Date(createdAtToDate(tweets[i].created_at));
          
          if(tweetTime.getTime() <= currentTime.getTime()){
            filteredTweets.push(tweets[i]);
          }
          else
            break;
        }
        plot(filteredTweets);
        var rangevalue = document.getElementById("rangevalue");
        rangevalue.value = currentTime;
        // document.getElementById("showCount").innerHTML = filteredTweets.length;
      }

      function updateTweets(filteredTweets)
      {
        tweets = filteredTweets;
        if(tweets)
        {
          minTime = createdAtToDate(tweets[0].created_at);
          maxTime = createdAtToDate(tweets[tweets.length-1].created_at);
          timeRange = maxTime-minTime;
          var slider = document.getElementById("timeslider");
          slider.value = 100;
          updateMap(100);  
        }
      }
              
      function filterByTime(){
        filteredTweets = new Array();
        document.getElementById("showCount").innerHTML = 0;
        for(var i = 0; i < tweets.length; i++){
          tweetTime = new Date(tweets[i].created_at);
          
          if(tweetTime.getTime() <= currentTime.getTime()){
            filteredTweets.push(tweets[i]);
          }
          else
            break;
        }
        plot(filteredTweets);
        document.getElementById("showCount").innerHTML = filteredTweets.length;
      }

      function search()
      {
        var hashtag=document.forms["searchForm"]["hashtag"].value;
        console.log(hashtag);
        queryURL = "/search/" + hashtag;
        disableButton();
        // $("#searchButton").button('loading');
        $.ajax({
            type:"GET",
            url :queryURL,
            datatype:"json",
            error:function(data){enableButton();alert('Error:');},
            success:function(data){
              enableButton();
              tweets = JSON.parse(data);
              console.log(tweets);
              console.log(tweets.length);
              updateTweets(tweets);
              
            },
          });

        return false;
      }
      function toggleButton () {
        console.log("toggling yo!");
        $("#searchButton").toggleClass('active');
      }
      function disableButton()
      {
        console.log("disabling yo");
        // $('#searchButton searchButtonText').text('Searching...');
        //$('button[data-loading-text]').button('loading');
        var span = document.getElementById('searchButton');
        while( span.firstChild ) {
            span.removeChild( span.firstChild );
        }
        span.appendChild( document.createTextNode("Searching...") );

      }
      function enableButton()
      {
        console.log("enabling yo");
        // $('#searchButton searchButtonText').text('Search!');
        // var btn = $("#searchButton");
        // btn.button('reset');
        var span = document.getElementById('searchButton');
        while( span.firstChild ) {
            span.removeChild( span.firstChild );
        }
        span.appendChild( document.createTextNode("Search!") );

      }