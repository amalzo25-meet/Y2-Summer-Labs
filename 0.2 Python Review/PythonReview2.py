def create_youtube_video(title, description):
	youtubevid = {"title":title,"description":description,"likes":0,"dislikes":0,"comments":{},"hashtag":[]}

	return youtubevid

def like(youtubevid):
	if "likes" in youtubevid:
		youtubevid["likes"] += 1 
		
	return youtubevid


def dislike(youtubevid):
	if "dislikes" in youtubevid:
		youtubevid["dislikes"] += 1

	return youtubevid


def add_comment(youtubevid,username,comment_text):
	youtubevid["comments"][username] = comment_text

	return youtubevid


title = input("title : ")
description = input("description : ")


youtubevid = create_youtube_video(title, description)

while youtubevid["likes"] < 494:
	youtubevid["likes"] += 1 

youtubevid = like(youtubevid)
youtubevid = dislike(youtubevid)

print(youtubevid["likes"], "people liked this")
print(youtubevid["dislikes"], "people disliked this")
print("comments:")
print("======")
username = input("username : ")
comment_text = input("comment : ")



youtubevid = add_comment(youtubevid, username, comment_text)
