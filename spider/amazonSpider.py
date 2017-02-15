#   -*- coding:utf-8 -*-
import requests
import re
import xlwt
import urllib
import os
import base64
thisdir = os.path.dirname(os.path.abspath(__file__))

# use this path to organize file
FILE_DIR = '{}'.format(thisdir)
FILE_EXCEL = FILE_DIR +"\\execl"

# this is necessary because the amazon use header to figure out whether we are robot or not
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

needs = {
    '音乐鉴赏':r'https://www.amazon.cn/s/ref=sr_nr_p_n_binding_browse-b_0?fst=as%3Aoff&rh=n%3A658390051%2Ck%3A%E9%9F%B3%E4%B9%90%E9%89%B4%E8%B5%8F%2Cp_n_binding_browse-bin%3A2038564051&keywords=%E9%9F%B3%E4%B9%90%E9%89%B4%E8%B5%8F&ie=UTF8&qid=1486972240&rnid=2038547051',
    '美术鉴赏':r'https://www.amazon.cn/s/ref=sr_nr_p_n_binding_browse-b_0?fst=as%3Aoff&rh=n%3A658390051%2Ck%3A%E7%BE%8E%E6%9C%AF%E9%89%B4%E8%B5%8F%2Cp_n_binding_browse-bin%3A2038564051&keywords=%E7%BE%8E%E6%9C%AF%E9%89%B4%E8%B5%8F&ie=UTF8&qid=1486972204&rnid=2038547051',
    '艺术创作':r'https://www.amazon.cn/s/ref=sr_nr_p_n_binding_browse-b_0?fst=as%3Aoff&rh=n%3A658390051%2Ck%3A%E8%89%BA%E6%9C%AF%E5%88%9B%E4%BD%9C%2Cp_n_binding_browse-bin%3A2038564051&keywords=%E8%89%BA%E6%9C%AF%E5%88%9B%E4%BD%9C&ie=UTF8&qid=1486972154&rnid=2038547051'
}


# this is the first page,if you want more data, you can add '&page=num' to get more infomation
pageDetail = r'<a class="a-link-normal s-access-detail-page  a-text-normal"[^>]*href=\"([^>]*)\"[^>]*?>'

"""
the html label
"""
dateDetail = ('出版时间',r'<span class="a-size-medium a-color-secondary a-text-normal">&ndash; ([\s\S]*?)</span>')
authorDetail = ('作者名',r'<span class="author notFaded"[^>]*?>[\s\S]*?<a class="a-link-normal"[^>]*?>([^>]*?)</a>')
priceDetail = ('售价',r'<span class="a-size-medium a-color-price inlineBlock-display offer-price a-text-normal price3P">(.*?)</span>')
publishingDetail = ('出版社',r'<b>出版社:</b>([\s\S]*?)<')
seriesDetail = ('丛书名',r'<b>丛书名:</b>&nbsp;<a [\s\S]*?>([\s\S]*?)</a>')
contentDetail = ('内容简介',r'bookDescEncodedData = \"([\s\S]*?)\",')
ISBNDetail = ('ISBN',r'<b>ISBN:</b> ([\s\S]*?)</li>')

# PictureDetail = ['PictureName',r'id="imgBlkFront" data-a-dynamic-image="{&quot;([\s\S]*?)&quot']
PictureDetail = ['PictureName',r'<img alt="" src="\ndata:image/jpeg;base64,([\s\S]*?)\n\n']

def GetHTML(url,**argv):
    """ get pages
    argv :any argument that can use in url
    ret html if url is right,else return None
    """
    try:
        res = requests.get(url ,headers = header)
    except Exception as e:
        print(e)
        return ''

    return res.text

def MatchDetail(html, patterns):
    """ match all detail we need
    html: the html we need to match
    patterns: a list of pattern to match 

    ret: a list with other list of patterns results
    """
    result = []
    for eachP in patterns:
        if "内容简介" in eachP[0]:
            cont = re.findall(eachP[1],html)
            cont = ''.join(list(map(urllib.parse.unquote,cont)))
            result.append((eachP[0], cont))
            continue
        result.append((eachP[0], ','.join(re.findall(eachP[1], html))))
    return result

def SaveInExcel(booklist,name):
    """ save all booklist in a excel

    booklist: a list of a information of book
    name: the table na,e
    """
    wb = xlwt.Workbook()
    sh = wb.add_sheet(name)
    row = 0;col = 0

    # add each col's name
    font_style = xlwt.easyxf('font:height 240')
    for eachname,_ in booklist[0]:
        sh.write(row, col, eachname, font_style)
        col+=1

    row+=1
    col = 0
    for eachbook in booklist:
        for bookname,cont in eachbook:
            sh.write(row, col, cont)
            col+=1
        col = 0
        row+=1
    wb.save(FILE_EXCEL +"\\"+ name)
    print("save file "+name)

def GetPicture(cont, dire):
    """get picture base64 and save it

    cont: the picture base64-encoding
    dire: the name picture would be and it's dir
    """

    file = open(dire, 'wb')
    # print(cont)
    file.write(base64.standard_b64decode(cont))
    file.close()

def Spider(needs):
    """the whole function of this spider

    needs: a dictionary:{keywords:url}, if url is not correct ,it will output error!

    Ret: if url is error it will return false, else it will return true
    """

    # create a filename to save excel
    if not os.path.exists(FILE_EXCEL):
        os.mkdir(FILE_EXCEL)
    
    patterns = [dateDetail, authorDetail, priceDetail, publishingDetail, seriesDetail, contentDetail,ISBNDetail]
    for eachNeed in needs:
        html = GetHTML(needs[eachNeed])
        if html == '':
            # input error url
            return False

        if not os.path.exists(FILE_DIR + '\\' + eachNeed):
            os.mkdir(FILE_DIR + '\\' + eachNeed)
        pattern = pageDetail
        urlList = re.findall(pattern, html)
        if len(urlList):
            # the url is not the amazon url
            return False

        bookInfo = []
        for eachurl in urlList:
            eachHTML = GetHTML(eachurl)
            bookInfo.append(MatchDetail(eachHTML, patterns))

            # and save book picture
            pictureInfo = MatchDetail(eachHTML, [PictureDetail])
            # to find ISBN in the bookInfo
            thisBook = bookInfo[-1]
            for info in thisBook:
                name,cont = info
                if 'ISBN' == name:
                    GetPicture(pictureInfo[0][1], FILE_DIR + "\\" + eachNeed + '\\' + cont +'.jpg')
                    print(name+'write')
                    break

        SaveInExcel(bookInfo, eachNeed+'.xls')
    return True

if __name__ == "__main__":
    Spider(needs)
    # html = GetHTML(needs['音乐鉴赏'])
    # pattern = pageDetail
    # urlList = re.findall(pattern, html)
    # testHtml = GetHTML(urlList[1])
    # # patterns = [dateDetail, authorDetail, priceDetail, publishingDetail, seriesDetail, contentDetail,ISBNDetail]
    # patterns = [PictureDetail]
    # result = MatchDetail(testHtml, patterns)
    # # SaveInExcel([result],'test.xls')   
    # print(result)
    # name,pic = result[0]
    # # pic = requests.get(cont, headers = header)
    # file = open("test.jpg",'wb')
    # # print(pic.text)
    # file.write(base64.standard_b64decode(pic))
    # file.close()
    # for name,cont in result:
    #     # for cont in eachlist:
    #     print(name + ':' + cont)