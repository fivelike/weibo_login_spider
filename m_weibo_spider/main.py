# -*- coding: utf-8 -*-


from user_spider import UserByUrl
from comment_spider import Comment
from repost_spider import Repost
import openpyxl

#写入用户微博数据
ids = ["1699432410", "1638781994", "3937348351", "1878335471", "1642634100",
       "1642512402", "1691761292", "1644948230", "1653603955", "1638629382",
       "2656274875", "2803301701", "1703371307", "1507921471", "1977460817",
       "1618051664", "1640601392", "1726918143", "1900552512", "1649173367",
       "2993049293", "1974576991", "3802580928", "2286908003", "2647566747",
       "1642591402", "1271638160", "1323527941", "1893711543", "1749990115",
       "2591595652", "3802580928", "1644114654", "1218698200", "1642088277",
       "1784473157", "6004281123", "1886903325", "5375583682", "2610940895", 
       "2707505983", "3699083130"]

for id in ids:
    user = UserByUrl("https://m.weibo.cn/u/"+id)
    user.write_content_data()
    
    #获取id_list
    wbname = user.get_user_data()+".xlsx"
    wb = openpyxl.load_workbook(wbname)
    
    ws1 = wb["微博信息"]
    
    
    id_list = [] #文章id列表
    for var in ws1.iter_rows():
        id_list.append(var[0].value)
        
    id_list.pop(0) #删除
    
    
    #写入评论信息
#    passage_counts = 0
#    for passage_id in id_list:
#        comment = Comment(passage_id,wbname)
#        comment.write_contents()
#        passage_counts+=1
#        if passage_counts%100==0:
#            print("已写入{0}条微博的所有评论".format(passage_counts))
#    print("{0}条微博的所有评论写入完毕".format(passage_counts))
    print("-----------------------------")
    print("写入抓取微博数目共计：——{0}条".format(len(id_list)))
    print("所有微博对应评论信息抓取完毕！")
    print("所有微博对应转发信息抓取完毕！")
#写入转发信息
#repost_counts = 0
#for passage_id in id_list:
#    repost = Repost(passage_id,wbname)
#    repost.write_contents()
#    repost_counts+=1
#    if repost_counts%100==0:
#        print("已写入{0}条微博的转发信息".format(repost_counts))
#print("{0}条微博的转发信息写入完毕".format(repost_counts))

#end
