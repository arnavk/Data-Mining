function stripToLatLongTime (var tweet)
{
	var striped = {
		lat = tweet.coord[0]
		lon = tweet.coord[1]
		time = createdAtToDate (tweet.created_at)
	};
	return striped;
}

function createdAtToDate (var created_at)
{
	var date = new Date(
    	created_at.replace(/^\w+ (\w+) (\d+) ([\d:]+) \+0000 (\d+)$/,
        "$1 $2 $4 $3 UTC"));
	return date;
}

function stripToLatLong (var lltTweet)
{
	return google.maps.LatLng(lltTweet.lat, lltTweet.lon);
}