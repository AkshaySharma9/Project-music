import pandas as pd

userItemData = pd.read_csv('data//kaggle_visible_evaluation_triplets.txt', sep = '\t')
f = open('data//collab_try.txt', 'w')
userItemData.columns = ['userId', 'ItemId' ,'count']
userItemData.head()

#Get list of unique items
itemList=list(set(userItemData["ItemId"].tolist()))

#Get count of users
userCount=len(set(userItemData["userId"].tolist()))

#Create an empty data frame to store item affinity scores for items.
itemAffinity= pd.DataFrame(columns=('item1', 'item2', 'score'))
rowCount=0

#For each item in the list, compare with other items.
for ind1 in range(len(itemList)):
    
    #Get list of users who bought this item 1.
    item1Users = userItemData[userItemData.ItemId==itemList[ind1]]["userId"].tolist()
    #print("Item 1 ", item1Users)
    
    #Get item 2 - items that are not item 1 or those that are not analyzed already.
    for ind2 in range(ind1, len(itemList)):
        
        if ( ind1 == ind2):
            continue
       
        #Get list of users who bought item 2
        item2Users=userItemData[userItemData.ItemId==itemList[ind2]]["userId"].tolist()
        #print("Item 2",item2Users)
        
        #Find score. Find the common list of users and divide it by the total users.
        commonUsers= len(set(item1Users).intersection(set(item2Users)))
        score=commonUsers / userCount

        #Add a score for item 1, item 2
        #itemAffinity.loc[rowCount] = [itemList[ind1],itemList[ind2],score]
        #rowCount +=1
        f.write(str(itemList[ind1]) + '\t' + str(itemList[ind2]) + '\t' + str(score) + '\n')

        #Add a score for item2, item 1. The same score would apply irrespective of the sequence.
        #itemAffinity.loc[rowCount] = [itemList[ind2],itemList[ind1],score]
        #rowCount +=1
        f.write(str(itemList[ind2]) + '\t' + str(itemList[ind1]) + '\t' + str(score) + '\n')

f.close()
        
#Check final result
itemAffinity.head()

searchItem='SOAXGDH12A8C13F8A1'
recoList=itemAffinity[itemAffinity.item1==searchItem]\
        [["item2","score"]]\
        .sort_values("score", ascending=[0])
        
print("Recommendations for item 5001\n", recoList)
