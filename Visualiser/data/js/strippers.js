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