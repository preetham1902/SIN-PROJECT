import comment_downloader as CD
import fancySentiment as FS
def main():
	videoId = input("Enter the videoID : ")
	count = int(input("Enter the no. of comment to extract : "))
	comments = CD.commentExtract(videoId, count)	
	FS.fancySentiment(comments)
if __name__ == '__main__':
	main()
