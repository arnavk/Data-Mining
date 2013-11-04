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

function stripToLatLong (lltTweet)
{
  var point = new google.maps.LatLng(lltTweet.lat, lltTweet.lon);
  if (point) return point;
  else
  {
    console.log("Invalid point");
    return new google.maps.LatLng(90, 90);
  }
}
function removePlottedTweets()
{
  if(heatmap)
  { 
    heatmap.setMap(null);
    document.getElementById("timeslider").style.visibility="hidden";
  }
}
function plot(tweets)
{
  removeCurrentClusters();
  removePlottedTweets();
  var points = new Array();
  console.log(tweets.length);
  for (var i = 0; i <tweets.length; i++)
  {
    points.push(stripToLatLong(stripToLatLongTime(tweets[i])));
  }
  var pointArray = new google.maps.MVCArray(points);  
  removePlottedTweets

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
      error:function(data){enableButton();alert('The operation timed out. Please refresh the page and try again. Sorry, but we have limited memory resources.');},
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
function plotTrends(startPercentage, endPercentage)
{
  console.log("Plotting trends yo!");
  var startTime = new Date (absoluteMinTime.getTime() + (startPercentage*absoluteRange*0.01));
  var endTime = new Date (absoluteMinTime.getTime() + (endPercentage*absoluteRange*0.01));
  console.log(convertDateToUTC(startTime).toString());
  console.log(convertDateToUTC(endTime).toString());

  removePlottedTweets();
  queryURL = "/clusters/" + convertDateToUTC(startTime).toString() + "|" + convertDateToUTC(endTime).toString() + "/";
  $.ajax({
    type:"GET",
    url :queryURL,
    datatype:"json",
    error:function(data){alert('The operation timed out. Please refresh the page and try again. Sorry, but we have limited memory resources.');},
    success:function(data){
      console.log("Got data!");
      var new_clusters = JSON.parse(data);
      console.log(new_clusters);
      updateClusters(new_clusters);
    },
  });
}


function getAllClusters()
{
  console.log("Came here");
  queryURL = "/clusters/all/";
  $.ajax({
    type:"GET",
    url :queryURL,
    datatype:"json",
    error:function(data){alert('Error:');},
    success:function(data){
      console.log("Got data!");
      var new_clusters = JSON.parse(data);
      console.log(new_clusters);
      updateClusters(new_clusters);
    },
  });

  return false;
}
function removeCurrentClusters ()
{
  if (clusterLabels)
  {
    for (var i = 0; i < clusterLabels.length; i++)
    {
      clusterLabels[i].setMap(null);
    }
  }
  clusterLabels = new Array();
}
function updateClusters(new_clusters)
{
  removeCurrentClusters();
  removePlottedTweets();
  clusters = new_clusters;
  clusterLabels = new Array();
  for (var i = 0; i < clusters.length; i++)
  {
    var cluster = clusters[i];
    console.log(cluster);
    clusterLabels.push(new MapLabel({
      text: cluster['hashtag'],
      fontFamily : '"Trebuchet MS", Helvetica, sans-serif',
      position: new google.maps.LatLng(cluster['centroid'][0], cluster['centroid'][1]),
      map: map,
      fontSize: (20+5*(i)),
      align: 'right'
    }));
  }
}