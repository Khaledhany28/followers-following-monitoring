from Instagram_class import Instagram
from File_handling import File_handling

class User:
    def __init__(self) -> None:
        self.insta = Instagram()
        self.fileSys = File_handling(self.insta.username)
        self.username = self.insta.username

    def updateFollowers(self):
        followersList = self.insta.getFollowers()

        self.fileSys.compareLists(followersList, "followers")

        self.fileSys.fileAppend(followersList, "followers")

    def updateFollowing(self):
        followingList = self.insta.getFollowing()

        self.fileSys.compareLists(followingList, "following")

        self.fileSys.fileAppend(followingList, "following")

    def getNewFollowers(self):
        return self.insta.getFollowers()
    
    def getNewFollowing(self):
        return self.insta.getFollowing()
    
    def loadOldFollowers(self):
        return self.fileSys.getOldList("followers")
    
    def loadOldFollowing(self):
        return self.fileSys.getOldList("following")